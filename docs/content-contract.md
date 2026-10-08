# Content contract

A content repository has this layout, and `boardify check` enforces it.

```
content/
  index.md                      # optional home page
  policies/
    0100-mission/               # section folder: <4-digit code>-<slug>
      index.md                  # section page: title and a quoted code ("0100"), no kind
      0100-01-mission-statement/  # policy folder: <####-##>-<slug>
        index.md                # the Policy (required)
        regulation.md           # the Regulation (optional, never without a Policy)
```

## Frontmatter

| Field | Policy / Regulation | Section page |
| --- | --- | --- |
| `code` | required, `####-##`, equal to the folder's code | required, quoted string equal to the section folder's code (`"0100"`) |
| `title` | required; a Regulation's should equal its Policy's | required |
| `kind` | required, `Policy` or `Regulation` (the file name is not the source of truth) | must be absent |
| `updated` | expected (the CMS sets it on every save) | |
| `reference` | optional; external citations shown in the footer and on the PDF | |

Quote section codes: unquoted, YAML reads `0100` as the number 100 (or an octal), losing the leading zero.

## What `check` reports

Errors (exit status 1): bad folder names, stray or unexpected files, a missing `index.md`, unreadable
frontmatter, missing `code`/`title`/`kind`, a code or kind that disagrees with the folder or file, duplicate
codes, a section code that is not the quoted string, and titles containing characters that are unsafe in a PDF
name or URL (`/ \ ? # % & : ; ' " + = @ < > [ ] { } | ^ ~ ` * ! $`).

Warnings: a missing `updated`, a Regulation whose title differs from its Policy's, and an internal reference
(`####-##`) to a code that does not exist. School years such as `2017-18` are ignored.

## PDF names

PDFs are named `{code}-{kind}-{title-slug}.pdf`, from frontmatter (`boardify.naming`): lower-case, spaces become
hyphens, commas and parentheses are removed. The theme's "Download PDF" link repeats that rule in Jinja
(`boardify_theme/main.html`); a test keeps the two in step, so change them together.
