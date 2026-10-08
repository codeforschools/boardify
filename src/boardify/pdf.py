import os

import frontmatter
from jinja2 import Environment, PackageLoader
from mistune import html as markdown_html
from weasyprint import HTML as weasy_html

from .line_numbers import annotate_body, body_start_line
from .naming import pdf_name
from .s3 import upload_file


def get_env():
    """
    Set up the Jinja environment for local use
    """
    env = Environment(
        loader=PackageLoader("boardify", "templates"),
    )
    return env


def get_template(template):
    """
    Get the template using the Jinja template loader
    """
    env = get_env()
    template = env.get_template(template)
    return template


def get_html(content):
    """
    Get the rendered HTML from the Markdown content specifically
    """
    output = markdown_html(content)
    return output


def get_context(filepath, cfg):
    """
    Get the context using frontmatter parser
    """
    with open(filepath) as f:
        raw = f.read()
    data = frontmatter.loads(raw)
    context = data.to_dict()

    start = body_start_line(raw, data.content)
    context["content"] = annotate_body(data.content, start)
    context["category"] = "Policy"
    if {"code", "kind", "title"} <= set(data.metadata):
        context["filename"] = pdf_name(data.metadata)
    context["logo_url"] = cfg["logo_url"]
    return context


def render_template(template, context):
    """
    Render the context into the policy template, returning HTML
    """
    template = get_template(
        template,
    )
    output = template.render(
        context=context,
    )
    return output


def build_pdf(filepath, cfg, upload=False):

    TEMPLATE_MAP = {
        "Policy": "policy.html",
    }

    # Get context; section index pages have no code/kind and get no PDF
    context = get_context(filepath, cfg)
    if not {"code", "kind", "title"} <= set(context):
        return

    # Convert markdown content to HTML
    try:
        context["content"] = get_html(context["content"])
    except TypeError:
        return

    # Get template based on category
    template = TEMPLATE_MAP.get(context["category"])

    # Select template based on context
    output = render_template(
        template=template,
        context=context,
    )

    filename = context["filename"]

    # Dump HTML for debugging
    # with open(f'output/{filename}.html', 'w') as f:
    #     f.write(output)

    # Create file
    os.makedirs(cfg["output_dir"], exist_ok=True)
    outfile = f"{cfg['output_dir']}/{filename}.pdf"

    weasy_obj = weasy_html(
        string=output,
    )
    weasy_obj.write_pdf(outfile)

    if upload:
        upload_file(outfile, key=f"{cfg['pdf_prefix']}/{filename}.pdf")
    return


def main(filepaths, cfg, upload=False):
    for filepath in filepaths:
        build_pdf(filepath, cfg, upload=upload)
