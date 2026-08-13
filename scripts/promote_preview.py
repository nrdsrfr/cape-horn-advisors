#!/usr/bin/env python3
"""Promote preview/ (pages, layouts, includes, nav data, assets) over the root site.

Run once you're happy with what's in preview/, or let the "Publish preview
site" GitHub Action run it and open a PR:
    python3 scripts/promote_preview.py

Overwrites the root content pages, _layouts/*, _includes/*, _data/nav.yml,
and assets/ with what's currently in preview/, stripping /preview prefixes,
preview-* names, and the noindex meta tag back out.
"""
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _preview_transform import NOINDEX_LINE, strip_preview_prefix

ROOT = pathlib.Path(__file__).resolve().parent.parent
PREVIEW_DIR = ROOT / "preview"

PAGES = ["index.html", "tools.html", "contact.html", "partners.html", "sample-engagements.html"]
LAYOUT_FILES = ["default.html", "home.html", "page.html"]
INCLUDE_FILES = ["header.html", "footer.html"]


def write(src: pathlib.Path, dest: pathlib.Path) -> None:
    dest.write_text(strip_preview_prefix(src.read_text()))
    print(f"wrote {dest.relative_to(ROOT)}")


def main() -> None:
    write(ROOT / "_data" / "preview_nav.yml", ROOT / "_data" / "nav.yml")

    for name in PAGES:
        write(PREVIEW_DIR / name, ROOT / name)

    for name in LAYOUT_FILES:
        src = ROOT / "_layouts" / f"preview-{name}"
        dest = ROOT / "_layouts" / name
        text = strip_preview_prefix(src.read_text()).replace(NOINDEX_LINE, "")
        dest.write_text(text)
        print(f"wrote {dest.relative_to(ROOT)}")

    for name in INCLUDE_FILES:
        write(ROOT / "_includes" / f"preview-{name}", ROOT / "_includes" / name)

    root_assets = ROOT / "assets"
    shutil.rmtree(root_assets)
    shutil.copytree(PREVIEW_DIR / "assets", root_assets)
    print(f"copied {(PREVIEW_DIR / 'assets').relative_to(ROOT)} -> assets/")


if __name__ == "__main__":
    main()
