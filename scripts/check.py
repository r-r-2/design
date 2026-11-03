#!/usr/bin/env python3
"""Conformance checker for the design systems at https://design.rr2.dev.

Standalone, standard library only. Download it into any site and run it there:

  curl -sO https://design.rr2.dev/check.py
  python3 check.py site .  --system personal          # lint a site folder against a system
  python3 check.py tokens  --system personal          # WCAG AA contrast of the system's colour pairs

Inside the design repo it also has:
  python3 scripts/check.py all                        # tokens + DESIGN.md lint for every system

site checks
  errors    unknown-class   a prefixed class (e.g. pb-foo) that the system doesn't define
            raw-color       a hex/rgb/hsl colour in a <style> block, style="" attribute or .css file
            no-stylesheet   a full page (with <html> or <head>) that uses the system's classes but doesn't load or inline its CSS
  warnings  raw-font        a font-family that isn't one of the system's font tokens
            off-scale-size  a font-size in px that isn't on the type scale
            unpinned-css    the system's CSS linked without a /v<major>/ path
            no-root-class   <html> is missing class="<prefix>"
            many-primary    more than one primary button on a page
            img-alt         <img> without an alt attribute
            unlabelled-btn  a <button> with no text and no aria-label
A page can switch off a rule with <meta name="check-ignore" content="rule-a, rule-b"> (for pattern libraries and the like).
Exit code 1 if there are errors (or warnings, with --strict).
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

SITE = "https://design.rr2.dev"
HERE = Path(__file__).resolve().parent
REPO = HERE.parent if (HERE.parent / "systems").is_dir() else None
SKIP_DIRS = {".git", "node_modules", ".wrangler", "__pycache__", ".venv", "venv"}
COLOR_RE = re.compile(r"(?<![\w&%-])(#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\()")
ALLOWED_COLOR_CONTEXT = re.compile(r"url\(\s*[\"']?data:", re.I)


# ---------- loading a system ----------

def fetch(path_or_url: str) -> str:
    if re.match(r"https?://", path_or_url):
        req = urllib.request.Request(path_or_url, headers={"User-Agent": "design-check/1"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8")
    return Path(path_or_url).read_text()


def load_system(system: str, major: str, css: str = None, tokens: str = None) -> dict:
    local = REPO / "systems" / system if REPO else None
    if local and local.is_dir():
        sysm = json.loads((local / "system.json").read_text())
        major = sysm["version"].split(".")[0]
        built = REPO / "docs" / system / f"v{major}" / "brand.css"
        css_text = fetch(css) if css else (built.read_text() if built.exists() else "")
        tok = json.loads(fetch(tokens) if tokens else (local / "tokens.json").read_text())
        prefix = sysm["prefix"]
    else:
        base = f"{SITE}/{system}/v{major}"
        css_text = fetch(css or f"{base}/brand.css")
        tok = json.loads(fetch(tokens or f"{base}/tokens.json"))
        m = re.search(r"\.([a-z]+)-wrap\b", css_text)
        prefix = m.group(1) if m else "pb"
    classes = set(re.findall(rf"\.({prefix}-[A-Za-z0-9_-]+)", css_text))
    classes.add(prefix)
    fonts = {v.split(",")[0].strip().strip('"').lower() for v in tok["font"].values()}
    sizes = {int(v[:-2]) for k, v in tok["size"].items() if not k.startswith("$") and v.endswith("px")}
    for v in tok.get("typography", {}).values():
        if isinstance(v, dict) and str(v.get("size", "")).endswith("px"):
            sizes.add(int(v["size"][:-2]))
    return {"id": system, "major": major, "prefix": prefix, "classes": classes, "fonts": fonts, "sizes": sizes, "tokens": tok}


# ---------- site lint ----------

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []          # (tag, attrs dict, line)
        self.styles = []        # (css text, start line)
        self._in_style = None
        self._btn = None        # [attrs, line, text]

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        line = self.getpos()[0]
        self.tags.append((tag, a, line))
        if tag == "style":
            self._in_style = [line, ""]
        if tag == "button":
            self._btn = [a, line, ""]
        if self._btn is not None and tag in ("svg", "img") and a.get("aria-label"):
            self._btn[2] += a["aria-label"]

    def handle_endtag(self, tag):
        if tag == "style" and self._in_style:
            self.styles.append((self._in_style[1], self._in_style[0]))
            self._in_style = None
        if tag == "button" and self._btn is not None:
            self.tags.append(("/button", {"_text": self._btn[2].strip(), **self._btn[0]}, self._btn[1]))
            self._btn = None

    def handle_data(self, data):
        if self._in_style is not None:
            self._in_style[1] += data
        if self._btn is not None:
            self._btn[2] += data


def declarations(css: str, inline: bool):
    """Yield (line offset, property, value) for every declaration. Selectors are never scanned."""
    css = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), css, flags=re.S)
    bodies = [(0, css)] if inline else [(css.count("\n", 0, m.start(1)), m.group(1)) for m in re.finditer(r"\{([^{}]*)\}", css)]
    for off, body in bodies:
        pos = 0
        for decl in body.split(";"):
            line = off + body.count("\n", 0, pos)
            pos += len(decl) + 1
            if ":" in decl:
                prop, _, val = decl.partition(":")
                yield line + (1 if decl.startswith("\n") else 0), prop.strip().lower(), val.strip()


def css_findings(css: str, start: int, fname: str, s: dict, out: list, inline: bool = False) -> None:
    # Ignore the system's own CSS when a page inlines it.
    if re.search(rf"--{s['prefix']}-paper\s*:", css) and "@font-face" in css:
        return
    p = s["prefix"]
    for off, prop, val in declarations(css, inline):
        ln = start + off
        if prop.startswith("--"):
            continue
        if COLOR_RE.search(val) and not ALLOWED_COLOR_CONTEXT.search(val):
            out.append(("error", fname, ln, "raw-color", f"{prop}: {val[:60]} — use a var(--{p}-*) colour token"))
        if prop == "font-family" and f"var(--{p}-font" not in val:
            first = val.split(",")[0].strip().strip("\"'").lower()
            if first not in s["fonts"] and first not in ("inherit", "monospace", "system-ui"):
                out.append(("warning", fname, ln, "raw-font", f"font-family: {val[:50]} — use var(--{p}-font-*)"))
        if prop in ("font-size", "font"):
            for px in re.findall(r"(?<![\w.-])(\d+(?:\.\d+)?)px", val if prop == "font-size" else val.split("/")[0]):
                if float(px) not in s["sizes"]:
                    out.append(("warning", fname, ln, "off-scale-size", f"{prop}: {val[:50]} — {px}px isn't on the type scale; use a type class or var(--{p}-size-*)"))


def lint_html(path: Path, rel: str, s: dict, out: list) -> None:
    text = path.read_text(errors="replace")
    page = Page()
    try:
        page.feed(text)
    except Exception as e:  # malformed HTML shouldn't stop the run
        out.append(("warning", rel, 1, "parse", str(e)))
    p = s["prefix"]
    uses = False
    loads = False
    primaries = []
    html_root = None
    ignored = set()
    start = len(out)
    for tag, a, line in page.tags:
        cls = (a.get("class") or "").split()
        if tag == "html":
            html_root = (cls, line)
        for c in cls:
            if c.startswith(p + "-") or c == p:
                uses = True
                if c not in s["classes"]:
                    out.append(("error", rel, line, "unknown-class", f'class "{c}" isn\'t defined by the {s["id"]} system'))
        if tag == "meta" and a.get("name") == "check-ignore":
            ignored.update(r.strip() for r in (a.get("content") or "").split(","))
        if (f"{p}-btn" in cls and not ({"is-secondary", "is-quiet"} & set(cls)) and tag != "/button"
                and "disabled" not in a and a.get("aria-disabled") != "true"):
            primaries.append(line)
        if tag == "link" and "stylesheet" in (a.get("rel") or ""):
            href = a.get("href") or ""
            if f"/{s['id']}/" in href or "brand" in href:
                loads = True
                if f"/{s['id']}/" in href and not re.search(r"/v\d+/", href):
                    out.append(("warning", rel, line, "unpinned-css", f"{href} — link /{s['id']}/v{s['major']}/brand.css"))
        if "style" in a and a["style"]:
            css_findings(a["style"], line, rel, s, out, inline=True)
        if tag == "img" and "alt" not in a:
            out.append(("warning", rel, line, "img-alt", "<img> needs an alt attribute (alt=\"\" if decorative)"))
        if tag == "/button" and not a.get("_text") and not a.get("aria-label") and not a.get("aria-labelledby"):
            out.append(("warning", rel, line, "unlabelled-btn", "<button> has no text; add an aria-label"))
    for css, line in page.styles:
        if f"--{p}-paper" in css:
            loads = True
        css_findings(css, line, rel, s, out)
    whole = any(tag in ("html", "head") for tag, _, _ in page.tags)  # fragments/partials skip page-level checks
    if uses and whole and not loads:
        out.append(("error", rel, 1, "no-stylesheet", f"uses {p}- classes but doesn't link or inline the {s['id']} CSS"))
    if uses and html_root and p not in html_root[0]:
        out.append(("warning", rel, html_root[1], "no-root-class", f'add class="{p}" to <html>'))
    if len(primaries) > 1:
        out.append(("warning", rel, primaries[1], "many-primary", f"{len(primaries)} primary buttons on one page (lines {', '.join(map(str, primaries))}); keep one"))
    if ignored:
        out[start:] = [o for o in out[start:] if o[3] not in ignored]


def cmd_site(args) -> int:
    s = load_system(args.system, args.major, args.css, args.tokens)
    root = Path(args.folder)
    files = [root] if root.is_file() else [f for f in sorted(root.rglob("*"))
                                           if f.suffix in (".html", ".htm", ".css") and not (SKIP_DIRS & set(f.parts))]
    out = []
    for f in files:
        rel = str(f.relative_to(root)) if root.is_dir() else f.name
        if f.suffix == ".css":
            if re.match(r"(brand|tokens)(\.inline)?(\.min)?\.css$", f.name):
                continue
            css_findings(f.read_text(errors="replace"), 1, rel, s, out)
        else:
            lint_html(f, rel, s, out)
    errors = [o for o in out if o[0] == "error"]
    warns = [o for o in out if o[0] == "warning"]
    for sev, f, ln, rule, msg in sorted(out, key=lambda o: (o[1], o[2])):
        print(f"{sev:7} {f}:{ln}  {rule}  {msg}")
    print(f"\n{len(files)} file(s) checked against {s['id']} v{s['major']}: {len(errors)} error(s), {len(warns)} warning(s).")
    return 1 if errors or (args.strict and warns) else 0


# ---------- tokens: contrast ----------

PAIRS = [
    ("ink", "paper"), ("ink", "surface"), ("text", "paper"), ("text", "surface"),
    ("muted", "paper"), ("muted", "surface"), ("muted", "surface-hover"), ("muted", "sunken"),
    ("ink", "sunken"), ("ink", "glass"), ("ink", "surface-hover"),
    ("raspberry", "paper"), ("raspberry", "surface"), ("raspberry", "raspberry-soft"), ("raspberry-strong", "surface"),
    ("slate", "paper"), ("slate", "surface"), ("slate-strong", "slate-soft"), ("slate-strong", "surface"),
    ("amber", "amber-soft"), ("amber", "surface"), ("green", "green-soft"), ("green", "surface"), ("red", "red-soft"), ("red", "surface"),
    ("on-accent", "raspberry"), ("on-accent", "raspberry-strong"), ("on-accent", "slate"), ("on-accent", "slate-strong"),
    ("on-accent", "amber"), ("on-accent", "green"), ("on-accent", "muted"),
    ("paper", "ink"),
]


def rgb(value: str, under=(255, 255, 255)):
    v = value.strip()
    if v.startswith("#"):
        v = v[1:]
        if len(v) == 3:
            v = "".join(ch * 2 for ch in v)
        return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))
    nums = [float(x) for x in v[v.index("(") + 1:v.index(")")].split(",")]
    a = nums[3] if len(nums) == 4 else 1
    return tuple(round(c * a + u * (1 - a)) for c, u in zip(nums[:3], under))


def lum(c):
    def ch(x):
        x /= 255
        return x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(x) for x in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def check_tokens(tok: dict, name: str, verbose: bool) -> int:
    colors = tok["color"]
    failed = 0
    for mode in ("light", "dark"):
        paper = rgb(colors["paper"][mode])
        for fg, bg in PAIRS:
            if fg not in colors or bg not in colors:
                continue
            r = contrast(rgb(colors[fg][mode], paper), rgb(colors[bg][mode], paper))
            ok = r >= 4.5
            failed += not ok
            if verbose or not ok:
                print(f"  {'ok  ' if ok else 'FAIL'} {r:5.2f}  {mode:5} {fg} on {bg}")
    print(f"{name}: {'all pairs pass WCAG AA' if not failed else f'{failed} pair(s) below 4.5:1'}")
    return failed


def cmd_tokens(args) -> int:
    s = load_system(args.system, args.major, None, args.tokens)
    return 1 if check_tokens(s["tokens"], s["id"], args.verbose) else 0


# ---------- repo-only: DESIGN.md lint and all ----------

def lint_design(path: Path) -> int:
    if not shutil.which("npx"):
        print(f"{path}: skipped DESIGN.md lint (npx not found)")
        return 0
    r = subprocess.run(["npx", "--yes", "@google/design.md", "lint", str(path)], capture_output=True, text=True)
    try:
        data = json.loads(r.stdout)
    except ValueError:
        print(r.stdout or r.stderr)
        return 1
    for f in data["findings"]:
        if f["severity"] != "info":
            print(f"  {f['severity']:7} {f.get('path', '')}  {f['message']}")
    sm = data["summary"]
    print(f"{path.relative_to(REPO)}: {sm['errors']} error(s), {sm['warnings']} warning(s)")
    return sm["errors"] + sm["warnings"]


def cmd_all(args) -> int:
    if not REPO:
        print("'all' only runs inside the design repo")
        return 2
    bad = 0
    for d in sorted((REPO / "systems").iterdir()):
        if (d / "system.json").exists():
            bad += check_tokens(json.loads((d / "tokens.json").read_text()), d.name, args.verbose)
            bad += lint_design(d / "DESIGN.md")
    # The hub (docs/) is styled with the personal system and must pass its checker too.
    print("hub (docs/):")
    bad += cmd_site(argparse.Namespace(folder=str(REPO / "docs"), system="personal", major="1", css=None, tokens=None, strict=True))
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("site", help="lint a site folder or file")
    a.add_argument("folder")
    a.add_argument("--strict", action="store_true", help="fail on warnings too")
    t = sub.add_parser("tokens", help="check colour contrast")
    t.add_argument("-v", "--verbose", action="store_true")
    for p in (a, t):
        p.add_argument("--system", default="personal")
        p.add_argument("--major", default="1", help="major version (default 1)")
        p.add_argument("--css", help="path or URL of the system's brand.css (default: the published one)")
        p.add_argument("--tokens", help="path or URL of the system's tokens.json")
    al = sub.add_parser("all", help="(design repo) contrast + DESIGN.md lint for every system")
    al.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()
    return {"site": cmd_site, "tokens": cmd_tokens, "all": cmd_all}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
