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


def test_since_label_and_suffix_flow_through_to_the_redline_pdf(tmp_path, monkeypatch):
    import json
    import subprocess
    from pathlib import Path

    from boardify import config, diff, redline

    def git(*args):
        return subprocess.run(["git", *args], cwd=tmp_path, check=True, capture_output=True, text=True).stdout

    git("init", "-q")
    git("config", "user.email", "t@example.com")
    git("config", "user.name", "t")
    page = tmp_path / "index.md"
    page.write_text("---\ncode: 0100-01\ntitle: Mission\nkind: Policy\n---\n\nthe quick fox\n")
    git("add", ".")
    git("commit", "-qm", "one")
    before = git("rev-parse", "HEAD").strip()
    page.write_text(page.read_text().replace("quick", "slow"))
    git("commit", "-qam", "two")

    cfg = {**config.DEFAULTS, "output_dir": str(tmp_path / "out")}
    (tmp_path / "out").mkdir()
    (tmp_path / "out" / "diff.diff").write_text(git("diff", "--no-renames", before, "HEAD", "--", "index.md"))
    monkeypatch.chdir(tmp_path)

    json_path = str(tmp_path / "out" / "since.json")
    diff.save_json(str(tmp_path / "out" / "diff.diff"), cfg, json_path=json_path, since="Changes since 2026-11-16")
    data = json.loads(Path(json_path).read_text())
    assert data["modified_files"][0]["since"] == "Changes since 2026-11-16"
    assert "<del>quick</del>" in data["modified_files"][0]["redline_html"]

    redline.main(json_path, cfg, suffix="_since-meeting")
    assert (tmp_path / "out" / "0100-01-policy-mission_redline_since-meeting.pdf").exists()
