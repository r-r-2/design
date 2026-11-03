---
version: alpha
name: "Personal brand"
description: "Calm paper-and-ink pages with a raspberry accent. Used by rr2.dev, notes.rr2.dev and resume.rr2.dev."
colors:
  primary: "#a8325e"
  secondary: "#3a5a80"
  neutral: "#f3f4f6"
  on-surface: "#1f2329"
  error: "#c2302f"
  paper: "#f3f4f6"
  surface: "#ffffff"
  surface-hover: "#f6f7f9"
  sunken: "#e9ecf0"
  line: "#e2e5ea"
  line-strong: "#cdd1d8"
  ink: "#1f2329"
  text: "#2c3038"
  muted: "#5d636d"
  raspberry: "#a8325e"
  raspberry-strong: "#8f2950"
  raspberry-soft: "#f8e5ed"
  slate: "#3a5a80"
  slate-strong: "#2f6690"
  slate-soft: "#e2edf6"
  amber: "#995700"
  amber-soft: "#fff1dc"
  green: "#0e7553"
  green-soft: "#ddf3ea"
  red: "#c2302f"
  red-soft: "#fbe6e6"
  on-accent: "#ffffff"
  glass: "rgba(243,244,246,.86)"
  scrim: "rgba(15,17,20,.45)"
typography:
  headline-display:
    fontFamily: "Fraunces"
    fontSize: 52px
    fontWeight: 600
    lineHeight: 1.08
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: "Fraunces"
    fontSize: 40px
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: -0.01em
  headline-md:
    fontFamily: "Fraunces"
    fontSize: 28px
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: "Fraunces"
    fontSize: 22px
    fontWeight: 500
    lineHeight: 1.35
  title:
    fontFamily: "Instrument Sans"
    fontSize: 18px
    fontWeight: 600
    lineHeight: 1.4
  body-lg:
    fontFamily: "Instrument Sans"
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.6
  body-md:
    fontFamily: "Instrument Sans"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
  body-sm:
    fontFamily: "Instrument Sans"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.6
  label-md:
    fontFamily: "Instrument Sans"
    fontSize: 13px
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: 0.08em
  label-sm:
    fontFamily: "JetBrains Mono"
    fontSize: 12px
    fontWeight: 600
    lineHeight: 1.5
  button:
    fontFamily: "Instrument Sans"
    fontSize: 15px
    fontWeight: 600
    lineHeight: 1
  code:
    fontFamily: "JetBrains Mono"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.6
  hand:
    fontFamily: "Caveat"
    fontSize: 19px
    fontWeight: 600
    lineHeight: 1.15
rounded:
  sm: 4px
  md: 8px
  lg: 12px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  sm-plus: 12px
  md: 16px
  md-plus: 20px
  lg: 24px
  lg-plus: 32px
  xl-minus: 36px
  xl: 48px
  xxl: 72px
  column: 720px
  wide: 1024px
  gutter: 24px
  header: 60px
components:
  button-primary:
    backgroundColor: "{colors.raspberry}"
    textColor: "{colors.on-accent}"
    typography: "{typography.button}"
    rounded: "{rounded.full}"
    height: "40px"
    padding: "18px"
  button-primary-hover:
    backgroundColor: "{colors.raspberry-strong}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.full}"
    height: "40px"
    padding: "18px"
  button-secondary-hover:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.md}"
    padding: "20px"
  tag:
    backgroundColor: "{colors.raspberry-soft}"
    textColor: "{colors.raspberry}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
  badge-new:
    backgroundColor: "{colors.amber-soft}"
    textColor: "{colors.amber}"
    rounded: "{rounded.full}"
  chip-selected:
    backgroundColor: "{colors.raspberry}"
    textColor: "{colors.on-accent}"
    rounded: "{rounded.full}"
    height: "32px"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    height: "40px"
    padding: "12px"
  toast:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    rounded: "{rounded.full}"
  dialog:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.lg}"
    padding: "24px"
  page:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.text}"
    typography: "{typography.body-lg}"
  meta:
    textColor: "{colors.muted}"
    typography: "{typography.body-sm}"
  list-row-hover:
    backgroundColor: "{colors.surface-hover}"
    textColor: "{colors.ink}"
  code-inline:
    backgroundColor: "{colors.sunken}"
    textColor: "{colors.ink}"
    typography: "{typography.code}"
    rounded: "{rounded.sm}"
  divider:
    backgroundColor: "{colors.line}"
    height: "1px"
  divider-strong:
    backgroundColor: "{colors.line-strong}"
    height: "1px"
  focus-ring:
    backgroundColor: "{colors.slate-soft}"
    textColor: "{colors.slate}"
  date-tile:
    backgroundColor: "{colors.slate-strong}"
    textColor: "{colors.on-accent}"
    rounded: "{rounded.md}"
    width: "44px"
  badge-live:
    backgroundColor: "{colors.green-soft}"
    textColor: "{colors.green}"
    rounded: "{rounded.full}"
  field-error:
    backgroundColor: "{colors.red-soft}"
    textColor: "{colors.red}"
  header:
    backgroundColor: "{colors.glass}"
    textColor: "{colors.ink}"
    height: "60px"
  dialog-backdrop:
    backgroundColor: "{colors.scrim}"
---

<!-- Generated by scripts/build.py from systems/personal/design.src.md, tokens.json and components/. Edit those, not this file. Version 1.0.0. -->
# Personal design system

## Overview

Calm, readable pages that feel written by a person, not generated by a product team. The look is **paper and ink**: a cool grey page, white cards, near-black text, and a single warm accent used sparingly. Long-form reading comes first: an 18px body in a 720px column, generous line height, and headings in a warm serif.

The feel is quiet and confident rather than flashy. Motion is calm, decoration is rare, and one small playful touch per page (a stick-figure guide, a handwritten aside) is the most there should ever be.

Built for plain, self-contained HTML pages with no framework. Every class is prefixed `pb-`, every variable `--pb-`. Add `class="pb"` to `<html>` to switch on the base styles.

**Load it** (pinned to major version 1):

```html
<html lang="en" class="pb">
<link rel="stylesheet" href="https://design.rr2.dev/personal/v1/brand.css">
```

For a single self-contained file, paste `https://design.rr2.dev/personal/v1/brand.inline.min.css` into a `<style>` tag instead. Its font URLs are absolute, so it works anywhere.

## Colors

Two brand colours on top of a neutral base.

- **Raspberry (`raspberry`, #a8325e):** the primary. The one main action per view, quotes, emphasis links, the default tag colour.
- **Slate (`slate`, #3a5a80):** the secondary. Focus rings, the current menu item, input focus. Never a filled button.
- **Paper (`paper`, #f3f4f6) and Surface (`surface`, #ffffff):** the page and the cards on it.
- **Ink (`ink`), Text (`text`), Muted (`muted`):** headings, body copy, and meta text, in that order of weight.
- **Line (`line`) and Line strong (`line-strong`):** hairline borders and dividers. Never use them for text.
- **Amber, green, red:** status only ("New", "Live", errors). Each has a `-soft` tint for backgrounds.

Text on a solid raspberry or slate fill uses `on-accent`. Every text and background pair passes WCAG AA (4.5:1) in both themes.

Sections can switch the accent with `data-accent="raspberry|slate|amber|green|neutral"`. Tags, chips, date tiles, callouts and card hovers inside follow it.

### Dark mode

Dark mode follows the system setting. To let visitors choose, set `<html data-theme="light">` or `data-theme="dark"` and store the choice. The tokens swap automatically; never write separate dark styles. Dark values:

| Token | Light | Dark |
|---|---|---|
| `paper` | `#f3f4f6` | `#1d1e20` |
| `surface` | `#ffffff` | `#2e2e33` |
| `surface-hover` | `#f6f7f9` | `#34353a` |
| `sunken` | `#e9ecf0` | `#37383e` |
| `line` | `#e2e5ea` | `#3a3b3f` |
| `line-strong` | `#cdd1d8` | `#4a4b4f` |
| `ink` | `#1f2329` | `#dadadb` |
| `text` | `#2c3038` | `#c4c4c5` |
| `muted` | `#5d636d` | `#a8a9aa` |
| `raspberry` | `#a8325e` | `#ec8db1` |
| `raspberry-strong` | `#8f2950` | `#f4a9c5` |
| `raspberry-soft` | `#f8e5ed` | `#3a1f2b` |
| `slate` | `#3a5a80` | `#93b4da` |
| `slate-strong` | `#2f6690` | `#82b6dd` |
| `slate-soft` | `#e2edf6` | `#1c2b38` |
| `amber` | `#995700` | `#f2a94a` |
| `amber-soft` | `#fff1dc` | `#3a2c19` |
| `green` | `#0e7553` | `#7fcca2` |
| `green-soft` | `#ddf3ea` | `#1f3328` |
| `red` | `#c2302f` | `#ef8f8e` |
| `red-soft` | `#fbe6e6` | `#3a2020` |
| `on-accent` | `#ffffff` | `#1d1e20` |
| `glass` | `rgba(243,244,246,.86)` | `rgba(29,30,32,.86)` |
| `scrim` | `rgba(15,17,20,.45)` | `rgba(0,0,0,.6)` |

## Typography

**Fraunces** (serif, 500 and 600) for page titles, section headings and card titles. **Instrument Sans** (400 to 600) for all reading and interface text. **JetBrains Mono** for code, tags and token names. **Caveat** only for the guide's speech bubble.

Use the type classes rather than setting sizes by hand:

| Style | Class | Font | Size / weight / line height |
|---|---|---|---|
| `headline-display` | `.pb-display` | Fraunces | 52px / 600 / 1.08 |
| `headline-lg` | `.pb-h1` | Fraunces | 40px / 600 / 1.15 |
| `headline-md` | `.pb-h2` | Fraunces | 28px / 600 / 1.3 |
| `headline-sm` | `.pb-h3` | Fraunces | 22px / 500 / 1.35 |
| `title` | `.pb-h4` | Instrument Sans | 18px / 600 / 1.4 |
| `body-lg` | `.pb-body` | Instrument Sans | 18px / 400 / 1.6 |
| `body-md` | `.pb-ui` | Instrument Sans | 16px / 400 / 1.5 |
| `body-sm` | `.pb-small` | Instrument Sans | 14px / 400 / 1.6 |
| `label-md` | `.pb-label` | Instrument Sans | 13px / 600 / 1.4 |
| `label-sm` | `.pb-tag` | JetBrains Mono | 12px / 600 / 1.5 |
| `button` | `.pb-btn` | Instrument Sans | 15px / 600 / 1 |
| `code` | `.pb-code` | JetBrains Mono | 14px / 400 / 1.6 |
| `hand` | `.pb-hand` | Caveat | 19px / 600 / 1.15 |

Headings use slightly negative tracking and `text-wrap: balance`. Labels are uppercase with `0.08em` tracking. Dates and counts use tabular figures. Never go bigger than `headline-display` (52px), and use it at most once per page.

## Layout

A centred **720px reading column** (`pb-wrap`) for articles, and a **1024px wide column** (`pb-wrap is-wide`) for headers, listings and dashboards, both with 24px gutters (16px on phones). The header is a 60px sticky bar with a frosted background.

Spacing follows a **4px scale**: 4, 8, 12, 16, 20, 24, 32, 36, 48, 72. Use `pb-stack` (vertical) and `pb-cluster` (wrapping row) for gaps between elements, with `is-tight` (8px), default (16px), `is-loose` (24px) and `is-section` (48px). Sections on a page sit 48 to 72px apart.

One breakpoint matters: at **560px and below**, headings step down a size, gutters shrink to 16px, and the header hides the "rr2.dev" text and optional menus.

## Elevation & Depth

Depth comes from **tone and hairlines**, not shadows. White cards sit on grey paper with a 1px `line` border. The resting shadow is barely visible; the lift shadow appears only on hover for clickable cards. In dark mode shadows are off and borders do all the work.

Hover lifts are small: cards rise 3px, chips 1px, date tiles tilt 3°.

## Shapes

Soft but not bubbly. **8px corners** for cards, panels, inputs and code blocks; **4px** for inline code; **12px** for dialogs and speech bubbles; **fully round** for buttons, chips, tags, badges and toasts; circles for avatars. Borders are always 1px.

## Components

Copy the markup exactly. Each component's rules come first, then its HTML. Live previews of all of them are at https://design.rr2.dev/personal/.

### Text

#### Type

Type classes for every text style. Use these instead of setting sizes.

- One pb-display or pb-h1 per page. Section headings are pb-h2, sub-sections pb-h3.
- pb-lede goes right under the page title; pb-label goes above a heading or a group.
- Inside long-form content, plain <h2>/<h3>/<p> in .pb-content are styled for you.

```html
<div class="pb-stack is-tight">
  <p class="pb-label">Section label</p>
  <h1 class="pb-display">Display heading</h1>
  <h1 class="pb-h1">Page title</h1>
  <h2 class="pb-h2">Section heading</h2>
  <h3 class="pb-h3">Sub-section heading</h3>
  <h4 class="pb-h4">Small heading</h4>
  <p class="pb-lede">A lede introduces the page in a sentence or two.</p>
  <p class="pb-ui">Interface text for lists, menus and forms.</p>
  <p class="pb-small">Small text for summaries and captions.</p>
  <p class="pb-ui">Inline <code class="pb-code">code</code> and an <a class="pb-link" href="#">emphasis link</a>.</p>
</div>
```

### Layout

#### Page skeleton

Every page starts from this. Skip link, sticky header, main column, footer.

- Put class="pb" on <html> and load brand.css (or inline brand.inline.min.css).
- Use <main class="pb-wrap"> for reading pages and <main class="pb-wrap is-wide"> for listings.
- The skip link is the first thing in <body> and points at the main element's id.
- Keep the inline theme script in <head> so the saved theme applies before paint.

```html
<!doctype html>
<html lang="en" class="pb">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Page title — rr2.dev</title>
  <link rel="stylesheet" href="https://design.rr2.dev/personal/v1/brand.css">
  <script>try{var t=localStorage.getItem('pb-theme');if(t)document.documentElement.dataset.theme=t}catch(e){}</script>
</head>
<body>
  <a class="pb-skip" href="#main">Skip to content</a>
  <!-- Header component here -->
  <main class="pb-wrap" id="main">
    <h1 class="pb-h1">Page title</h1>
    <p class="pb-lede">One or two sentences that say what this page is for.</p>
  </main>
  <!-- Footer component here -->
</body>
</html>
```

#### Header

Sticky frosted bar. Avatar and "rr2.dev / section" on the left, menu and theme toggle on the right.

- "rr2.dev" always links to https://rr2.dev; the section name links to the site's home.
- At most four menu items. Mark the current page with aria-current="page" on the link and wrap its text in <span>.
- Add is-optional to the menu if it can disappear on phones (in-page jump links). Real site menus should have three short items or fewer so they fit.
- The toggle needs the small script shown, and its aria-label.

```html
<div class="pb-top">
  <header class="pb-nav">
    <div class="pb-logo">
      <a href="https://rr2.dev" aria-label="rr2.dev"><img class="pb-ico" src="https://design.rr2.dev/personal/v1/assets/avatar.webp" width="24" height="24" alt=""><span class="pb-root">rr2.dev</span></a>
      <span class="pb-slash">/</span><a href="/">section</a>
    </div>
    <div class="pb-cluster is-tight">
      <ul class="pb-menu">
        <li><a href="/posts/" aria-current="page"><span>Posts</span></a></li>
        <li><a href="/about/"><span>About</span></a></li>
      </ul>
      <button class="pb-toggle" type="button" aria-label="Switch light or dark theme" onclick="var r=document.documentElement,d=r.dataset.theme?r.dataset.theme==='dark':matchMedia('(prefers-color-scheme: dark)').matches;r.dataset.theme=d?'light':'dark';try{localStorage.setItem('pb-theme',r.dataset.theme)}catch(e){}">
        <svg class="pb-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        <svg class="pb-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
      </button>
    </div>
  </header>
</div>
```

#### Footer

Quiet, centred footer with social icons and one line of links.

- Keep it to the social row and one line. No sitemaps, no newsletter boxes.
- Every icon link needs an aria-label.

```html
<footer class="pb-footer">
  <div class="pb-social">
    <a href="https://github.com/r-r-2" aria-label="GitHub"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg></a>
    <a href="https://x.com/rahul_r007" aria-label="X"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.9 2H22l-7.6 8.7L23 22h-6.8l-5.3-6.9L4.8 22H1.7l8.1-9.3L1 2h6.9l4.8 6.3L18.9 2zm-1.2 18h1.7L6.4 3.9H4.6L17.7 20z"/></svg></a>
  </div>
  <p>Part of <a href="https://rr2.dev">rr2.dev</a> · <a href="/about/">About</a></p>
</footer>
```

#### Stack and cluster

Layout primitives for spacing. A stack spaces children vertically; a cluster lays them out in a wrapping row.

- Use these instead of margins between siblings.
- Gaps: is-tight 8px, default 16px, is-loose 24px, is-section 48px (stack only). is-between spreads a cluster.

```html
<div class="pb-stack">
  <div class="pb-cluster is-between">
    <h2 class="pb-h3">Recent posts</h2>
    <a class="pb-btn is-quiet" href="#">See all</a>
  </div>
  <div class="pb-cluster is-tight">
    <span class="pb-tag">design</span><span class="pb-tag" data-accent="slate">notes</span><span class="pb-tag" data-accent="neutral">draft</span>
  </div>
</div>
```

### Actions

#### Button

Pill buttons. Primary (raspberry), secondary (outlined), quiet (text), and small.

- One primary button per view, for the single most important action.
- Secondary for every other action. Quiet for dismiss, cancel and "see all".
- Use <a> for navigation and <button type="button"> for actions. Never a <div>.
- Slate is not a button colour.
- Disabled: add disabled to a <button>, or aria-disabled="true" to an <a>.

```html
<div class="pb-cluster">
  <button class="pb-btn" type="button">Save changes</button>
  <a class="pb-btn is-secondary" href="#">View details</a>
  <button class="pb-btn is-secondary is-small" type="button">Small</button>
  <button class="pb-btn is-quiet" type="button">Cancel</button>
  <button class="pb-btn" type="button" disabled>Disabled</button>
</div>
```

#### Icon button

Round 32px button holding a single 16px icon.

- Always give it an aria-label that says what it does.
- Use for previous/next, close and similar compact controls only.

```html
<div class="pb-cluster is-tight">
  <button class="pb-icon-btn" type="button" aria-label="Previous"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg></button>
  <button class="pb-icon-btn" type="button" aria-label="Next"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg></button>
  <button class="pb-icon-btn" type="button" aria-label="Close"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
</div>
```

#### Filter chips

Pill links for filtering a list by section. The current one fills with its accent.

- Mark the active chip with aria-current="page" (links) or aria-pressed="true" (buttons).
- Give each chip the accent of the section it filters with data-accent. The "All" chip keeps the default.
- Counts go in a <span class="pb-n">.

```html
<ul class="pb-chips">
  <li><a href="#" aria-current="page">All <span class="pb-n">24</span></a></li>
  <li><a href="#" data-accent="slate">Notes <span class="pb-n">17</span></a></li>
  <li><a href="#" data-accent="green">Guides <span class="pb-n">5</span></a></li>
  <li><a href="#" data-accent="amber">Reports <span class="pb-n">2</span></a></li>
</ul>
```

### Content

#### Tags and badges

Tags are mono pills tinted by their accent. Badges are tiny uppercase status pills.

- Tags name a category; set data-accent to match the section.
- Badges show state ("New", "Live", "Draft"). The default badge is amber, for new.
- Keep both to one or two words, lowercase for tags.

```html
<div class="pb-cluster is-tight">
  <span class="pb-tag">design</span>
  <span class="pb-tag" data-accent="slate">notes</span>
  <span class="pb-tag" data-accent="green">guide</span>
  <span class="pb-tag" data-accent="neutral">draft</span>
  <span class="pb-badge">New</span>
  <span class="pb-badge" data-accent="green">Live</span>
</div>
```

#### Meta row

Date, reading time and tag under a title, separated by middle dots.

- Always use <time datetime="YYYY-MM-DD"> for dates.
- Order: badge (optional), date, reading time, tag. Separators are added for you.

```html
<div class="pb-meta">
  <span class="pb-badge">New</span>
  <time datetime="2026-11-02">Nov 2, 2026</time>
  <span>3 min read</span>
  <span class="pb-tag" data-accent="slate">notes</span>
</div>
```

#### Card

White card with a serif title, a two-line summary and a meta row. Lifts on hover when clickable.

- Make the whole card clickable with a .pb-cover link as the first child, with an aria-label of the title.
- Put cards in a .pb-grid. Never nest cards inside cards.
- data-accent on the card sets the hover title colour and the tag.

```html
<ul class="pb-grid">
  <li class="pb-card" data-accent="slate">
    <a class="pb-cover" href="#" aria-label="A short, specific title"></a>
    <h3>A short, specific title</h3>
    <p>One or two lines that tell the reader what they will get from this.</p>
    <div class="pb-meta"><time datetime="2026-11-02">Nov 2</time><span>3 min read</span><span class="pb-tag" data-accent="slate">notes</span></div>
  </li>
  <li class="pb-card">
    <a class="pb-cover" href="#" aria-label="Another title that runs a little longer than the first"></a>
    <h3>Another title that runs a little longer than the first</h3>
    <p>Summaries are clamped visually by length, so keep them short.</p>
    <div class="pb-meta"><time datetime="2026-10-28">Oct 28</time><span>8 min read</span><span class="pb-tag">design</span></div>
  </li>
</ul>
```

#### Grouped list with date tiles

An archive grouped by month. Each row has a calendar tile, a title and a sub-line.

- One .pb-list per group, with an <h3> holding the group name and a count in a <span>.
- The tile shows a three-letter month in <b> and the day in <span>. Its colour follows data-accent on the <li>.
- Wrap the title in .pb-t so it underlines on hover.

```html
<div class="pb-list">
  <h3>November 2026 <span>2 posts</span></h3>
  <ol>
    <li data-accent="slate"><a href="#"><span class="pb-cal"><b>Nov</b><span>2</span></span><span class="pb-body"><span class="pb-t">A short, specific title</span><span class="pb-sub"><span class="pb-tag" data-accent="slate">notes</span> 3 min read</span></span></a></li>
    <li><a href="#"><span class="pb-cal"><b>Nov</b><span>1</span></span><span class="pb-body"><span class="pb-t">Another post title</span><span class="pb-sub"><span class="pb-tag">design</span> 8 min read</span></span></a></li>
  </ol>
</div>
```

#### Callout

A boxed note with an accent edge. Dashed variant for placeholders.

- Start with a bold lead-in ("Heads up.", "Tip.").
- Slate for information, raspberry for tips, amber for warnings, green for success.
- One callout per section at most.

```html
<div class="pb-stack is-tight">
  <div class="pb-note" data-accent="slate"><strong>Heads up.</strong> This changes how links open on every page.</div>
  <div class="pb-note" data-accent="amber"><strong>Careful.</strong> This can't be undone once it is published.</div>
  <div class="pb-note is-dashed">Placeholder for something that hasn't been written yet.</div>
</div>
```

#### Long-form content

Article styles for plain HTML inside .pb-content. Headings, lists, quotes, code, tables and figures.

- Wrap the article body in <article class="pb-content"> inside a reading-width .pb-wrap.
- Each h2 opens a section with a hairline above it. Don't add your own dividers.
- Nested bullets change marker per level automatically.

```html
<article class="pb-content">
  <p>Opening paragraph in body text, with an <a href="#">inline link</a> and some <strong>strong text</strong>.</p>
  <h2>A section heading</h2>
  <ul>
    <li>A first point.
      <ul><li>A nested detail, a little quieter.</li></ul></li>
    <li>A second point with <code>inline code</code>.</li>
  </ul>
  <blockquote>A short quote that deserves to stand out.</blockquote>
  <pre><code>npm run build</code></pre>
</article>
```

### Forms

#### Text field

Label, input and help text stacked. Also textarea and select. Error state in red.

- Every input has a visible <label for>. Placeholders are examples, never labels.
- Help text goes under the input and is linked with aria-describedby.
- Error: add is-error to .pb-field, aria-invalid="true" to the input, and say how to fix it in the help text.
- Mark optional fields, not required ones.

```html
<form class="pb-stack" onsubmit="return false">
  <div class="pb-field">
    <label for="f-name">Name</label>
    <input class="pb-input" id="f-name" name="name" autocomplete="name" placeholder="Alex Lee">
  </div>
  <div class="pb-field is-error">
    <label for="f-email">Email</label>
    <input class="pb-input" id="f-email" name="email" type="email" value="alex@" aria-invalid="true" aria-describedby="f-email-help">
    <p class="pb-help" id="f-email-help">Add the part after the @, like alex@example.com.</p>
  </div>
  <div class="pb-field">
    <label for="f-topic">Topic</label>
    <select class="pb-select" id="f-topic" name="topic"><option>General</option><option>Feedback</option></select>
  </div>
  <div class="pb-field">
    <label for="f-msg">Message <span class="pb-optional">(optional)</span></label>
    <textarea class="pb-textarea" id="f-msg" name="message" aria-describedby="f-msg-help"></textarea>
    <p class="pb-help" id="f-msg-help">A few lines is plenty.</p>
  </div>
  <div class="pb-cluster"><button class="pb-btn" type="submit">Send</button><button class="pb-btn is-quiet" type="reset">Clear</button></div>
</form>
```

#### Checkbox and radio

Native checkboxes and radios with a raspberry accent, wrapped in their label.

- Group related options in a <fieldset class="pb-fieldset"> with a <legend>.
- Put the input inside its <label class="pb-check"> so the whole line is clickable.
- Extra description goes in a <small> inside a <span> next to the input.

```html
<div class="pb-stack is-loose">
  <fieldset class="pb-fieldset">
    <legend>Email me about</legend>
    <label class="pb-check"><input type="checkbox" checked> New posts</label>
    <label class="pb-check"><input type="checkbox"><span>Project updates <small>About once a month.</small></span></label>
  </fieldset>
  <fieldset class="pb-fieldset">
    <legend>Theme</legend>
    <label class="pb-check"><input type="radio" name="theme-demo" checked> Match my system</label>
    <label class="pb-check"><input type="radio" name="theme-demo"> Light</label>
    <label class="pb-check"><input type="radio" name="theme-demo"> Dark</label>
  </fieldset>
</div>
```

### Navigation

#### Tabs

A row of links with a raspberry underline on the current one. Works without JavaScript.

- Use for switching between pages or sections of the same thing. Each tab is a real link.
- Mark the current tab with aria-current="page".
- Two to six tabs. Scrolls sideways on phones.

```html
<nav aria-label="Sections">
  <ul class="pb-tabs">
    <li><a href="#" aria-current="page">Overview</a></li>
    <li><a href="#">Notes</a></li>
    <li><a href="#">Guides</a></li>
    <li><a href="#">Archive</a></li>
  </ul>
</nav>
```

#### Breadcrumbs

Small path above a page title.

- Wrap in <nav aria-label="Breadcrumb">. The last item is the current page, with aria-current="page" and no link.

```html
<nav aria-label="Breadcrumb">
  <ol class="pb-crumbs">
    <li><a href="#">Home</a></li>
    <li><a href="#">Notes</a></li>
    <li><span aria-current="page">This page</span></li>
  </ol>
</nav>
```

#### Pagination

Previous and next pills with a page count between them.

- Disable the end you are at with aria-disabled="true".
- Use rel="prev" and rel="next" on the links.

```html
<nav class="pb-pager" aria-label="Pagination">
  <a href="#" rel="prev" aria-disabled="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg>Newer</a>
  <span>Page 1 of 4</span>
  <a href="#" rel="next">Older<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg></a>
</nav>
```

### Data

#### Table

A bordered table on a white surface, with uppercase column labels and tabular figures.

- Always wrap in .pb-table-wrap so wide tables scroll inside themselves on phones.
- Give it a <caption>. Use <th scope="col"> for headers and <th scope="row"> for the first cell of each row.
- Right-align number columns with is-num.

```html
<div class="pb-table-wrap">
  <table class="pb-table">
    <caption>Builds this week</caption>
    <thead><tr><th scope="col">Site</th><th scope="col">Status</th><th scope="col" class="is-num">Pages</th><th scope="col" class="is-num">Size</th></tr></thead>
    <tbody>
      <tr><th scope="row">Home</th><td><span class="pb-badge" data-accent="green">Live</span></td><td class="is-num">12</td><td class="is-num">84 KB</td></tr>
      <tr><th scope="row">Notes</th><td><span class="pb-badge" data-accent="green">Live</span></td><td class="is-num">31</td><td class="is-num">212 KB</td></tr>
      <tr><th scope="row">Profile</th><td><span class="pb-badge">New</span></td><td class="is-num">1</td><td class="is-num">146 KB</td></tr>
    </tbody>
  </table>
</div>
```

#### Empty state

What shows when a list has nothing in it yet. A short title, one line of why, one action.

- Say what will appear here and how to get it. No apologies, no illustrations.
- At most one button, secondary unless it's the main action on the page.

```html
<div class="pb-empty">
  <strong>Nothing here yet</strong>
  <p>Posts you save will show up here, newest first.</p>
  <a class="pb-btn is-secondary is-small" href="#">Browse posts</a>
</div>
```

### Feedback

#### Dialog

A native <dialog> with a title, a sentence and actions in the footer.

- Open with dialog.showModal(). Close with a <form method="dialog"> button so Escape and focus return work for free.
- Title in an <h2>, linked with aria-labelledby.
- Actions right-aligned: quiet cancel first, then the primary action.
- Only for decisions that block. Everything else is a toast or an inline message.

```html
<dialog class="pb-dialog" id="confirm" aria-labelledby="confirm-title">
  <div class="pb-dialog-body">
    <h2 id="confirm-title">Delete this draft?</h2>
    <p>The draft and its images will be removed. Published posts aren't affected.</p>
  </div>
  <form class="pb-dialog-actions" method="dialog">
    <button class="pb-btn is-quiet" value="cancel">Cancel</button>
    <button class="pb-btn" value="delete">Delete draft</button>
  </form>
</dialog>
<button class="pb-btn is-secondary" type="button" onclick="document.getElementById('confirm').showModal()">Open dialog</button>
```

#### Toast

A short dark pill confirming something happened, with an optional undo.

- One sentence, past tense ("Link copied"). role="status" so screen readers announce it.
- Place it in a .pb-toast-region fixed at the bottom centre. Hide after about 4 seconds; keep it while hovered or focused.
- The dot takes the accent: green for success, red for errors.

```html
<div class="pb-toast" role="status" data-accent="green"><span class="pb-dot" aria-hidden="true"></span>Link copied to clipboard<button type="button">Undo</button></div>
```

### Signature

#### Guide

A stick figure in ink lines with a handwritten speech bubble. The one playful element.

- At most one guide per page. It offers help or points at something; it never blocks content.
- The speech bubble uses Caveat (pb-bubble p). Keep it under 15 words.
- It waves once on hover or with is-waving; nothing else moves.

```html
<div class="pb-guide">
  <svg class="pb-figure" viewBox="0 0 60 88" aria-hidden="true"><path class="ln wave-arm" d="M30 41 L22 52 L20 61"/><path class="ln" d="M30 41 L38 52 L40 61"/><path class="ln" d="M30 36 L30 63 M30 63 L26 75 L24 86 M30 63 L34 75 L36 86"/><circle class="hd" cx="30" cy="23" r="13"/><circle class="eye" cx="25.5" cy="22" r="1.6"/><circle class="eye" cx="34.5" cy="22" r="1.6"/><path class="mouth" d="M25.5 27 Q30 30.5 34.5 27"/><g class="wv"><path class="ln" d="M30 41 L18 38"/><path class="ln fa" d="M18 38 L12 26"/></g></svg>
  <div class="pb-bubble" role="status">
    <p>Hi! Want to see the newest post?</p>
    <div class="pb-acts"><a class="pb-btn is-small is-secondary" href="#">Show me</a><button class="pb-btn is-quiet" type="button">Later</button></div>
  </div>
</div>
```


## Do's and Don'ts

- Do use one raspberry (primary) button per view. Everything else is secondary or quiet.
- Do use only `--pb-` tokens and `pb-` classes. Never write a hex colour, a font family or a pixel font size in a page.
- Do keep body copy at 18px in the 720px column for anything people read top to bottom.
- Do give every icon-only button an `aria-label`, every input a `<label>`, and keep touch targets at least 24px.
- Do let reduced motion show finished states: no animation should be needed to understand the page.
- Don't fill large areas with raspberry or slate. Colour is a highlight, not a background.
- Don't make slate a button, and don't use status colours for decoration.
- Don't add drop shadows to things that aren't clickable, and don't stack shadows.
- Don't introduce new fonts, weights above 700, or text below 12px.
- Don't put more than one playful element (the guide, a handwritten note) on a screen.
- Don't nest cards inside cards.

## Motion

Durations: `--pb-motion-fast` (.18s) for hover and focus, `--pb-motion-base` (.3s) for state changes, `--pb-motion-slow` (.45s) for movement. Easing `--pb-motion-ease`. One main motion per view; loops are slow; nothing moves on its own except the guide's single wave. With `prefers-reduced-motion: reduce`, all animation is cut and finished states show.

## Iconography

Line icons on a 24px grid, `stroke-width` 2 (2.2 for small chevrons), round caps and joins, `fill="none"`, `stroke="currentColor"` so they take the text colour. Shown at 16px in buttons and 18px in the header. Decorative icons get `aria-hidden="true"`.

## Agent Prompt Guide

When building UI with this system:

1. Start from the page skeleton component: skip link, header, `<main class="pb-wrap">`, footer.
2. Pick components from the list above and copy their markup. Change text, links and `data-accent` only.
3. If something you need isn't here, compose it from existing classes and tokens and leave an HTML comment `<!-- pb: new pattern -->` so it can be reviewed and added to the system.
4. Write any extra CSS with `var(--pb-*)` tokens only, in a `<style>` block, with selectors that don't start with `pb-`.
5. Check the result with `python3 check.py site <folder>` (download from https://design.rr2.dev/check.py). Fix every error before handing it over.
