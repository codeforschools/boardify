"""Organization settings, read from [tool.boardify] in pyproject.toml in the working directory."""
import tomllib
from pathlib import Path

DEFAULTS = {
    "policies_root": "content/policies",  # where <section>/<code>-<slug>/ folders live
    "pdf_prefix": "pdfs",  # S3 key prefix (the bucket and credentials come from AWS_S3_* env vars)
    "output_dir": "output",
    "logo_url": "",  # shown on generated PDFs: an https URL, or a path relative to the repo root
    "pdf_css": "",  # optional stylesheet appended to every PDF (the brand manager's file)
    "templates_dir": "",  # optional directory whose templates override the bundled PDF templates
}

CMS_DEFAULTS = {
    "repo": "",  # GitHub "owner/name" the CMS commits to (required for `cms-config`)
    "branch": "main",
    "base_url": "",  # OAuth proxy for the GitHub backend
    "app_title": "Policy Manager",
    "sveltia_version": "",  # exact @sveltia/cms version to load (required: no unpinned CDN scripts)
    "sveltia_integrity": "",  # optional Subresource Integrity hash for that version's script
    "logo": "/assets/images/logo.png",  # shown on the CMS login screen
    "config_path": "content/admin/config.yml",
    "index_path": "content/admin/index.html",
    "media_folder": "content/assets",
    "public_folder": "/assets",
}


def load(path="pyproject.toml"):
    config = dict(DEFAULTS)
    cms = dict(CMS_DEFAULTS)
    p = Path(path)
    if p.exists():
        settings = tomllib.loads(p.read_text()).get("tool", {}).get("boardify", {})
        cms.update(settings.pop("cms", {}))
        config.update(settings)
    config["cms"] = cms
    return config
