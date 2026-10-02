"""Audit an interactive workflow page and export PNGs of its canvas.

Usage:
    python scripts/wf_check.py "<Topic> - workflow (interactive).html" [theme ...]

Runs the audit function in SKILL.md (the only ```js block there, read from the
file so there is one copy of it) in headless Chromium and prints
{"findings": [...], "console_errors": [...]} as JSON. Both lists empty is a
pass, and only then is the exit code 0. For each theme given (ocean, forest,
ember, graphite) it saves "<name> - <theme>.png" next to the HTML file, where
<name> is the HTML file name without ".html".

Needs Playwright:  pip install playwright && python -m playwright install chromium
"""
import json
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

THEMES = {"ocean", "forest", "ember", "graphite"}


def load_audit():
    skill = pathlib.Path(__file__).resolve().parent.parent / "SKILL.md"
    blocks = re.findall(r"^```js\n(.*?)^```", skill.read_text(encoding="utf-8"), re.S | re.M)
    if len(blocks) != 1:
        sys.exit(f"expected exactly one ```js block in {skill}, found {len(blocks)}")
    return blocks[0]


def settle(page):
    page.wait_for_load_state("load")
    page.evaluate("document.fonts.ready.then(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))))")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    page_file = pathlib.Path(sys.argv[1]).resolve()
    if not page_file.is_file():
        sys.exit(f"not found: {page_file}")
    themes = sys.argv[2:]
    unknown = [t for t in themes if t not in THEMES]
    if unknown:
        sys.exit("unknown theme(s): " + ", ".join(unknown))
    audit = load_audit()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 2180, "height": 1180}, device_scale_factor=2)
        errors = []
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: errors.append(str(exc)))
        page.goto(page_file.as_uri())
        settle(page)
        findings = page.evaluate(audit)
        saved = []
        for theme in themes:
            page.goto(page_file.as_uri() + "?theme=" + theme)
            settle(page)
            out = page_file.with_name(f"{page_file.stem} - {theme}.png")
            page.locator("#c").screenshot(path=str(out))
            saved.append(str(out))
        browser.close()
    print(json.dumps({"findings": findings, "console_errors": errors}, indent=1))
    for out in saved:
        print("saved", out)
    sys.exit(1 if findings or errors else 0)


if __name__ == "__main__":
    main()
