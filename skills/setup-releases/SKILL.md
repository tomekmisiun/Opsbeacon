---
name: setup-releases
description: Activate versioning, changelog generation and a release flow for a project that already works. Use ONLY when the user explicitly asks to start versioning/releases/changelog ("chcę wersjonować", "zróbmy release", "dodaj changelog") or declares the MVP working. Do NOT suggest or run this on early-stage projects - premature versioning is noise.
---

# Set up releases (deferred by design)

This project intentionally ships without versioning. Activate it only on explicit request. Precondition check: at least one ROADMAP phase ✅ and a runnable app — if not, say so and stop.

## What to set up
1. **git-cliff** for changelog generation from Conventional Commits (this is the payoff for the commit discipline — zero manual changelog writing):
   - Create `cliff.toml` with the standard conventional-commits template, grouping: feat → Features, fix → Bug Fixes, perf → Performance, refactor/docs/chore → hidden or grouped, breaking changes (`!`) highlighted on top.
   - Add command to AGENTS.md → Commands: `git cliff --tag <version> -o CHANGELOG.md`.
2. **Semver from commit types**: `feat:` → minor, `fix:`/`perf:` → patch, `type!:` or `BREAKING CHANGE:` footer → major. First release of a working MVP: `v0.1.0` (stay 0.x until the public contract stabilizes; document this in DECISIONS.md as D-xxx).
3. **Release procedure** — append to AGENTS.md as a short section:
   - releases cut from main only, never from a task branch
   - flow: `/drift-check` clean → tests green → `git cliff --tag vX.Y.Z -o CHANGELOG.md` → commit `chore(release): vX.Y.Z` → `git tag vX.Y.Z` → push with tags
4. **Optional CI release job** (ask first): a workflow triggered on `v*` tags that builds and attaches artifacts / publishes. Keep it minimal.

## Rules
- The changelog is generated, never hand-edited (fix the commits, not the changelog).
- A release is a task on the board like any other work: `chore/T-xxx-release-vX-Y-Z` with VERIFY = "tag pushed, changelog rendered, pipeline green".
- Log the versioning-start decision in DECISIONS.md (why now, chosen scheme).
