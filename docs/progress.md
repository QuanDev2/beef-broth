# beef-broth — Progress Log

> Append-only. Update at the end of each session. Never edit past entries.
> Status: [done], [skipped], [modified], or blank (not started).

---

## Pre-Week-8 Sprint

### Week 1 — Talk to a model + structured output

| Day | Concept | Status | Notes |
|-----|---------|--------|-------|
| 1 | Python env + first API call | | |
| 2 | Messages, roles, statelessness | | |
| 3 | Tokens, context window, cost | | |
| 4 | Temperature + params | | |
| 5 | System prompts | | |
| 6 | Structured JSON output (build) | | |
| 7 | `llm.py` helper (build) | | |

### Week 2 — Vision + story generator

| Day | Concept | Status | Notes |
|-----|---------|--------|-------|
| 1 | Vision calls: image → description | | |
| 2 | Structured captions (JSON) | | |
| 3 | Grounded generation | | |
| 4 | Tone + length controls | | |
| 5 | Structured story (title/sections/tags) | | |
| 6 | `caption.py` (build) | | |
| 7 | `story.py` + grounding-check seed (build) | | |

### Week 3 — Embeddings + matching

| Day | Concept | Status | Notes |
|-----|---------|--------|-------|
| 1 | The meaning-vs-keyword problem | | |
| 2 | What an embedding is | | |
| 3 | Cosine similarity by hand | | |
| 4 | Text embeddings via API | | |
| 5 | First look at image embeddings (CLIP) | | |
| 6 | Embed beats + captions (build) | | |
| 7 | `match.py` (build) | | |

### Week 4 — pgvector + culling

| Day | Concept | Status | Notes |
|-----|---------|--------|-------|
| 1 | Why a vector DB; pgvector setup | | |
| 2 | Store embeddings in Postgres | | |
| 3 | Similarity queries (`<=>`) | | |
| 4 | Indexes (IVFFlat/HNSW) | | |
| 5 | De-dupe near-frames | | |
| 6 | Select top N: quality + greedy-max-min diversity | | |
| 7 | `cull.py` (build) | | |

### Week 5 — Assemble + FastAPI service + light evals

| Day | Concept | Status | Notes |
|-----|---------|--------|-------|
| 1 | Pipeline orchestration | | |
| 2 | FastAPI basics | | |
| 3 | The `POST /draft` contract | | |
| 4 | Light evals | | |
| 5 | A taste of agentic (optional) | | |
| 6 | `app/main.py` end-to-end (build) | | |
| 7 | Run Saigon trip; Week 8 port checklist (build) | | |

---

## Pholio Week 8 — Integration

| Step | Status | Notes |
|------|--------|-------|
| Deploy beef-broth service | | |
| pgvector column on Pholio Postgres + backfill | | |
| Express calls `POST /draft` via BullMQ | | |
| Save draft post; refine + publish UI | | |
| End-to-end test with real photos | | |

---

## Post-Week-8 — Hardening (modules)

| Module | Status | Notes |
|--------|--------|-------|
| 1. Evals | | |
| 2. Agentic upgrade | | |
| 3. Cost + latency | | |
| 4. Robustness | | |
| 5. Deployment + packaging | | |
| 6. Observability | | |
| 7. Scaling | | |
| 8. Frameworks | | |
| 9. Multimodal/CLIP + curation | | |
| 10. Packaging for the job | | |

### Module 2 — Agentic upgrade (daily)

| Day | Concept | Status | Notes |
|-----|---------|--------|-------|
| 1 | LLM vs agent: decide → act → observe | | |
| 2 | Tool calling, one tool | | |
| 3 | The full toolset | | |
| 4 | Loop, stop conditions, caps | | |
| 5 | State + memory across steps | | |
| 6 | Agentic pipeline end-to-end (build) | | |
| 7 | Agent vs fixed, scored + verdict (build) | | |

### Breadth add-ons (interview prep, optional)

| Add-on | Fold in at | Status | Notes |
|--------|-----------|--------|-------|
| RAG depth (chunking, hybrid/BM25, rerank, contextual) | Pre-W8 Week 3 | | |
| Workflow patterns vocabulary (chain/route/parallel, workflow vs agent) | Post-W8 Module 2 | | |
| MCP awareness (build for real in Module 8) | Post-W8 Module 2 | | |

---

## Session Log

<!-- YYYY-MM-DD | Week X Day Y | Topic | Duration | Key insight or deviation -->
