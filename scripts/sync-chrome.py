#!/usr/bin/env python3
"""
sync-chrome.py — single source of truth for the shared nav + footer.

Edit the chrome once in partials/, then run this to propagate it into every
page. Pages stay complete HTML (so local preview still works and the deploy
stays fully static), but you never hand-edit the same nav/footer 16 times.

Usage:
    python3 scripts/sync-chrome.py

What it does:
  • partials/marginalia-nav.html  -> the <nav> block in every marginalia page
  • partials/footer.html          -> the <footer> block in the pages listed below
"""
import re, glob, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

def read(p): return (ROOT / p).read_text().rstrip("\n")

MARGINALIA_NAV = read("partials/marginalia-nav.html")
FOOTER         = read("partials/footer.html")

# Marginalia pages share one nav + the common footer.
marginalia_pages = glob.glob(str(ROOT / "marginalia/index.html")) + \
                   glob.glob(str(ROOT / "marginalia/posts/*.html"))

NAV_RE    = re.compile(r"[ \t]*<nav>.*?</nav>", re.S)
FOOTER_RE = re.compile(r"[ \t]*<footer\b[^>]*>.*?</footer>", re.S)

def apply(path, nav=None, footer=None):
    text = pathlib.Path(path).read_text()
    orig = text
    if nav is not None:
        text, n = NAV_RE.subn(lambda _: nav, text, count=1)
        if n == 0: print(f"  ! no <nav> in {path}")
    if footer is not None:
        text, n = FOOTER_RE.subn(lambda _: footer, text, count=1)
        if n == 0: print(f"  ! no <footer> in {path}")
    if text != orig:
        pathlib.Path(path).write_text(text)
        return True
    return False

changed = 0
for p in marginalia_pages:
    if apply(p, nav=MARGINALIA_NAV, footer=FOOTER):
        changed += 1
        print(f"  updated {pathlib.Path(p).relative_to(ROOT)}")

print(f"Done. {changed} file(s) changed, {len(marginalia_pages)} scanned.")
