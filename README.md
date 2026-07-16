# Cape Horn Advisors

Static [Jekyll](https://jekyllrb.com/) rebuild of the Cape Horn Advisors brochure site (formerly WordPress), hostable free on GitHub Pages. All 12 pages are reproduced at their original URLs with a sticky nav (dropdowns + responsive mobile menu) and a JavaScript `mailto:` contact form.

## Local development

```sh
bundle install
bundle exec jekyll serve
```

Then open http://127.0.0.1:4000. Edits to content, layouts, or assets regenerate automatically (add `--livereload` if you want auto-refresh).

## Structure

- `index.html` + the 11 root `*.html` files — one page each, front-matter driven (`layout`, `permalink`, and optional `hero_image`/`hero_title`).
- `_layouts/` — `default` (shell), `home` (full-screen hero), `page` (hero image _or_ compact title band).
- `_includes/` — `header.html` (logo + nav from `_data/nav.yml`), `footer.html`.
- `_data/nav.yml` — navigation hierarchy (edit here to change the menu).
- `assets/` — `css/style.css`, `js/main.js` (sticky header, mobile menu, mailto handler), `images/`.

## Deploying to GitHub Pages

This site uses the native GitHub Pages build (the `github-pages` gem, whitelisted plugins only — no Actions workflow needed).

1. Push this repository to GitHub.
2. Repo **Settings → Pages → Source: "Deploy from a branch"**, branch `main`, folder `/ (root)`.

The site serves at `https://<user>.github.io/<repo>/`.

### Custom domain (optional)

To serve at `capehornadvisors.com`, add a `CNAME` file at the repo root containing `capehornadvisors.com`, configure the domain in **Settings → Pages**, and point your DNS at GitHub Pages. Leave `url`/`baseurl` in `_config.yml` empty for an apex domain.

## Notes

- The contact form has no backend: submitting opens the visitor's mail client addressed to `info@capehornadvisors.com`. A plain `mailto:` link is shown as a fallback.
- The footer copyright year is preserved from the original ("COPYRIGHT 2017"); change it in `_includes/footer.html` if desired.
- `capehornadvisors.WordPress.2026-07-16.xml` is the original export, kept for reference and excluded from the build.
