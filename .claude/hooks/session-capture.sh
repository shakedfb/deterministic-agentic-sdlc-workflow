#!/bin/bash
# Session capture hook - saves session context at session end

# Skip if .arscontexta doesn't exist
if [ ! -f ".arscontexta" ]; then
    exit 0
fi

# Check if session capture is enabled
CAPTURE_ENABLED=$(grep "^session_capture:" .arscontexta | cut -d':' -f2 | tr -d ' ' | tr -d '\n')
if [ "$CAPTURE_ENABLED" = "false" ]; then
    exit 0
fi

# Create sessions directory if it doesn't exist
mkdir -p ops/sessions

# Generate session file with timestamp
SESSION_FILE="ops/sessions/$(date +%Y%m%d-%H%M%S).md"

# Capture session summary
cat > "$SESSION_FILE" <<EOF
---
date: $(date +%Y-%m-%d)
time: $(date +%H:%M:%S)
---

# Session $(date +%Y-%m-%d)

## What Was Done

[Session activity summary - populated by claude during session]

## Agents Created/Modified

[List of agent profiles created or updated]

## Design Decisions

[Key design decisions made]

## Next Steps

[What to work on next session]

---
EOF

echo "Session context saved to $SESSION_FILE"

exit 0
