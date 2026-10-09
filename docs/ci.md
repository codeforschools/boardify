# CI, secrets and roles

`examples/workflows/` has the two workflows a content repo needs:

- `draft-pdfs.yml` — on a pull request: `boardify check`, draft PDFs and redlines as an artifact.
- `deploy.yml` — on `main`: `boardify check`, build the site, upload changed PDFs, delete removed ones, deploy Pages.

Both pass file names through NUL-separated files and `xargs -0`, never through `${{ }}` interpolation into shell,
so a hostile file name cannot run commands. Keep it that way when editing them. Make the `check` job a required
status check in branch protection.

## AWS access

PDF uploads need `pdf_bucket` and `pdf_region` in `[tool.boardify]` (public values, so they live in the repo, not in
secrets) and an IAM role, assumed via GitHub OIDC. boardify reads no key pairs: it uses boto3's default credential chain.

Set the repository variable `AWS_ROLE_ARN` (an ARN is not secret); `deploy.yml` assumes it in the region from config.
The role's trust policy must match the token's `sub` claim. The deploy job uses the `github-pages` environment, so
`sub` is `repo:OWNER/REPO:environment:github-pages` by default, but repositories using GitHub's immutable subject
(check `gh api repos/OWNER/REPO/actions/oidc/customization/sub`) get `repo:OWNER@ID/REPO@ID:environment:github-pages`.
An "Not authorized to perform sts:AssumeRoleWithWebIdentity" error means they differ. Scope the role to `s3:PutObject`
and `s3:DeleteObject` on `arn:aws:s3:::<bucket>/<pdf_prefix>/*`.

Local uploads are optional; they use your own AWS profile.

## Who owns what

A content repo has three kinds of change, and `.github/CODEOWNERS` can route review for each:

| Owner | Files |
| --- | --- |
| Content | `content/policies/**`, `content/index.md` |
| Brand | `content/assets/**` (including `brand.css`), the theme and extra keys in `zensical.toml`, `logo_url` |
| IT | `.github/**`, `pyproject.toml`, `uv.lock`, `content/admin/**` (generated), secrets and variables |

Content editors using the CMS need write access to the repository, which also lets them edit workflows that run
with secrets. Protect `main`, require the owner review, and require the `check` job.
