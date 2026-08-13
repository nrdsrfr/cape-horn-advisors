#!/usr/bin/env python3
"""Refresh preview/ as a standalone copy of the live site (content + assets).

Run whenever you want to reset the preview sandbox to match the current
root content, before making preview-only edits:
    python3 scripts/build_preview.py

This overwrites preview/*.html and preview/assets/ — any hand edits made
directly in preview/ since the last refresh are replaced.
"""
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
PREVIEW_DIR = ROOT / "preview"

# (source file, layout used in preview)
PAGES = [
    ("index.html", "preview-home"),
    ("tools.html", "preview-default"),
    ("contact.html", "preview-page"),
    ("partners.html", "preview-page"),
    ("sample-engagements.html", "preview-page"),
]

FRONT_MATTER_RE = re.compile(r"\A---\n(.*?\n)---\n", re.DOTALL)
LITERAL_PATH_RE = re.compile(r"(\{\{\s*)'(/[^']+)'")


def transform(src: pathlib.Path, preview_layout: str) -> str:
    text = src.read_text()
    match = FRONT_MATTER_RE.match(text)
    if not match:
        raise SystemExit(f"{src}: expected Jekyll front matter at top of file")

    front_lines = match.group(1).splitlines()
    body = text[match.end():]

    new_front_lines = []
    for line in front_lines:
        if line.startswith("layout:"):
            line = f"layout: {preview_layout}"
        elif line.startswith("permalink:"):
            value = line.split(":", 1)[1].strip()
            line = f"permalink: /preview{value}"
        new_front_lines.append(line)

    # Prefix any root-relative literal path used in a Liquid filter
    # (asset refs, cross-page links) so they stay inside /preview.
    body = LITERAL_PATH_RE.sub(r"\1'/preview\2'", body)

    return "---\n" + "\n".join(new_front_lines) + "\n---\n" + body


def main() -> None:
    PREVIEW_DIR.mkdir(exist_ok=True)

    preview_assets = PREVIEW_DIR / "assets"
    if preview_assets.exists():
        shutil.rmtree(preview_assets)
    shutil.copytree(ROOT / "assets", preview_assets)
    print(f"copied assets/ -> {preview_assets.relative_to(ROOT)}")

    for name, preview_layout in PAGES:
        src = ROOT / name
        dest = PREVIEW_DIR / name
        dest.write_text(transform(src, preview_layout))
        print(f"wrote {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
