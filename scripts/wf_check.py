"""Audit an interactive workflow page and export PNGs of its canvas.

Usage:
    python scripts/wf_check.py "<Topic> - workflow (interactive).html" [theme ...]

Runs the audit from section 7 of SKILL.md (read from the file, so there is one
copy of it) in headless Chromium, prints the findings and any console errors as
JSON, then saves "<page> - <theme>.png" for each theme given (ocean, forest,
ember, graphite). Exit code 0 only when there are no findings and no errors.

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
    text = skill.read_text(encoding="utf-8")
    m = re.search(r"^## 7\. Audit.*?^```js\n(.*?)^```", text, re.S | re.M)
    if not m:
        sys.exit("audit block not found in " + str(skill))
    return m.group(1)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    page_file = pathlib.Path(sys.argv[1]).resolve()
    themes = sys.argv[2:]
    unknown = [t for t in themes if t not in THEMES]
    if unknown:
        sys.exit("unknown theme(s): " + ", ".join(unknown))
    audit = load_audit()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 2140, "height": 1160}, device_scale_factor=2)
        errors = []
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: errors.append(str(exc)))
        page.goto(page_file.as_uri())
        page.wait_for_timeout(300)
        findings = page.evaluate(audit)
        print(json.dumps({"findings": findings, "console_errors": errors}, indent=1))
        for theme in themes:
            page.goto(page_file.as_uri() + "?theme=" + theme)
            page.wait_for_timeout(300)
            out = page_file.with_name(f"{page_file.stem} - {theme}.png")
            page.locator("#c").screenshot(path=str(out))
            print("saved", out)
        browser.close()
    sys.exit(1 if findings or errors else 0)


if __name__ == "__main__":
    main()
