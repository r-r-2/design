# AGENTS.md

Guidance for AI coding agents working on this repo. (To *use* a design system in another site, read that system's `DESIGN.md` instead.)

## Working rules

1. **Confirm before building.** Propose the change in plain words and wait for Rahul's go-ahead before editing. Show a preview (screenshots of the review page, light and dark) before anything is pushed.
2. **Edit sources, never output.** Sources: `systems/<id>/{tokens.json,design.src.md,css/,components/,system.json}`, `site/`, `scripts/`. Generated: `systems/<id>/DESIGN.md` and everything in `public/`. Run `python3 scripts/build.py` after every change and commit both.
3. **Gates before handing over:**
   - `python3 scripts/check.py all`: AA contrast passes, DESIGN.md lints with 0 errors and 0 warnings.
   - `python3 scripts/check.py site systems/<id>/css --system <id>`: 0 errors, 0 warnings. The system must pass its own checker.
   - axe-core shows no WCAG A/AA violations on `/<id>/` in light, dark and at 390px wide, and nothing scrolls sideways.
4. **Tokens only.** Component CSS uses `var(--<prefix>-*)` for every colour, font, size, radius, shadow and duration. If a value is missing, add a token to `tokens.json` first.
5. **Snippets are the contract.** Every class a component needs appears in its snippet in `components/`. Snippets use generic copy (no real posts or people). The metadata comment has `name`, `group` (one of the groups in `build.py`), `summary` and `rules`.
6. **Versioning.** Additions and fixes: bump minor or patch in `system.json` and add a `CHANGELOG.md` entry. Renaming or removing a class or token is breaking: bump the major, which publishes a new `/v<major>/` folder. Never delete an old major's folder from `public/`.
7. **Prefixes never clash.** Each system has its own class and variable prefix, set in `system.json`.
8. **No JavaScript in components** beyond one-line inline handlers (theme toggle, opening a dialog). Prefer native elements: `<details>`, `<dialog>`, links for tabs.
9. **Commits:** Conventional Commits, lowercase, imperative, no trailing period.

## Sensitive information

This repo is public. Don't add personal contact details, credentials, or anything about Rahul's employer.
