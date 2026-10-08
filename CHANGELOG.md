# Changelog

## 0.2.0
- `check` parses with python-frontmatter and validates required fields, unique codes, quoted section codes,
  URL-safe titles and internal references.
- Brand configuration: `pdf_css`, `templates_dir`, a repo-local `logo_url`; local files cannot be pulled into PDFs.
- `cms-config` generates the Sveltia CMS configuration from the content folders.
- S3 falls back to boto3's default credential chain (OIDC roles, profiles); PDFs upload as `application/pdf`.
- CLI paths may be separate arguments, commas or newlines.
- Hardened example workflows; West Ada-specific wiki and workflows moved out.
- Python 3.11+ (was 3.14+), tests and CI.

## 0.1.0
- Initial extraction of the engine from `board`.
