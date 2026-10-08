# CLAUDE.md

Boardify is the engine for policy-manual sites. It contains no policy content; content repos (e.g. `../policy`) depend on it. Run it from a content repo, which supplies `[tool.boardify]` in its `pyproject.toml`.

- Source: `src/boardify/`; CLI entry `cli.py`. Bundled PDF templates in `src/boardify/templates/` (loaded with `PackageLoader`).
- The frontmatter schema and folder layout (see README) are the contract with content repos; change them deliberately and keep `check.py` in sync.
- S3 credentials come from `AWS_S3_*` environment variables, never from config.
- Package manager is uv. There is no test suite; verify by running the CLI against a content repo.
