# boardify

Tooling for policy-manual sites built with a static site generator (Zensical) and a git-backed CMS. It is the engine; the content lives in a separate repository (for example `policy`).

## Content contract
A content repo has `content/policies/<section>/<code>-<slug>/index.md` (the Policy) and, optionally, `regulation.md` (the Regulation). Frontmatter: `code`, `title`, `kind` (`Policy` or `Regulation`), `updated`, `reference`.

## Commands
Run from the content repo root; settings come from `[tool.boardify]` in `pyproject.toml` (see `src/boardify/config.py` for defaults).

```bash
boardify check                          # validate structure and frontmatter
boardify pdf PATH[,PATH...] [--upload]  # build PDFs into output/ (S3 upload uses AWS_S3_* env vars)
boardify delete-pdf --base REV PATH...  # remove PDFs for files deleted since REV
boardify diff                           # output/diff.diff -> output/diff.json
boardify redline                        # output/diff.json -> redline PDFs
```

PDFs are named `{code}-{kind}-{title-slug}.pdf` from frontmatter, matching the site's "Download PDF" link.

## Using it from a content repo
```toml
# pyproject.toml
dependencies = ["boardify"]
[tool.uv.sources]
boardify = { git = "https://github.com/codeforschools/boardify", tag = "v0.1.0" }

[tool.boardify]
policies_root = "content/policies"
pdf_prefix = "pdfs"
logo_url = "https://example.org/logo.png"
```

`examples/workflows/` holds the GitHub Actions the original site used. They still reference MkDocs in places and have not yet been converted to reusable workflows. `overrides/` and `wiki/` are carried over from the original `board` repo and are not yet generalized.
