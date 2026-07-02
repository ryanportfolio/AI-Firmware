# claude-starter

A Claude Code project template that stays in sync with the projects it spawns. Every project starts with a tuned rule kernel, 31 workflow skills, a self-populating project memory, and session hooks. Improvements made in any project flow back to the template; template updates flow out to every project.

Distilled from a production repo, with the project-specific content stripped out.

## Why this exists

Claude Code works better with standing instructions, skills, and accumulated project knowledge. That setup usually lives in one repo and dies there. This template turns it into a fleet:

- **Spawn configured.** New projects start with the kernel rules, skill set, and memory system in place. `/init-project` tailors them to the stack in one Q&A.
- **Self-improving.** `/recall` and `/learning` capture gotchas into a committed reference library as you work. `/sync-starter` moves generic wins back to the template, and a weekly session-start nudge tells projects when the template is ahead.
- **Measurably lean.** Always-loaded context is a per-turn tax. `bash .claude/scripts/context-weight.sh` prints the exact weight (template baseline: ~4.5k tokens/turn); the `/optimize-context` skill is the playbook for cutting it.

## Quick start

**Use as a template (the full setup: kernel, hooks, memory, skills):**

- GitHub UI: **Use this template → Create a new repository**, clone, open in Claude Code, run `/init-project`.
- One-click (Windows): double-click `bootstrap/New-ClaudeProject.cmd`. It creates a private repo from the template via `gh`, clones it, and strips template-only files.
- CLI: `.\bootstrap\new-claude-project.ps1 -Name my-app -Dest C:\code`

**Or install just the skills as a plugin (any existing project, no clone):**

```
/plugin marketplace add Aoh1578/claude-starter
/plugin install claude-starter@claude-starter
```

Plugin skills are namespaced (`/claude-starter:recall`, and so on). Projects spawned from the template ship the skills un-namespaced, so they don't need the plugin. If both end up active anyway, the session-start hook detects the overlap and tells you the one-line fix.

## What's inside

| Piece | What it does |
|---|---|
| `CLAUDE.md` | Kernel rules loaded every turn: verification honesty, git auto-commit/PR workflow, subagent discipline, context-restraint principles. Two `FILL IN` sections configured per project by `/init-project`. |
| `.claude/skills/` | 31 skills: lifecycle (`init-project`, `sync-starter`, `addskill`, `optimize-context`), workflow (`recall`, `learning`, `safe-ship`, `pr`, `merge`, `caveman`, `enhance-prompt`, `handoff-audit`, `why`, `lab`, `conflict`), discipline (`brainstorming`, `writing-plans`, `executing-plans`, `systematic-debugging`, `test-driven-development`, `verification-before-completion`, `impartial-review`, `subagent-driven-development`, `dispatching-parallel-agents`, `using-git-worktrees`, `using-superpowers`, `writing-skills`, `applying-best-practices`, `finishing-a-development-branch`), craft (`impeccable`, `humanizer`). |
| `.claude/reference/` | Project memory: six topic files (`secrets`, `architecture`, `pitfalls`, `commands`, `tech-stack`, `deployment`) that `/recall` and `/learning` populate as you work. Committed, so it travels to every machine and sandbox. |
| `.claude/hooks/session-start.sh` | Cloud: auto-rebase onto origin/main. Local: read-only fetch. Both: re-assert session defaults, weekly template-drift nudge. |
| `.claude/scripts/context-weight.sh` | Prints the per-turn always-loaded context cost with a per-skill breakdown. |
| `.claude/settings.json` | Hook wiring plus a read-only Bash permission allowlist. |
| `.claude-plugin/` | Plugin and marketplace manifests (the no-clone install path). Template-only; removed by `/init-project`. |
| `bootstrap/` | Project creator scripts and `setup-machine.ps1` (below). Template-only. |

## After spawning a project

Run `/init-project` once. It detects the stack, asks a short Q&A (deploy target, verification limits, hard lines), and picks a **profile** (web-app / backend-CLI-library / data / writing) that prunes skills the project will never use. It then seeds the reference files, tunes the best-practices catalog, and commits.

From then on the project runs itself: gotchas get saved with `/recall save`, debug arcs end with `/learning`, and `/sync-starter` keeps improvements moving in both directions.

## Dotfiles for Claude

Machine-level `~/.claude` files (global CLAUDE.md, keybindings, personal skills) don't travel with any repo. Keep your copies in `bootstrap/machine/home-claude/` in your fork, then on any new machine:

```powershell
.\bootstrap\setup-machine.ps1          # copies missing files only; -Force overwrites; -DryRun previews
```

## Forking this template

One command retargets every functional upstream reference (template repo id in the skills, drift-check URL in the hook, bootstrap defaults, plugin manifests) to your fork:

```
bash bootstrap/retarget-fork.sh <you>/<your-fork>
```

Review the diff and commit. LICENSE attribution is left untouched, and the script verifies nothing was missed.

## Provenance & license

MIT (see `LICENSE`). Several skills are forked from upstream work, notably Jesse Vincent's [superpowers](https://github.com/obra/superpowers) (MIT) and Paul Bakaus's impeccable (Apache 2.0, itself based on Anthropic's frontend-design skill). `.claude/skills/PROVENANCE.md` tracks every skill's origin, license, and local deltas; per-skill LICENSE/NOTICE files ship in the skill folders.
