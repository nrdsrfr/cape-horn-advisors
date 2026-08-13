#!/usr/bin/env python3
"""Promote preview/ over the root site content + assets.

Run once you're happy with what's in preview/, or let the "Publish preview
site" GitHub Action run it and open a PR:
    python3 scripts/promote_preview.py

Overwrites the root content pages and assets/ with what's currently in
preview/, stripping the /preview prefix and preview-* layout names back out.
"""
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
PREVIEW_DIR = ROOT / "preview"

LAYOUT_MAP = {
    "preview-home": "home",
    "preview-default": "default",
    "preview-page": "page",
}

PAGES = ["index.html", "tools.html", "contact.html", "partners.html", "sample-engagements.html"]

FRONT_MATTER_RE = re.compile(r"\A---\n(.*?\n)---\n", re.DOTALL)
PREVIEW_PATH_RE = re.compile(r"(\{\{\s*)'/preview(/[^']+)'")


def transform(src: pathlib.Path) -> str:
    text = src.read_text()
    match = FRONT_MATTER_RE.match(text)
    if not match:
        raise SystemExit(f"{src}: expected Jekyll front matter at top of file")

    front_lines = match.group(1).splitlines()
    body = text[match.end():]

    new_front_lines = []
    for line in front_lines:
        if line.startswith("layout:"):
            value = line.split(":", 1)[1].strip()
            line = f"layout: {LAYOUT_MAP.get(value, value)}"
        elif line.startswith("permalink:"):
            value = line.split(":", 1)[1].strip()
            if not value.startswith("/preview"):
                raise SystemExit(f"{src}: permalink {value!r} is not under /preview")
            value = value[len("/preview"):] or "/"
            line = f"permalink: {value}"
        new_front_lines.append(line)

    body = PREVIEW_PATH_RE.sub(r"\1'\2'", body)

    return "---\n" + "\n".join(new_front_lines) + "\n---\n" + body


def main() -> None:
    for name in PAGES:
        src = PREVIEW_DIR / name
        dest = ROOT / name
        dest.write_text(transform(src))
        print(f"wrote {dest.relative_to(ROOT)}")

    root_assets = ROOT / "assets"
    shutil.rmtree(root_assets)
    shutil.copytree(PREVIEW_DIR / "assets", root_assets)
    print(f"copied {(PREVIEW_DIR / 'assets').relative_to(ROOT)} -> assets/")


if __name__ == "__main__":
    main()
