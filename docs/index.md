# boardify

Tooling for policy-manual sites: structure checks, PDFs, redlines and a git-backed editing CMS. The engine lives here; the content lives in a separate repository.

## Setting up a content repo
- [Content contract](content-contract.md): folder layout, frontmatter, what `boardify check` enforces.
- [Branding](branding.md): colors, fonts, logo, template overrides.
- [CMS](cms.md): generating the Sveltia configuration.
- [CI, secrets and roles](ci.md): the example workflows, AWS access, code owners.

## Using the CMS (editor guides)
Written from the point of view of one deployment (West Ada's), as a model for your own. The policy style guide itself belongs to each organization's content repo.

- [Authentication](editors/Authentication.md): logging in.
- [Editing Workflow](editors/Editing-Workflow.md): create, update and delete policies and regulations.
- [Markdown Syntax](editors/Markdown-Syntax.md), [Using Microsoft Word](editors/Using-Microsoft-Word.md).
- [Publishing Workflow](editors/Publishing-Workflow.md) and [Project Management](editors/Project-Management.md).
- [System Architecture](editors/System-Architecture.md) and [GitHub Backend](editors/Github-Backend.md).
