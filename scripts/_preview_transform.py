"""Shared add/strip-prefix logic for build_preview.py and promote_preview.py.

Plain literal string substitution only — no regex — so every rule is a
fixed find/replace pair you can read and verify by eye. Both scripts must
stay exact inverses of each other; STRIP_REPLACEMENTS is just ADD_REPLACEMENTS
with each pair reversed.
"""

NOINDEX_LINE = '  <meta name="robots" content="noindex, nofollow">\n'

# (find in root text, replace with in preview text)
ADD_REPLACEMENTS = [
    ("'/", "'/preview/"),                          # literal path strings, e.g. {{ '/assets/...' | relative_url }}
    ("permalink: /", "permalink: /preview/"),       # front-matter permalink
    ("layout: default", "layout: preview-default"),
    ("layout: home", "layout: preview-home"),
    ("layout: page", "layout: preview-page"),
    ("include header.html", "include preview-header.html"),
    ("include footer.html", "include preview-footer.html"),
    ("site.data.nav", "site.data.preview_nav"),
    ("url: /", "url: /preview/"),                   # _data/nav.yml -> _data/preview_nav.yml
]

STRIP_REPLACEMENTS = [(preview_text, root_text) for root_text, preview_text in ADD_REPLACEMENTS]


def add_preview_prefix(text: str) -> str:
    for find, replace in ADD_REPLACEMENTS:
        text = text.replace(find, replace)
    return text


def strip_preview_prefix(text: str) -> str:
    for find, replace in STRIP_REPLACEMENTS:
        text = text.replace(find, replace)
    return text
