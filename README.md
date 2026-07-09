# Agent Firmware

An AI operating layer for coding agents: a small rule kernel, curated skills,
durable project memory, session hooks, and sync tooling that make every new
project start with battle-tested agent behavior instead of an empty prompt.

This began as `claude-starter`, and Claude Code is still the first-class
runtime. The broader framing is **agent firmware**: not an app and not a full
operating system, but the low-level configuration that tells an AI coding
environment how to boot, remember, verify, ship, and stay lean. It is OS-like in
outcome and firmware-like in scope.

## Why This Exists

Coding agents become more useful when their working system is explicit:

- **Kernel rules:** short, always-loaded guidance for verification, git hygiene,
  context restraint, and collaboration norms.
- **Skills:** reusable playbooks for recurring work such as debugging, planning,
  TDD, PRs, design polish, context trimming, and handoff reviews.
- **Memory:** committed reference files under `.claude/reference/` so project
  gotchas survive beyond one chat, one machine, or one sandbox.
- **Hooks:** session-start checks that surface drift, overlap, and Claude-specific
  defaults when Claude Code is the runtime.
- **Sync:** a two-way path for moving generic improvements back to the starter
  and pulling starter improvements into spawned projects.
- **Budget awareness:** `bash .claude/scripts/context-weight.sh` measures the
  always-loaded context tax instead of guessing.

Systems like `caveman` exist for the same reason: agent behavior should be
intentional, measurable, and reversible. Ultra-terse mode is not a gimmick; it is
a token-budget control with carve-outs for security, irreversible actions, and
ambiguous decisions.

## Claude Code And Codex

This repository now separates runtime-specific behavior:

| Runtime | Entry point | Behavior |
|---|---|---|
| Claude Code | `CLAUDE.md`, `.claude/settings.json`, `.claude/hooks/`, `.claude/skills/` | Full firmware: project memory, slash skills, session hook, plugin path, and Claude-specific workflow rules. |
| Codex | `AGENTS.md`, `.agents/skills/` | Safe compatibility layer plus native skill discovery, backed by the unchanged canonical Claude workflows. |

Codex discovers thin adapters under `.agents/skills/`. Each adapter delegates to
the matching canonical `.claude/skills/` workflow, so both runtimes use one
source of truth. Codex does not run Claude SessionStart hooks.

## Highlights

- **Two-way sync, not copy-paste.** Most templates are one-shot scaffolds.
  `/sync-starter` moves generic wins between spawned projects and the starter.
- **Context cost is measured.** `context-weight.sh` prints the per-turn weight of
  the kernel and skill descriptions, with a per-skill breakdown.
- **Memory survives the session.** `/recall save` and `/learning` write durable
  project knowledge into `.claude/reference/`.
- **Ultra-terse mode with guardrails.** `caveman` compresses prose while keeping
  technical symbols, code, errors, commits, and warnings readable.
- **Independent review paths.** `impartial-review` and `handoff-audit` create
  fresh-context review pressure instead of trusting the implementation thread.
- **Prototype before committing.** `/lab` supports disposable UI tuning before
  porting exact values back into production code.
- **CI-gated config.** Bootstrap scripts, hooks, and JSON manifests are
  parse-checked on every push.

## Quick Start

There are three ways to use the repo.

### A. Full Claude Code Template

Use this when you want the full firmware: kernel, hooks, memory, skills, and
template sync.

- GitHub UI: **Use this template -> Create a new repository**, clone it, open it
  in Claude Code, then run `/init-project`.
- Windows one-click: double-click `bootstrap/New-ClaudeProject.cmd`.
- Windows CLI: `.\bootstrap\new-claude-project.ps1 -Name my-app -Dest C:\code`

`/init-project` detects the stack, asks a short Q&A, fills the placeholder
verification/deploy sections, seeds reference files, prunes irrelevant skills,
removes template-only plugin files, and commits the setup.

### B. Codex-Safe Use

Use this when opening a spawned project or the starter itself in Codex.

1. Open the repo in Codex.
2. Let Codex read `AGENTS.md` as the authoritative Codex instruction boundary.
3. Use `.claude/reference/` for shared project memory.
4. Let Codex discover the generated repo skills under `.agents/skills/`.
5. Do not run Claude hooks or inherit Claude auto-commit/auto-merge rules unless
   the user explicitly asks in the current Codex session.

For a fresh project, ask Codex to initialize the starter or select the
`init-project` skill. Its adapter delegates to the same canonical workflow
Claude Code uses.

### C. Claude Plugin Skills Only

Use this when you want the Claude skills in an existing project without cloning
the template:

```text
/plugin marketplace add ryanportfolio/claude-starter
/plugin install claude-starter@claude-starter
```

This path requires the repository to be public. Plugin skills are namespaced
such as `/claude-starter:recall`. Projects spawned from the template ship the
skills un-namespaced and do not need the plugin.

## What's Inside

| Piece | What it does |
|---|---|
| `CLAUDE.md` | Claude Code kernel rules loaded every turn. Two placeholder sections are configured per project by `/init-project`. |
| `AGENTS.md` | Codex compatibility boundary. Inherits project facts while excluding Claude-only runtime behavior. |
| `.claude/skills/` | 32 canonical Markdown playbooks used by Claude Code and Codex. |
| `.agents/skills/` | Generated Codex-native adapters; metadata only, no duplicated workflow bodies. |
| `.claude/reference/` | Durable project memory: secrets, architecture, pitfalls, commands, tech stack, and deployment notes. |
| `.claude/hooks/session-start.sh` | Claude Code SessionStart hook for drift checks, overlap warnings, and Claude-specific session defaults. |
| `.claude/scripts/context-weight.sh` | Measures always-loaded context weight. |
| `.claude/settings.json` | Claude Code hook wiring plus a Bash permission allowlist. |
| `.claude-plugin/` | Claude plugin and marketplace manifests. Template-only for spawned projects. |
| `bootstrap/` | Project creator, fork-retargeting, and machine setup scripts. |

## Skill Set

See `.claude/skills/PROVENANCE.md` for each skill's origin, license, and local
changes.

- **Lifecycle:** `init-project`, `sync-starter`, `addskill`,
  `optimize-context`.
- **Workflow:** `recall`, `learning`, `safe-ship`, `pr`, `merge`, `caveman`,
  `enhance-prompt`, `handoff-audit`, `why`, `advocate`, `lab`, `conflict`.
- **Discipline:** `brainstorming`, `writing-plans`, `executing-plans`,
  `systematic-debugging`, `test-driven-development`,
  `verification-before-completion`, `impartial-review`,
  `subagent-driven-development`, `dispatching-parallel-agents`,
  `using-git-worktrees`, `using-superpowers`, `writing-skills`,
  `applying-best-practices`, `finishing-a-development-branch`.
- **Craft:** `impeccable`, `humanizer`.

## Safety Model

The starter is allowed to be opinionated, but shipped defaults must be safe:

- Runtime-specific rules stay runtime-specific. Claude hooks and Claude popup
  constraints do not become Codex instructions.
- Template memory must not contain private checkout paths, personal workflow
  mandates, secrets, tokens, or maintainer-only merge rules.
- Git automation must stage explicit paths and protect against direct pushes to
  `main`, force-pushes, secret files, and unverified completion claims.
- Installing dependencies, running migrations, deploying, deleting work, and
  touching external checkouts require explicit user authority for the current
  session.
- Verification claims must name the check that actually ran. If the authoritative
  signal is elsewhere, say that plainly.

## Forking This Template

One command retargets functional upstream references to your fork:

```bash
bash bootstrap/retarget-fork.sh <you>/<your-fork>
```

Review the diff and commit. LICENSE attribution is intentionally left untouched.

## Dotfiles For Claude

Machine-level `~/.claude` files do not travel with any repo. Keep your copies in
`bootstrap/machine/home-claude/` in your fork, then on a new machine run:

```powershell
.\bootstrap\setup-machine.ps1
```

The script copies missing files only; `-Force` overwrites; `-DryRun` previews.

## Requirements

- Claude Code for the full template and plugin workflow.
- Codex uses `AGENTS.md` and native `.agents/skills/` adapters. It does not run
  Claude SessionStart hooks.
- `gh` CLI is optional for the Windows project creator. Without it, the script
  falls back to a local copy plus printed manual GitHub steps.
- Bootstrap is Windows-first PowerShell. The Claude session hook is Bash and is
  validated under Ubuntu CI.

## Provenance And License

MIT (see `LICENSE`). Several skills are forked from upstream work, notably Jesse
Vincent's `superpowers` (MIT) and Paul Bakaus's `impeccable` (Apache 2.0, based
on Anthropic's frontend-design skill). `.claude/skills/PROVENANCE.md` tracks
origins, licenses, and local changes; per-skill LICENSE/NOTICE files ship in the
skill folders.
