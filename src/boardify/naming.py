"""PDF names come from frontmatter, not filenames (files are index.md / regulation.md)."""
import subprocess

import frontmatter


def slugify_title(title):
    # Same rule the site's "Download PDF" link uses, so keys and links agree.
    slug = str(title).lower().replace(" ", "-")
    for ch in ",()":
        slug = slug.replace(ch, "")
    return slug


def pdf_name(meta):
    return f"{meta['code']}-{str(meta['kind']).lower()}-{slugify_title(meta['title'])}"


def meta_from_file(path):
    return frontmatter.load(path).metadata


def meta_from_revision(rev, path):
    """Frontmatter of a file as it was at `rev` (for files since deleted)."""
    text = subprocess.run(
        ["git", "show", f"{rev}:{path}"], capture_output=True, encoding="utf-8", check=True
    ).stdout
    return frontmatter.loads(text).metadata
