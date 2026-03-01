#!/bin/bash
# Find agents stuck in 'iterating' status

echo "Agents stuck in iterating status:"
echo ""

rg -l "^status: iterating$" agents/ 2>/dev/null | while read -r file; do
    agent_name=$(basename "$file" .md)
    modified_date=$(stat -f "%Sm" -t "%Y-%m-%d" "$file" 2>/dev/null || stat -c "%y" "$file" 2>/dev/null | cut -d' ' -f1)
    echo "  - $agent_name (last modified: $modified_date)"
done

echo ""
echo "Review these agents - are they blocked on something or ready to finalize?"
