import json

from jinja2 import Environment, PackageLoader
from weasyprint import HTML as weasy_html


def get_env():
    """
    Set up the Jinja environment for local use
    """
    env = Environment(
        loader=PackageLoader("boardify", "templates"),
    )
    return env


def get_template():
    env = get_env()
    return env.get_template("diff.j2")


def render_template(context):
    """
    Render one changed file's context into the redline template, returning HTML
    """
    template = get_template()
    output = template.render(
        context=context,
    )
    return output


def build_redline_pdf(context, cfg):
    context = {**context, "logo_url": cfg["logo_url"]}
    output = render_template(context)
    outfile = f"{cfg['output_dir']}/{context['filename']}_redline.pdf"
    weasy_obj = weasy_html(
        string=output,
    )
    weasy_obj.write_pdf(outfile)
    return


def main(json_path, cfg):
    with open(json_path) as f:
        data = json.load(f)

    files = data["added_files"] + data["removed_files"] + data["modified_files"]
    for context in files:
        build_redline_pdf(context, cfg)
    return

