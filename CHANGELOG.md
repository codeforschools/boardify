# Changelog

## Unreleased
- `examples/workflows/draft-pdfs.yml`: grant `pull-requests: read` (`gh pr diff` failed with "Resource not accessible by integration" under `contents: read` alone) and sanitize the PR title used as the artifact name (a colon, slash or quote in a title failed the upload).

## 0.2.0
- `check` parses with python-frontmatter and validates required fields, unique codes, quoted section codes,
  URL-safe titles and internal references.
- Brand configuration: `pdf_css`, `templates_dir`, a repo-local `logo_url`; local files cannot be pulled into PDFs.
- `cms-config` generates the Sveltia CMS configuration from the content folders.
- S3 falls back to boto3's default credential chain (OIDC roles, profiles); PDFs upload as `application/pdf`.
- CLI paths may be separate arguments, commas or newlines.
- Hardened example workflows; West Ada-specific wiki and workflows moved out.
- Python 3.11+ (was 3.14+), tests and CI.
- Documentation site built with Zensical (`docs/`, `zensical.toml`), including the generic editor guides.

## 0.1.0
- Initial extraction of the engine from `board`.
