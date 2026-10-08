import json

from .render import add_brand, get_env, write_pdf


def build_redline_pdf(context, cfg):
    context = add_brand(context, cfg)
    output = get_env(cfg).get_template("diff.j2").render(context=context)
    write_pdf(output, f"{cfg['output_dir']}/{context['filename']}_redline.pdf", cfg)


def main(json_path, cfg):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    files = data["added_files"] + data["removed_files"] + data["modified_files"]
    for context in files:
        build_redline_pdf(context, cfg)
    return 0
