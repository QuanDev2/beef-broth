# beef-broth

The AI service behind [Pholio](../pholio). Pholio is named for *pho*; beef-broth is the
part that makes the pho good. This service turns a casual trip into a finished post:
you drop in your phone photos and a few bullet notes, and it culls the photos, writes
the story in your voice, and matches each photo to the part of the story it illustrates.

## What it does

Given a batch of phone photos and the user's rough bullet notes (location, date, what
happened), beef-broth produces a **draft post**:

1. **Understands each photo** with a vision model (content, mood, quality flags).
2. **Culls** the batch down to the user's chosen number, removing near-duplicates.
3. **Writes the story** from the user's bullet notes, in their chosen tone and length,
   grounded in what they actually wrote (no invented events).
4. **Matches photos to story beats** by semantic similarity (the food photo lands next
   to "the pho was amazing").

The user then refines (swap photos, edit text, reorder) and publishes. The AI does the
tedious 80%; the human keeps creative control over the last 20%.

## Architecture

A standalone **Python (FastAPI)** service. Pholio's Node/Express backend calls it over
HTTP; long-running work runs through Pholio's existing BullMQ queue. Embeddings live in
Postgres via **pgvector**.

```
Pholio (Node) ──HTTP──> beef-broth (Python/FastAPI) ──> LLM + vision + embedding APIs
      │                        │
      └── BullMQ jobs          └── Postgres + pgvector
```

## Status

Pre-build. Currently a learning + design repo: a 5-week sandbox sprint grows into the
service, then integrates into Pholio. See `docs/` for the roadmap and `design/overview.md`
for the full product + technical design.

## Layout

| Path | What |
|------|------|
| `design/overview.md` | Product concept, UX, feature spec, AI implementation design |
| `docs/roadmap-pre-week8.md` | The 5-week sandbox sprint (learn + build) |
| `docs/roadmap-post-week8.md` | Hardening + scaling track (after Pholio integration) |
| `docs/progress.md` | Append-only progress log |
| `sandbox/` | Weeks 1-4 practice code |
| `app/` | The FastAPI service (week 5+) |
