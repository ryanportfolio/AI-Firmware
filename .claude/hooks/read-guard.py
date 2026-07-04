#!/usr/bin/env python3
"""PreToolUse guard for the Read tool: block full reads of huge files.

Forces sample-then-target on large files: head sample, Grep to locate,
then a targeted offset/limit read. Stdlib only.

Exit 0 = allow the Read. Exit 2 = block; stderr guidance is fed back to
the model so it can self-correct with a partial read.
"""
import json
import os
import sys

LIMIT_KB = 200
# Formats the Read tool handles specially (rendered, paged, or cell-based) —
# "sample with Grep" guidance would be a dead end for these.
EXEMPT_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".ico",
    ".pdf", ".ipynb",
}


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return 0
    tool_input = data.get("tool_input") or {}
    path = tool_input.get("file_path")
    if not path:
        return 0
    # Explicit offset/limit = intentional partial read; that IS the escape hatch.
    if tool_input.get("offset") is not None or tool_input.get("limit") is not None:
        return 0
    if os.path.splitext(path)[1].lower() in EXEMPT_EXTS:
        return 0
    try:
        size = os.path.getsize(path)
    except OSError:
        return 0  # missing/unreadable — let Read report its own error
    if size <= LIMIT_KB * 1024:
        return 0
    kb = size // 1024
    sys.stderr.write(
        f"read-guard: {path} is {kb} KB (>{LIMIT_KB} KB) — "
        "full read blocked to protect context.\n"
        "Sample structure first, then read only the region you need:\n"
        "  1. Read(file_path, limit=100) for the head; "
        "Read(file_path, offset=<near end>, limit=50) for the tail\n"
        "  2. Grep(pattern, path=<this file>, -n=true) to locate exact lines\n"
        "  3. Read(file_path, offset=N, limit=M) for the targeted slice\n"
        "Passing an explicit offset/limit bypasses this guard when a full "
        "pass is truly needed.\n"
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
