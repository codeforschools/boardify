"""Organization settings, read from [tool.boardify] in pyproject.toml in the working directory."""
import tomllib
from pathlib import Path

DEFAULTS = {
    "policies_root": "content/policies",  # where <section>/<code>-<slug>/ folders live
    "pdf_prefix": "pdfs",  # S3 key prefix (the bucket and credentials come from AWS_S3_* env vars)
    "output_dir": "output",
    "logo_url": "",  # shown on generated PDFs
}


def load(path="pyproject.toml"):
    config = dict(DEFAULTS)
    p = Path(path)
    if p.exists():
        config.update(tomllib.loads(p.read_text()).get("tool", {}).get("boardify", {}))
    return config
