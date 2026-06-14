# beef-broth

The AI service behind [Pholio](https://github.com/quandev/pholio) — a photo-blog where every post is a story.

Pholio is named for *pho*. beef-broth is the part that makes the pho good.

---

## What it does

You take 200 photos on a weekend trip. Normally those die on the camera roll because culling, editing, and writing is hours of work. beef-broth removes those three chores.

Drop in your phone photos and a few rough bullet notes. Walk away. Come back to a draft post.

Behind the scenes, four things happen:

1. **Understand each photo** — a vision model reads every photo and produces a structured caption: what's in it, the mood, and quality flags (blurry, dark, eyes-closed).
2. **Cull the batch** — near-duplicate burst frames are grouped and trimmed. Then the user's chosen number of keepers are selected by quality and scene diversity (no five identical food shots).
3. **Write the story** — the bullet notes expand into a grounded story in the user's chosen tone and length. The model may only use what's in the notes; it cannot invent events.
4. **Match photos to beats** — each story beat is paired with its illustrating photo by semantic similarity ("the pho was amazing" finds the food photo, even though they share no words).

The user then refines — swap a photo, fix a sentence, reorder — and publishes. The AI does the tedious 80%; the human keeps creative control over the last 20%.

---

## How it fits into Pholio

beef-broth is a standalone **Python / FastAPI** service. Pholio's Node/Express backend calls it over HTTP; the heavy work runs through Pholio's existing BullMQ queue so it never blocks a request. Embeddings are stored in Postgres via **pgvector** — the same database Pholio already runs.

```
Pholio (Node/Express)
  └── BullMQ worker
        └── POST /draft ──> beef-broth (Python/FastAPI)
                                  ├── Vision + LLM API  (captions, story)
                                  ├── Text embedding API (semantic matching)
                                  ├── CLIP local model   (image de-dupe)
                                  └── Postgres + pgvector (embeddings store)
```

The service returns a structured draft payload — `{ title, sections[], photoAssignments[], tags[] }` — which Pholio saves as a draft post for the user to review.

---

## Why this project exists

I'm a full-stack engineer pivoting toward AI engineering. beef-broth is two things at once:

- **A learning vehicle** — a 5-week sandbox sprint that teaches LLM APIs, vision models, embeddings, semantic matching, pgvector, and pipeline orchestration by building toward this exact service.
- **A real Pholio feature** — the sandbox grows into the production service and integrates into Pholio at week 8.

The skills covered: LLM API + prompt engineering + structured output, vision models, text and image embeddings, cosine similarity, pgvector similarity queries and indexing, RAG-style grounded generation, semantic photo-to-beat matching, pipeline orchestration, FastAPI, and a light eval harness.

---

## Stack

| Layer | Technology |
|-------|-----------|
| Service | Python, FastAPI |
| LLM + Vision | Anthropic API (Claude) |
| Text embeddings | Anthropic API |
| Image embeddings (de-dupe) | CLIP (runs locally) |
| Vector storage | Postgres + pgvector |
| Queue (Pholio side) | BullMQ (Node) |

---

## Project layout

| Path | Contents |
|------|----------|
| `design/overview.md` | Full product concept, UX walkthrough, feature spec, AI implementation design |
| `docs/roadmap-pre-week8.md` | The 5-week sandbox sprint — one concept per day, building toward the full pipeline |
| `docs/roadmap-post-week8.md` | Hardening + scaling track after the Pholio integration |
| `docs/progress.md` | Append-only session log |
| `sandbox/` | Week 1–4 practice code (`llm.py`, `caption.py`, `story.py`, `match.py`, `cull.py`) |
| `app/` | The FastAPI service (assembled in week 5) |

---

## Status

Active development — currently in the week 1 sandbox sprint. See `docs/progress.md` for the current position and `design/overview.md` for the full technical design.
