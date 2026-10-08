# CLAUDE.md

Boardify is the engine for policy-manual sites. It contains no policy content; content repos (e.g. `../policy`) depend on it. Run it from a content repo, which supplies `[tool.boardify]` in its `pyproject.toml`.

- Source: `src/boardify/`; CLI entry `cli.py`. Bundled PDF templates in `src/boardify/templates/` (loaded with `PackageLoader`).
- The frontmatter schema and folder layout (see README) are the contract with content repos; change them deliberately and keep `check.py` in sync.
- S3 settings come from `AWS_S3_*` environment variables, never from config; without a key pair boto3's default credential chain applies (OIDC role in CI).
- Package manager is uv. `uv run ruff check .` and `uv run pytest` (CI runs both on Python 3.11–3.14); also try the CLI against a content repo (`uv run --with-editable ../boardify boardify check` there).
- Documentation for users is in `docs/` (contract, branding, CMS, CI); keep it in step with `check.py`, `config.py` and the workflows in `examples/`.

## Commands
Run from a content repo root (settings: `[tool.boardify]`, defaults in `config.py`). During development use `uv run boardify <cmd>` there, with boardify installed editable (e.g. `uv run --with-editable ../boardify boardify check`).

- `check` validates layout/frontmatter; `pdf PATHS [--upload]` and `delete-pdf --base REV PATHS` take comma-separated paths.
- Redline pipeline is two stages with an external input: CI writes `output/diff.diff` (`gh pr diff N`), then `diff` → `output/diff.json`, then `redline` → `output/*_redline.pdf`.

## Architecture notes
- `naming.py` is the single source of PDF names (`{code}-{kind}-{title-slug}`); keys must match the site's "Download PDF" link, so change the slug rule in both places. `delete-pdf` reads frontmatter of removed files via `git show REV:path`.
- `diff.py` doesn't just parse hunks: it fetches full before/after blobs by hash (`git cat-file`) and does word-level diffing, so it must run inside a git checkout of the content repo.
- `check.py`, `pdf` and `diff` all parse frontmatter with `python-frontmatter`. `check` also requires titles to be URL-safe (`naming.UNSAFE_TITLE_CHARS`) because the slug rule only strips commas and parentheses.
- `src/boardify_theme/` is a Zensical theme registered via the `mkdocs.themes` entry point (`name = "boardify"`). `partials/nav-item.html`, `nav.html` and `copyright.html` are copies of Zensical's with marked edits (section titles, `extra.nav_root`/`nav_title`, no "Made with Zensical"); re-sync them on Zensical upgrades. Templates only see Zensical's own theme keys, so site-specific values (e.g. `pdf_base_url`) come from `[project.extra]`, and the PDF slug rule is duplicated in `main.html` (keep in sync with `naming.py`).
- `render.py` is the one PDF pipeline (Jinja env with `templates_dir` overrides, brand CSS, logo, and a WeasyPrint fetcher that blocks local files outside the logo/CSS folders). `cms.py` generates the Sveltia config from the folder tree; `config.py` holds all settings, including `[tool.boardify.cms]`.
- `examples/workflows/` are the hardened workflows content repos copy (file names go through NUL-separated files, never `${{ }}` into shell). The old `wiki/` (West Ada's editor guides) moved to the `policy` repo's `docs/`.
