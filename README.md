# claude-starter

A batteries-included Claude Code project template: the workflow skills, reference/recall memory system, session hooks, and kernel CLAUDE.md distilled from a heavily-tuned production repo — with all project-specific content stripped out.

## What's inside

- **`CLAUDE.md`** — kernel rules: popup-tool ban, caveman-ultra default prose mode, verification honesty rules, subagent dispatch discipline, git auto-commit workflow, reference-library index. Two `FILL IN` sections (verification limits, deploy target) to configure per project.
- **`.claude/skills/`** — 29 portable skills, including:
  - *Template lifecycle:* `init-project` (one-time guided setup of a spawned project), `sync-starter` (two-way sync with this template)
  - *Workflow:* `recall` (project memory), `caveman` (terse mode), `safe-ship`, `pr`, `addskill`, `enhance-prompt`, `handoff-audit`, `why`, `learning`, `lab`, `conflict`
  - *Discipline:* `brainstorming`, `writing-plans`, `executing-plans`, `systematic-debugging`, `test-driven-development`, `verification-before-completion`, `impartial-review`, `subagent-driven-development`, `dispatching-parallel-agents`, `using-git-worktrees`, `using-superpowers`, `writing-skills`, `applying-best-practices`, `finishing-a-development-branch`
  - *Craft:* `impeccable` (frontend design), `humanizer` (de-AI writing)
- **`.claude/reference/`** — six skeleton topic files (`secrets`, `architecture`, `pitfalls`, `commands`, `tech-stack`, `deployment`) that `recall` and `learning` populate over time.
- **`.claude/hooks/session-start.sh`** — auto-rebase onto origin/main (cloud), read-only fetch (local), caveman directive + universal-skills reminder injection.
- **`.claude/settings.json`** — hook wiring + read-only Bash permission allowlist.
- **`bootstrap/`** — the one-click project creator (template-only; removed from spawned projects).
- **`.claude-plugin/`** — plugin + marketplace manifests so the skill set is installable without cloning (template-only).

## Installing the skills as a plugin (no clone)

Want the skills in an existing project without adopting the whole template? This repo doubles as a plugin marketplace:

```
/plugin marketplace add Aoh1578/claude-starter
/plugin install claude-starter@claude-starter
```

Plugin skills are namespaced (`/claude-starter:recall`, `/claude-starter:caveman`, …). The plugin ships **skills only** — the kernel `CLAUDE.md`, hooks, and reference library come with the template path below.

**Don't install the plugin into a project spawned from this template** — those already have the skills under `.claude/skills/` and you'd get duplicates.

## Creating a new project

### One click (recommended)

Double-click `bootstrap/New-ClaudeProject.cmd` (keep a copy anywhere). It prompts for a name, then:

1. Creates a **private** GitHub repo from this template (`gh repo create --template`)
2. Clones it locally
3. Removes the template-only bootstrap files

Requires the `gh` CLI authenticated (`gh auth status`). Without it, the script builds the folder locally and prints the manual repo-creation steps.

### Command line

```powershell
.\bootstrap\new-claude-project.ps1 -Name my-app -Dest C:\code
```

### GitHub UI

This repo is marked as a template — click **Use this template → Create a new repository** on GitHub, then clone. Delete `bootstrap/` and replace this README in the new project.

## After creating a project

1. Open the new folder in Claude Code.
2. Run `/init-project` — guided one-time setup: detects the stack, fills the `FILL IN` sections of `CLAUDE.md` via Q&A, seeds the reference files, tunes `applying-best-practices` to the stack, expands the README stub.
3. Start working — `recall`/`learning` will grow the reference library as quirks surface.

## Maintaining the template

Improvements discovered in any project flow back here, and template updates flow out to projects — `/sync-starter` handles both directions (selective, diff-driven; never clobbers project-tuned files). Future projects inherit template changes automatically at spawn.
