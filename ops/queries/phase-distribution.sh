#!/bin/bash
# Show distribution of agents across SDLC phases

echo "Agent distribution by SDLC phase:"
echo ""

for phase in requirements design development testing deployment operations; do
    count=$(rg -c "^sdlc_phase: $phase$" agents/ 2>/dev/null | cut -d':' -f2 | paste -sd+ | bc 2>/dev/null || echo "0")
    printf "  %-15s: %d agents\n" "$phase" "$count"
done

echo ""
