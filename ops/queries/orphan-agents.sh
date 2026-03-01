#!/bin/bash
# Find agents with no interactions (orphaned in the workflow)

echo "Agents with no interactions:"
echo ""

rg -l "^interactions: \[\]$" agents/ 2>/dev/null | while read -r file; do
    agent_name=$(basename "$file" .md)
    echo "  - $agent_name"
done

echo ""
echo "These agents should be integrated into the workflow or marked as deprecated."
