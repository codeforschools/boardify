from pathlib import Path

import pytest

from boardify import config, pdf, render, s3


def cfg(tmp_path, **extra):
    return {**config.DEFAULTS, "output_dir": str(tmp_path / "out"), **extra}


def test_builds_pdf_with_brand_css_and_local_logo(tmp_path):
    (tmp_path / "logo.png").write_bytes(
        bytes.fromhex(
            "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
            "0000000d4944415478da63f8ffff3f0005fe02fea7d6a38a0000000049454e44ae426082"
        )
    )
    (tmp_path / "brand.css").write_text(":root { --brand-heading: #123456; }")
    policy = tmp_path / "index.md"
    policy.write_text("---\ncode: 0100-01\ntitle: Mission\nkind: Policy\n---\n\nHello\n")
    settings = cfg(tmp_path, logo_url=str(tmp_path / "logo.png"), pdf_css=str(tmp_path / "brand.css"))
    out = pdf.build_pdf(str(policy), settings)
    assert out.endswith("0100-01-policy-mission.pdf")
    assert Path(out).read_bytes().startswith(b"%PDF-")


def test_section_index_gets_no_pdf(tmp_path):
    page = tmp_path / "index.md"
    page.write_text("---\ntitle: Section\ncode: '0100'\n---\n\nHi\n")
    assert pdf.build_pdf(str(page), cfg(tmp_path)) is None


def test_untrusted_content_cannot_read_local_files(tmp_path):
    fetcher = render.RestrictedFetcher(cfg(tmp_path))
    with pytest.raises(ValueError, match="blocked local file"):
        fetcher.fetch("file:///etc/hosts")


def test_template_directory_overrides_bundled(tmp_path):
    (tmp_path / "policy.html").write_text("custom {{ context.title }}")
    env = render.get_env(cfg(tmp_path, templates_dir=str(tmp_path)))
    assert env.get_template("policy.html").render(context={"title": "T"}) == "custom T"


def test_s3_requires_bucket():
    with pytest.raises(SystemExit):
        s3.get_bucket({})
    assert s3.get_bucket({"pdf_bucket": "example.org"}) == "example.org"


def test_s3_uses_configured_region_and_default_credential_chain(monkeypatch):
    seen = {}
    monkeypatch.setenv("AWS_S3_ACCESS_KEY", "ignored")
    monkeypatch.setenv("AWS_S3_SECRET_KEY", "ignored")
    monkeypatch.setattr(s3.boto3, "client", lambda name, **kw: seen.update(kw))
    s3.get_client({"pdf_region": "us-west-2"})
    assert seen == {"region_name": "us-west-2"}
