from pathlib import Path

import boardify_theme
from boardify.naming import slugify_title


def test_theme_slug_rule_matches_naming():
    """main.html repeats the slug rule in Jinja; render its chain in Python and compare."""
    from jinja2 import Environment

    template = (Path(boardify_theme.__file__).parent / "main.html").read_text()
    start = template.index("page.meta.title | lower")
    chain = template[start : template.index("}}", start)]
    title = "Student Records (Access), Privacy and More"
    rendered = Environment().from_string("{{ " + chain + " }}").render(page={"meta": {"title": title}})
    assert rendered == slugify_title(title)
