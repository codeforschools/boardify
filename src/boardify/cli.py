import argparse
import sys

from . import check, config, delete, diff, pdf, redline


def main(argv=None):
    parser = argparse.ArgumentParser(prog="boardify")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("check", help="validate the policies folder structure and frontmatter")

    p = sub.add_parser("pdf", help="build PDFs for comma-separated policy files")
    p.add_argument("paths")
    p.add_argument("--upload", action="store_true", help="upload to S3 (AWS_S3_* env vars)")

    p = sub.add_parser("delete-pdf", help="delete the S3 PDFs for comma-separated removed files")
    p.add_argument("paths")
    p.add_argument("--base", required=True, help="git revision the files still existed at")

    p = sub.add_parser("diff", help="convert output/diff.diff to output/diff.json")
    p.add_argument("--diff-file", default=None)

    p = sub.add_parser("redline", help="build redline PDFs from output/diff.json")
    p.add_argument("--json", default=None)

    args = parser.parse_args(argv)
    cfg = config.load()
    if args.command == "check":
        return check.main(cfg)
    if args.command == "pdf":
        return pdf.main(args.paths.split(","), cfg, upload=args.upload)
    if args.command == "delete-pdf":
        return delete.main(args.paths.split(","), cfg, base=args.base)
    if args.command == "diff":
        return diff.save_json(args.diff_file or f"{cfg['output_dir']}/diff.diff", cfg)
    if args.command == "redline":
        return redline.main(args.json or f"{cfg['output_dir']}/diff.json", cfg)


if __name__ == "__main__":
    sys.exit(main())
