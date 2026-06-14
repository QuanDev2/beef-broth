# CLAUDE.md — beef-broth

Orientation for any Claude session opened on this repo. Read this fully, then read
`design/overview.md` (the product + AI design) and the relevant roadmap file in `docs/`.

## What beef-broth is

The **AI service for Pholio**. Pholio (`~/projects/apps/pholio`) is a post-centric
photo-blog. beef-broth is a **standalone Python (FastAPI) service** that turns a casual
trip into a draft post: the user drops in phone photos + rough bullet notes, and the
service culls the photos, writes the story in the user's voice, and matches photos to
the story beats. Human reviews and publishes. AI does the tedious 80%; the user keeps
control of the last 20%.

Full product concept, UX walkthrough, feature spec, and the AI implementation design
are in **`design/overview.md`**. Read it before doing product or implementation work.

## Why this repo exists (the meta-goal)

Quan is a full-stack engineer pivoting toward **AI engineering** to get a new job.
beef-broth is two things at once:
1. A **learning vehicle**: a 5-week sandbox sprint teaches the AI-engineering skills
   (LLM APIs, prompting, embeddings, RAG-style grounding, vision, pgvector, agents)
   by building toward this exact service.
2. A **portfolio piece + Pholio feature**: the sandbox grows into the real service and
   integrates into Pholio.

The job is the priority. Pholio (the web app) is the thing that gets interviews;
beef-broth is the AI differentiator on top.

## ‼️ Quan's learning style — READ BEFORE TEACHING ANYTHING

**One concept at a time, step by step. Never dump.**
1. Introduce **exactly one** concept. Not a list. One.
2. Build it up in stages, problem first, then the fix.
3. **Stop and check** he's with you before the next concept. Wait for his go-ahead.
4. Use an analogy when the concept is new.
5. Direct and concise; no sugarcoating, no filler.

A roadmap day that lists several concepts is a **queue**, not one message. Teach item 1,
pause, then item 2. Do not front-load. (Same standing rule as Pholio's CLAUDE.md.)

## How the plan is structured

- **`docs/roadmap-pre-week8.md`** — the 5-week sandbox sprint. Learn a concept, practice
  it in `sandbox/`, accumulate. By the end, the whole pipeline runs on dummy data (a
  fake "Saigon trip"). 1 hr/day, 7 days/week, **timeline is flexible** (a week or two of
  slip is fine; never compress to catch up).
- **`docs/roadmap-post-week8.md`** — hardening + scaling after the Pholio integration:
  evals, cost/latency, robustness, the agentic upgrade, observability, CLIP/multimodal.
- **`docs/progress.md`** — append-only log. Update at the end of each session. Never edit
  past entries.

## The Pholio integration point (Week 8)

Around Pholio's **Week 8**, the sandbox service ports into Pholio: Pholio's Express
backend calls beef-broth over HTTP, work runs through Pholio's existing BullMQ queue,
embeddings stored in Postgres via pgvector. Quan has budgeted a few days of Pholio delay
for this. Pholio's own roadmap lives in `~/projects/apps/pholio/docs/roadmap/`.

## Stack

Python · FastAPI · a multimodal LLM API (vision + text generation) · a text-embedding
model · CLIP (local, for image de-dupe) · Postgres + pgvector. Pholio side: Node/Express
/Prisma/BullMQ/React.

## Working agreements

- Sandbox code in `sandbox/`; the real service in `app/`. The sandbox *becomes* the
  service, so write it like it will live, not like throwaway.
- Build the **fixed pipeline first**, make it **agentic later** (raw before frameworks).
- Keep the **human-in-the-loop** principle: the service proposes, the user disposes.
  Culling is non-destructive (suggest, never delete).
- Roadmap and progress are public/committable. No secrets in them.
