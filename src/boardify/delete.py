from .naming import meta_from_revision, pdf_name
from .s3 import delete_file


def main(filepaths, cfg, base):
    for filepath in filepaths:
        name = pdf_name(meta_from_revision(base, filepath))
        delete_file(f"{cfg['pdf_prefix']}/{name}.pdf")
    return 0
