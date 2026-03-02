"""Parallel task execution within the Development phase.

When a requirement decomposes into multiple independent subtasks,
this module executes code generation for each in parallel using asyncio.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any

import structlog
from langchain_core.messages import HumanMessage, SystemMessage
from agents.cache import GenerationCache
from agents.llm import get_llm
from agents.models import CodeArtifact, DependencyChange, RequirementSpec, SourceFile
from agents.prompts import DEV_CODEGEN_PROMPT
from agents.tracing import trace_phase
from config.guardrails_code import validate_code

logger = structlog.get_logger()

MAX_CONCURRENT = 4


def _classify_dependencies(subtasks: list[dict[str, Any]]) -> tuple[list[list[int]], list[int]]:
    """Classify subtasks into dependency layers for parallel execution.

    Returns:
        - layers: list of index lists, each layer can run in parallel
        - order: flat execution order
    """
    n = len(subtasks)
    files_created_by: dict[str, int] = {}
    for i, task in enumerate(subtasks):
        for f in task.get("files_to_create", []):
            files_created_by[f] = i

    deps: dict[int, set[int]] = {i: set() for i in range(n)}
    for i, task in enumerate(subtasks):
        for f in task.get("files_to_modify", []):
            if f in files_created_by and files_created_by[f] != i:
                deps[i].add(files_created_by[f])
        for d in task.get("dependencies_on", []):
            if isinstance(d, int) and d < n:
                deps[i].add(d)

    layers: list[list[int]] = []
    completed: set[int] = set()
    remaining = set(range(n))

    while remaining:
        layer = [i for i in remaining if deps[i].issubset(completed)]
        if not layer:
            layer = [min(remaining)]
        layers.append(layer)
        completed.update(layer)
        remaining -= set(layer)

    order = [i for layer in layers for i in layer]
    return layers, order


@trace_phase("development", parallel=True)
async def parallel_codegen(
    ticket_id: str,
    requirement_spec: RequirementSpec,
    subtasks: list[dict[str, Any]],
    codebase_context: str = "",
    error_context: str = "",
) -> CodeArtifact:
    """Execute code generation for multiple subtasks in parallel where possible."""
    layers, _ = _classify_dependencies(subtasks)
    cache = GenerationCache()
    llm = get_llm(temperature=0.1)

    all_source_files: list[SourceFile] = []
    all_deps: list[DependencyChange] = []

    try:
        for layer_idx, layer in enumerate(layers):
            await logger.ainfo(
                "parallel_layer_start",
                layer=layer_idx,
                task_count=len(layer),
                task_indices=layer,
            )

            semaphore = asyncio.Semaphore(MAX_CONCURRENT)

            async def process_subtask(idx: int) -> tuple[list[SourceFile], list[DependencyChange]]:
                async with semaphore:
                    subtask = subtasks[idx]
                    cache_key = {
                        "subtask": subtask,
                        "spec": requirement_spec.model_dump(),
                        "context": codebase_context,
                    }

                    cached = await cache.get(cache_key)
                    if cached:
                        files = [SourceFile(**f) for f in cached.get("files", [])]
                        deps = [DependencyChange(**d) for d in cached.get("dependencies", [])]
                        return files, deps

                    prompt = DEV_CODEGEN_PROMPT.format(
                        subtask=json.dumps(subtask, indent=2),
                        requirement_spec=requirement_spec.model_dump_json(indent=2),
                        existing_code=codebase_context,
                        error_context=error_context,
                    )

                    response = await llm.ainvoke([
                        SystemMessage(content="You are a senior software engineer. Return only valid JSON."),
                        HumanMessage(content=prompt),
                    ])

                    try:
                        result = json.loads(response.content)
                    except json.JSONDecodeError:
                        return [], []

                    files: list[SourceFile] = []
                    for f in result.get("files", []):
                        validation = validate_code(f["content"], f.get("language", "python"))
                        if validation.valid:
                            files.append(SourceFile(
                                path=f["path"],
                                content=f["content"],
                                language=f.get("language", "python"),
                            ))

                    deps = [DependencyChange(**d) for d in result.get("dependencies", [])]

                    await cache.put(cache_key, {
                        "files": [f.model_dump() for f in files],
                        "dependencies": [d.model_dump() for d in deps],
                    })

                    return files, deps

            results = await asyncio.gather(
                *[process_subtask(idx) for idx in layer],
                return_exceptions=True,
            )

            for result in results:
                if isinstance(result, Exception):
                    await logger.aerror("parallel_subtask_failed", error=str(result))
                    continue
                files, deps = result
                all_source_files.extend(files)
                all_deps.extend(deps)
    finally:
        await cache.close()

    branch = f"agentic/{ticket_id.lower().replace('-', '_')}"
    return CodeArtifact(
        ticket_id=ticket_id,
        branch_name=branch,
        source_files=all_source_files,
        dependency_changes=all_deps,
    )
