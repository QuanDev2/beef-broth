# beef-broth — Pre-Week-8 Roadmap (the 5-week sandbox sprint)

Learn the AI-engineering concepts and practice each in a Python sandbox, accumulating,
so that by Pholio's Week 8 the whole pipeline runs on dummy data and integration is just
a port. Builds the feature in `../design/overview.md`.

## How this works

- **Cadence:** ~1 hr/day, 7 days/week. **Timeline is flexible** — a week or two of slip
  is fine. Never compress two weeks into one to catch up; slip the schedule instead.
- **Teaching:** one concept per session, problem-first, stop-and-check (see `../CLAUDE.md`).
  A day lists **exactly one** idea; if a day's Learn block names a couple of sub-points,
  they build that single idea — they are not a queue to dump in one message.
- **Sandbox:** all code in `../sandbox/`. Write it like it will live; in Week 5 it becomes
  the real service in `../app/`.
- **Running example:** a fake **Saigon trip** — the bullet notes from `design/overview.md`
  plus ~30 sample phone photos. This is the single thread through every week; each day
  adds a real piece against it.
- **Fixed pipeline first, agentic later.** Build the steps as a plain ordered pipeline.
  The agent loop is a *taste* in Week 5 and the real work post-Week-8. Raw before frameworks.
- **Stack:** Python · a multimodal LLM API · a text-embedding model · CLIP (local) ·
  Postgres + pgvector · FastAPI (Week 5).

Each session: update `progress.md` at the end.

---

## Setup / Prerequisites (do this before Week 1 Day 1)

Quan flagged these as the likely Day-1 blockers. Have all three in place first, or Day 1
stalls on plumbing instead of teaching the concept.

- **API access (small spend from day one).** An API key for a multimodal LLM (vision +
  text) and a text-embedding model. Budget a few dollars; you start spending on real calls
  on Day 1. Put the key in a git-ignored `.env`, **never commit it** (roadmap and progress
  files are public/committable). **Pick one default provider so Day 1 teaches instead of
  shops** (e.g. the Anthropic or OpenAI API for the multimodal + text model, plus that
  vendor's or a small open text-embedding model). Wrap it behind `llm.py` so it stays
  swappable; the curriculum is vendor-neutral, but Day 1 needs a concrete key to call.
- **Local Postgres with pgvector.** You don't need it until Week 4, but install it now so
  Week 4 Day 1 isn't a setup day. Use Docker to match Pholio's stack (a `postgres:16` image
  with the `pgvector` extension). Note up front: you'll store **text caption embeddings**
  here (one dimension, e.g. `vector(1536)`); the **CLIP image embeddings** used for de-dupe
  are a *different* dimension (e.g. 512) and are not the same column. See `overview.md` §5
  "Two kinds of vector."
- **Sample Saigon-trip photos.** A folder of ~30 phone photos (JPEGs, the casual-user norm)
  in `../sandbox/`, deliberately including a couple of **near-duplicate bursts** and a few
  **bad frames** (blurry/dark) so de-dupe and quality flags have something real to catch.
  Pair them with the bullet notes from `design/overview.md`. This set is sized to *learn*
  and *demo the mechanics*, not to headline a big percentage; for a real cost-reduction
  number, run a large bursty batch once later (see Week 4 Day 6).

---

## Week 1 — Talk to a model + reliable structured output

**Why this week matters:** everything downstream is "call a model and get back something
your code can use." By the end you can call the API by hand, control it, reason about
cost, and reliably get valid JSON out.

**Sandbox artifact:** `sandbox/llm.py` — wraps the API and returns validated structured JSON.
**Feeds the feature:** the backbone of the story generator (job 3) and parsing vision
output (job 1).

### Day 1 — Python env + project setup; what an LLM API call is (request → response)

**Learn:** An LLM API call is just an HTTP request — you send a JSON payload (model +
your text), you get back a JSON response with generated text. No magic, no state. Analogy:
it's a vending machine; coin in (prompt), snack out (completion), and the machine forgets
you the instant it dispenses.

**Build:** Set up the `sandbox/` project (virtualenv, dependencies, API key loaded from a
git-ignored `.env`). Write the first lines of `sandbox/llm.py`: one function that sends a
hard-coded prompt ("Describe Saigon in one sentence") and prints the raw response.

**Done:** You can run `python sandbox/llm.py` and see a real model response, confirm no
secrets are committed, and explain what left your machine (request) and what came back
(response).

### Day 2 — Messages, roles (system/user/assistant), and why the model has no memory

**Learn:** A call sends a list of messages, each tagged with a role — system (standing
instructions), user (your input), assistant (the model's past replies). The model has no
memory; "conversation" is an illusion you create by resending the whole transcript every
call. Analogy: the model is an actor handed the full script each take; it remembers nothing
between takes, you just keep handing it a longer script.

**Build:** Extend `llm.py` to accept a messages list. Simulate a two-turn exchange about
the Saigon trip by manually appending the assistant's first reply and a follow-up user
message; then drop the earlier messages and show the model "forget."

**Done:** You can run a multi-message call and demonstrate, by deleting prior messages,
that memory is just resent context. You can explain the three roles and why statelessness
is the default.

### Day 3 — Tokens, context window, and cost (output costs more than input)

**Learn:** What a token is (~3/4 of a word); the context window as short-term memory; why
input vs output are billed differently and output is pricier.

**Build:** Add token + cost reporting to `sandbox/llm.py`: print prompt/completion/total
tokens and the dollar cost per call.

**Done:** You can run a call, read back exact token usage and cost, and explain why a long
caption prompt costs more.

### Day 4 — Temperature and params; making output predictable

**Learn:** Temperature controls randomness — low (~0) makes the model pick the most likely
next token every time (near-deterministic, repeatable), high makes it wander (varied,
creative). Related params: `max_tokens` (output cap), `top_p`. Analogy: temperature is how
loose the dice are; at 0 they're loaded to land the same way every roll. A pipeline wants
repeatable, so default low.

**Build:** Add `temperature` and `max_tokens` parameters to `llm.py`. Run the same Saigon
caption prompt three times at temp 0 and three times at temp 1; print the outputs side by
side.

**Done:** You can show identical outputs at temp 0 and varied outputs at temp 1, and
explain which setting the captioning and story steps should use and why.

### Day 5 — System prompts; steering behavior

**Learn:** The system prompt is the standing instruction that shapes every reply without
being part of the user's input — role, tone, rules, output expectations. It's the
highest-leverage lever for steering behavior before you touch the user message. Analogy:
it's the job description you give the actor before any scene; it colors every line.

**Build:** Add a configurable system prompt to `llm.py`. Write one that makes the model
behave like a terse travel-journal assistant, and show how the same Saigon user message
produces a different style with vs without it.

**Done:** You can flip the system prompt and watch the behavior change, and explain why
standing instructions belong there rather than glued onto each user message.

### Day 6 — Structured output: forcing valid JSON + validating it (build day)

**Learn:** Free-text replies are unparseable by code; you need the model to return JSON
matching a known shape, and you must *validate* it because models occasionally emit
malformed or extra fields. Approach: ask for JSON / use the API's JSON mode, then validate
with a schema (Pydantic). Analogy: a structured response is a form with labeled boxes, not
a handwritten letter; validation is checking every required box got filled.

**Build:** Add a structured-output path to `llm.py`: request JSON, parse it, and validate
against a small Pydantic model (e.g. `{summary: str, tags: list[str]}` over the Saigon
notes). Handle the failure case (retry or raise) when the JSON is invalid.

**Done:** You can call `llm.py` and get back a validated Python object (not a string), and
show what happens when the model returns bad JSON and how your code catches it.

> **Standing decision (2026-06-20):** use the **modern structured-outputs path from now on** —
> `client.messages.parse(output_format=schema)` (or `output_config.format`), which constrains
> the model at decode time and returns a validated object directly. Strict tool use is the other
> acceptable option. The ask-for-JSON + assistant-prefill (`"{"`) + manual-validate approach is
> **legacy/fallback only** (it 400s on Opus 4.6+/Fable 5; works on Haiku 4.5). It was learned once
> for understanding; don't reach for it by default. This applies to every later structured call —
> `caption.py` (job 1) and `story.py` (job 3) should both use `messages.parse`.

### Day 7 — Consolidate: `llm.py` helper, review (build day)

**Learn:** No new concept — consolidation. The week's payoff is one clean helper that wraps
the API, handles messages/system/temperature, reports tokens + cost, and returns validated
structured output. This is the backbone every later job calls.

**Build:** Refactor `llm.py` into a tidy reusable module: `call_llm(...)` for text and
`call_llm_structured(..., schema)` for JSON, with cost logging baked in. Add a couple of
inline usage examples against the Saigon notes.

**Done:** `llm.py` is a clean, documented helper you can import. You can walk an interviewer
through each parameter and demonstrate both a text call and a validated-JSON call in under
a minute.

**Week 1 Recap.** You built `sandbox/llm.py`: messages/roles, temperature and `max_tokens`,
a steering system prompt, token + cost reporting, and validated structured-JSON output with
a failure path. Everything downstream now has a reliable model wrapper to call.

**You can now answer:** "Why does the model have no memory, and how do you fake a
conversation?" and "Why does output cost more than input, and how do you get reliable JSON
out of an LLM?"

**Check-in:** Explain what each of the three roles does, and why you'd run the captioning
step at temperature 0 but might not run a creative story step there.

---

## Week 2 — Vision + the story generator (the generation half)

**Why this week matters:** you build two of the four AI jobs — turning photos into captions,
and turning bullet notes into a grounded story.

**Sandbox artifacts:** `sandbox/caption.py`, `sandbox/story.py`.
**Feeds the feature:** jobs 1 and 3 directly.

### Day 1 — Vision model calls: image → description

**Learn:** A multimodal LLM accepts images alongside text — you send the image (base64 or
URL) plus a prompt and get a text description back. Same request/response shape as Week 1,
one new input type. Analogy: same vending machine, it now takes a photo as the coin. This
is job 1, the trick that turns pixels into text so every later step is cheap text work.

**Build:** Start `sandbox/caption.py`. Send one Saigon sample photo to the vision model
with "describe this photo" and print the description.

**Done:** You can caption a real photo from the sample set and explain why turning a photo
into text early makes jobs 2b, 3, and 4 cheaper.

### Day 2 — Structured captions: content, mood, quality flags as JSON

**Learn:** A freeform description isn't usable downstream; you want a fixed schema —
`content` (what's in it), `mood`, and `quality_flags` (blurry, dark, eyes-closed) — as
validated JSON. This reuses Week 1's structured-output muscle on a vision call. Those
quality flags are exactly what culling will read later.

**Build:** Extend `caption.py` to request a structured caption per photo —
`{content, mood, quality_flags}` validated with Pydantic via `llm.py`. Run it on a few
Saigon photos, including a deliberately bad frame.

**Done:** You get a consistent JSON caption per photo, including quality flags, and can
explain how those flags feed the de-dupe/selection job in Week 4.

### Day 3 — Grounded generation: expand notes without inventing events

**Learn:** "Grounded" means the model may only use facts present in the input — it must not
invent a temple visit Sam never mentioned. This is the core trust requirement of the story
job. Technique: instruct the model to use only the provided notes, then test that nothing
fabricated slips in. Analogy: the model is a ghostwriter who can only use your interview
notes, not make up your weekend.

**Build:** Start `sandbox/story.py`. Feed the Saigon bullet notes and prompt for an expanded
paragraph that adds zero new events. Deliberately probe for hallucinated details.

**Done:** You can expand the notes into prose that invents nothing, and show a failure case
(a fabricated detail) plus the prompt wording that suppresses it.

### Day 4 — Controllable generation: tone and length as parameters

**Learn:** The user controls tone and length, so these become explicit inputs to the prompt,
not hard-coded values. One idea: parameterize generation so the same notes yield a
punchy-short or reflective-long story on demand.

**Build:** Extend `story.py` so `tone` and `length` are arguments injected into the prompt.
Generate the Saigon story in two tones (casual vs reflective) and two lengths.

**Done:** You can produce visibly different stories from the same notes by changing the
tone/length args, and explain why these are user controls per the feature spec.

### Day 5 — Assembling a structured story: title / sections (prose + beat_summary) / tags

**Learn:** The output isn't a blob of prose; it's a structured draft —
`{title, sections[], tags[]}`, where each section is a story beat. Each section carries
two text fields: the `prose` (what the reader sees) and a short `beat_summary` (a terse,
concrete phrase like "a bowl of pho, street food"). The `beat_summary` exists for **one
reason**: job 4 will match photos against *it*, not against the flowery prose. A long
narrative paragraph and a one-line photo caption point in different directions in
embedding space even when they're about the same thing, so matching paragraph-vs-caption
is noisy; matching summary-vs-caption is clean because both are short and concrete. This
shape is what Pholio saves and what job 4 consumes. Reuses structured output for the whole
story object.

**Build:** Extend `story.py` to return the validated
`{title, sections[{prose, beat_summary}], tags[]}` object from the Saigon notes, each
section a beat (arrival, food, museum, evening, …) with its own one-line `beat_summary`.

**Done:** You get a structured story object with discrete beats, each carrying a short
matching summary, and can explain why you match on `beat_summary` (not the prose) and why
sections (not one paragraph) are what the photo-matching step needs.

### Day 6 — Build: `caption.py` — caption the sample photos

**Learn:** Consolidation of job 1 — no new concept. Make `caption.py` production-shaped:
batch over the ~30 Saigon photos, save captions to disk, handle a bad image gracefully.

**Build:** Finish `caption.py`: iterate the sample photo folder, produce a structured
caption per photo, write them to a captions JSON file, and log token/cost totals via
`llm.py`.

**Done:** Running `caption.py` captions the whole sample set into a JSON file. You can state
the cost of captioning all 30 and explain why later you'll caption only the survivors.

### Day 7 — Build: `story.py` — Saigon bullets → grounded story (tone + length) + seed a grounding check

**Learn:** Consolidation of job 3 — tie grounding + controls + structure into one callable.
Plus: drop a *tiny* eval seed now so you're not flying blind for five weeks. The full eval
harness is post-Week-8, but a single grounding check costs ten minutes and catches
regressions the moment you change a prompt.

**Build:** Finish `story.py`: notes + tone + length → validated
`{title, sections[{prose, beat_summary}], tags[]}`, grounded, saved to disk. Then add
`sandbox/check_grounded.py`: a throwaway function that takes the story + the source notes
and flags any sentence that asserts an event not traceable to a note (simplest version:
ask the LLM "does every claim here trace to these notes? list any that don't"). Run it on
today's output. This seed grows into Week 5's light evals and post-Week-8 Module 1.

**Done:** One call turns the Saigon notes into a complete structured, grounded story in a
chosen tone and length, with `beat_summary` on each section. A one-shot grounding check
runs against it and would flag a fabricated sentence. You can walk an interviewer through
how it avoids hallucination, how you *check* that it did, and why the structure matters.

**Week 2 Recap.** You built `caption.py` (job 1: photos → structured captions with quality
flags) and `story.py` (job 3: grounded, tone/length-controlled, structured story from the
Saigon notes). Two of the four AI jobs now run against the real sample data.

**You can now answer:** "How do you turn a photo into something cheap to reason over?" and
"How do you stop an LLM from inventing events the user never mentioned?"

**Check-in:** Why caption a photo into structured text before doing anything else with it,
and how do you keep the generated story grounded in the notes?

---

## Week 3 — Embeddings + semantic matching (the retrieval half)

**Why this week matters:** the core new mental model. By the end you can match each story
beat to the photo that illustrates it.

**Sandbox artifact:** `sandbox/match.py` (the "pho is amazing" → food-photo demo).
**Feeds the feature:** job 4.

### Day 1 — The problem: why keyword matching fails to connect meaning

**Learn:** Keyword matching links exact words, not meaning — the beat "the food was
unforgettable" and a photo captioned "a steaming bowl of pho" share no words but belong
together. You need to compare meaning, not strings. Analogy: keyword search matches by
spelling; you need matching by idea. This is what motivates embeddings.

**Build:** In a scratch script (toward `match.py`), show the failure: do a naive word-overlap
match between a Saigon beat and the photo captions, and watch the right photo fail to match.

**Done:** You can demonstrate keyword matching missing an obviously-correct pairing, and
articulate why that pushes you to embeddings.

### Day 2 — What an embedding is; turning text into a vector

**Learn:** An embedding is a list of numbers (a vector) that encodes a piece of text's
meaning, positioned so similar meanings sit near each other in space. One concept: text →
vector. Analogy: it's a GPS coordinate for meaning; "pho" and "noodle soup" land on nearly
the same spot.

**Build:** Add an embed call (text-embedding API, via `llm.py` or a sibling helper) and
print the vector for one Saigon caption — show its length (dimensions) and that it's just
numbers.

**Done:** You can turn a caption into a vector and explain, in one sentence, what those
numbers represent.

### Day 3 — Cosine similarity, by hand

**Learn:** Cosine similarity measures the angle between two vectors — ~1 means same
direction (similar meaning), ~0 means unrelated. Doing it by hand demystifies the "magic."
Analogy: two arrows pointing the same way are about the same thing, regardless of length.

**Build:** Write a tiny cosine-similarity function by hand (no library) and score a
food-beat vector against a pho-photo vector vs a museum-photo vector.

**Done:** You compute similarity manually and show the food beat scoring higher against the
food photo than the museum photo. You can explain why angle, not raw distance, is the
measure.

### Day 4 — Text embeddings via API; comparing meanings

**Learn:** Now use the real embeddings API at scale and lean on a library for cosine. The
concept is comparing many meanings reliably: batch-embed and rank by similarity.

**Build:** In `match.py`, embed all Saigon `beat_summary` strings and all photo caption
`content` fields via the API, and for one beat rank every photo by cosine similarity.
(Match the short summary against the short caption content, not the full prose — see
Week 2 Day 5 for why.)

**Done:** For a given beat you get a ranked list of photos by meaning. You can explain the
cheap-text insight (matching happens on captions, not pixels) and why you embed the
`beat_summary` rather than the narrative prose.

### Day 5 — First look at image embeddings (CLIP) — for next week's de-dupe

**Learn:** CLIP produces embeddings for images (and text) in a shared space; next week you
use image embeddings to spot near-duplicate frames. One concept: an image can become a
vector too, locally, with no API call — which is why Python earns its place in the stack.
This is a look-ahead, not used in text matching.

**Build:** Install CLIP locally; embed two near-duplicate Saigon photos and one different
photo; print the pairwise similarities.

**Done:** You can produce image embeddings locally and see burst frames score as
near-identical. You understand this sets up Week 4's de-dupe.

### Day 6 — Build: embed the story beats and photo captions

**Learn:** Consolidation toward job 4 — produce and persist the two sets of vectors you'll
match.

**Build:** In `match.py`, embed all `beat_summary` strings (from `story.py` output) and all
caption `content` fields (from `caption.py` output), saving each vector alongside its source.

**Done:** You have stored vectors for every beat summary and every caption from the Saigon
trip, ready to pair. You can explain why both sides are embedded into the same space and
why you use the summary, not the prose.

### Day 7 — Build: `match.py` — pair each beat with its best photo

**Learn:** Consolidation — the "pho is amazing → food photo" demo, the whole of job 4.

**Build:** Finish `match.py`: for each beat, pick the highest-similarity photo (handle "one
photo per beat / don't reuse a photo" with a simple greedy pass) and output beat → photo
assignments.

**Interview note (know the tradeoff, ship the simple thing):** greedy assignment (take the
best pair, remove both, repeat) is easy but *not optimal* — an early greedy pick can steal
the only good photo for a later beat. The optimal version is the **assignment problem**,
solved by the Hungarian algorithm (`scipy.optimize.linear_sum_assignment`), which minimizes
total mismatch across all beats at once. Ship greedy for the MVP; be able to say in an
interview *why* it's suboptimal and what you'd reach for if it mattered.

**Done:** `match.py` assigns the Saigon beats to their illustrating photos, with the food
beat landing on the pho photo. You can demo it, explain the matching end to end, and name
the greedy-vs-optimal (Hungarian) tradeoff.

**Week 3 Recap.** You built `match.py` (job 4): the meaning-vs-keyword problem, embeddings,
cosine similarity by hand then via API, a first local CLIP image embedding, and beat → photo
assignments for the Saigon trip. The retrieval half is done.

**You can now answer:** "Why does keyword search fail to connect meaning?" and "What is an
embedding and how does cosine similarity rank by meaning?"

**Check-in:** Walk through how "the food was amazing" finds the pho photo when they share no
words — what's computed, and on what (captions, not pixels)?

> **Breadth add-on (interview prep, optional, ~1 day).** Job 4 is a *narrow slice* of RAG:
> embed two short sides, cosine-match. Real RAG over documents adds steps your product
> doesn't need but interviews ask about. Know each by name and a one-line purpose:
> - **Chunking:** split long docs into passages before embedding. You skip it because
>   captions are already short, so be ready to say *why* you don't chunk.
> - **Hybrid search (BM25 + vector):** keyword search catches exact terms (names, codes)
>   that embeddings blur; combine the two and merge scores.
> - **Reranking:** a second model re-scores the top-k retrieved items for precision.
> - **Contextual retrieval:** prepend a short context blurb to each chunk before embedding
>   so it isn't stranded out of context.
>
> Be able to say where you'd add hybrid or rerank if matching quality dropped. The Anthropic
> "Building with the Claude API" course covers this section hands-on (note: it uses Voyage +
> BM25, not your pgvector + CLIP, so take the concepts, not the code).

---

## Week 4 — pgvector + culling (storage + photo selection)

**Why this week matters:** move embeddings into Postgres/pgvector (exactly what Pholio uses)
and build the photo-selection job.

**Sandbox artifact:** `sandbox/cull.py` + a local pgvector database.
**Feeds the feature:** job 2, plus the pgvector pattern Pholio will use.

### Day 1 — Why a vector DB; set up pgvector locally

**Learn:** Holding vectors in memory doesn't persist or scale; a vector database stores them
and runs similarity search in SQL. pgvector adds this to Postgres — the exact stack Pholio
uses. One concept: why a vector DB, and getting pgvector running. Analogy: you've been
keeping flashcards in a shoebox; pgvector is the filing cabinet with a built-in "find
similar" drawer.

**Build:** Stand up local Postgres with the `pgvector` extension (Docker, matching Pholio's
`postgres:16` setup). Confirm the extension loads.

**Done:** You have local Postgres with pgvector enabled and can explain why embeddings belong
in the DB Pholio already runs.

### Day 2 — Store embeddings in Postgres; the `vector` column type

**Learn:** pgvector adds a `vector(n)` column type; you store an embedding as a row alongside
its source text and metadata. One concept: persisting vectors with their data. **`n` is
fixed per column** — this table holds **text caption embeddings** at the embedding model's
dimension (e.g. `vector(1536)`). The CLIP *image* embeddings from Day 5 are a different
dimension (e.g. 512) and do **not** go in this column; they're a separate space for a
separate job (see `overview.md` §5 "Two kinds of vector").

**Build:** Create a table for Saigon captions with a `vector(1536)` column (use your model's
actual dimension); insert the text caption-`content` embeddings from Week 3.

**Done:** The caption embeddings live in Postgres, queryable. You can explain the schema
(id, source text, vector), why the column dimension is fixed, and why the CLIP image vectors
are not stored here.

### Day 3 — Similarity queries in SQL; the `<=>` cosine-distance operator

**Learn:** pgvector exposes distance operators; `<=>` is cosine distance (smaller = closer).
You do similarity search in a SQL `ORDER BY` instead of in Python. One concept: the query.

**Build:** Write a SQL query that, given a beat's vector, returns the nearest photo captions
by `<=>`. Run it for the Saigon food beat.

**Done:** You retrieve the best-matching photo via SQL and can explain `<=>` (smaller
distance = more similar) and how it relates to the cosine similarity you computed by hand.

### Day 4 — Indexes (IVFFlat/HNSW) and what they trade

**Learn:** Without an index, similarity search scans every row; IVFFlat and HNSW are
approximate-nearest-neighbor indexes that trade a little accuracy for big speed. One concept:
the speed/recall tradeoff. Analogy: a library index lets you skip scanning every shelf, at
the rare cost of missing a mis-shelved book.

**Build:** Add an HNSW (or IVFFlat) index to the vector column; compare query time (and the
plan) with and without it on the Saigon set.

**Done:** You can show the indexed query is faster and explain what accuracy it trades.
Interview-ready on "how does similarity search scale?"

### Day 5 — De-dupe near-frames: image embeddings + a distance threshold

**Learn:** Burst photos are near-identical; using the Week 3 CLIP image embeddings, photos
within a small distance threshold are duplicates — keep the sharpest, suggest dropping the
rest. **Non-destructive: suggest, never delete.** One concept: thresholding image similarity
for de-dupe (job 2a).

**Build:** Start `sandbox/cull.py`: embed the Saigon photos with CLIP, group ones under a
distance threshold as near-dupes, and mark all-but-the-sharpest as suggested-drop. These
CLIP image vectors live **in memory for the run** (de-dupe only compares photos within one
trip's batch); they're a different space and dimension from the pgvector caption store, so
they don't go in that table.

**Done:** `cull.py` flags the burst duplicates in the sample set and keeps one per group.
You can explain the threshold, why it's a suggestion (not a deletion), and why the CLIP
vectors stay in memory rather than in the caption table.

### Day 6 — Selecting top N: quality score + a concrete diversity algorithm

**Learn:** After de-dupe, pick the user's N keepers. Two signals, and "diversity" is the one
people hand-wave, so make it concrete:

1. **Quality** — a score per photo from the caption `quality_flags` (penalize blurry, dark,
   eyes-closed). Easy.
2. **Scene diversity** — don't return five near-identical food shots. The method:
   **greedy max-min selection** over the caption embeddings. Start with the highest-quality
   photo; then repeatedly add the photo whose *minimum distance to everything already picked*
   is largest (i.e. the one least like what you've already chosen), breaking ties by quality.
   That spreads picks across scenes instead of clustering them. Analogy: you're seating N
   guests at a table and each new guest sits as far as possible from everyone already seated.

One concept: turning "diverse" from a vibe into an algorithm. Honest-risk note from
`overview.md` §7: "best N" is subjective and the weakest link; greedy max-min + quality is a
defensible, explainable heuristic, and the user-refinement step absorbs the rest of the
taste. Don't oversell it as beauty-ranking.

This is also where the **cheap-before-expensive ordering** pays off: de-dupe ran on free
local CLIP vectors first, so you only spent paid vision calls on the survivors, and only
those survivors needed captions to score here.

**Build:** Extend `cull.py`: score survivors by quality, then run greedy max-min over their
caption embeddings to select N diverse keepers. Confirm captioning happened *after* de-dupe
(survivors only).

**Done:** `cull.py` returns N diverse, good-quality keepers from the Saigon set, you can
explain greedy max-min in one breath, and you can articulate the cheap → expensive ordering.
(Want a hard cost-reduction number for the portfolio? Run `cull.py` once on a large, bursty
batch and record how many paid vision calls de-dupe avoided. The ~30-photo dev set
demonstrates the mechanic; a big batch gives you the quotable figure.)

### Day 7 — Build: `cull.py` — de-dupe, pick N, store + query in pgvector

**Learn:** Consolidation of job 2 plus the pgvector pattern Pholio will reuse.

**Build:** Finish `cull.py` end to end: CLIP de-dupe → caption survivors → store embeddings in
pgvector → select top N via quality + diversity, all on the Saigon photos.

**Done:** One run takes the raw Saigon photo set to N suggested keepers, with embeddings
persisted in pgvector. You can walk through the whole selection and why each step is ordered
as it is.

**Week 4 Recap.** You stood up local pgvector, stored and queried text caption embeddings with
the `<=>` operator, added an ANN index, and built `cull.py` (job 2): CLIP de-dupe by threshold
(in-memory image vectors), quality + greedy-max-min diversity selection of top N, and the
cheap-before-expensive ordering, non-destructive throughout.

**You can now answer:** "Why store embeddings in Postgres instead of memory, and how do you
query them?" and "Why run free local de-dupe before paid vision captioning, and how much it
saves depends on what?"

**Check-in:** Explain the cheap-before-expensive ordering: what runs first, what runs only on
survivors, and what determines how much expensive work it saves (hint: how bursty the batch is).

---

## Week 5 — Assemble + wrap as a FastAPI service + light evals

**Why this week matters:** chain the pieces into one pipeline, expose it as the HTTP service
Pholio will call, and sanity-check quality. This *is* the service.

**Sandbox/app artifact:** `app/main.py` — the FastAPI service: `POST /draft` with notes +
photos → `{ title, sections[], photoAssignments[], tags[] }`.
**Feeds the feature:** this is the deployable service, shaped for Pholio.

### Day 1 — Pipeline orchestration: wiring the steps cheap → expensive

**Learn:** The four jobs become one ordered pipeline: de-dupe (cheap) → caption the survivors
→ story from notes → match photos to beats. Orchestration is calling them in the cost-smart
order and passing each step's output to the next. One concept: the fixed pipeline (fixed now,
agentic later). Analogy: an assembly line where cheap filtering stations come before
expensive ones.

**Build:** In the sandbox (toward `app/main.py`), write a script that calls cull → caption →
story → match in order on the Saigon trip and prints the assembled draft.

**Done:** The whole Saigon trip runs through one ordered script to a draft. You can explain
the ordering and why you build the fixed pipeline before any agent.

### Day 2 — FastAPI basics: an endpoint, request/response

**Learn:** FastAPI turns a Python function into an HTTP endpoint with typed request/response
models. One concept: the endpoint. This is how Pholio's Node backend reaches the service.
Analogy: you've been calling functions locally; FastAPI puts a doorbell on them that others
can ring.

**Build:** Create `app/main.py` with a minimal FastAPI app and a health-check endpoint; run
it locally and hit it.

**Done:** A FastAPI server runs and responds to a request. You can explain request/response
models and why the service is exposed over HTTP.

### Day 3 — The service contract Node will call (`POST /draft`)

**Learn:** The contract is the promise: `POST /draft` takes `{notes, photos, n, tone, length}`
and returns `{title, sections[], photoAssignments[], tags[]}`. One concept: defining the
request/response schema the integration depends on. Pin it now so Week 8 is just wiring.

**Build:** Define the Pydantic request/response models for `POST /draft` in `app/main.py`;
stub the endpoint returning a fixed example payload in the exact agreed shape.

**Done:** `POST /draft` accepts and returns the agreed shape. You can explain why pinning the
contract early de-risks the Pholio port.

### Day 4 — Light evals: is matching right? is the story grounded?

**Learn:** You can't ship quality you don't measure; light evals are cheap checks — is each
beat matched to a sensible photo, did the story stay grounded (no invented events). One
concept: sanity-check quality. This is deliberately light; the full eval harness is
post-Week-8.

**Build:** Promote the Week 2 Day 7 `check_grounded.py` seed into a couple of real eval checks
on the Saigon output: a grounding check (every story claim traces back to a note) and a
matching spot-check; print pass/fail. These are the seed of post-Week-8 Module 1.

**Done:** You can run evals that flag a hallucinated sentence or a bad photo match. You can
explain what you measure and why output quality matters *more* when a lazy user reviews less.

### Day 5 — A first taste of making one step agentic (optional, just a teaser)

**Learn:** The fixed pipeline can't react to surprises; an agent is the model *deciding* which
tool to call and retrying failures instead of obeying a hard-coded order. Today is only a
teaser of that idea: wrap one step (e.g. re-caption a low-quality result) in a decide-then-act
loop, so you've felt the shape of it. One concept, kept light: fixed vs agentic, and why you
earn the agent only after the fixed version works *and* you have evals to prove it helps. The
real agent build is a dedicated module post-Week-8 (Module 2, right after the eval harness).

**Build:** Optionally, in a scratch file, let the model decide whether a caption is too weak
and call `caption` again, a one-tool mini-loop. Don't rewire the real pipeline.

**Done:** You can show one step retried by a model decision, and explain the line between the
fixed MVP and the dedicated agent module that follows evals (and why fixed comes first).

### Day 6 — Build: end-to-end `app/main.py` — notes + photos → draft post

**Learn:** Consolidation — the real service. `POST /draft` runs the actual pipeline, not a
stub.

**Build:** Wire `POST /draft` to run cull → caption → story → match and return the real
`{title, sections[], photoAssignments[], tags[]}` for posted notes + photos.

**Done:** A live `POST /draft` turns Saigon notes + photos into a real draft payload. You can
demo the request and walk through the pipeline behind it.

### Day 7 — Build: run the whole Saigon trip through it; write the Week 8 port checklist

**Learn:** Consolidation + handoff. Validate end to end and write down exactly what the Pholio
port needs.

**Build:** Run the full Saigon trip through `POST /draft`; capture the output; write the
Week 8 port checklist (deploy the service, add the pgvector column to Pholio's DB, have
Express call `/draft` via BullMQ, save the draft, test with real photos).

**Done:** The Saigon trip produces a complete draft through the deployed-shape service, and a
concrete port checklist exists. You can present the whole service as a portfolio piece.

**Week 5 Recap.** You chained the four jobs into one fixed, cheap → expensive pipeline behind
a FastAPI `POST /draft` with a pinned contract, added light grounding/matching evals, took a
single taste of agentic retry, and ran the full Saigon trip end to end with a Week 8 port
checklist written. This is the deployable service.

**You can now answer:** "How is your pipeline ordered and why?", "What's the service contract
Pholio calls?", and "Fixed pipeline vs agent — when and why does each apply?"

**Check-in:** Trace one Saigon request through `POST /draft` — every step in order, what it
produces, and where you'd later swap in an agent.

---

## → Pholio Week 8 (the port, a few days)

Pre-built skill makes this a wiring job, not a from-scratch build. Keep this deploy
**minimal** on purpose; hardening it (Docker image, hosting, secrets, retries) is its own
post-Week-8 module, not a Week-8 yak-shave.

1. Stand up the beef-broth service so Pholio can reach it. Minimal: containerize `app/`
   (a Dockerfile), run it somewhere Pholio's backend can hit over HTTP (local Docker network
   or one small host), with the API key supplied via env, not committed. "Production-grade"
   deploy is post-Week-8 Module 5; here you just need a reachable URL.
2. Add the pgvector column(s) to Pholio's Postgres at the **right dimension** (the text
   caption-embedding dim, e.g. `vector(1536)`); backfill if needed. Remember CLIP image
   vectors are a separate concern, not this column.
3. Have Pholio's Express backend call `POST /draft`; run the work through BullMQ so it never
   blocks a request thread.
4. Save the returned payload as a draft post; wire the refine + publish UI.
5. Test end-to-end with real phone photos.

**Watch for:** the contract drift (Pholio sends the shape `POST /draft` expects), the
embedding-dimension match on the new column, and async handoff (the worker, not the request,
does the slow work). These three are where ports usually bite.

Then continue with `roadmap-post-week8.md` (evals first, then the agent, then hardening + scaling).

---

## Skills covered by the sprint

LLM API + prompting + structured output · vision models · text embeddings · image
embeddings (CLIP) · pgvector similarity · RAG-style grounded generation · semantic
matching · pipeline orchestration · a Python FastAPI service · light evals. (Deeper
evals, robustness, the agentic upgrade, frameworks, and CLIP search live in the
post-Week-8 track.)
