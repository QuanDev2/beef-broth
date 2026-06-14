---
name: simmer-it
description: >
  Run a beef-broth daily learning and build session: load project context and
  progress, teach today's single concept problem-first, walk through the build
  interactively, then commit and verify the day's deliverables and log progress.
  Use when Quan starts a beef-broth study or build session. Triggers on: "simmer
  it", "start today's session", "start beef-broth", "what's today", "let's cook",
  or any signal of beginning a beef-broth work session. Always use this skill when
  beef-broth is mentioned alongside session-start intent.
---

# Simmer It — Beef-Broth Daily Session Runner

Combined session skill: context load → brief → teach → build → commit → log.

## REPO ROOT

All paths below are relative to `~/projects/apps/beef-broth/` (bash: `$HOME/projects/apps/beef-broth`).

---

## PHASE 1 — Load Context

Read both files in parallel:
- `CLAUDE.md` — product vision, AI integration context, and the standing learning rules
- `design/overview.md` — current design state, data model, architecture decisions

Extract from `CLAUDE.md`:
- The **standing learning rule**: one concept per session, problem-first, stop-and-check before continuing. This overrides any efficiency pressure.
- Any other session-behavior notes.

---

## PHASE 2 — Find Position

Read `docs/progress.md`.

Locate the first day not marked **done**. That is today's target.

Determine which roadmap file owns that day:
- Before week 8: read `docs/roadmap-pre-week8.md`
- Week 8 and beyond: read `docs/roadmap-post-week8.md`

If `progress.md` shows the entire pre-week-8 sprint complete, switch to `docs/roadmap-post-week8.md` automatically; note this in the brief.

---

## PHASE 3 — Brief

Present in this order, concisely:

**1. Position**
One line: "Week X, Day Y — [topic name]"

**2. Week at a glance**
List all days in the current week. Mark ✓ done, → today, · upcoming.

**3. Today's objectives**
Show the full entry for today's day from the roadmap:
- **Concept** (what will be taught)
- **Learn** (what to understand by end of session)
- **Build** (what to produce / extend)
- **Done** (completion criteria)

**4. Flags from past sessions**
Scan `progress.md` for deviations, carry-overs, design drift, or notes marked for today. Surface anything relevant. If none, skip.

Keep this brief. Do not start teaching yet.

---

## PHASE 4 — Teach

**Standing rule (from CLAUDE.md):** One concept only. Problem-first. Stop-and-check. Never dump multiple concepts.

Procedure:
1. Open with the **problem** the concept solves — a concrete situation where you'd be stuck without it.
2. If the concept is likely new to Quan, lead with an analogy before the mechanism.
3. Explain the concept in one coherent block.
4. **Stop.** Ask: "Does that track? Any questions before we build?"
5. Do not proceed to Phase 5 until Quan confirms he's with you.

If Quan asks about a second concept mid-session, answer it briefly but do not expand it into a full teaching block. Keep the session anchored to today's one concept.

---

## PHASE 5 — Build

Walk through the build exercise interactively. Produce or extend the day's sandbox artifact:

| Roadmap stage | Primary artifact |
|---|---|
| Pre-week-5 | `sandbox/llm.py`, `sandbox/caption.py`, or equivalent day script |
| Week 5+ | `app/` — the running application |
| Post-week-8 | Per the post-week-8 roadmap entry |

Rules:
- Build one step at a time. Show code, explain what it does, let Quan run/extend it.
- If something deviates from `design/overview.md` (different field name, different call signature, architectural shortcut), flag it immediately: "This drifts from `design/overview.md` — do you want to update the design doc or stay on plan?"
- Do not produce the entire day's code in one dump. Interactive means interactive.

---

## PHASE 6 — Verify + Commit

Triggered when Quan signals he's done ("that's it", "wrap it", "commit it", or similar).

### 6a. Check git state

```bash
# Is the repo initialized?
git -C ~/projects/apps/beef-broth rev-parse --is-inside-work-tree 2>/dev/null || echo "NOT_INITIALIZED"

# If initialized — recent log and status
git -C ~/projects/apps/beef-broth log --oneline -5
git -C ~/projects/apps/beef-broth status
```

If the repo is **not initialized yet** (early days or first session), note it: "Repo isn't git-initialized yet — commits start once it is. Skipping git steps." Then proceed to Phase 7 (logging only).

### 6b. Commit uncommitted changes

If `git status` shows uncommitted changes:

```bash
git -C ~/projects/apps/beef-broth add -A
git -C ~/projects/apps/beef-broth commit -m "<clear message: what concept was built and what artifact changed>"
```

### 6c. Diff and verify

```bash
git -C ~/projects/apps/beef-broth diff HEAD~1 HEAD
```

Compare the diff against today's **Build** tasks and **Done** criteria from the roadmap. Mark each criterion:
- ✓ Done — evidence in the diff
- ✗ Missing — no evidence
- ~ Deviation — done differently; describe what changed and whether it matters

Present this table to Quan. If there are missing items or deviations, explicitly name them. Do not soft-pedal gaps.

If design drifted (new field, renamed route, different abstraction), say: "This changes `design/overview.md` — want me to update it now?"

---

## PHASE 7 — Log

Append to `docs/progress.md`. Never edit past entries.

Format:

```
### Week N, Day X — [topic name]
Date: YYYY-MM-DD
Status: done | partial | missed

Completed:
- [what was built]

Skipped (if partial):
- [what wasn't done, and whether it blocks the next session]

Notes:
- [deviations, design drift, key insight, things to revisit]
```

After appending, update the **Current position** marker in `docs/progress.md` to the next day (format used in that file — match whatever convention is already there).

---

## EDGE CASES

**Repo not git-initialized:** Skip 6a–6c. Note it. Log only.

**Pre-week-8 sprint fully done:** Announce it, auto-switch to `docs/roadmap-post-week8.md`, load it, find day 1 of the post-week-8 block, continue with the brief.

**Quan asks to wrap independently:** He can say "wrap it" at any point and Phase 6–7 runs immediately against whatever is committed.

**Concept already known:** If Quan says "I know this one, let's just build", skip the full teach block but still surface the one-liner problem statement so the build has context. Do not teach a second concept to fill the time.

**Burnout signal:** If Quan says he's burnt out or can't engage, do not present the day's plan. Say: "Rest day. Nothing logged. Come back when ready." Log nothing.

---

## WHAT NOT TO DO

- Do not load both roadmap files on every session. Load the one that owns today.
- Do not teach more than one concept per session, even if Quan asks.
- Do not produce the full day's code in one block. Build interactively.
- Do not edit past entries in `progress.md`.
- Do not proceed past Phase 4 without a stop-and-check confirmation.
- Do not manufacture encouragement or filler. Concise and honest.
