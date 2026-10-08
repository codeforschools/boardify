# Contributing

```bash
uv sync
uv run ruff check .
uv run pytest
```

WeasyPrint needs Pango at runtime (`brew install pango` on macOS, `libpango-1.0-0 libpangoft2-1.0-0` on Debian/Ubuntu).

- The content contract (`docs/content-contract.md`) and PDF naming are public interfaces. Change them deliberately,
  update `check.py`, the theme and the docs together, and note it in `CHANGELOG.md`.
- `src/boardify_theme/partials/{nav,nav-item,copyright}.html` are copies of Zensical's with marked edits;
  re-sync them when upgrading Zensical.
- Add a test with each behavior change; CI runs ruff and pytest on Python 3.11–3.14.
