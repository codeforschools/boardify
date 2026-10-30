import difflib
import json
import os
import re
import subprocess

import frontmatter
from mistune import html as markdown_html
from unidiff import PatchSet

from .line_numbers import annotate_line, body_start_line, split_marker
from .naming import pdf_name

INDEX_RE = re.compile(r"^index ([0-9a-f]+)\.\.([0-9a-f]+)")


def strip_prefix(path):
    return path[2:] if path[:2] in ("a/", "b/") else path


def get_blob(blob_hash):
    """
    Fetch the exact file content for a git blob hash straight from the
    object database, so we can diff full before/after documents rather
    than just the hunks in a unified diff.
    """
    if not blob_hash or set(blob_hash) == {"0"}:
        return ""
    result = subprocess.run(
        ["git", "cat-file", "-p", blob_hash],
        capture_output=True,
        encoding="utf-8",
        check=False,
    )
    return result.stdout if result.returncode == 0 else ""


def get_index_hashes(patchfile):
    for line in patchfile.patch_info:
        match = INDEX_RE.match(line)
        if match:
            return match.group(1), match.group(2)
    return None, None


def get_frontmatter(text):
    if not text:
        return {}
    return frontmatter.loads(text).to_dict()


def get_body(text):
    if not text:
        return ""
    return frontmatter.loads(text).content


def tokenize(line):
    """Split a line into whitespace and non-whitespace runs, so word-level
    diffing can recombine them without disturbing spacing."""
    return re.findall(r"\s+|\S+", line)


def word_diff(old_line, new_line):
    """
    Inline word-level diff between two corresponding lines: unchanged words
    pass through untouched, removed words are wrapped in <del> (rendered
    with strikethrough + red highlight), and added words in <ins> (rendered
    bold + green highlight).
    """
    old_tokens = tokenize(old_line)
    new_tokens = tokenize(new_line)
    matcher = difflib.SequenceMatcher(None, old_tokens, new_tokens, autojunk=False)
    out = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            out.append("".join(new_tokens[j1:j2]))
            continue
        if i1 != i2:
            old_run = "".join(old_tokens[i1:i2])
            # A whitespace-only run (e.g. a trailing-newline mismatch at
            # EOF) has nothing meaningful to highlight.
            out.append(f"<del>{old_run}</del>" if old_run.strip() else old_run)
        if j1 != j2:
            new_run = "".join(new_tokens[j1:j2])
            out.append(f"<ins>{new_run}</ins>" if new_run.strip() else new_run)
    return "".join(out)


TABLE_DELIMITER_RE = re.compile(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$")
CELL_SPLIT_RE = re.compile(r"(?<!\\)\|")


def is_table_row(line):
    return line.lstrip().startswith("|")


def is_table_delimiter(line):
    return is_table_row(line) and bool(TABLE_DELIMITER_RE.match(line))


def map_cells(line, fn):
    """
    Apply `fn` to the text of each non-empty cell of a table row, keeping
    the pipes (and the row's leading `|`) intact so mistune still sees a table.
    """
    text = line.rstrip("\n")
    trailing_newline = "\n" if line.endswith("\n") else ""
    parts = CELL_SPLIT_RE.split(text)
    for i, part in enumerate(parts):
        core = part.strip()
        if core:
            parts[i] = f" {fn(core)} "
    return "|".join(parts) + trailing_newline


def table_row_diff(old_line, new_line):
    """
    Cell-by-cell word diff of two table rows with the same number of cells,
    or None if the rows can't be paired that way.
    """
    old_parts = CELL_SPLIT_RE.split(old_line.rstrip("\n"))
    new_parts = CELL_SPLIT_RE.split(new_line.rstrip("\n"))
    if len(old_parts) != len(new_parts):
        return None
    cells = [word_diff(o.strip(), n.strip()) for o, n in zip(old_parts, new_parts, strict=True)]
    text = "|".join(f" {c} " if c.strip() else c for c in cells)
    return text + ("\n" if new_line.endswith("\n") else "")


def wrap_whole_line(line, tag, line_no=None):
    if is_table_row(line):
        # No line-number span or whole-row wrapper: either would stop the row being a table row.
        if is_table_delimiter(line):
            return line
        return map_cells(line, lambda cell: f"<{tag}>{cell}</{tag}>")
    text = line.rstrip("\n")
    if not text.strip():
        # Leave blank lines untouched -- mistune relies on genuinely blank
        # lines to detect paragraph breaks, and there's nothing to highlight.
        return line
    marker, rest = split_marker(text)
    span = f'<span class="ln">{line_no}</span>' if line_no is not None else ""
    return f"{marker}{span}<{tag}>{rest}</{tag}>\n"


def number_replaced_line(merged, line_no):
    """
    Prefix a word-diffed (already <ins>/<del>-tagged) replacement line with
    its line-number span, matching the numbering used elsewhere.
    """
    text = merged.rstrip("\n")
    if not text.strip():
        return merged
    trailing_newline = "\n" if merged.endswith("\n") else ""
    marker, rest = split_marker(text)
    return f'{marker}<span class="ln">{line_no}</span>{rest}{trailing_newline}'


def emit_deleted(out, line):
    """
    Append a wholly deleted line. A deleted table delimiter row is kept only
    when it follows a deleted header row (the whole table went away); on its
    own it would add a stray row to a table that still exists.
    """
    if is_table_delimiter(line):
        if out and is_table_row(out[-1]) and "<del>" in out[-1]:
            out.append(line)
        return
    out.append(wrap_whole_line(line, "del"))


def build_redline_body(old_body, new_body, new_start=1):
    """
    Two-level diff of a full document body: a line-level pass finds which
    lines are unchanged, wholly added/removed, or replaced; replaced lines
    then get a nested word-level diff so only the changed words themselves
    are marked up, keeping everything else rendered inline as normal prose.

    Lines are numbered against the resulting (new) document, matching the
    clean-version PDF's numbering, starting at `new_start`. Lines that only
    ever existed in the old document (pure deletions) have no new-document
    line number, so they're left unnumbered.
    """
    old_lines = old_body.splitlines(keepends=True)
    new_lines = new_body.splitlines(keepends=True)
    matcher = difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False)

    out = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for offset, line in enumerate(new_lines[j1:j2]):
                out.append(annotate_line(line, new_start + j1 + offset))
        elif tag == "replace":
            old_chunk = old_lines[i1:i2]
            new_chunk = new_lines[j1:j2]
            paired = min(len(old_chunk), len(new_chunk))
            for k in range(paired):
                old_line, new_line = old_chunk[k], new_chunk[k]
                if is_table_row(old_line) or is_table_row(new_line):
                    merged = None
                    if is_table_delimiter(new_line):
                        merged = new_line
                    elif is_table_row(old_line) and is_table_row(new_line):
                        merged = table_row_diff(old_line, new_line)
                    if merged is None:
                        emit_deleted(out, old_line)
                        merged = wrap_whole_line(new_line, "ins", new_start + j1 + k)
                    out.append(merged)
                    continue
                merged = word_diff(old_line, new_line)
                out.append(number_replaced_line(merged, new_start + j1 + k))
            for line in old_chunk[paired:]:
                emit_deleted(out, line)
            for offset, line in enumerate(new_chunk[paired:]):
                out.append(wrap_whole_line(line, "ins", new_start + j1 + paired + offset))
        elif tag == "delete":
            for line in old_lines[i1:i2]:
                emit_deleted(out, line)
        elif tag == "insert":
            for offset, line in enumerate(new_lines[j1:j2]):
                out.append(wrap_whole_line(line, "ins", new_start + j1 + offset))
    return "".join(out)


def convert_patchfile(patchfile):
    old_hash, new_hash = get_index_hashes(patchfile)
    old_text = get_blob(old_hash)
    new_text = get_blob(new_hash)

    meta = get_frontmatter(new_text) or get_frontmatter(old_text)
    old_body = get_body(old_text)
    new_body = get_body(new_text)
    new_start = body_start_line(new_text, new_body) if new_body else 1

    output = {}
    output["code"] = meta.get("code", patchfile.path.rpartition("/")[2].partition(".")[0])
    output["title"] = meta.get("title", "")
    output["kind"] = meta.get("kind", "")
    output["reference"] = meta.get("reference", "")
    output["old_path"] = strip_prefix(patchfile.source_file)
    output["new_path"] = strip_prefix(patchfile.target_file)
    output["is_rename"] = bool(patchfile.is_rename) and output["old_path"] != output["new_path"]
    output["redline_html"] = markdown_html(build_redline_body(old_body, new_body, new_start))

    # Same frontmatter-derived name as pdf.py, so the redline PDF lands
    # next to its clean-version counterpart.
    output["filename"] = pdf_name(meta) if {"code", "kind", "title"} <= set(meta) else output["code"]

    return output


def convert_patchset(filename):
    output = {}
    patchset = PatchSet.from_filename(filename)

    output["filename"] = filename
    output["added"] = patchset.added
    output["removed"] = patchset.removed

    output["added_files"] = [
        convert_patchfile(x) for x in patchset.added_files if x.path.endswith(".md")
    ]
    output["removed_files"] = [
        convert_patchfile(x) for x in patchset.removed_files if x.path.endswith(".md")
    ]
    output["modified_files"] = [
        convert_patchfile(x) for x in patchset.modified_files if x.path.endswith(".md")
    ]

    return output


def save_json(filename, cfg):
    data = convert_patchset(filename)
    data["title"] = os.getenv("TITLE", "Policy/Regulation Changes")
    with open(f"{cfg['output_dir']}/diff.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

