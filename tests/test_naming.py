from boardify.naming import pdf_name, slugify_title


def test_slug_matches_site_rule():
    assert slugify_title("Student Records (Access), Privacy") == "student-records-access-privacy"


def test_pdf_name_uses_code_kind_and_title():
    meta = {"code": "0100-01", "kind": "Regulation", "title": "Mission Statement"}
    assert pdf_name(meta) == "0100-01-regulation-mission-statement"


def test_title_safety():
    from boardify.naming import title_is_safe

    assert title_is_safe("Repairs – General (and) Emergency, Plus")
    assert not title_is_safe("Q&A")
    assert not title_is_safe("Either/Or")
