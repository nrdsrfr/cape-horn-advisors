# Cape Horn Advisors

Static [Jekyll](https://jekyllrb.com/) rebuild of the Cape Horn Advisors brochure site (formerly WordPress), hostable free on GitHub Pages. All 12 pages are reproduced at their original URLs with a sticky nav (dropdowns + responsive mobile menu) and a JavaScript `mailto:` contact form.

## Local development

```sh
bundle install
bundle exec jekyll serve
```

Then open http://127.0.0.1:4000/cape-horn-advisors/ (the site currently serves under a `baseurl` for GitHub Pages project-page hosting — see below). Edits to content, layouts, or assets regenerate automatically (add `--livereload` if you want auto-refresh).

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

The site currently serves at `https://nrdsrfr.github.io/cape-horn-advisors/` — a **project page**, not a user/org page or custom domain, so every internal link and asset reference uses Jekyll's `relative_url` filter (never hardcoded `/assets/...` paths) and `_config.yml` sets:
```yaml
url: "https://nrdsrfr.github.io"
baseurl: "/cape-horn-advisors"
```
`relative_url` prepends `baseurl` automatically, so this is the only place that needs to change per environment — no template edits required when the hosting target changes.

### Custom domain

When `capehornadvisors.com` (or any custom domain) is ready:
1. Add a `CNAME` file at the repo root containing the bare domain, e.g. `capehornadvisors.com`.
2. Configure the domain under **Settings → Pages → Custom domain**.
3. Update `_config.yml`:
   ```yaml
   url: "https://capehornadvisors.com"
   baseurl: ""
   ```
4. Rebuild/redeploy — every link updates automatically via `relative_url`.

## Notes

- The contact form has no backend: submitting opens the visitor's mail client addressed to `info@capehornadvisors.com`. A plain `mailto:` link is shown as a fallback.
- `capehornadvisors.WordPress.2026-07-16.xml` is the original export, kept for reference and excluded from the build.
