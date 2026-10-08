from boardify.line_numbers import annotate_body, body_start_line, split_marker


def test_split_marker_keeps_block_syntax():
    assert split_marker("- item") == ("- ", "item")
    assert split_marker("## Heading") == ("## ", "Heading")
    assert split_marker("plain") == ("", "plain")


def test_body_start_line_counts_frontmatter():
    raw = "---\ntitle: X\n---\n\nbody\n"
    assert body_start_line(raw, "\nbody\n") == 4


def test_annotate_skips_blank_lines():
    out = annotate_body("one\n\ntwo\n", start=5)
    assert out == '<span class="ln">5</span>one\n\n<span class="ln">7</span>two\n'
