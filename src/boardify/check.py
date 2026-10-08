"""Consistency check for content/policies/<section>/<code>-<slug>/{index,regulation}.md.

The layout and frontmatter rules here are the contract between boardify and a content repo
(see README, "Content contract").
"""
import re
from pathlib import Path

import frontmatter

from .naming import title_is_safe

FILES = (("index.md", "Policy"), ("regulation.md", "Regulation"))
CODE_RE = re.compile(r"\d{4}-\d{2}")
SECTION_RE = re.compile(r"(\d{4})-.+")
# An internal reference: ####-## not part of a longer number, date or citation.
REFERENCE_RE = re.compile(r"(?<![\d.\-/])(\d{4}-\d{2})(?![\d\-/])")


def is_school_year(ref):
    """2017-18 reads like a code but is a school year."""
    start, end = int(ref[:4]), int(ref[5:])
    return 1900 <= start <= 2199 and (start + 1) % 100 == end


def load(path, errors, root):
    """Frontmatter and body of a file, recording a parse failure instead of raising."""
    try:
        post = frontmatter.load(path)
    except Exception as exc:  # noqa: BLE001  malformed YAML, bad encoding
        errors.append(f"unreadable frontmatter in {path.relative_to(root)}: {exc}")
        return None
    return post


def check_section(section, root, errors, warnings, codes, bodies):
    rel = section.relative_to(root)
    m = SECTION_RE.match(section.name)
    if not m:
        errors.append(f"bad section folder name: {rel}")
        return
    index = section / "index.md"
    if not index.exists():
        errors.append(f"missing index.md: {rel}")
    elif post := load(index, errors, root):
        if str(post.get("code")) != m.group(1) or not isinstance(post.get("code"), str):
            errors.append(f'section code must be the quoted string "{m.group(1)}": {rel}/index.md')
        if not post.get("title"):
            errors.append(f"missing title: {rel}/index.md")
        if "kind" in post.metadata:
            errors.append(f"section index must not have a kind: {rel}/index.md")

    for item in sorted(section.iterdir()):
        if item.name in ("index.md", ".DS_Store"):
            continue
        if item.is_file():
            errors.append(f"stray flat file: {item.relative_to(root)}")
            continue
        check_policy(item, root, errors, warnings, codes, bodies)


def check_policy(item, root, errors, warnings, codes, bodies):
    rel = item.relative_to(root)
    m = re.match(r"(\d{4}-\d{2})-.+", item.name)
    if not m:
        errors.append(f"bad folder name: {rel}")
        return
    code = m.group(1)
    if code in codes:
        errors.append(f"duplicate code {code}: {rel} and {codes[code]}")
    codes[code] = rel

    files = {p.name for p in item.iterdir() if p.name != ".DS_Store"}
    for extra in sorted(files - {n for n, _ in FILES}):
        errors.append(f"unexpected file: {rel}/{extra}")
    if "index.md" not in files:
        errors.append(f"missing index.md: {rel}")
        return

    titles = {}
    for name, kind in FILES:
        if name not in files:
            continue
        post = load(item / name, errors, root)
        if post is None:
            continue
        where = f"{rel}/{name}"
        for field in ("code", "title", "kind"):
            if not post.get(field):
                errors.append(f"missing {field}: {where}")
        if post.get("code") != code:
            errors.append(f"code {post.get('code')!r} != folder {code}: {where}")
        if post.get("kind") != kind:
            errors.append(f"kind {post.get('kind')!r} != {kind}: {where}")
        if not post.get("updated"):
            warnings.append(f"missing updated: {where}")
        title = post.get("title")
        if title and not title_is_safe(title):
            errors.append(f"title has characters that are unsafe in a PDF name/URL: {title!r}: {where}")
        titles[name] = title
        bodies[where] = (code, post.content)
    if len(titles) == 2 and titles["index.md"] != titles["regulation.md"]:
        warnings.append(f"titles differ: {rel}")


def main(cfg):
    root = Path(cfg["policies_root"]).resolve()
    errors, warnings, codes, bodies = [], [], {}, {}
    for section in sorted(p for p in root.iterdir() if p.is_dir()):
        check_section(section, root, errors, warnings, codes, bodies)

    # Internal references (####-##) should point at a policy that exists.
    for where, (own_code, body) in bodies.items():
        for ref in sorted(set(REFERENCE_RE.findall(body)) - {own_code}):
            if ref not in codes and not is_school_year(ref):
                warnings.append(f"reference to unknown code {ref}: {where}")

    for w in warnings:
        print("warn:", w)
    for e in errors:
        print("error:", e)
    print(f"{len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0
