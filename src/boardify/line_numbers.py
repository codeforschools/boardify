import re


BLOCK_MARKER_RE = re.compile(r"^(\s*(?:[-*+]\s+|\d+\.\s+|#{1,6}\s+|>\s+))(.*)$", re.DOTALL)


def split_marker(line):
    """
    Split a line into its leading block-level markdown marker (list bullet,
    numbering, heading hashes, blockquote) and the remaining text, so
    content can be wrapped or annotated without mistune losing track of the
    heading/list/blockquote syntax.
    """
    match = BLOCK_MARKER_RE.match(line)
    if match:
        return match.group(1), match.group(2)
    return "", line


def body_start_line(raw_text, body_text):
    """
    Line number (1-indexed) where `body_text` begins within `raw_text`, so
    line numbers can be reported relative to the whole source file
    (frontmatter included) rather than just the body.
    """
    index = raw_text.rfind(body_text)
    return raw_text[:index].count("\n") + 1


def annotate_line(line, line_no):
    """
    Prefix a single markdown source line with a `<span class="ln">` marker
    carrying its source line number, placed after any leading block marker
    so mistune still recognizes the heading/list/blockquote syntax. Blank
    lines, and lines with no line number to show, pass through unchanged.
    """
    text = line.rstrip("\n")
    if not text.strip() or line_no is None:
        return line
    trailing_newline = "\n" if line.endswith("\n") else ""
    marker, rest = split_marker(text)
    return f'{marker}<span class="ln">{line_no}</span>{rest}{trailing_newline}'


def annotate_body(body_text, start=1):
    """
    Annotate every non-blank line of a markdown body with its source line
    number, counting from `start`.
    """
    lines = body_text.splitlines(keepends=True)
    return "".join(annotate_line(line, start + i) for i, line in enumerate(lines))
