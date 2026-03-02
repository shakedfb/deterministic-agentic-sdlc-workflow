#!/usr/bin/env python3
"""
verify-links.py -- Check wiki link resolution for a note file.
Usage: python3 verify-links.py <note_path>
"""
import os
import re
import sys

BASE = "/Users/shaked/playground/agent-workflow-research"

def title_to_slug(title):
    """Convert a wiki link title to a filename slug."""
    # Remove characters that don't appear in filenames
    slug = title.lower()
    # Replace spaces with hyphens
    slug = slug.replace(" ", "-")
    # Remove commas, parentheses, apostrophes
    slug = re.sub(r"[,'\(\)]", "", slug)
    return slug

def find_file_for_link(title, base):
    """Try to find a file matching a wiki link title."""
    slug = title_to_slug(title)

    # Known special cases
    if title == "agent-registry" or slug == "agent-registry":
        path = f"{base}/agents/agent-registry.md"
        return path, os.path.exists(path)

    # Check common locations
    candidates = [
        f"{base}/agents/{slug}.md",
        f"{base}/sdlc-phases/{slug}.md",
        f"{base}/agents/agent-registry.md" if slug == "agent-registry" else None,
    ]

    for c in candidates:
        if c and os.path.exists(c):
            return c, True

    # Exact match search in agents/ and sdlc-phases/
    for search_dir in [f"{base}/agents", f"{base}/sdlc-phases"]:
        if os.path.exists(search_dir):
            for fname in os.listdir(search_dir):
                if fname.endswith('.md'):
                    fname_slug = fname[:-3]  # remove .md
                    if fname_slug == slug:
                        return os.path.join(search_dir, fname), True

    # Partial match as fallback
    for search_dir in [f"{base}/agents", f"{base}/sdlc-phases", f"{base}/ops/queue"]:
        if os.path.exists(search_dir):
            for fname in os.listdir(search_dir):
                if fname.endswith('.md') and slug[:20] in fname.lower():
                    return os.path.join(search_dir, fname), True

    return None, False

def check_note(note_path, verbose=True):
    if not os.path.exists(note_path):
        print(f"ERROR: Note file not found: {note_path}")
        return False

    with open(note_path) as f:
        content = f.read()

    links = re.findall(r'\[\[([^\]]+)\]\]', content)
    unique_links = sorted(set(links))

    failures = []
    ok_count = 0

    for link in unique_links:
        path, found = find_file_for_link(link, BASE)
        if found:
            ok_count += 1
            if verbose:
                print(f"  OK: [[{link}]]")
        else:
            failures.append(link)
            if verbose:
                print(f"  MISSING: [[{link}]]")

    if failures:
        print(f"\nLINK CHECK: FAIL ({len(failures)} dangling links)")
        for f in failures:
            print(f"  - [[{f}]]")
    else:
        print(f"  LINK CHECK: PASS ({ok_count} links resolved)")

    return len(failures) == 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 verify-links.py <note_path>")
        sys.exit(1)

    note_path = sys.argv[1]
    success = check_note(note_path)
    sys.exit(0 if success else 1)
