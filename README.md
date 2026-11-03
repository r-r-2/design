# design

Design systems for my sites, written for AI coding agents first. Served at **https://design.rr2.dev**.

Each system gives an agent everything it needs to build on-brand UI without guessing:

- **`DESIGN.md`** in [Google's DESIGN.md format](https://github.com/google-labs-code/design.md): tokens in YAML front matter, then rules, do's and don'ts, and the exact markup of every component.
- **Versioned CSS** at `/<system>/v<major>/brand.css`, so a site pinned to `v1` never gets a breaking change.
- **Copy-ready components**, one HTML snippet each, with their rules.
- **`check.py`**, a conformance checker an agent runs on the site it just built.

The pages on the site are review sheets for people: live previews, light and dark, with the HTML next to each one.

## Systems

| System | Prefix | Version | Used by |
|---|---|---|---|
| [personal](https://design.rr2.dev/personal/) | `pb-` | 1.0.0 | rr2.dev, notes.rr2.dev, resume.rr2.dev |

## Use a system in a site

Add this to the site's `AGENTS.md` or `CLAUDE.md` (the review page has a copy button for it):

```md
## UI
This site uses the Personal brand design system v1.
- Before any UI work, read https://design.rr2.dev/personal/v1/DESIGN.md and follow it.
- Load https://design.rr2.dev/personal/v1/brand.css and put class="pb" on <html>.
- Copy component markup from DESIGN.md exactly. Use only --pb-* tokens and pb- classes.
- After changing UI, run: curl -sO https://design.rr2.dev/check.py && python3 check.py site . --system personal
  Fix every error before handing over.
```

For self-contained single-file pages, paste `brand.inline.min.css` into a `<style>` tag instead of linking `brand.css`. Its font URLs are absolute.

## Layout

```
systems/<id>/
  system.json        name, prefix, version, status, palette
  tokens.json        source of truth: colours (light/dark), type, spacing, radius, shadow, motion
  design.src.md      hand-written DESIGN.md prose, with markers the build fills
  DESIGN.md          generated, committed so agents can read it from the repo too
  css/*.css          component styles, using tokens only
  components/*.html  one snippet per component: metadata comment (name, group, summary, rules) + markup
  fonts/ assets/     woff2 files with licences, images
  CHANGELOG.md
site/                hub templates: index, system review page, hub.css, 404, _headers
scripts/build.py     builds every system into public/
scripts/check.py     contrast, DESIGN.md lint and site conformance (also published at /check.py)
public/              generated and committed; this is what Cloudflare serves
```

## Change something

1. Edit `tokens.json`, `css/`, `components/` or `design.src.md` in a system.
2. `python3 scripts/build.py`
3. `python3 scripts/check.py all`: every colour pair must pass AA, and DESIGN.md must lint with 0 errors and 0 warnings (needs `npx`).
4. `python3 scripts/check.py site systems/<id>/css --system <id>`: the system has to pass its own checker.
5. `python3 -m http.server -d public` and look at `/<id>/` in light, dark and at phone width.
6. Note the change in the system's `CHANGELOG.md`. Bump the patch or minor version for additions and fixes. A breaking change (renamed class, removed token) needs a new major, which creates a new `/v<major>/` folder and leaves the old one in place.

## Add a system

Copy `systems/personal/` to `systems/<new-id>/`, change `system.json` (pick a new prefix so classes never clash), rewrite the tokens, CSS and snippets, and build. The hub index and `llms.txt` pick it up automatically.

## Deploy

`public/` is served by a Cloudflare Worker with static assets (`wrangler.jsonc`), the same setup as resume.rr2.dev. Connect the repo in the Cloudflare dashboard, with no build command (the output is committed), and add the custom domain `design.rr2.dev`. `public/_headers` allows other sites to load the fonts and CSS cross-origin.

## Commits

[Conventional Commits](https://www.conventionalcommits.org/): `type(scope): summary`, lowercase, imperative, no trailing period. Scope is the system id or `hub`, `build`, `check`, `docs`.

## Licences

Code and docs: MIT. Fonts: SIL Open Font License 1.1, see each system's `fonts/LICENSE-*.txt`. Images in `assets/` (avatar, portrait, favicon) are not covered by the MIT licence.
