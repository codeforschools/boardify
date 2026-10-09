# boardify

Tooling for policy-manual sites built with a static site generator ([Zensical](https://zensical.org)) and a git-backed CMS ([Sveltia](https://github.com/sveltia/sveltia-cms)). It is the engine; the content lives in a separate repository, so many organizations can share one tool.

What it does:

- **Validates** a content repo's folder layout and frontmatter (`boardify check`).
- **Builds PDFs** of each policy and regulation, named from frontmatter, and uploads them to S3.
- **Builds redlines**: word-level change PDFs from a pull request's diff.
- **Generates the CMS configuration** from the folders (`boardify cms-config`).
- **Ships a Zensical theme** that adds the policy header, references and a "Download PDF" link.

## Install

Python 3.11+. PDFs use WeasyPrint, which needs Pango installed on the system (see [CONTRIBUTING](CONTRIBUTING.md)).

```toml
# pyproject.toml of a content repo
dependencies = ["boardify"]

[tool.uv.sources]
boardify = { git = "https://github.com/codeforschools/boardify", tag = "v0.2.0" }

[tool.boardify]
policies_root = "content/policies"
pdf_bucket = "example.org"
pdf_region = "us-west-2"
pdf_prefix = "pdfs"
logo_url = "content/assets/images/logo.png"   # an https URL, or a path from the repo root
pdf_css = "content/assets/brand.css"
```

## Commands

Run from the content repo root; settings come from `[tool.boardify]` (defaults in `src/boardify/config.py`).

```bash
boardify check                          # validate structure and frontmatter
boardify pdf PATH [PATH...] [--upload]  # build PDFs into output/ (S3 upload needs pdf_bucket, pdf_region)
boardify delete-pdf --base REV PATH...  # remove PDFs for files deleted since REV
boardify diff                           # output/diff.diff -> output/diff.json
boardify redline                        # output/diff.json -> redline PDFs
boardify cms-config [--check]           # generate content/admin/{config.yml,index.html}
```

`PATH`s may be separate arguments or one comma- or newline-separated argument.

## Documentation

Published at <https://codeforschools.github.io/boardify/> (built from `docs/` with Zensical: `uv run zensical serve`).

- [Content contract](docs/content-contract.md): folder layout, frontmatter, what `check` enforces, PDF names.
- [Branding](docs/branding.md): colors, fonts, logo, template overrides; the theme.
- [CMS](docs/cms.md): `cms-config` and the pinned Sveltia script.
- [CI, secrets and roles](docs/ci.md): the example workflows, AWS access, code owners.
- [Editor guides](docs/editors/): logging in, editing, style, publishing (written from one deployment's point of view).

## Theme

```toml
# zensical.toml
[project.theme]
name = "boardify"

[project.extra]
# https://s3.<region>.amazonaws.com/<bucket>/<pdf_prefix>   (path style: bucket names may contain dots)
pdf_base_url = "https://s3.us-west-2.amazonaws.com/example.org/pdfs"
```

`pdf_base_url` cannot be derived from `pdf_bucket`/`pdf_region` in `[tool.boardify]` at build time: Zensical passes only its own theme keys to templates, so keep the two in step.

## License

BSD 3-Clause.
