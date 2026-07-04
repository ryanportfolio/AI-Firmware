#!/usr/bin/env bash
# Interpreter shim for read-guard.py. Probes candidates because on Windows
# `python`/`python3` can resolve to Microsoft Store stub aliases that print
# an install nag and fail; `py` is the real launcher there. Linux/sandbox
# hits python3 on the first probe. exec preserves stdin and exit code.
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for cand in python3 python py; do
  if "$cand" -c pass >/dev/null 2>&1; then
    exec "$cand" "$DIR/read-guard.py"
  fi
done
# No working interpreter — fail open (allow the Read) rather than break the tool.
exit 0
