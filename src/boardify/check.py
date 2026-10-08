"""Consistency check for content/policies/<section>/<code>-<slug>/{index,regulation}.md."""
import re
from pathlib import Path


def frontmatter(path):
    m = re.match(r"---\n(.*?)\n---", path.read_text(), re.DOTALL)
    return dict(re.findall(r"^([A-Za-z_][\w-]*):[ ]*(.*)$", m.group(1), re.MULTILINE)) if m else {}


def main(cfg):
    root = Path(cfg["policies_root"]).resolve()
    errors, warnings = [], []
    for section in sorted(p for p in root.iterdir() if p.is_dir()):
        for item in sorted(section.iterdir()):
            if item.name in ("index.md", ".DS_Store"):
                continue
            if item.is_file():
                errors.append(f"stray flat file: {item.relative_to(root)}")
                continue
            m = re.match(r"(\d{4}-\d{2})-.+", item.name)
            if not m:
                errors.append(f"bad folder name: {item.relative_to(root)}")
                continue
            code = m.group(1)
            files = {p.name for p in item.iterdir() if p.name != ".DS_Store"}
            for extra in files - {"index.md", "regulation.md"}:
                errors.append(f"unexpected file: {item.relative_to(root)}/{extra}")
            if "index.md" not in files:
                errors.append(f"missing index.md: {item.relative_to(root)}")
                continue
            fms = {}
            for name, kind in (("index.md", "Policy"), ("regulation.md", "Regulation")):
                if name not in files:
                    continue
                fm = frontmatter(item / name)
                fms[name] = fm
                if fm.get("code") != code:
                    errors.append(f"code {fm.get('code')!r} != folder {code}: {item.name}/{name}")
                if fm.get("kind") != kind:
                    errors.append(f"kind {fm.get('kind')!r} != {kind}: {item.name}/{name}")
            if len(fms) == 2 and fms["index.md"].get("title") != fms["regulation.md"].get("title"):
                warnings.append(f"titles differ: {item.name}")

    for w in warnings:
        print("warn:", w)
    for e in errors:
        print("error:", e)
    print(f"{len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0
