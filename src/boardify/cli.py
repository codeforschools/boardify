import argparse
import sys

from . import check, cms, config, delete, diff, pdf, redline


def parse_paths(values):
    """Paths as separate arguments, or one argument split on commas or newlines; blanks dropped."""
    return [p.strip() for v in values for p in v.replace("\n", ",").split(",") if p.strip()]


def main(argv=None):
    parser = argparse.ArgumentParser(prog="boardify")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("check", help="validate the policies folder structure and frontmatter")

    p = sub.add_parser("pdf", help="build PDFs for the given policy files")
    p.add_argument("paths", nargs="*", help="files, space-, comma- or newline-separated")
    p.add_argument("--upload", action="store_true", help="upload to S3 (AWS_S3_* env vars)")

    p = sub.add_parser("delete-pdf", help="delete the S3 PDFs for the given removed files")
    p.add_argument("paths", nargs="*", help="files, space-, comma- or newline-separated")
    p.add_argument("--base", required=True, help="git revision the files still existed at")

    p = sub.add_parser("diff", help="convert output/diff.diff to output/diff.json")
    p.add_argument("--diff-file", default=None)

    p = sub.add_parser("redline", help="build redline PDFs from output/diff.json")
    p.add_argument("--json", default=None)

    p = sub.add_parser("cms-config", help="generate the Sveltia CMS config from the content folders")
    p.add_argument("--check", action="store_true", help="fail if the generated files are out of date")

    args = parser.parse_args(argv)
    cfg = config.load()
    if args.command == "check":
        return check.main(cfg)
    if args.command == "cms-config":
        return cms.main(cfg, check=args.check)
    if args.command == "pdf":
        return pdf.main(parse_paths(args.paths), cfg, upload=args.upload)
    if args.command == "delete-pdf":
        return delete.main(parse_paths(args.paths), cfg, base=args.base)
    if args.command == "diff":
        return diff.save_json(args.diff_file or f"{cfg['output_dir']}/diff.diff", cfg)
    if args.command == "redline":
        return redline.main(args.json or f"{cfg['output_dir']}/diff.json", cfg)


if __name__ == "__main__":
    sys.exit(main())
