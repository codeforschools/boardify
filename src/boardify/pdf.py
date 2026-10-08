import frontmatter
from mistune import html as markdown_html

from .line_numbers import annotate_body, body_start_line
from .naming import pdf_name
from .render import add_brand, get_env, write_pdf
from .s3 import upload_file

REQUIRED = {"code", "kind", "title"}


def get_context(filepath, cfg):
    """
    Template context from a file's frontmatter, with line numbers annotated into the body
    """
    with open(filepath, encoding="utf-8") as f:
        raw = f.read()
    data = frontmatter.loads(raw)
    context = data.to_dict()

    start = body_start_line(raw, data.content)
    context["content"] = annotate_body(data.content, start)
    if REQUIRED <= set(data.metadata):
        context["filename"] = pdf_name(data.metadata)
    return add_brand(context, cfg)


def build_pdf(filepath, cfg, upload=False):
    context = get_context(filepath, cfg)
    # Section index pages have no code/kind and get no PDF
    if not REQUIRED <= set(context):
        return None

    context["content"] = markdown_html(context["content"])
    output = get_env(cfg).get_template("policy.html").render(context=context)

    outfile = f"{cfg['output_dir']}/{context['filename']}.pdf"
    write_pdf(output, outfile, cfg)

    if upload:
        upload_file(outfile, key=f"{cfg['pdf_prefix']}/{context['filename']}.pdf")
    return outfile


def main(filepaths, cfg, upload=False):
    for filepath in filepaths:
        build_pdf(filepath, cfg, upload=upload)
    return 0
