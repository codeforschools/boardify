# Branding

Look and feel is configuration, not code. A content repo never needs to fork boardify to restyle itself.

| What | Where | Setting |
| --- | --- | --- |
| Site and PDF colors, fonts | one stylesheet, e.g. `content/assets/brand.css` | `extra_css` in `zensical.toml` (site) and `pdf_css` in `[tool.boardify]` (PDFs) |
| Logo on PDFs | a file in the repo, or an https URL | `logo_url` (a path is resolved from the repo root) |
| Logo and name on the site | `zensical.toml` | `[project.theme] logo`, `site_name`, `copyright` |
| PDF layout and markup | a folder of templates that override the bundled ones | `templates_dir` |

## One brand stylesheet

Write CSS custom properties once and use them for both outputs:

```css
:root {
  /* PDFs (boardify/templates/base.html reads these) */
  --brand-font: "Source Sans 3", Helvetica, sans-serif;
  --brand-text: #333;
  --brand-heading: #1b3a5c;

  /* Site (Zensical's theme variables) */
  --md-primary-fg-color: #1b3a5c;
  --md-accent-fg-color: #b5651d;
}
```

`pdf_css` is appended after the bundled styles, so any rule in it wins; PDFs are rendered with WeasyPrint, which
supports CSS variables. Local files that PDFs may load (the logo, assets next to `pdf_css`) are limited to those
folders; policy text cannot pull other files from disk into a PDF.

## Overriding PDF templates

Set `templates_dir = "overrides/pdf"` and put `policy.html`, `diff.j2` or `base.html` there; any template found
there replaces the bundled one of the same name (extend the bundled one with `{% extends "base.html" %}` to change
only a block).
