import pytest
import yaml

from boardify import cms, config


def page(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


@pytest.fixture
def site(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    page(tmp_path / "content" / "index.md", "---\ntitle: Home\n---\n")
    page(tmp_path / "content/policies/0100-mission/index.md", '---\ntitle: Mission\ncode: "0100"\n---\n')
    page(tmp_path / "content/policies/0100-mission/0100-01-x/index.md", "---\ncode: 0100-01\n---\n")
    page(tmp_path / "content/policies/0400-hr/index.md", '---\ntitle: Human Resources\ncode: "0400"\n---\n')
    page(tmp_path / "content/policies/0400-hr/0400-01-y/index.md", "---\ncode: 0400-01\n---\n")
    page(tmp_path / "content/policies/0400-hr/0400-01-y/regulation.md", "---\ncode: 0400-01\n---\n")
    cfg = config.load()
    cfg["cms"].update(repo="o/r", base_url="https://oauth.example", sveltia_version="1.2.3")
    return cfg


def test_collections_follow_the_folder_tree(site):
    data = yaml.safe_load(cms.build_config(site))
    assert [s["name"] for s in data["singletons"]] == ["home", "mission_page", "hr_page"]
    assert [c["name"] for c in data["collections"]] == [
        "mission_policies", "hr_policies", "hr_regulations",
    ]
    reg = data["collections"][2]
    assert reg["path"] == "{{code}}-{{title}}/regulation"
    assert reg["filter"] == {"field": "kind", "value": "Regulation"}


def test_index_pins_the_script_version(site):
    site["cms"]["sveltia_integrity"] = "sha384-abc"
    html = cms.build_index(site)
    assert "@sveltia/cms@1.2.3/dist" in html and 'integrity="sha384-abc"' in html


def test_unpinned_version_is_refused(site):
    site["cms"]["sveltia_version"] = ""
    with pytest.raises(SystemExit):
        cms.build_index(site)


def test_check_detects_stale_files(site, capsys):
    assert cms.main(site, check=True) == 1
    assert cms.main(site) == 0
    assert cms.main(site, check=True) == 0
