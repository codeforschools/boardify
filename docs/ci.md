# CI, secrets and roles

`examples/workflows/` has the two workflows a content repo needs:

- `draft-pdfs.yml` — on a pull request: `boardify check`, draft PDFs and redlines as an artifact.
- `deploy.yml` — on `main`: `boardify check`, build the site, upload changed PDFs, delete removed ones, deploy Pages.

Both pass file names through NUL-separated files and `xargs -0`, never through `${{ }}` interpolation into shell,
so a hostile file name cannot run commands. Keep it that way when editing them. Make the `check` job a required
status check in branch protection.

## AWS access

PDF uploads need `AWS_S3_BUCKET` and `AWS_S3_REGION`. Credentials, in order of preference:

1. **An IAM role via GitHub OIDC.** Set the repository variable `AWS_ROLE_ARN`; `deploy.yml` assumes it. boardify
   then uses boto3's default credential chain.
2. A key pair in `AWS_S3_ACCESS_KEY` / `AWS_S3_SECRET_KEY`. Scope the IAM user to `s3:PutObject` and
   `s3:DeleteObject` on `arn:aws:s3:::<bucket>/<pdf_prefix>/*`.

## Who owns what

A content repo has three kinds of change, and `.github/CODEOWNERS` can route review for each:

| Owner | Files |
| --- | --- |
| Content | `content/policies/**`, `content/index.md` |
| Brand | `content/assets/**` (including `brand.css`), the theme and extra keys in `zensical.toml`, `logo_url` |
| IT | `.github/**`, `pyproject.toml`, `uv.lock`, `content/admin/**` (generated), secrets and variables |

Content editors using the CMS need write access to the repository, which also lets them edit workflows that run
with secrets. Protect `main`, require the owner review, and require the `check` job.
