---
description: Devil's advocate on a change you just made — argue the honest case AGAINST it. "Any reason not to?" A deliberate second-thoughts pass on the diff in front of you, before it lands. Surfaces scope creep, blast radius, irreversibility, a simpler path you skipped, YAGNI, or "this doesn't belong in this change" — the doubts your build-momentum buries. ONLY use when the user explicitly types the `/advocate` slash command. Reviews the change(s) just made (uncommitted diff by default, or an argument-scoped slice). Dispatches one fresh Opus subagent as a devil's advocate, fed only the diff and its stated goal, to build the counter-case with genuine distance, then synthesizes a keep / revise / drop verdict. Lightweight — one scoped skeptic, not the multi-agent /impartial-review, and not a bug hunt.
disable-model-invocation: true
---

# Advocate — any reason not to?

The user typed `/advocate`. They (or you) just made a change and, before it lands, want the devil's-advocate case: **any reason not to do this?** Not "is it buggy" — assume it works. The question is whether the change should exist, in this form, in this scope, at all.

You made the change. Your bias is to keep it. This skill exists to fight that bias on purpose.

**Trigger:** runs ONLY on the explicit `/advocate` command — slash-only, model auto-invocation disabled in the frontmatter. Don't fire on the word "advocate" in ordinary conversation.

## How this differs from neighbors

- **`/why`** pressure-tests a *recommendation* (a pick, advice) and stays well-rounded — both sides. `/advocate` pressure-tests a *change already made* and leans adversarial: the case against, because your confirmation bias already argues the case for.
- **`/impartial-review` / `/code-review`** hunt *bugs* in the diff. `/advocate` assumes the code is correct and asks whether it should ship — a judgment call, not a defect scan. If it turns up an actual bug in passing, name it and point at the bug-hunt skills; don't turn into one.
- **`/verification-before-completion`** runs the checks. `/advocate` questions the change itself, not whether tests pass.

## Step 1: Lock onto what's under review

- **Default: the change(s) just made** — the uncommitted working diff. Run `git status --short` and `git diff` (plus `git diff --staged`) to see it. If the working tree is clean, fall back to the most recent commit (`git show HEAD`) — the change just landed and the doubt is still worth voicing.
- If the user passed an argument (`/advocate the retry logic`, `/advocate the new dependency`), let it scope or redirect to that slice of the diff. Honor the argument over the default.
- If there is **no change to review** (clean tree, no relevant recent commit), say so in one line and stop. Don't invent a change to second-guess.
- Before anything else, get the change's **goal** clear in your own words: what problem it solves, why it was made. The counter-case is only fair if it's arguing against the real intent, not a strawman.

Open the final review with a single line restating what changed and its goal, so the user can confirm you're aimed right.

## Step 2: Get fresh eyes on the case against

Dispatch **one** subagent via the Agent tool — an independent devil's advocate. A model reviewing its own change rubber-stamps; the whole value of "any reason not to?" is distance the self-review can't manufacture.

- **Model:** the Agent tool's `opus` model (currently Opus 4.8). **Type:** `general-purpose`, fresh context.
- **Feed it only:** the diff under review (or the scoped slice) and a one-line statement of the change's goal. Do **not** paste the conversation or unrelated history. Minimal context is the point.
- **Ask it to build the strongest honest case *against* keeping this change**, specifically:
  - **Scope** — does this do more than the goal needs? Unrequested refactor, extra abstraction, defensive code, drive-by edits that belong in a separate change.
  - **Necessity** — does the change need to exist at all? Is it solving a symptom instead of the cause? Would doing nothing be defensible?
  - **Blast radius** — what else does this touch or break assumptions for? Callers, config, other environments, public API, on-disk/DB state.
  - **Reversibility** — how expensive is it to undo once it lands? A migration, a format change, a dependency added, a name others will build on.
  - **Simpler path** — was there a smaller or more local change that hits the same goal with less surface?
  - **Wrong-place / wrong-time** — right idea, wrong PR / wrong layer / premature (YAGNI).
  - Tell it to be specific and skeptical, cite the diff, and **not** restate what the change does approvingly. One or two cheap greps/reads are fine to ground a claim; no deep repo spelunking.
- **One agent only.** If dispatch fails or it returns nothing useful, build the counter-case yourself — don't block on it.

Then **you** own the synthesis: drop anything off-base (the agent lacks full repo/project context), keep what lands, fold it into the review below. Integrate — don't relay raw output.

## Step 3: Check the change against project rules

Quickly, where relevant, confirm the change doesn't collide with this project's own constraints — these are concrete "reasons not to" the generic reviewer can't know:

- `CLAUDE.md` kernel rules (scope discipline, naming/copy policies, no unrequested refactors, migration/install policy).
- The relevant `.claude/reference/` file for the area (`pitfalls.md`, `architecture.md`, etc.) via a quick read or `/recall`.

A change that works but violates a project rule is a real reason not to ship it as-is. Flag it.

## Step 4: Write the review

One line restating the change + goal (Step 1), then:

### The case against

The meat. The honest reasons not to do this, sharpened by the fresh reviewer and the project-rule check. Lead with the strongest. Be specific to *this* diff — "adds `lodash` for one `groupBy` you could write in three lines, and it's the only dep in this package" beats "adds a dependency." If the case against is weak, say that plainly rather than manufacturing doubt.

### Then, tight and conversational (no rigid headers):

- **Counter-weight** — the honest reasons the change *is* worth keeping despite the above. Keeps this from being contrarian theater. One or two lines.
- **Cheaper alternative** — only if a real smaller path exists. One line: what it is, what it gives up.
- **Verdict** — one line: **keep as-is / revise / drop**, with a confidence read and the one thing that would flip it. A calibrated "keep, but split the unrelated rename into its own change" beats a blanket thumbs-up or a reflexive "revert it."

## Style

- **Concise.** A handful of lines, not an essay. Cut anything that doesn't change how the user sees the change.
- **Adversarial but honest.** The job is to voice the doubt build-momentum buried — but a change that genuinely should ship should get a clear "keep." Don't invent objections to look rigorous.
- **Specific over generic.** No "consider the tradeoffs." Name the scope creep, the caller that breaks, the dependency, the simpler diff.
- **Render in caveman *full*** (default intensity) even when the session runs caveman *ultra* — a review carries nuance that ultra mangles. Resume the session's mode after. If the session isn't in caveman at all, write plainly.
- This skill **reviews — it does not implement.** No file edits while running it. If the verdict is revise or drop, that's a separate follow-up the user green-lights.

## Worked example

Change under review: *added a `retryWithBackoff` wrapper around every outbound HTTP call in `client.ts`; goal was to stop one flaky webhook from failing.* An ideal `/advocate` response (caveman full):

> **Change:** `retryWithBackoff` wrapped around all outbound calls in `client.ts`. Goal: stop one flaky webhook failing.
>
> ### The case against
> Scope > goal. One flaky endpoint → retry applied to *every* call, incl. non-idempotent POSTs → silent double-submits under transient errors. Blast radius wide: every caller now inherits added latency + swallowed-then-retried errors, harder to debug. Simpler path skipped: wrap the one webhook call, not the whole client. Reversibility: fine to undo now, but callers will start assuming retries → cost grows the longer it sits.
>
> **Counter-weight:** central retry is a real eventual want; the backoff impl itself looks sound.
>
> **Cheaper alternative:** retry only the webhook call site — 3-line change, zero blast radius. Promote to client-wide later with an idempotency guard.
>
> **Verdict:** revise — scope down to the one call. High confidence. Flip to "keep" only if the goal was actually "make the whole client resilient," which it wasn't.

Note the shape: restate → case against (the meat) → honest counter-weight → cheaper path → calibrated verdict. Short.

## Anti-patterns

- Firing on the word "advocate" outside the explicit `/advocate` command.
- Turning into a bug hunt — that's `/impartial-review` / `/code-review`. `/advocate` assumes correctness and questions the *decision*.
- Manufacturing objections so the review looks thorough. A clean change gets "keep."
- Contrarian theater — only downsides, reflexive "revert." The counter-weight and a calibrated verdict are mandatory.
- Feeding the subagent the whole conversation. Scope it to the diff + the goal, nothing more.
- Implementing the revision while running the skill. Review, verdict, stop.
- Generic caveats that fit any change ("weigh the tradeoffs", "consider maintainability").
