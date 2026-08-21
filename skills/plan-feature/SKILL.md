---
name: plan-feature
description: Break a feature or large task into small verifiable tasks on the board BEFORE writing code. Use when the user asks to "plan", "rozplanuj", "break down" a feature, when starting a feature that clearly needs multiple steps, or when a task in progress turns out bigger than expected and needs splitting.
---

# Plan a feature

Output of this skill is an updated `docs/tasks/TASKS.md` (and possibly ROADMAP/DECISIONS) — not code.

## Steps
1. **Anchor**: quote the SPEC feature (F-x) and ROADMAP phase this belongs to. If it's in neither, flag it: either it extends the plan (propose SPEC/ROADMAP edit + DECISIONS entry) or it's scope creep (propose Backlog or rejection). Do not plan unanchored work.
2. **Slice vertically**: prefer tasks that each produce something demo-able through the whole stack (thin end-to-end slice first, then widen). Avoid layer-cake tasks ("all models", then "all endpoints", then "all UI") — they defer integration risk to the end.
3. **Size**: each task ≤ ~half a work session and one branch's worth of change. If you can't write its VERIFY line in one sentence, it's too big.
4. **Order by risk**: unknowns and integrations first (external API, auth, file parsing), polish last.
5. **Write tasks**: `T-xxx · title · (Phase N, F-x)` + VERIFY line + suggested branch name `<type>/T-xxx-slug`. First one to Next (or Now if the board is empty), rest to Backlog in order.
6. **Surface decisions**: planning usually forces 1-2 choices (data shape, library). Log them in DECISIONS.md now, or add an explicit "decide X" task if genuinely open.

## Anti-patterns
- Tasks named "implement X" with no VERIFY — that's a wish, not a task.
- A plan that requires touching >10 files per task — slice thinner.
- Planning 20 tasks ahead in detail — plan the next 3-5 precisely, keep the rest coarse.
