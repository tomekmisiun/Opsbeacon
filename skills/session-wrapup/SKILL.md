---
name: session-wrapup
description: End-of-session ritual - sync the board with reality, log decisions, close out branches, leave a clean handoff so the next session (in any agent) starts cold without losing context. Use when the user says they're done for now, "podsumuj", "kończymy", "wrap up", before long breaks, or when context is about to be compacted/cleared during a long session.
---

# Session wrap-up

The next session starts with zero memory — possibly in a different tool. Everything worth keeping must land in files, git, or the board — now.

## Checklist
1. **Board sync** (`docs/tasks/TASKS.md`): finished work → Done with date; the Now task's real state reflected (still Now? split? blocked → Parked with unblock condition); discovered items → Backlog with `←T-xxx` origin notes.
2. **Decisions**: scan the session for choices made in conversation but not logged (library picked, schema shaped, approach rejected) → append to DECISIONS.md. Rejections are decisions too.
3. **Docs drift**: if the session changed structure or scope, update ARCHITECTURE/SPEC/ROADMAP or add an explicit "update docs: X" task — never leave it implicit.
4. **Branch hygiene**: `git status` + `git branch` — commit completed coherent work on the task branch (Conventional Commits, no attribution); if the task finished and merged, delete the branch locally and remotely; list any stale branches for the user. A half-done change needs a note on its task: what's done, what's not, next concrete step, any gotcha discovered.
5. **Handoff summary** (in chat, short): ✅ done this session / 🔨 state of Now + its branch / ⏭ first action next session / ⚠️ warnings (flaky test, TODO left in code, env quirk).

## Rule
No vague breadcrumbs ("continue the refactor"). The next-step note must be executable by someone with amnesia: file, function, what to do, how to verify.
