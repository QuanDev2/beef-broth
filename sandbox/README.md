# sandbox

Weeks 1-4 practice code from the 5-week sprint (`../docs/roadmap-pre-week8.md`).

Each week adds a piece of the pipeline against a fake "Saigon trip" example
(sample phone photos + bullet notes):

- Week 1 — `llm.py`: reliable LLM calls + structured JSON output
- Week 2 — `caption.py`, `story.py`: vision captioning + grounded story generation
- Week 3 — `match.py`: embeddings + photo-to-beat matching
- Week 4 — `cull.py`: pgvector + de-dupe + selection

Week 5 assembles these into the real service under `../app/`.
