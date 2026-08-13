#!/usr/bin/env python3
"""Refresh preview/ (pages, layouts, includes, nav data, assets) as a standalone
copy of root.

Run whenever you want to reset the preview sandbox to match current root
content, before making preview-only edits:
    python3 scripts/build_preview.py

Overwrites preview/*.html, preview/assets/, _data/preview_nav.yml, and the
preview-* layout/include twins in _layouts/ and _includes/ — any hand edits
made since the last refresh are replaced. Use promote_preview.py to push
preview/ changes back.
"""
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _preview_transform import NOINDEX_LINE, add_preview_prefix

ROOT = pathlib.Path(__file__).resolve().parent.parent
PREVIEW_DIR = ROOT / "preview"

PAGES = ["index.html", "tools.html", "contact.html", "partners.html", "sample-engagements.html"]
LAYOUT_FILES = ["default.html", "home.html", "page.html"]
INCLUDE_FILES = ["header.html", "footer.html"]

VIEWPORT_LINE = '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'


def write(src: pathlib.Path, dest: pathlib.Path) -> None:
    dest.write_text(add_preview_prefix(src.read_text()))
    print(f"wrote {dest.relative_to(ROOT)}")


def main() -> None:
    PREVIEW_DIR.mkdir(exist_ok=True)

    preview_assets = PREVIEW_DIR / "assets"
    if preview_assets.exists():
        shutil.rmtree(preview_assets)
    shutil.copytree(ROOT / "assets", preview_assets)
    print(f"copied assets/ -> {preview_assets.relative_to(ROOT)}")

    write(ROOT / "_data" / "nav.yml", ROOT / "_data" / "preview_nav.yml")

    for name in PAGES:
        write(ROOT / name, PREVIEW_DIR / name)

    for name in LAYOUT_FILES:
        src = ROOT / "_layouts" / name
        dest = ROOT / "_layouts" / f"preview-{name}"
        text = add_preview_prefix(src.read_text())
        if name == "default.html":
            text = text.replace(VIEWPORT_LINE, VIEWPORT_LINE + NOINDEX_LINE)
        dest.write_text(text)
        print(f"wrote {dest.relative_to(ROOT)}")

    for name in INCLUDE_FILES:
        write(ROOT / "_includes" / name, ROOT / "_includes" / f"preview-{name}")


if __name__ == "__main__":
    main()
