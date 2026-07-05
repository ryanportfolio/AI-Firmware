# claude-starter

A Claude Code project template that stays in sync with the projects it spawns.

This template turns the config into a fleet: every new project starts from a tuned rule kernel, a curated skill set, a self-populating memory library, and session hooks. Improvements made in any project flow back to the template, and template updates flow out to every project.

Distilled from a production repo, with the project-specific content stripped out.

## Highlights

What sets this apart from a folder of dotfiles:

- **Two-way sync, not copy-paste.** Most templates are a one-shot scaffold. Here, `/sync-starter` pushes generic wins from any project back to the template, and a weekly session-start nudge tells every project when the template has moved ahead. The config is a fleet, not a snapshot.
- **Context cost is measured, not guessed.** `bash .claude/scripts/context-weight.sh` prints the exact per-turn token weight of everything always loaded, with a per-skill breakdown. `/optimize-context` is the playbook for cutting it. Almost no setups treat context as a budgeted resource — this one does.
- **Memory that survives the session.** `/recall save` and `/learning` write gotchas into a committed reference library (`.claude/reference/`), so hard-won knowledge travels to every machine, sandbox, and teammate instead of dying with the conversation.
- **Ultra-terse mode with guardrails.** The `caveman` skill cuts prose token usage ~75% while keeping full technical accuracy — with automatic clarity carve-outs for security warnings and irreversible actions.
- **Multi-agent review on demand.** `/impartial-review` dispatches five parallel fresh-context reviewers (four bucket specialists plus one loaded with the project's own rules); `/handoff-audit` generates a self-contained prompt so a *separate* zero-context session can independently verify a change.
- **Prototype before you commit.** `/lab` builds a throwaway HTML lab with live sliders so you tune a visual or feel element by hand, then ports the exact values into real code and deletes the lab.
- **One-click spawn, one-command fork.** `bootstrap/New-ClaudeProject.cmd` creates, clones, and strips a new private repo in one double-click. `bash bootstrap/retarget-fork.sh <you>/<fork>` repoints every functional upstream reference to your fork and verifies nothing was missed.
- **Hooks that do real work.** Session start auto-rebases in the cloud, primes git locally, re-asserts session defaults, and detects plugin/skill overlap — with the one-line fix printed for you.
- **CI-gated config.** Every push parse-checks the executable surface: bootstrap scripts, hooks, and JSON manifests. Broken config never lands.

## Why this exists

Claude Code works better with standing instructions, reusable skills, and accumulated project knowledge. But that value normally lives in a single repo and never propagates. claude-starter fixes the propagation problem in three ways:

- **Spawn configured.** New projects start with the kernel rules, skill set, and memory system already in place. `/init-project` tailors them to the actual stack in one short Q&A.
- **Self-improving.** `/recall` and `/learning` capture gotchas into a committed reference library as you work. `/sync-starter` moves generic wins back to the template, and a weekly session-start nudge tells a project when the template has moved ahead of it.
- **Measurably lean.** Always-loaded context is a per-turn tax. `bash .claude/scripts/context-weight.sh` prints the exact weight (the template-only baseline is roughly 4.5k tokens/turn as of this writing), and the `/optimize-context` skill is the playbook for cutting it.

## What you get

- A cross-cutting **rule kernel** (`CLAUDE.md`) loaded every turn: verification honesty, a git auto-commit/PR workflow, subagent discipline, and context-restraint principles.
- **32 skills** covering the project lifecycle, everyday workflow, engineering discipline, and craft.
- A committed **memory library** (`.claude/reference/`) that accumulates project knowledge instead of losing it between sessions.
- **Session hooks** that rebase in the cloud, prime git locally, re-assert session defaults, and warn about template drift and plugin overlap.
- **CI** that parse-gates the executable surface (bootstrap scripts, hooks, JSON manifests) on every push.

## Quick start

There are two independent ways to use this repo. Pick based on whether you want the whole setup or just the skills.

**A. Use it as a template** (the full setup: kernel, hooks, memory, skills)

- GitHub UI: **Use this template -> Create a new repository**, clone, open in Claude Code, run `/init-project`.
- One-click (Windows): double-click `bootstrap/New-ClaudeProject.cmd`. It creates a private repo from the template via the `gh` CLI, clones it, and strips the template-only files.
- CLI (Windows): `.\bootstrap\new-claude-project.ps1 -Name my-app -Dest C:\code`

**B. Install just the skills as a plugin** (any existing project, no clone)

```
/plugin marketplace add ryanportfolio/claude-starter
/plugin install claude-starter@claude-starter
```

This path reads the repo's marketplace manifest, so it works only once the repo is **public**. Plugin skills are namespaced (`/claude-starter:recall`, and so on). Projects spawned from the template ship the skills un-namespaced and do not need the plugin. If both end up active in the same project, the session-start hook detects the overlap and prints the one-line fix.

## What's inside

| Piece | What it does |
|---|---|
| `CLAUDE.md` | Kernel rules loaded every turn: verification honesty, git auto-commit/PR workflow, subagent discipline, context-restraint principles. Two `FILL IN` sections are configured per project by `/init-project`. |
| `.claude/skills/` | 32 skills (enumerated below), each a self-contained Markdown playbook. |
| `.claude/reference/` | Project memory: six topic files (`secrets`, `architecture`, `pitfalls`, `commands`, `tech-stack`, `deployment`) that `/recall` and `/learning` populate as you work. Committed, so they travel to every machine and sandbox. |
| `.claude/hooks/session-start.sh` | Cloud: auto-rebase onto origin/main. Local: read-only fetch. Both: re-assert session defaults, run the weekly template-drift nudge, warn on plugin overlap. |
| `.claude/scripts/context-weight.sh` | Prints the per-turn always-loaded context cost with a per-skill breakdown. |
| `.claude/settings.json` | Hook wiring plus a read-only Bash permission allowlist. |
| `.claude-plugin/` | Plugin and marketplace manifests (the no-clone install path). Template-only; removed by `/init-project`. |
| `bootstrap/` | Project-creator scripts plus `setup-machine.ps1` (see below). Template-only. |

## The skill set

32 skills, grouped by role. See `.claude/skills/PROVENANCE.md` for each skill's origin, license, and local changes.

- **Lifecycle** (5): `init-project`, `sync-starter`, `addskill`, `optimize-context`, `minimal`.
- **Workflow** (11): `recall`, `learning`, `safe-ship`, `pr`, `merge`, `caveman`, `enhance-prompt`, `handoff-audit`, `why`, `lab`, `conflict`.
- **Discipline** (14): `brainstorming`, `writing-plans`, `executing-plans`, `systematic-debugging`, `test-driven-development`, `verification-before-completion`, `impartial-review`, `subagent-driven-development`, `dispatching-parallel-agents`, `using-git-worktrees`, `using-superpowers`, `writing-skills`, `applying-best-practices`, `finishing-a-development-branch`.
- **Craft** (2): `impeccable`, `humanizer`.

## After spawning a project

Run `/init-project` once. It detects the stack, asks a short Q&A (deploy target, verification limits, hard lines), and picks a **profile** (web-app / backend-CLI-library / data / writing) that prunes skills the project will never use. It then seeds the reference files, tunes the best-practices catalog, removes the template-only files (including `.claude-plugin/`), and commits.

From then on the project runs itself: gotchas get saved with `/recall save`, debug arcs end with `/learning`, and `/sync-starter` keeps improvements moving in both directions.

## Self-improvement loop

- **`/recall save <text>`** appends a dated entry to the right reference file when a project quirk bites you.
- **`/learning`** captures the takeaways from a multi-attempt debug arc.
- **`/sync-starter`** pushes a generic win back to the template (or, rarely, pulls a template-born one down).
- The **weekly drift nudge** in the session-start hook tells a project when the template has shared-surface changes worth reviewing.
- **`context-weight.sh` + `/optimize-context`** keep the always-loaded footprint honest over time.

## Dotfiles for Claude

Machine-level `~/.claude` files (global `CLAUDE.md`, keybindings, personal skills) do not travel with any repo. Keep your copies in `bootstrap/machine/home-claude/` in your fork, then on any new machine:

```powershell
.\bootstrap\setup-machine.ps1          # copies missing files only; -Force overwrites; -DryRun previews
```

## Forking this template

One command retargets every functional upstream reference (the template repo id in the skills, the drift-check URL in the hook, the bootstrap defaults, the plugin manifests) to your fork:

```
bash bootstrap/retarget-fork.sh <you>/<your-fork>
```

Review the diff and commit. LICENSE attribution is left untouched, and the script verifies nothing was missed.

## Requirements

- **Claude Code** (this is a Claude Code configuration; nothing here runs standalone).
- **`gh` CLI** (optional): the one-click and CLI project creators use it to make a private repo. Without it, the scripts fall back to a local copy plus printed manual steps.
- **Windows-first bootstrap.** The creator/setup scripts are PowerShell (`.ps1` / `.cmd`); the session hooks are bash (they run under git-bash locally and in the cloud sandbox). Non-Windows users can still use the template via the GitHub "Use this template" path and adapt the scripts.

## Provenance & license

MIT (see `LICENSE`). Several skills are forked from upstream work, notably Jesse Vincent's [superpowers](https://github.com/obra/superpowers) (MIT) and Paul Bakaus's impeccable (Apache 2.0, itself based on Anthropic's [frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) skill). `.claude/skills/PROVENANCE.md` tracks every skill's origin, license, and local deltas; per-skill LICENSE/NOTICE files ship in the skill folders.
