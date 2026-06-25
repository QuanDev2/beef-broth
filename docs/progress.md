# beef-broth — Progress Log

> Append-only. Update at the end of each session. Never edit past entries.
> Status: [done], [skipped], [modified], or blank (not started).

---

## Pre-Week-8 Sprint

### Week 1 — Talk to a model + structured output

| Day | Concept | Status | Notes |
|-----|---------|--------|-------|
| 1 | Python env + first API call | done | |
| 2 | Messages, roles, statelessness | done | |
| 3 | Tokens, context window, cost | done | |
| 4 | Temperature + params | done | |
| 5 | System prompts | done | |
| 6 | Structured JSON output (build) | done | |
| 7 | `llm.py` helper (build) | done | |

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

### Week 1, Day 7 — Consolidate `llm.py` helper
Date: 2026-06-25
Status: done

Completed:
- Extracted the duplicated token/cost-reporting block (copy-pasted across both functions) into one module-private `_report_cost(usage)` helper; both `call_llm` and `call_llm_structured` now call it
- Removed Day-6 leftovers: the now-redundant `system=` JSON-API prompt on the structured path (`messages.parse` constrains shape at decode time), the dead `prompt` variable, and the unused `ValidationError` import
- `__main__` now demonstrates both paths in one run: a text call (`call_llm`, "Describe Saigon in one sentence") and a validated-JSON call (`call_llm_structured` → `NoteSummary`)
- Verified by running: text call 16 in / 49 out; structured call 281 in / 93 out (schema input-token cost as seen Day 6); structured returns a validated `NoteSummary` object

Notes:
- Week 1 complete. `sandbox/llm.py` is the reusable wrapper every later job (`caption.py`, `story.py`, `match.py`) imports: messages/system/temperature/max_tokens, cost logging, text + validated-structured paths
- Kept Haiku prices (`0.80`/`4.00`) inline rather than hoisting to named constants — fine at one model; revisit when a second model enters
- `_report_cost` is defined below its callers (works — name resolved at call time); left as-is
- Untracked `.vscode/` not committed; candidate for `.gitignore`

### Week 1, Day 6 — Structured JSON output
Date: 2026-06-20
Status: done

Completed:
- Added `call_llm_structured(messages, schema, ...)` to `sandbox/llm.py` with a Pydantic `NoteSummary` model
- First built the post-hoc validation path: requested JSON, hit the two real failures (code-fence wrapper → invalid JSON; wrong-shape keys like `trip_summary`), forced shape via a JSON-API system prompt + assistant prefill (`"{"`), and added a `try/except ValidationError` failure path
- Then refactored to the modern path: `client.messages.parse(output_format=schema)` → `response.parsed_output` returns a validated object with no system prompt, no prefill, no fence-stripping, no manual validation

Notes:
- Prefill (`"{"`) works on Haiku 4.5 but 400s on Opus 4.6+/Fable 5 — it's the legacy technique; structured outputs (`output_config.format` / `messages.parse`) is the current standard, with strict tool use as the other option
- Structured outputs costs input tokens for the schema (121 → 328 on this call); SDK caches a compiled schema ~24h so repeat calls with the same schema amortize it
- Leftover in `__main__`: still passes the now-unneeded `system=` and defines an unused `prompt`/`system` — harmless cruft to clean up on the Day 7 consolidation

### Week 1, Day 5 — System prompts
Date: 2026-06-14
Status: done

Completed:
- Added `system: Optional[str] = None` parameter to `call_llm()`
- Used `**kwargs` pattern to conditionally pass `system` only when not None (API rejects `system=None`)
- Demonstrated behavior change: same Saigon prompt produced different style with vs without system prompt
- System prompt added 16 tokens to input cost (17 → 33)

Notes:
- Python 3.9 requires `Optional[str]` from `typing` — `str | None` is 3.10+ only
- Anthropic SDK raises 400 if `system=None` is passed explicitly — must omit the key

---

### Week 1, Day 4 — Temperature and params
Date: 2026-06-14
Status: done

Completed:
- Added `temperature` and `max_tokens` as parameters to `call_llm()` with defaults (0 and 256)
- Ran same prompt 3× at temp 0 (identical token counts, near-identical output) and 3× at temp 1 (varied length and phrasing)
- Confirmed Anthropic caps temperature at 1.0 (not 2 like some other providers)

Notes:
- Captioning and matching steps will run at temp 0 for repeatability; story step may go slightly higher (0.3–0.5) if style variation is wanted

---

### Week 1, Day 3 — Tokens, context window, cost
Date: 2026-06-14
Status: done

Completed:
- Added token + cost reporting to `sandbox/llm.py`: prints input/output tokens and USD cost per call
- Observed Turn 2 input tokens jump from 17 → 74 (statelessness — full transcript resent)
- Cost formula: input * (0.80/1M) + output * (4.00/1M), formatted with `:.6f`

Notes:
- Output tokens cost 5× more than input on Haiku; shapes downstream design (keep output short/structured)

---

### Week 1, Day 2 — Messages, roles, statelessness
Date: 2026-06-14
Status: done

Completed:
- `call_llm` refactored to accept `messages: list[dict]` instead of a bare string
- Two-turn Saigon exchange built manually (user → assistant → user)
- Demonstrated forgetting by stripping history from the second call

Notes:
- Standing rule added to skill + memory: never auto-edit sandbox/app files during teaching

---

### Week 1, Day 1 — Python env + first API call
Date: 2026-06-14
Status: done

Completed:
- Virtualenv set up in `sandbox/.venv`, deps installed from `requirements.txt`
- `sandbox/llm.py` written: one function, hard-coded Saigon prompt, raw response printed
- Real API call confirmed working; `.env` verified git-ignored
- Repo published to GitHub: https://github.com/QuanDev2/beef-broth

Notes:
- Model set to `claude-haiku-4-5-20251001` for cheap iteration; will make it a parameter on Day 7
- README updated for GitHub audience before pushing
