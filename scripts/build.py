#!/usr/bin/env python3
"""Build every design system in systems/ into docs/ (served by GitHub Pages).

For each systems/<id>/ (with system.json, tokens.json, css/, components/, design.src.md):
  systems/<id>/DESIGN.md                 generated: front matter from tokens.json + prose + component snippets
  docs/<id>/v<major>/brand.css         fonts + tokens + components, readable
  docs/<id>/v<major>/brand.min.css     minified, fonts relative to the CSS file
  docs/<id>/v<major>/brand.inline.min.css  minified, absolute font URLs, for pasting into a <style>
  docs/<id>/v<major>/tokens.css|tokens.json|DESIGN.md|llms.txt|components/|fonts/|assets/
  docs/<id>/index.html                 the review page

And for the whole site: docs/index.html, docs/llms.txt, docs/check.py, docs/404.html, docs/CNAME, docs/.nojekyll.

Standard library only. Running it twice changes nothing.
"""
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "docs"
SITE = "https://design.rr2.dev"

CSS_ORDER = ["base", "type", "header", "content", "controls", "forms", "cards", "nav", "feedback", "guide", "footer"]
FONTS = [
    ("Fraunces", "fraunces.woff2", "500 600"),
    ("Instrument Sans", "instrument-sans-400.woff2", "400"),
    ("Instrument Sans", "instrument-sans-500.woff2", "500"),
    ("Instrument Sans", "instrument-sans-600.woff2", "600"),
    ("JetBrains Mono", "jetbrains-mono-400.woff2", "400"),
    ("JetBrains Mono", "jetbrains-mono-500.woff2", "500"),
    ("Caveat", "caveat.woff2", "600"),
]
GROUP_ORDER = ["Text", "Layout", "Actions", "Content", "Forms", "Navigation", "Data", "Feedback", "Signature"]


# ---------- small helpers ----------

def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text() != text:
        path.write_text(text)
        print("wrote", path.relative_to(ROOT))


def copytree(src: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def minify(css: str) -> str:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    css = re.sub(r":\s+", ":", css)
    return css.replace(";}", "}").strip() + "\n"


def fill(page: str, name: str, content: str) -> str:
    """Replace <!-- pb:name --> (and anything up to <!-- /pb:name --> if present)."""
    start, end = f"<!-- pb:{name} -->", f"<!-- /pb:{name} -->"
    if end in page:
        a, b = page.index(start), page.index(end) + len(end)
    else:
        a = page.index(start)
        b = a + len(start)
    return page[:a] + content + page[b:]


# ---------- tokens ----------

def themed(group: dict, prefix: str, name: str, mode: str) -> dict:
    out = {}
    for k, v in group.items():
        if k.startswith("$"):
            continue
        key = f"--{prefix}-{name}-{k}" if name else f"--{prefix}-{k}"
        out[key] = v[mode] if isinstance(v, dict) else v
    return out


def tokens_css(t: dict, p: str) -> str:
    light = {**themed(t["color"], p, "", "light"), **themed(t["shadow"], p, "shadow", "light")}
    dark = {**themed(t["color"], p, "", "dark"), **themed(t["shadow"], p, "shadow", "dark")}
    static = {f"--{p}-font-{k}": v for k, v in t["font"].items()}
    for group in ("size", "leading", "tracking", "space", "layout", "radius", "motion"):
        static.update({f"--{p}-{group}-{k}": v for k, v in t[group].items() if not k.startswith("$")})

    def block(sel, props, extra="", ind=""):
        body = "\n".join(f"{ind}  {k}: {v};" for k, v in props.items())
        return f"{ind}{sel} {{\n{body}\n{ind}  {extra}\n{ind}}}\n"

    css = "/* Generated from tokens.json by scripts/build.py. Do not edit. */\n"
    css += block(":root", {**static, **light}, "color-scheme: light;")
    css += "@media (prefers-color-scheme: dark) {\n" + block(':root:not([data-theme="light"])', dark, "color-scheme: dark;", "  ") + "}\n"
    css += block(':root[data-theme="dark"]', dark, "color-scheme: dark;")
    return css


def fonts_css(base: str) -> str:
    return "".join(
        f'@font-face {{ font-family: "{fam}"; src: url({base}{file}) format("woff2"); font-weight: {w}; font-style: normal; font-display: swap; }}\n'
        for fam, file, w in FONTS)


# ---------- component snippets ----------

def parse_snippet(path: Path) -> dict:
    text = path.read_text()
    m = re.match(r"\s*<!--(.*?)-->\s*", text, flags=re.S)
    if not m:
        raise SystemExit(f"{path}: missing metadata comment")
    meta = {"rules": [], "preview": "live", "file": path.name, "slug": re.sub(r"^\d+-", "", path.stem)}
    key = None
    for line in m.group(1).strip().splitlines():
        if line.startswith("- ") and key == "rules":
            meta["rules"].append(line[2:].strip())
        elif ":" in line and not line.startswith(" "):
            key, val = line.split(":", 1)
            key = key.strip()
            if val.strip():
                meta[key] = val.strip()
    meta["markup"] = text[m.end():].rstrip() + "\n"
    for k in ("name", "group", "summary"):
        if k not in meta:
            raise SystemExit(f"{path}: missing '{k}'")
    if meta["group"] not in GROUP_ORDER:
        raise SystemExit(f"{path}: unknown group {meta['group']}")
    return meta


def load_snippets(sysdir: Path) -> list:
    snips = [parse_snippet(p) for p in sorted((sysdir / "components").glob("*.html"))]
    return sorted(snips, key=lambda s: (GROUP_ORDER.index(s["group"]), s["file"]))


# ---------- DESIGN.md ----------

def yq(v) -> str:
    """YAML scalar."""
    if isinstance(v, (int, float)):
        return str(v)
    return '"' + str(v).replace('"', '\\"') + '"'


def first_family(stack: str) -> str:
    return stack.split(",")[0].strip().strip('"')


def front_matter(sysm: dict, t: dict) -> str:
    c = {k: v for k, v in t["color"].items() if not k.startswith("$")}
    L = ["---", "version: alpha", f"name: {yq(sysm['title'])}", f"description: {yq(sysm['description'])}", "colors:"]
    aliases = {"primary": "raspberry", "secondary": "slate", "neutral": "paper", "on-surface": "ink", "error": "red"}
    for a, src in aliases.items():
        L.append(f"  {a}: {yq(c[src]['light'])}")
    for k, v in c.items():
        L.append(f"  {k}: {yq(v['light'])}")
    L.append("typography:")
    for k, v in t["typography"].items():
        if k.startswith("$"):
            continue
        L.append(f"  {k}:")
        L.append(f"    fontFamily: {yq(first_family(t['font'][v['font']]))}")
        L.append(f"    fontSize: {v['size']}")
        L.append(f"    fontWeight: {v['weight']}")
        L.append(f"    lineHeight: {v['leading']}")
        if "tracking" in v:
            L.append(f"    letterSpacing: {v['tracking']}")
    r = t["radius"]
    L += ["rounded:", f"  sm: {r['sm']}", f"  md: {r['md']}", f"  lg: {r['lg']}", "  full: 9999px"]
    L.append("spacing:")
    names = {"1": "xs", "2": "sm", "3": "sm-plus", "4": "md", "5": "md-plus", "6": "lg", "8": "lg-plus", "9": "xl-minus", "12": "xl", "18": "xxl"}
    for k, v in t["space"].items():
        if not k.startswith("$"):
            L.append(f"  {names.get(k, k)}: {v}")
    lay = t["layout"]
    L += [f"  column: {lay['column']}", f"  wide: {lay['wide']}", f"  gutter: {lay['gap']}", f"  header: {lay['bar']}"]
    comps = {
        "button-primary": {"backgroundColor": "{colors.raspberry}", "textColor": "{colors.on-accent}", "typography": "{typography.button}",
                           "rounded": "{rounded.full}", "height": "40px", "padding": "18px"},
        "button-primary-hover": {"backgroundColor": "{colors.raspberry-strong}"},
        "button-secondary": {"backgroundColor": "{colors.surface}", "textColor": "{colors.ink}", "typography": "{typography.button}",
                             "rounded": "{rounded.full}", "height": "40px", "padding": "18px"},
        "button-secondary-hover": {"backgroundColor": "{colors.ink}", "textColor": "{colors.paper}"},
        "card": {"backgroundColor": "{colors.surface}", "textColor": "{colors.text}", "rounded": "{rounded.md}", "padding": "20px"},
        "tag": {"backgroundColor": "{colors.raspberry-soft}", "textColor": "{colors.raspberry}", "typography": "{typography.label-sm}", "rounded": "{rounded.full}"},
        "badge-new": {"backgroundColor": "{colors.amber-soft}", "textColor": "{colors.amber}", "rounded": "{rounded.full}"},
        "chip-selected": {"backgroundColor": "{colors.raspberry}", "textColor": "{colors.on-accent}", "rounded": "{rounded.full}", "height": "32px"},
        "input": {"backgroundColor": "{colors.surface}", "textColor": "{colors.ink}", "typography": "{typography.body-md}", "rounded": "{rounded.md}",
                  "height": "40px", "padding": "12px"},
        "toast": {"backgroundColor": "{colors.ink}", "textColor": "{colors.paper}", "rounded": "{rounded.full}"},
        "dialog": {"backgroundColor": "{colors.surface}", "textColor": "{colors.text}", "rounded": "{rounded.lg}", "padding": "24px"},
        "page": {"backgroundColor": "{colors.neutral}", "textColor": "{colors.text}", "typography": "{typography.body-lg}"},
        "meta": {"textColor": "{colors.muted}", "typography": "{typography.body-sm}"},
        "list-row-hover": {"backgroundColor": "{colors.surface-hover}", "textColor": "{colors.ink}"},
        "code-inline": {"backgroundColor": "{colors.sunken}", "textColor": "{colors.ink}", "typography": "{typography.code}", "rounded": "{rounded.sm}"},
        "divider": {"backgroundColor": "{colors.line}", "height": "1px"},
        "divider-strong": {"backgroundColor": "{colors.line-strong}", "height": "1px"},
        "focus-ring": {"backgroundColor": "{colors.slate-soft}", "textColor": "{colors.slate}"},
        "date-tile": {"backgroundColor": "{colors.slate-strong}", "textColor": "{colors.on-accent}", "rounded": "{rounded.md}", "width": "44px"},
        "badge-live": {"backgroundColor": "{colors.green-soft}", "textColor": "{colors.green}", "rounded": "{rounded.full}"},
        "field-error": {"backgroundColor": "{colors.red-soft}", "textColor": "{colors.red}"},
        "header": {"backgroundColor": "{colors.glass}", "textColor": "{colors.ink}", "height": "60px"},
        "dialog-backdrop": {"backgroundColor": "{colors.scrim}"},
    }
    L.append("components:")
    for name, props in comps.items():
        L.append(f"  {name}:")
        for k, v in props.items():
            L.append(f"    {k}: {yq(v)}")
    L.append("---")
    return "\n".join(L) + "\n\n"


def dark_table(t: dict) -> str:
    rows = ["| Token | Light | Dark |", "|---|---|---|"]
    for k, v in t["color"].items():
        if not k.startswith("$"):
            rows.append(f"| `{k}` | `{v['light']}` | `{v['dark']}` |")
    return "\n".join(rows)


def type_table(t: dict) -> str:
    rows = ["| Style | Class | Font | Size / weight / line height |", "|---|---|---|---|"]
    for k, v in t["typography"].items():
        if k.startswith("$"):
            continue
        rows.append(f"| `{k}` | `.{v['class']}` | {first_family(t['font'][v['font']])} | {v['size']} / {v['weight']} / {v['leading']} |")
    return "\n".join(rows)


def components_md(snips: list) -> str:
    out = []
    group = None
    for s in snips:
        if s["group"] != group:
            group = s["group"]
            out.append(f"### {group}\n")
        out.append(f"#### {s['name']}\n\n{s['summary']}\n")
        if s["rules"]:
            out.append("\n".join(f"- {r}" for r in s["rules"]) + "\n")
        out.append(f"```html\n{s['markup']}```\n")
    return "\n".join(out)


def design_md(sysdir: Path, sysm: dict, t: dict, snips: list) -> str:
    body = (sysdir / "design.src.md").read_text()
    body = fill(body, "dark-table", dark_table(t))
    body = fill(body, "type-table", type_table(t))
    body = fill(body, "components", components_md(snips))
    head = (f"<!-- Generated by scripts/build.py from systems/{sysm['id']}/design.src.md, tokens.json and components/. "
            f"Edit those, not this file. Version {sysm['version']}. -->\n")
    return front_matter(sysm, t) + head + body


# ---------- review page ----------

def lum(hexv: str) -> float:
    h = hexv.lstrip("#")
    if len(h) != 6:
        return 0.0
    def ch(x):
        x /= 255
        return x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(int(h[i:i + 2], 16)) for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a: str, b: str) -> float:
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


SWATCH_GROUPS = [
    ("Brand", ["raspberry", "raspberry-strong", "raspberry-soft", "slate", "slate-strong", "slate-soft"]),
    ("Surfaces and lines", ["paper", "surface", "surface-hover", "sunken", "line", "line-strong"]),
    ("Status", ["amber", "amber-soft", "green", "green-soft", "red", "red-soft"]),
]
TEXT_TOKENS = ["ink", "text", "muted"]


def swatches(t: dict, p: str) -> str:
    c = t["color"]
    out = ['<p class="pb-label">Text on paper</p><div class="sg-textsw">']
    for k in TEXT_TOKENS:
        r1 = ratio(c[k]["light"], c["paper"]["light"])
        r2 = ratio(c[k]["dark"], c["paper"]["dark"])
        out.append(f'<div><span style="color:var(--{p}-{k})">Aa {k}</span><code>--{p}-{k}</code>'
                   f'<small>{c[k]["light"]} · {c[k]["dark"]}</small><small>{r1:.1f}:1 · {r2:.1f}:1 on paper</small></div>')
    out.append("</div>")
    for title, keys in SWATCH_GROUPS:
        out.append(f'<p class="pb-label">{title}</p><ul class="sg-sw">')
        for k in keys:
            v = c[k]
            note = f"<small>{esc(v['$description'])}</small>" if "$description" in v else ""
            out.append(f'<li><i style="background:var(--{p}-{k})"></i><div><code>--{p}-{k}</code>'
                       f'<small class="sg-hex">{v["light"]} · {v["dark"]}</small>{note}</div></li>')
        out.append("</ul>")
    return "".join(out)


def type_rows(t: dict) -> str:
    out = []
    for k, v in t["typography"].items():
        if k.startswith("$") or k in ("button",):
            continue
        cls = v["class"]
        sample = {"pb-tag": '<span class="pb-tag">label-sm</span>', "pb-code": '<code class="pb-code">code sample</code>',
                  "pb-hand": '<span class="pb-hand">Handwritten aside</span>'}.get(cls, f'<span class="{cls}" style="margin:0">The quick brown fox</span>')
        out.append(f'<div class="sg-trow"><div><code>.{cls}</code><small>{k} · {v["size"]}/{v["weight"]}</small></div><div>{sample}</div></div>')
    return "".join(out)


def space_rows(t: dict, p: str) -> str:
    cells = "".join(f'<div><i style="width:var(--{p}-space-{k});height:var(--{p}-space-{k})"></i><code>{k}</code><small>{v}</small></div>'
                    for k, v in t["space"].items() if not k.startswith("$"))
    radii = "".join(f'<div style="border-radius:var(--{p}-radius-{k})"><code>radius-{k}</code><small>{v}</small></div>'
                    for k, v in t["radius"].items() if k not in ("round",))
    shadows = "".join(f'<div style="border-radius:var(--{p}-radius-md);box-shadow:var(--{p}-shadow-{k})"><code>shadow-{k}</code></div>'
                      for k in ("rest", "lift"))
    return f'<div class="sg-panel"><div class="sg-space">{cells}</div></div><div class="sg-shapes">{radii}{shadows}</div>'


def component_sections(snips: list) -> tuple:
    nav, body = [], []
    group = None
    for s in snips:
        if s["group"] != group:
            group = s["group"]
            nav.append(f'<li class="sg-navgroup">{group}</li>')
        sid = "c-" + s["slug"]
        nav.append(f'<li><a href="#{sid}">{esc(s["name"])}</a></li>')
        rules = "".join(f"<li>{esc(r)}</li>" for r in s["rules"])
        live = s["markup"].replace(SITE + "/", "/")
        preview = "" if s["preview"] == "code-only" else f'<div class="sg-preview pb">{live}</div>'
        body.append(
            f'<section class="sg-comp" id="{sid}"><div class="sg-comp-head"><p class="sg-eyebrow">{group}</p>'
            f'<h3>{esc(s["name"])}</h3><p>{esc(s["summary"])}</p></div>'
            f'{preview}'
            f'<details class="sg-code"{" open" if s["preview"] == "code-only" else ""}><summary>HTML</summary>'
            f'<button class="sg-copybtn" type="button" data-copy="{sid}">Copy</button>'
            f'<pre tabindex="0" aria-label="{esc(s["name"])} HTML"><code id="code-{sid}">{esc(s["markup"])}</code></pre></details>'
            f'{"<ul class=sg-rules>" + rules + "</ul>" if rules else ""}</section>')
    return "".join(nav), "".join(body)


def switcher(systems: list, current: str) -> str:
    items = "".join(
        f'<li><a href="/{s["id"]}/"{" aria-current=page" if s["id"] == current else ""}>'
        f'<span class="sg-dot" style="background:{esc(s["accent"])}"></span><span><b>{esc(s["title"])}</b>'
        f'<small>v{s["version"].split(".")[0]} · {esc(s["status"])}</small></span></a></li>' for s in systems)
    return f'<ul class="sg-switch-list">{items}<li><a href="/"><span class="sg-dot"></span><span><b>All systems</b></span></a></li></ul>'


def review_page(sysm: dict, t: dict, snips: list, systems: list) -> str:
    tpl = (ROOT / "site/system.html").read_text()
    p, sid, major = sysm["prefix"], sysm["id"], sysm["version"].split(".")[0]
    nav, comps = component_sections(snips)
    base = f"/{sid}/v{major}"
    rep = {
        "{{title}}": esc(sysm["title"]), "{{description}}": esc(sysm["description"]), "{{id}}": sid,
        "{{version}}": sysm["version"], "{{major}}": major, "{{base}}": base, "{{site}}": SITE, "{{prefix}}": p,
        "{{used_by}}": " · ".join(esc(u) for u in sysm["used_by"]), "{{status}}": esc(sysm["status"]),
    }
    for k, v in rep.items():
        tpl = tpl.replace(k, v)
    tpl = fill(tpl, "switcher", switcher(systems, sid))
    tpl = fill(tpl, "swatches", swatches(t, p))
    tpl = fill(tpl, "type", type_rows(t))
    tpl = fill(tpl, "space", space_rows(t, p))
    tpl = fill(tpl, "compnav", nav)
    tpl = fill(tpl, "components", comps)
    return tpl


def root_index(systems: list) -> str:
    tpl = (ROOT / "site/index.html").read_text()
    cards = "".join(
        f'<li class="sg-sys"><div class="sg-swatchbar">{"".join(f"<i style=background:{esc(c)}></i>" for c in s.get("palette", [s["accent"]]))}</div>'
        f'<h2><a href="/{s["id"]}/">{esc(s["title"])}</a></h2><p>{esc(s["description"])}</p>'
        f'<div class="sg-meta"><span>v{s["version"]}</span><span>{esc(s["status"])}</span><span>prefix {esc(s["prefix"])}-</span></div></li>'
        for s in systems)
    cards += '<li class="sg-sys is-placeholder"><h2>Next system</h2><p>Add a folder under systems/ and run the build.</p></li>'
    return fill(tpl, "systems", cards)


def llms_root(systems: list) -> str:
    lines = ["# design.rr2.dev", "",
             "> Design systems by Rahul Ravikumar, written for AI coding agents. Each system has a DESIGN.md (tokens in YAML front matter, rules and copy-ready component markup in the body), versioned CSS, and a conformance checker.",
             "", "Before building UI for a site that uses one of these systems: read its DESIGN.md, load its versioned brand.css, copy component markup exactly, and run the checker.", "", "## Systems", ""]
    for s in systems:
        m = s["version"].split(".")[0]
        lines.append(f"- [{s['title']}]({SITE}/{s['id']}/v{m}/DESIGN.md): {s['description']} Prefix `{s['prefix']}-`. CSS: {SITE}/{s['id']}/v{m}/brand.css")
    lines += ["", "## Tools", "", f"- [check.py]({SITE}/check.py): `python3 check.py site <folder> --system <id>` lints a site for raw colours, unknown fonts, off-scale sizes and unknown classes.", ""]
    return "\n".join(lines)


def llms_system(s: dict) -> str:
    m = s["version"].split(".")[0]
    b = f"{SITE}/{s['id']}/v{m}"
    return "\n".join([
        f"# {s['title']} design system v{s['version']}", "", f"> {s['description']}", "",
        f"- [DESIGN.md]({b}/DESIGN.md): read this first. Tokens, rules, every component's markup.",
        f"- [brand.css]({b}/brand.css): link from <head>, with class=\"pb\" on <html>.",
        f"- [brand.inline.min.css]({b}/brand.inline.min.css): paste into a <style> tag for self-contained pages.",
        f"- [tokens.json]({b}/tokens.json): raw tokens, light and dark.",
        f"- [Components]({b}/components/): one HTML snippet per component.",
        f"- [Review page]({SITE}/{s['id']}/): live previews.", ""])


# ---------- main ----------

def build_system(sysdir: Path, systems: list) -> None:
    sysm = json.loads((sysdir / "system.json").read_text())
    t = json.loads((sysdir / "tokens.json").read_text())
    p, sid, major = sysm["prefix"], sysm["id"], sysm["version"].split(".")[0]
    snips = load_snippets(sysdir)
    out = PUBLIC / sid / f"v{major}"

    tok = tokens_css(t, p)
    comps = "\n".join((sysdir / f"css/{c}.css").read_text() for c in CSS_ORDER)
    head = f"/* {sysm['title']} design system v{sysm['version']} · {SITE}/{sid}/ */\n"
    brand = head + fonts_css("fonts/") + tok + comps
    write(sysdir / "DESIGN.md", design_md(sysdir, sysm, t, snips))

    copytree(sysdir / "fonts", out / "fonts")
    copytree(sysdir / "assets", out / "assets")
    copytree(sysdir / "components", out / "components")
    write(out / "brand.css", brand)
    write(out / "brand.min.css", minify(brand))
    write(out / "brand.inline.min.css", minify(head + fonts_css(f"{SITE}/{sid}/v{major}/fonts/") + tok + comps))
    write(out / "tokens.css", tok)
    write(out / "tokens.json", (sysdir / "tokens.json").read_text())
    write(out / "DESIGN.md", (sysdir / "DESIGN.md").read_text())
    write(out / "llms.txt", llms_system(sysm))
    write(out / "CHANGELOG.md", (sysdir / "CHANGELOG.md").read_text())
    write(PUBLIC / sid / "index.html", review_page(sysm, t, snips, systems))


def main() -> None:
    sysdirs = sorted(d for d in (ROOT / "systems").iterdir() if (d / "system.json").exists())
    systems = [json.loads((d / "system.json").read_text()) for d in sysdirs]
    for d in sysdirs:
        build_system(d, systems)
    write(PUBLIC / "index.html", root_index(systems))
    write(PUBLIC / "llms.txt", llms_root(systems))
    write(PUBLIC / "404.html", (ROOT / "site/404.html").read_text())
    write(PUBLIC / ".nojekyll", "")
    write(PUBLIC / "CNAME", "design.rr2.dev\n")
    write(PUBLIC / "check.py", (ROOT / "scripts/check.py").read_text())
    write(PUBLIC / "hub.css", (ROOT / "site/hub.css").read_text())
    # The hub uses the first system's assets for its own favicon.
    shutil.copy(sysdirs[0] / "assets/favicon.ico", PUBLIC / "favicon.ico")


if __name__ == "__main__":
    main()
