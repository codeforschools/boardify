from boardify.diff import build_redline_body, word_diff


def test_word_diff_marks_only_changed_words():
    out = word_diff("the quick fox\n", "the slow fox\n")
    assert "<del>quick</del>" in out and "<ins>slow</ins>" in out
    assert out.startswith("the ")


def test_redline_numbers_against_new_document():
    out = build_redline_body("a\nb\n", "a\nc\n", new_start=10)
    assert '<span class="ln">10</span>a' in out
    assert "<del>b</del>" in out and "<ins>c</ins>" in out
