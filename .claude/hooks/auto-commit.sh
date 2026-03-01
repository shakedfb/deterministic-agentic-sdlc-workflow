#!/bin/bash
# Auto-commit hook - commits changes to git after writes

# Skip if .arscontexta doesn't exist or git is disabled
if [ ! -f ".arscontexta" ]; then
    exit 0
fi

# Check if git is enabled in config
GIT_ENABLED=$(grep "^git:" .arscontexta | cut -d':' -f2 | tr -d ' ' | tr -d '\n')
if [ "$GIT_ENABLED" = "false" ]; then
    exit 0
fi

# Skip if not a git repo
if [ ! -d ".git" ]; then
    exit 0
fi

# Get the file that was written
FILE_PATH="${CLAUDE_TOOL_RESULT_file_path:-}"

if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# Commit the change
git add "$FILE_PATH" 2>/dev/null
git commit -m "Auto-commit: $(basename "$FILE_PATH")

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>" >/dev/null 2>&1

exit 0
