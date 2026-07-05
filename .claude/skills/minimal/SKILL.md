---
name: minimal
description: Toggle minimal-skills mode — disable all project skills except a small keep-list (recall, pr, merge, handoff-audit, caveman, minimal) to cut per-turn context weight. Use when the user says /minimal, "minimal mode", "disable extra skills", or /minimal off, "restore skills", "re-enable skills".
---

# Minimal skills mode

Moves every project skill except the keep-list out of `.claude/skills/` so the harness stops injecting their descriptions each turn. Real token savings, not a behavioral pretend-disable.

## Keep-list

```
recall  pr  merge  handoff-audit  caveman  minimal
```

- `caveman` stays because the kernel CLAUDE.md session-start default invokes it every session.
- `minimal` stays so the mode can be toggled back off.

## Turning ON (`/minimal`)

1. Create the parking folder if missing: `.claude/skills-off/`.
2. For every directory in `.claude/skills/` NOT in the keep-list:
   `git mv .claude/skills/<name> .claude/skills-off/<name>`
3. Run `bash .claude/scripts/context-weight.sh` before and after; report the per-turn savings to the user.
4. Commit, push, PR per the kernel git rules.

## Turning OFF (`/minimal off`)

1. For every directory in `.claude/skills-off/`:
   `git mv .claude/skills-off/<name> .claude/skills/<name>`
2. Remove the now-empty `.claude/skills-off/`.
3. Commit, push, PR per the kernel git rules.

## Caveats (tell the user)

- Takes effect **next session** — the current session's skill list is already injected.
- The change must land where sessions actually run: merge the PR AND pull in the main checkout.
- Only project skills are affected. Built-in and plugin skills (code-review, loop, deep-research, etc.) are injected by the harness/plugins and cannot be disabled here.
- Disabled skills are parked, not deleted — `PROVENANCE.md` and skill folders stay intact in `.claude/skills-off/`.
