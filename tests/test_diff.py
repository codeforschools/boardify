from boardify.diff import build_redline_body, word_diff


def test_word_diff_marks_only_changed_words():
    out = word_diff("the quick fox\n", "the slow fox\n")
    assert "<del>quick</del>" in out and "<ins>slow</ins>" in out
    assert out.startswith("the ")


def test_redline_numbers_against_new_document():
    out = build_redline_body("a\nb\n", "a\nc\n", new_start=10)
    assert '<span class="ln">10</span>a' in out
    assert "<del>b</del>" in out and "<ins>c</ins>" in out


def _tables(old, new):
    import mistune

    from boardify.diff import build_redline_body

    return mistune.html(build_redline_body(old, new))


def test_redline_changed_table_cell_stays_a_table():
    old = "| a | b |\n|---|---|\n| 1 | 2 |\n"
    new = "| a | b |\n|---|---|\n| 1 | 3 |\n"
    html = _tables(old, new)
    assert "<table>" in html
    assert "<del>2</del>" in html and "<ins>3</ins>" in html


def test_redline_added_and_removed_rows_stay_in_table():
    base = "| a | b |\n|---|---|\n| 1 | 2 |\n"
    added = _tables(base, base + "| 3 | 4 |\n")
    assert "<table>" in added and "<ins>3</ins>" in added
    removed = _tables(base + "| 3 | 4 |\n", base)
    assert "<table>" in removed and "<del>3</del>" in removed
    assert removed.count("<tr>") == 3


def test_redline_whole_table_added_or_removed():
    table = "| a | b |\n|---|---|\n| 1 | 2 |\n"
    assert "<table>" in _tables("", table)
    assert "<table>" in _tables(table, "")
