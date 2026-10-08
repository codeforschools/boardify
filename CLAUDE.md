# CLAUDE.md

Boardify is the engine for policy-manual sites. It contains no policy content; content repos (e.g. `../policy`) depend on it. Run it from a content repo, which supplies `[tool.boardify]` in its `pyproject.toml`.

- Source: `src/boardify/`; CLI entry `cli.py`. Bundled PDF templates in `src/boardify/templates/` (loaded with `PackageLoader`).
- The frontmatter schema and folder layout (see README) are the contract with content repos; change them deliberately and keep `check.py` in sync.
- S3 credentials come from `AWS_S3_*` environment variables, never from config.
- Package manager is uv. There is no test suite; verify by running the CLI against a content repo.

## Commands
Run from a content repo root (settings: `[tool.boardify]`, defaults in `config.py`). During development use `uv run boardify <cmd>` there, with boardify installed editable (e.g. `uv run --with-editable ../boardify boardify check`).

- `check` validates layout/frontmatter; `pdf PATHS [--upload]` and `delete-pdf --base REV PATHS` take comma-separated paths.
- Redline pipeline is two stages with an external input: CI writes `output/diff.diff` (`gh pr diff N`), then `diff` → `output/diff.json`, then `redline` → `output/*_redline.pdf`.

## Architecture notes
- `naming.py` is the single source of PDF names (`{code}-{kind}-{title-slug}`); keys must match the site's "Download PDF" link, so change the slug rule in both places. `delete-pdf` reads frontmatter of removed files via `git show REV:path`.
- `diff.py` doesn't just parse hunks: it fetches full before/after blobs by hash (`git cat-file`) and does word-level diffing, so it must run inside a git checkout of the content repo.
- `check.py` parses frontmatter with a regex, while `pdf`/`diff` use `python-frontmatter`; keep their expectations aligned.
- `examples/workflows/`, `overrides/`, `wiki/` are carried over from the old `board` repo and not yet generalized (some still reference MkDocs).
