
import pytest

from boardify import check
from boardify.cli import parse_paths


def write(path, **meta):
    path.parent.mkdir(parents=True, exist_ok=True)
    front = "".join(f"{k}: {v}\n" for k, v in meta.items())
    path.write_text(f"---\n{front}---\n\nbody\n")


@pytest.fixture
def root(tmp_path):
    write(tmp_path / "0100-mission" / "index.md", title="Mission", code='"0100"')
    folder = tmp_path / "0100-mission" / "0100-01-mission"
    write(folder / "index.md", code="0100-01", title="Mission", kind="Policy", updated="2026-01-01")
    return tmp_path


def run(root, capsys):
    status = check.main({"policies_root": str(root)})
    return status, capsys.readouterr().out


def test_valid_tree_passes(root, capsys):
    status, out = run(root, capsys)
    assert status == 0 and "0 errors, 0 warnings" in out


def test_unquoted_section_code_is_an_error(root, capsys):
    write(root / "0100-mission" / "index.md", title="Mission", code="100")
    status, out = run(root, capsys)
    assert status == 1 and "section code must be the quoted string" in out


def test_unsafe_title_is_an_error(root, capsys):
    folder = root / "0100-mission" / "0100-01-mission"
    write(folder / "index.md", code="0100-01", title='"Q&A"', kind="Policy", updated="x")
    status, out = run(root, capsys)
    assert status == 1 and "unsafe" in out


def test_regulation_needs_matching_kind_and_code(root, capsys):
    folder = root / "0100-mission" / "0100-01-mission"
    write(folder / "regulation.md", code="0100-02", title="Mission", kind="Policy")
    status, out = run(root, capsys)
    assert status == 1 and "!= folder" in out and "!= Regulation" in out


def test_unknown_reference_warns_but_school_year_does_not(root, capsys):
    folder = root / "0100-mission" / "0100-01-mission"
    (folder / "index.md").write_text(
        "---\ncode: 0100-01\ntitle: Mission\nkind: Policy\nupdated: x\n---\nSee 0999-01 and 2017-18.\n"
    )
    status, out = run(root, capsys)
    assert status == 0 and "unknown code 0999-01" in out and "2017-18" not in out


def test_malformed_frontmatter_is_reported_not_raised(root, capsys):
    folder = root / "0100-mission" / "0100-01-mission"
    (folder / "index.md").write_text("---\ncode: [unclosed\n---\n")
    status, out = run(root, capsys)
    assert status == 1 and "unreadable frontmatter" in out


def test_parse_paths():
    assert parse_paths(["a.md,b.md"]) == ["a.md", "b.md"]
    assert parse_paths(["a.md", "b.md\nc.md"]) == ["a.md", "b.md", "c.md"]
    assert parse_paths([""]) == []
