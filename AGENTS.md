# Codex Instructions

This file is the Codex compatibility boundary for the Agent Firmware starter.
Claude Code continues to use `CLAUDE.md`, `.claude/settings.json`, and the
`.claude/` skill/hook system. Codex uses this file first, then reads the safe,
project-specific parts of `CLAUDE.md`.

## Runtime Boundary

- Do not execute `.claude/hooks/session-start.sh` in Codex.
- Read `CLAUDE.md` for project facts, verification requirements, architecture,
  reference-library pointers, scope rules, and engineering standards.
- Do not inherit Claude-only sections from `CLAUDE.md`: popup-tool rules,
  SessionStart behavior, default `caveman` activation, Claude model names,
  Claude skill invocation syntax, or automatic git integration.
- Treat `.claude/skills/` as the canonical skill library. Codex-native adapters
  under `.agents/skills/` expose those skills without duplicating them.
- Claude-only tool names inside skills must be translated to Codex tools only
  when a safe equivalent exists.
- Treat `$ARGUMENTS` inside a canonical skill as the current invocation's
  free-form input.
- Claude popup-tool bans in `CLAUDE.md` are Claude-specific. In Codex, follow
  the active Codex tool instructions for user input and planning.

## Codex Safety Rules

- Do not activate persistent modes such as `caveman` or auto-merge unless the
  user explicitly asks for that mode in the current Codex session.
- Do not inherit Claude's auto-commit, auto-push, auto-PR, or auto-merge rules.
  In Codex, ship only when the user asks for shipping or the current task
  explicitly includes it.
- Never push to `main`, force-push, merge, delete branches/worktrees, run
  migrations, deploy, install runtime dependencies, or modify checkouts outside
  the workspace without explicit current-session approval.
- Stage explicit paths only. Never use blanket staging for mixed worktrees.
- Keep private paths, secrets, tokens, and personal workflow mandates out of
  starter defaults.
- Verify before claiming completion. State exactly what ran; if the authoritative
  check is CI, deploy logs, or the user's machine, say so.

## Shared Assets

- Project memory lives in `.claude/reference/`. Read the relevant file before
  non-trivial work in an unfamiliar area.
- Codex discovers repo skills from `.agents/skills/`. Each generated adapter
  delegates to the matching canonical `.claude/skills/<name>/SKILL.md`.
- After adding, removing, or editing a canonical skill, run
  `node .claude/scripts/sync-codex-skills.mjs --write`.
- Codex tool mapping notes live in
  `.claude/skills/using-superpowers/references/codex-tools.md`.
- Context budget can be inspected with `bash .claude/scripts/context-weight.sh`
  when Bash is available.

## Starter Maintenance

- Bootstrap scripts under `bootstrap/` must stay ASCII-only for Windows
  PowerShell 5.1 compatibility.
- Shell scripts must keep LF line endings.
- Keep runtime-specific claims precise: Claude Code gets hooks and slash skills;
  Codex gets `AGENTS.md` plus native `.agents/skills` adapters.
- If a template memory file contains maintainer-only local workflow rules,
  remove or generalize them before shipping.
