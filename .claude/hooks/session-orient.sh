#!/bin/bash
# Session orientation hook - loads context at session start

echo "∵ ars contexta ∴"
echo ""
echo "Agent Workflow Research System"
echo ""

# Show file tree
echo "Vault structure:"
tree -L 2 -I 'node_modules|.git' 2>/dev/null || find . -maxdepth 2 -type d | grep -v ".git\|node_modules" | sort

echo ""

# Check for due reminders
if [ -f "ops/reminders.md" ]; then
    TODAY=$(date +%Y-%m-%d)
    DUE=$(grep -E "^\- \[ \] $TODAY:" ops/reminders.md 2>/dev/null)
    if [ -n "$DUE" ]; then
        echo "⚡ Reminders due today:"
        echo "$DUE"
        echo ""
    fi
fi

# Check task queue
if [ -f "ops/tasks.md" ]; then
    PENDING=$(grep -c "^\- \[ \]" ops/tasks.md 2>/dev/null || echo "0")
    if [ "$PENDING" -gt 0 ]; then
        echo "📋 $PENDING pending tasks in ops/tasks.md"
        echo ""
    fi
fi

# Check for stuck agents
STUCK=$(find agents -name "*.md" -type f -exec grep -l "^status: iterating$" {} \; 2>/dev/null | wc -l | tr -d ' ')
if [ "$STUCK" -gt 2 ]; then
    echo "⚠️  $STUCK agents stuck in 'iterating' status - consider reviewing"
    echo ""
fi

# Show current goals
if [ -f "self/goals.md" ]; then
    echo "Current focus:"
    grep -A 3 "## Active Threads" self/goals.md | tail -n +2
    echo ""
fi

echo "Ready to work on agent architecture."
echo ""
