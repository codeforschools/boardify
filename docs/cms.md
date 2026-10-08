# CMS (Sveltia)

`boardify cms-config` writes `content/admin/config.yml` and `index.html` from the content folders, so the editing
UI cannot drift from the folder structure: one singleton per section page, a Policies collection per section, and
a Regulations collection for each section that has a `regulation.md`. Rerun it after adding a section or the first
regulation in one; `boardify cms-config --check` fails when the files are stale (use it in CI).

```toml
[tool.boardify.cms]
repo = "owner/policy"
base_url = "https://oauth-proxy.example.org/"   # GitHub OAuth proxy
app_title = "Policy Manager"
sveltia_version = "0.220.0"        # required: an exact version, never "latest"
sveltia_integrity = "sha384-..."   # optional but recommended: Subresource Integrity for that version
layout = "section"                 # sidebar organization, see below
```

`layout` sets how the sidebar is organized (Sveltia cannot group collections, so it is only an ordering or a tree):

- `section` (default): flat list ordered by section, each section's Policies followed by its Regulations.
- `kind`: all Policies by section, then all Regulations by section.
- `tree`: one nested Policies collection and one nested Regulations collection, each a folder tree of sections.
  Experimental: new entries may not land in the right section folder.

The admin page holds an authenticated GitHub session, so the script is pinned. To compute the hash:

```bash
curl -s https://unpkg.com/@sveltia/cms@0.220.0/dist/sveltia-cms.js | openssl dgst -sha384 -binary | openssl base64 -A
```

The generated files say they are generated; change the settings or the folders instead of editing them.
