# beef-broth — Post-Week-8 Roadmap (hardening + scaling)

After the MVP is integrated into Pholio (Week 8), this track turns "it works" into
"it's measured, reliable, scalable, and I can talk about it in an interview." This is
also where the rest of the AI-engineering skill set lands.

## How this works

- These are **modules**, roughly one week each, ordered by dependency but flexible. The
  first two (Evals, then the Agent) are fixed in order on purpose; the rest you pick by
  need and interest. The job applications come first.
- Same teaching rule as `../CLAUDE.md`: **one concept per session, problem-first,
  stop-and-check.** A module that lists several bullets is a queue, not one lecture.
- Each module gives a **target metric** (what "good" means) and a concrete **Build/Done**,
  matching the daily rigor of the pre-Week-8 sprint. Don't start a module without writing
  down the number you're trying to move.
- Everything builds on the working MVP service in `../app/`.

The single guiding idea: **evals first, then the agent, then everything else.** You can't
improve, optimize, or trust what you don't measure, so you build the measuring stick
before you tune anything. And you only build the agent *after* evals exist, so you can
prove with numbers whether it actually beats the fixed pipeline.

**Module order:**

| # | Module | Why here |
|---|---|---|
| 1 | Evals | The measuring stick. Nothing after this is trustworthy without it. |
| 2 | The agentic upgrade | The headline AI-eng skill. Built right after evals so you can *prove* it helps. |
| 3 | Cost + latency | Now that you can measure, make it cheap and fast. |
| 4 | Robustness | Survive bad inputs and partial failures. |
| 5 | Deployment + packaging | Make it actually run somewhere, reproducibly. The demo depends on it. |
| 6 | Observability | See what it does in production. |
| 7 | Scaling | Handle volume without falling over. |
| 8 | Frameworks (if earned) | Adopt LangGraph/MCP now that you know what they abstract. |
| 9 | Multimodal + curation | The differentiator: true image search + richer layout. |
| 10 | Packaging for the job | Turn all of it into hireable proof. |

---

## Module 1 — Evals (do this first)

**Goal:** a harness that scores the pipeline so every later change is measurable.
**Target metric:** a repeatable scorecard with at least groundedness %, match-accuracy %,
mean latency, and mean cost per draft, run on a fixed golden set, committed and diffable.

- Why evals exist; the difference between "it seemed to work" and a number.
- Building a golden dataset (a handful of representative trips: notes + photos + the
  output you'd accept). Grow it from the Saigon set + your `check_grounded.py` seed.
- Scoring: story groundedness (did it invent anything?), match accuracy (right photo per
  beat?), selection sanity (diverse, in-quality keepers?).
- LLM-as-judge and its traps (it's lenient, inconsistent, and can be gamed; pin the judge
  prompt, spot-check it against your own labels).
- Latency and cost per run; logging every eval result; tracking regressions over time.

**Build:** an `eval/` harness that runs the golden set and prints a scorecard
(groundedness, match accuracy, latency, cost). Commit a baseline run.
**Done:** you can change a prompt, re-run, and see a number move (or regress). This
scorecard is the headline portfolio artifact and the baseline every later module is
measured against.

---

## Module 2 — The agentic upgrade (the agent in "AI engineer")

**Goal:** convert the fixed pipeline into a real agent and prove, against Module 1's
scorecard, whether it ships.
**Target metric:** agent variant scored head-to-head with the fixed pipeline on the golden
set; a clear, honest verdict (better / same / worse on quality, cost, latency) with the
numbers behind it.

This is a dedicated ~1-week block, taught day by day. The fixed pipeline obeys an order
you hard-coded; an agent is the **model deciding** what to do next from a set of tools.
Don't dump these days at once; one concept, stop-and-check.

### Day 1 — LLM vs agent: the decide → act → observe loop
**Learn:** the fixed pipeline can't react to surprises (a garbage caption sails downstream).
An agent runs a loop: the model picks a tool, your code runs it, the model reads the result,
repeat until done. Analogy: conveyor belt (fixed stations, fixed order) vs a cook (same
tools, tastes as they go and decides the next move). One concept: the loop.
**Done:** you can draw the decide → act → observe loop and name exactly which surprises the
fixed pipeline can't handle.

### Day 2 — Tool calling, one tool
**Learn:** how the model calls a function: you describe a tool (name, params, what it does),
the model returns a structured request to call it, your code runs it and feeds the result
back. Start with one tool, `caption_photo`. One concept: the tool-call mechanic.
**Done:** the model asks to call `caption_photo` with arguments, your code runs it and
returns the result, and you can explain the request/response of a tool call.

### Day 3 — The full toolset
**Learn:** expose `caption_photo`, `embed`, `draft_section`, `match_photos` as tools and let
the model choose which to call for a goal. One concept: a toolbox the model selects from.
**Done:** given a small goal, the model picks among several tools sensibly. You can explain
how tool descriptions steer its choices.

### Day 4 — The loop, stop conditions, and caps
**Learn:** an unbounded agent loops forever and burns money. You need a stop condition
(goal met) plus hard caps (max iterations, per-run token/cost ceiling). One concept: making
the loop terminate safely. Analogy: a Roomba needs a "done" signal and a battery limit, or
it runs all night.
**Done:** your loop stops on success and also stops at a max-iteration / cost cap, and you
can state both limits.

### Day 5 — State and memory across steps
**Learn:** the agent must carry context between steps (what it captioned, what it already
matched) without re-sending everything every call. One concept: managing run state.
**Done:** the agent reuses earlier results across iterations and you can show what's in its
working state at each step.

### Day 6 — Build: the agentic pipeline end to end
**Learn:** consolidation. The agent does the whole Saigon draft via tools, deciding the order
and retrying weak captions, instead of the hard-coded sequence.
**Build:** an agentic variant of the pipeline that produces a Saigon draft through the loop.
**Done:** the agent turns Saigon notes + photos into a draft, and you can point to a moment
where it *decided* something (retried a caption, skipped a step) the fixed pipeline couldn't.

### Day 7 — Build: agent vs fixed, scored, and a verdict
**Learn:** consolidation + the honest call. Sometimes the agent isn't worth it.
**Build:** run both the agent and the fixed pipeline through Module 1's eval harness; compare
groundedness, match accuracy, latency, cost.
**Done:** you have a side-by-side scorecard and a written verdict on which ships and why.
This "I measured the agent against the pipeline and here's the tradeoff" story is one of the
strongest things you can bring to an interview.

### Breadth add-ons to fold into this module (interview prep, optional)

> **Workflow patterns vocabulary (~1h).** You build chaining and an agent here already; just
> learn to *name* the taxonomy interviewers use:
> - **Chaining:** each step's output feeds the next. Your fixed pipeline IS this.
> - **Routing:** a classifier sends the input down one of several branches.
> - **Parallelization:** fan out independent subtasks, run them concurrently, gather results.
> - **Workflow vs agent:** in a workflow *you* fix the control flow; in an agent the *model*
>   decides it. That distinction is exactly your Day 7 verdict, stated in their words.
>
> **MCP awareness (~2h).** MCP (Model Context Protocol) is a standard way to expose tools and
> resources to any model client, so a tool you write once works across hosts instead of being
> hardcoded into one app. You build a real MCP server later (Module 8); for now just be able
> to explain what it is and when you'd reach for it (sharing tools across apps/clients, not
> re-wiring them per project).

---

## Module 3 — Cost + latency optimization

**Goal:** make it cheap and fast enough to run on real batches.
**Target metric:** a measurable drop in mean cost/draft and p50/p95 latency on the eval set
vs the Module 1 baseline, with the ordering's payoff re-confirmed by number.

- Caching (identical/near-identical requests and embeddings).
- Batching vision and embedding calls.
- Model tiering: cheap model where it's enough, expensive only where it matters.
- Hard caps: per-request budget and timeouts.
- Re-confirm the cheap-before-expensive ordering pays off; measure it on a large bursty
  batch (this is where you finally capture the quotable "cut N paid calls to M" number).

**Build:** apply the optimizations; re-run the eval set.
**Done:** a before/after table showing cost and latency down with quality held, plus the
real de-dupe reduction figure from a big batch.

---

## Module 4 — Robustness

**Goal:** survive bad inputs and partial failures without crashing or corrupting a post.
**Target metric:** every adversarial case in the eval set degrades gracefully (partial draft
or clear error), zero crashes, zero corrupted posts.

- Retries and backoff on API failures.
- Step error handling: a failed caption shouldn't kill the whole draft.
- Guardrails: input validation, output limits.
- Prompt-injection basics (a malicious caption or note shouldn't hijack the story).
- Edge cases: empty notes, one photo, hundreds of photos, all duplicates.

**Build:** add adversarial cases to the golden set; make the pipeline degrade gracefully.
**Done:** the adversarial eval cases pass (graceful degradation), and you can demo a forced
API failure that the pipeline recovers from instead of crashing.

---

## Module 5 — Deployment + packaging

**Goal:** make the service run somewhere reproducibly, so the demo and Pholio both have a
real URL to hit. (Week 8 stood up a *minimal* deploy; this hardens it.)
**Target metric:** a fresh clone builds and runs with one documented command, config comes
from env (no secrets in the image), and the service has a health check and clean startup.

- Dockerfile for `app/`; pin dependencies; small reproducible image.
- Config and secrets via environment, never committed; a `.env.example`.
- Run it on a real host (a small VM or container platform) reachable over HTTPS.
- Health/readiness endpoints; graceful startup/shutdown.
- Basic CI: lint + the eval harness on push, so regressions get caught.

**Build:** containerize and deploy; document the one-command run.
**Done:** someone (or future you) clones, runs one command, and the service is up and
answering `POST /draft`. The Saigon demo runs against the deployed URL.

---

## Module 6 — Observability

**Goal:** see what the service is doing in production.
**Target metric:** for any single draft request you can pull its full trace (per-step timing,
tokens, cost, outcome); dashboard shows latency, cost, and failure rate over time.

- Structured logging; tracing a single draft request end to end.
- Metrics: latency, cost, failure rate, per-step timing.
- A simple dashboard; alerting on cost/latency spikes; a kill switch.

**Build:** a dashboard + per-request traces for real Pholio traffic.
**Done:** you can take a draft ID and reconstruct exactly what happened, and you can show a
cost/latency trend line.

---

## Module 7 — Scaling

**Goal:** handle volume without falling over.
**Target metric:** a documented load test showing stable behavior (no unbounded queue
growth, controlled error rate, known throughput) at a target concurrency.

- Queue concurrency and worker tuning (BullMQ on the Pholio side).
- Large batches and backpressure; rate-limit handling against the model APIs.
- Where pgvector needs an index tune as posts grow.

**Build:** a load test; documented behavior under concurrency.
**Done:** a chart of throughput/latency under load and a written "here's where it breaks and
why" for the system-design interview question.

---

## Module 8 — Frameworks (only if they earn it)

**Goal:** adopt frameworks now that you know what they abstract.
**Target metric:** a framework version benchmarked against your raw loop on the eval set,
with an explicit keep/drop decision and the reasoning.

- LangGraph: rebuild the agent as a graph (nodes, edges, state); compare to your raw loop.
- MCP: expose a beef-broth tool as a standardized server.
- Decide deliberately whether they're worth the dependency.

**Build:** a framework version benchmarked against the raw one.
**Done:** a comparison and a decision you can defend ("I kept/dropped LangGraph because…").
Knowing when *not* to add a framework is itself a strong signal.

---

## Module 9 — The differentiator: multimodal + curation

**Goal:** the "real image search" and richer curation features.
**Target metric:** text-to-image search returns sensible photos for a query; reverse-image
"find similar" works; scene clustering visibly groups the trip.

- CLIP multimodal: embed images and text in one space → true pixel search. (This is where
  the CLIP image vectors finally get persisted, in their own `vector(512)` column.)
- Reverse-image search ("find similar photos") drops out of this almost for free.
- Scene clustering and sequencing/hero-image suggestions (feature V2).

**Build:** CLIP-powered matching + reverse-image lookup; richer draft layout.
**Done:** a working "search photos by description" + "find similar" demo, and clustering that
improves the draft's photo selection.

---

## Module 10 — Packaging for the job

**Goal:** turn the work into hireable proof.
**Target metric:** a recruiter or interviewer can, in five minutes, see what it does, that it
works (numbers), and how you'd scale it.

- Architecture writeup with a diagram and the decisions behind it.
- Presenting eval numbers (the proof it works) and the agent-vs-pipeline verdict.
- System-design talking points ("how would you scale this?").
- Common agent/RAG interview questions and your answers.
- A short demo (record the Saigon trip → draft post flow against the deployed service).

**Build:** README, architecture doc, eval scorecard, demo link.
**Done:** the repo tells the whole story without you in the room.

---

## Skill coverage (the full AI-engineer picture)

The MVP sprint gave you the building blocks. This track adds the parts that command the
pay premium: **evals, the agentic loop, cost engineering, production hardening, deployment,
observability, scaling, frameworks, and multimodal.** Combined with Pholio's full-stack +
system-design story, that's a strong AI-engineer profile.
