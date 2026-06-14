# beef-broth — Product & AI Design Overview

The single source of truth for *what* we're building and *how the AI works*. Read this
before product or implementation work. The build plan is in `../docs/`.

---

## 1. Product concept

Pholio is a post-centric **photo-blog**: a post is a story (title + rich text body) with
one or more photos. beef-broth is the AI service that makes *creating* those posts
effortless.

The core promise: **you shoot, it does the rest.** A casual traveler takes a pile of
phone photos and jots a few rough notes; beef-broth turns that into a publishable story
post. It is the inverse of Lightroom, which assumes you love the editing grind. Our user
does not.

### Audience: casual phone photographers (not pros)

We deliberately target **casual users shooting on phones**, not professionals shooting
RAW. This decision drives everything:

- Phone JPEGs are ~2-5 MB, not ~50 MB RAW. Storage, bandwidth, and processing cost all
  drop sharply.
- Casual users don't expect color grading or retouching; straight-from-phone is the
  norm (the Instagram standard). This **dissolves the photo-editing problem** entirely,
  because our user never wanted pixel editing in the first place.

### The persona

"Sam" shoots 300 photos on a weekend trip. Normally those die on the camera roll,
because culling + editing + writing is hours of work and Sam would rather be shooting.
Sam likes taking photos and dislikes editing, culling, and writing. beef-broth removes
exactly those three chores.

Note the persona flips the usual human-in-the-loop math: a precious pro wants control
over every pick; a lazy hobbyist *wants* the machine to decide and will often publish
with light review. That's good for adoption but raises the bar on output quality, since
there's less human catching mistakes.

---

## 2. What we are explicitly NOT building (and why)

This section exists so future sessions don't re-litigate settled calls.

| Rejected idea | Why |
|---|---|
| **Photo search engine** | A photo-blog has no haystack (a portfolio has dozens of posts, not thousands). Photo search pulls Pholio toward Flickr, the wrong identity. Users who want that go to photo-centric apps. |
| **Semantic search over posts** | Same haystack problem. Search is a weak place to put AI here, photo *or* text. |
| **AI photo editing (color/retouch)** | Real pixel editing is computer-vision/ML territory: GPU-heavy, needs model training (not the target skill), or a thin API wrapper (no differentiation). Crowded market (Lightroom, Photoshop). Casual users don't need it anyway. |
| **Mobile app (now)** | Deferred to a possible later side hustle. The AI service is form-factor agnostic, so web-first wastes nothing; mobile would later reuse the *same* beef-broth backend. Pivoting to mobile now resets the stack, the system-design narrative, and the job timeline. |

The reframe that survived all of this: don't make AI a *search* feature bolted on the
side; make it the *authoring* engine at the heart of how posts get made. Creating posts
is what a photo-blog is for.

---

## 3. UX walkthrough (first run)

1. **Onboarding (built for lazy).** Sign up, pick a username (`pholio.com/sam`), skip the
   rest. First screen: "Start a new trip post." One instruction.
2. **Dump the trip.** Enter location + date, jot a few bullet notes, drop in the phone
   photos. Then walk away; the work is async ("we'll sort this out").
3. **AI does the boring 80%.** Behind the scenes: cull near-duplicates, caption photos,
   pick the user's chosen number of keepers, draft the story from the notes, and match
   photos to story beats.
4. **Come back to a draft, not a chore.** A draft post: a title, the story in the user's
   tone and length, the selected photos placed next to the beats they illustrate.
5. **Refine (the user's 20%).** Swap a photo the AI dropped (the blurry one Sam loves),
   fix a sentence, reorder. Two minutes. Or on a lazy day, just publish.
6. **Publish.** A polished post is live. The portfolio fills up trip by trip with
   near-zero effort.

### The bullet-notes → story interaction (key)

The user writes the skeleton; the AI expands it. Example notes for a Saigon trip:

```
- Arrive 5am Sunday. Long immigration line at the airport.
- Hot and humid.
- Streets are crazy busy.
- Food is sooo good. Pho is amazing.
- War Remnants Museum, heartbreaking.
- Cafes and shopping in the evening.
- Met new people. Amazing day.
```

beef-broth turns this into a written story in the user's chosen **tone** and **length**,
**grounded** in the notes (it must not invent a temple visit Sam didn't mention).

Why skeleton-first instead of "AI writes everything":
- Stays authentic (the AI can't know what happened unless told).
- Avoids generic AI slop.
- The text-expansion alone is close to a plain ChatGPT call. **The moat is the
  integration** (notes + the right photos + matching + assembly into a post), not the
  prose generation. Build differentiation there.

---

## 4. Feature spec — the travel-journal post builder

**Input:** location, date, bullet notes, a batch of phone photos (e.g. ~100), the
desired number of photos in the post (user's choice, e.g. 5-10), tone, length.

**Output:** a draft post: `{ title, sections[], photoAssignments[], tags[] }`, where each
section is a story beat (its prose plus a short `beat_summary` used only for photo
matching) and photoAssignments pair photos to sections.

**Then:** the user refines (non-destructively) and publishes.

### Principles
- **Human-in-the-loop:** the AI proposes, the user disposes. Culling is a
  ranking/suggestion layer; rejected photos can be added back. Never delete.
- **Grounded generation:** the story uses only what's in the notes.
- **User controls:** number of photos, tone, length.

---

## 5. AI implementation design

Four AI jobs plus orchestration. (Concept names map to the sprint in
`../docs/roadmap-pre-week8.md`.)

| Job | Technique | Produces | Concept |
|---|---|---|---|
| 1. Understand each photo | Vision model (multimodal LLM) | Caption per photo: content, mood, quality flags | Vision API, structured output |
| 2a. Kill near-duplicates | Image embeddings (CLIP) + cosine similarity | Burst frames grouped; keep the sharp one | Embeddings, similarity, thresholds |
| 2b. Pick the best N | Quality heuristic + vision judgment + scene diversity | Top N keepers (user's number) | Ranking, combining signals |
| 3. Notes → story | LLM generation, grounded + controllable | Title + sections + tags, chosen tone/length, **plus a short `beat_summary` per section** | Prompt engineering, structured output, grounding |
| 4. Match photos to beats | Embeddings / semantic matching | Each beat paired with its illustrating photo | Retrieval / semantic similarity |

**Key trick:** job 1 turns every image into text. Once a photo is a caption, jobs 2b, 3,
and 4 are all text operations, which are cheaper and easier than reasoning over pixels.

**Matching detail (don't skip this):** job 4 must not embed the *full narrative section*
against the *terse caption*. A flowery paragraph and a one-line caption point in
different directions even when they're about the same thing, so cosine similarity gets
noisy. Fix: job 3 emits a short `beat_summary` per section (e.g. "a bowl of pho, street
food") and job 4 matches that summary against the caption's `content` field. Summary vs
caption, not paragraph vs caption. Both are short, concrete, and live in the same
text shape.

### Models
- Multimodal LLM API for vision (job 1) and story generation (job 3).
- Text-embedding model for matching (job 4).
- CLIP (runs locally in Python) for image de-dupe (job 2a). One reason Python earns
  its place in the stack.
- Postgres + pgvector to store captions and embeddings.

### Two kinds of vector (internalize this before Week 4)
There are **two different embedding spaces** in this system and they have **different
dimensions**, so they cannot share one column:

| Vector | From | Used by | Typical dim |
|---|---|---|---|
| **Text caption embedding** | text-embedding API | job 4 matching (and later cross-post search) | ~1536 |
| **CLIP image embedding** | CLIP, local | job 2a de-dupe | ~512 |

The persisted pgvector store holds the **text caption embeddings** (`vector(1536)`),
because that's what matching and any future search query against. The **CLIP image
vectors** are only needed within a single trip's batch to spot near-duplicate frames, so
they can stay in memory for the run (persist them later, in their own `vector(512)`
column, only when you build reverse-image search). Trying to stuff both into one column
is the classic Week-4 build-day crash.

### Data flow
```
Pholio (Node): upload photos to S3, collect notes, enqueue a "build draft" job
   └─ BullMQ worker calls →
        beef-broth (Python/FastAPI): vision captions, embeddings, cull, story, match
           └─ returns a structured draft payload
   └─ Pholio saves it as a draft post; user notified
Postgres + pgvector stores captions + embeddings.
```

### Cost-smart ordering (internalize this)
Vision-captioning is the slow, paid step; CLIP de-dupe is local and effectively free.
Order cheap → expensive: **de-dupe first with free local image embeddings, then caption
only the survivors**, not the whole batch. The savings scale with how bursty the input
is: a trip with lots of near-duplicate frames might drop a large fraction before any
paid call; a trip of all-distinct shots saves little. Sequencing cheap filters ahead of
expensive models is core AI-engineering instinct and a strong interview talking point.

A note on proof: the dev sample set is small (~30 photos), enough to *demonstrate* the
ordering and the de-dupe mechanic but too small to headline a big percentage. If you
want a concrete "cut N paid calls to M" number for the portfolio, run the pipeline once
on a real, large, bursty batch and capture the actual reduction. Cite measured numbers,
not assumed ones.

### Fixed pipeline now, agent right after evals
- **MVP:** a fixed pipeline, steps run in order, orchestrated by BullMQ. Enough for the
  Week 8 integration. Build this first; feel its limits.
- **Then evals (first post-Week-8 module):** a harness that scores the pipeline, so the
  next change is measurable, not vibes.
- **Then the agent (the very next module):** an agent with tools (`caption_photo`,
  `embed`, `draft_section`, `match_photos`) decides what to do, retries weak captions,
  handles odd inputs, instead of obeying a hard-coded order. The point of doing it *after*
  evals: you can prove with numbers whether the agent actually beats the fixed pipeline on
  quality, cost, and latency, or just costs more for the same result. Being the engineer
  who measured that is the hireable signal. Earn the agent after the fixed version works
  and the eval harness exists.

---

## 6. Scope tiers

| Tier | Scope | When |
|---|---|---|
| MVP | Batch → caption + embed → de-dupe → pick N → grounded story → match to beats → draft post. Fixed pipeline. | The 5-week sprint, integrated at Pholio Week 8 |
| V2 | Scene clustering, sequencing/hero-image suggestions | Post-Week-8 |
| V3 | Eval harness first, then the agentic pipeline; cost/latency optimization | Post-Week-8 |
| Differentiator | CLIP multimodal / reverse-image; frameworks (LangGraph, MCP) if they earn it | Post-Week-8 |

---

## 7. Honest risks

- **"Best N" selection is subjective** and the weakest link. Lean on de-dupe + scene
  diversity; let the user-refinement step absorb taste. Do not oversell beauty-ranking.
- **Cost + latency** scale with photo count. Mitigate with the cheap-before-expensive
  ordering, batching, caching, and caps. Never block the request thread.
- **Quality ceiling:** captions miss things; stories can read generic. Human-in-the-loop
  covers it, but with a lazy user reviewing less, output quality matters more, not less.
- **Ingest friction** is the real first-run hurdle. The lazy promise dies if getting
  photos in is annoying. Keep upload effortless.
- **Side-hustle competition** (Day One, Polarsteps, AI journal apps) matters *only* for a
  future product, not for the portfolio piece. Don't let it slow the build.

---

## 8. The meta-context (why this exists)

beef-broth is Quan's vehicle to learn AI engineering and land an AI-focused job, while
producing a real Pholio feature. The work is **AI engineering, not ML research**: wiring
smart API calls + embeddings + pipelines, not training models. That's why it's learnable
in weeks for an experienced full-stack engineer. The cut line is **MVP now, hardening
later**. Pholio (the web app) is what gets interviews; beef-broth is the differentiator.
