#!/bin/bash
# Validation hook - checks schema after Write operations

# Get the file that was just written from CLAUDE_TOOL_RESULT
FILE_PATH="${CLAUDE_TOOL_RESULT_file_path:-}"

if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# Only validate files in agents/ directory
if [[ ! "$FILE_PATH" =~ ^agents/.*\.md$ ]]; then
    exit 0
fi

# Skip if .arscontexta doesn't exist (not an ars contexta vault)
if [ ! -f ".arscontexta" ]; then
    exit 0
fi

echo "Validating agent profile schema..."

# Check for required fields
MISSING_FIELDS=()

grep -q "^description:" "$FILE_PATH" || MISSING_FIELDS+=("description")
grep -q "^sdlc_phase:" "$FILE_PATH" || MISSING_FIELDS+=("sdlc_phase")
grep -q "^version:" "$FILE_PATH" || MISSING_FIELDS+=("version")
grep -q "^responsibilities:" "$FILE_PATH" || MISSING_FIELDS+=("responsibilities")
grep -q "^interactions:" "$FILE_PATH" || MISSING_FIELDS+=("interactions")
grep -q "^inputs:" "$FILE_PATH" || MISSING_FIELDS+=("inputs")
grep -q "^outputs:" "$FILE_PATH" || MISSING_FIELDS+=("outputs")
grep -q "^current_prompt:" "$FILE_PATH" || MISSING_FIELDS+=("current_prompt")
grep -q "^metrics:" "$FILE_PATH" || MISSING_FIELDS+=("metrics")
grep -q "^status:" "$FILE_PATH" || MISSING_FIELDS+=("status")

if [ ${#MISSING_FIELDS[@]} -gt 0 ]; then
    echo "⚠️  Missing required fields: ${MISSING_FIELDS[*]}"
    echo "   See templates/agent-profile.md for schema"
    exit 1
fi

# Check status value is valid
STATUS=$(grep "^status:" "$FILE_PATH" | cut -d':' -f2 | tr -d ' ')
if [[ ! "$STATUS" =~ ^(draft|active|iterating|deprecated)$ ]]; then
    echo "⚠️  Invalid status value: $STATUS"
    echo "   Must be one of: draft, active, iterating, deprecated"
    exit 1
fi

echo "✓ Schema validation passed"
exit 0
