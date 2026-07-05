---
name: minimal
description: Toggle minimal-skills mode — disable all project skills except a small keep-list (recall, learning, pr, merge, handoff-audit, caveman, minimal) to cut per-turn context weight. Use when the user says /minimal, "minimal mode", "disable extra skills", or /minimal off, "restore skills", "re-enable skills".
---

# Minimal skills mode

Turns every project skill except the keep-list off via `skillOverrides` in committed `.claude/settings.json` — the same mechanism `/init-project` profiles use. An `"off"` entry hides the skill from the picker AND removes its description from the per-turn skills list. Real token savings, fully reversible, no folder moves.

## Keep-list

```
recall  learning  pr  merge  handoff-audit  caveman  minimal
```

- `learning` stays because the self-improvement loop (capture gotchas into `.claude/reference/`) is core to the template, not an optional extra.
- `caveman` stays because the kernel CLAUDE.md session-start default invokes it every session.
- `minimal` stays so the mode can be toggled back off.

## Turning ON (`/minimal`)

1. List project skills: directories under `.claude/skills/`.
2. In `.claude/settings.json`, add `"skillOverrides"` entries setting every project skill NOT in the keep-list to `"off"` (bare directory name as the key). Preserve any overrides already present (e.g. from an `/init-project` profile).
3. Run `bash .claude/scripts/context-weight.sh`; report the projected per-turn savings to the user.
4. Commit, push, PR per the kernel git rules.

## Turning OFF (`/minimal off`)

1. Remove the `"off"` entries this skill added from `skillOverrides` in `.claude/settings.json`. If an `/init-project` profile had its own pruning before minimal mode, restore that profile's entries rather than clearing everything — check git history of `.claude/settings.json` if unsure.
2. Commit, push, PR per the kernel git rules.

## Caveats (tell the user)

- Takes effect **next session** — the current session's skill list is already injected.
- The change must land where sessions actually run: merge the PR AND pull in the main checkout.
- Only project skills are affected. Built-in and plugin skills (code-review, loop, deep-research, etc.) are injected by the harness/plugins and cannot be disabled here.
- Nothing is deleted — skill folders stay in `.claude/skills/`; only the overrides change.
