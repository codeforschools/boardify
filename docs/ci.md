# CI, secrets and roles

`examples/workflows/` has the two workflows a content repo needs, plus two optional ones:

- `draft-pdfs.yml` — on a pull request: `boardify check`, draft PDFs and redlines as an artifact. The PDFs are built and uploaded even when `check` fails (for example a Regulation PR whose Policy has not merged); the job still ends red.
- `deploy.yml` — on `main`: `boardify check`, build the site, upload changed PDFs, delete removed ones, deploy Pages.
- `reading-packet.yml` (optional) — run on demand: collects the Draft PDFs artifacts of every open pull request labelled First Reading, Second Reading, Third Reading or Consent into one `reading-packet` artifact, grouped by label. It reuses the artifacts `draft-pdfs.yml` already uploaded, so a pull request whose current head commit has no Draft PDFs run is listed as missing in the job summary. Edit the `LABELS` list for your own labels.
- `rename-policy.yml` (optional) — run on demand from the default branch with a branch, a policy code and a new title: updates the `title` of the Policy and its Regulation on that branch, moves the folder to `<code>-<new-title-slug>` with `git mv` (the old URL stops working), runs the checks and commits to the branch. A push with the default token does not start other workflows, so close and reopen the pull request once to re-run the draft PDFs. `deploy.yml` removes the PDF under the old title when a merged change retitles a policy already on `main`.

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
