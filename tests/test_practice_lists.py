"""Where the repository, outside the skill-best-practices plugin, counts its practices.

These checks live here and not in the plugin's own tests, because an installed copy of the
plugin has no README.md, root CLAUDE.md or marketplace.json next to it.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "skill-best-practices"


def table_line_below_table_line(lines, row_start):
    matches = [i for i, line in enumerate(lines) if line.startswith(row_start)]
    return len(matches) == 1 and matches[0] > 0 and lines[matches[0] - 1].startswith("|")


# spec-example: skill-writing-reminder / the repository's files count nine practices
def test_repository_files_count_nine_practices() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Nine evidence-based practices" in readme
    assert table_line_below_table_line(
        readme.splitlines(), "| The vocabulary problem | Furnas, Landauer, Gomez, & Dumais (1987) |")

    claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    numeric = re.findall(r"(\d+) ?個 practice", claude)
    chinese = re.findall(r"([一二三四五六七八九十]+)個 practice", claude)
    assert numeric and all(n == "9" for n in numeric), numeric
    assert chinese and all(n == "九" for n in chinese), chinese

    marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    entry = next(p for p in marketplace["plugins"] if p["name"] == "skill-best-practices")
    assert re.search(r"(?<!\d)9 practices", entry["description"]), entry["description"]
    manifest = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert entry["version"] == manifest["version"]
