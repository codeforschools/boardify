"""Shared PDF rendering: Jinja environment (with optional template overrides), brand CSS, WeasyPrint."""
from pathlib import Path
from urllib.parse import unquote, urlparse

from jinja2 import ChoiceLoader, Environment, FileSystemLoader, PackageLoader
from weasyprint import HTML
from weasyprint.urls import URLFetcher


def get_env(cfg):
    loaders = []
    if cfg.get("templates_dir"):
        loaders.append(FileSystemLoader(cfg["templates_dir"]))
    loaders.append(PackageLoader("boardify", "templates"))
    return Environment(loader=ChoiceLoader(loaders))


def logo_source(cfg):
    """The logo as a URL WeasyPrint can load: https URLs pass through, paths become file URIs."""
    logo = cfg.get("logo_url", "")
    if not logo or urlparse(logo).scheme in ("http", "https", "data"):
        return logo
    return Path(logo).resolve().as_uri()


def brand_css(cfg):
    path = cfg.get("pdf_css")
    return Path(path).read_text() if path else ""


def add_brand(context, cfg):
    return {**context, "logo_url": logo_source(cfg), "extra_css": brand_css(cfg)}


class RestrictedFetcher(URLFetcher):
    """
    Policy text comes from pull requests, so it must not be able to pull local files into a
    PDF (e.g. <img src="file:///etc/passwd">). Local files are limited to the folders of the
    logo and brand stylesheet; remote and data: URLs are allowed.
    """

    def __init__(self, cfg, **kwargs):
        super().__init__(**kwargs)
        self.roots = []
        for key in ("logo_url", "pdf_css"):
            value = cfg.get(key)
            if value and urlparse(value).scheme not in ("http", "https", "data"):
                self.roots.append(Path(value).resolve().parent)

    def fetch(self, url, headers=None):
        parsed = urlparse(url)
        if parsed.scheme == "file":
            target = Path(unquote(parsed.path)).resolve()
            if not any(root == target or root in target.parents for root in self.roots):
                raise ValueError(f"blocked local file: {url}")
        return super().fetch(url, headers)


def write_pdf(html, outfile, cfg):
    Path(outfile).parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html, url_fetcher=RestrictedFetcher(cfg)).write_pdf(outfile)
