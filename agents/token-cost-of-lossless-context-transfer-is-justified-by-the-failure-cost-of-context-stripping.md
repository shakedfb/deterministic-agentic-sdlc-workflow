---
description: Stripping context at handoff boundaries to save tokens produces specialist failures that cost more in tokens, time, and iterations than the overhead of complete transfer — making lossless context transfer the economically optimal strategy, not merely the ideally correct one.
topics: ["[[agent-registry]]", "[[design-phase]]"]
source: "[[orchestrator-agent]]"
classification: closed
---

# token cost of lossless context transfer is justified by the failure cost of context stripping

The instinct to strip context at handoff boundaries is economically motivated: passing the full spec artifact plus all upstream outputs plus iteration feedback is expensive in tokens, and token cost translates directly to API cost. But this calculation is incomplete. It accounts for the input tokens on the handoff without accounting for the retry tokens when the stripped context causes failure.

The failure chain from context stripping is predictable. A specialist that receives incomplete context produces output that is partially misaligned with the spec or inconsistent with upstream work. The orchestrator's validation check catches this and returns the task with a failure signal. The specialist re-executes with the failure feedback — but still without the full context, because the orchestrator that stripped context once will strip it again. The second attempt may partially succeed, or it may fail again. In either case, the total token cost is: the stripped input tokens across multiple attempts, plus the full output tokens across multiple attempts, plus the validation overhead per round.

Compare this to lossless transfer: a larger input on the first attempt, the full output tokens once (or with a single retry for unrelated reasons), and a single validation pass. The crossover point where stripping becomes more expensive than complete transfer is reached after fewer than two retries in most cases. For tasks where stripping causes systematic misalignment — the specialist produces plausible but subtly wrong output across all attempts — there is no crossover: stripping never becomes cheaper.

The economic argument closes the loop on why lossless transfer is the designed behavior rather than an optimization. It is not trading cost for correctness; it is trading a smaller cost for a larger one. The decision to strip context is a false economy.

The constraint this creates: orchestrators must budget for full context transfers in their token allocation planning. Systems that are designed with tight per-task token budgets may find that the budget was calculated assuming stripped context, which is an incorrect baseline. The correct baseline is lossless transfer, with windowing as a fallback only when transfer is physically impossible due to context window limits (see [[intelligent context windowing is needed when spec artifacts exceed the context window]]).

---

**Source:** [[orchestrator-agent]]

**Relevant Notes:**
- [[lossless context transfer at handoff boundaries is the orchestrators most critical responsibility]] — this note provides the economic argument that makes lossless transfer the rational choice, supporting the design principle with a cost analysis
- [[intelligent context windowing is needed when spec artifacts exceed the context window]] — windowing is the appropriate fallback when full transfer is infeasible due to window limits; it is distinct from stripping because it is structured and conservative rather than arbitrary
- [[spec-centric architecture is the most reliable pattern for agents building systems]] — the spec artifact is the largest component of the context package; spec-centric architecture makes lossless transfer more expensive per handoff, which is justified by the alignment benefits downstream

**Topics:**
- [[agent-registry]]
- [[design-phase]]
