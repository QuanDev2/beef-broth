# app

The beef-broth FastAPI service. Built in Week 5 of the sprint
(`../docs/roadmap-pre-week8.md`) by assembling the sandbox pieces into one pipeline
behind an HTTP endpoint, then integrated into Pholio at Week 8.

Service contract (draft): `POST /draft` with the user's bullet notes + uploaded photo
references → returns a draft post `{ title, sections[], photoAssignments[], tags[] }`.
