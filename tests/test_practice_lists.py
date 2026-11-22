"""Where the repository, outside the skill-best-practices plugin, counts its practices.

These checks live here and not in the plugin's own tests, because an installed copy of the
plugin has no README.md, root CLAUDE.md or marketplace.json next to it.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "skill-best-practices"


# spec-example: skill-writing-reminder / the repository's files count nine practices
def test_repository_files_count_nine_practices() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Nine evidence-based practices" in readme
    assert "| The vocabulary problem | Furnas, Landauer, Gomez, & Dumais (1987) |" in readme

    claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    assert "全部 9 個 practice" in claude
    assert "九個 practice" in claude
    assert "8 個 practice" not in claude and "八個 practice" not in claude

    marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    entry = next(p for p in marketplace["plugins"] if p["name"] == "skill-best-practices")
    assert "9 practices" in entry["description"]
    manifest = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert entry["version"] == manifest["version"]
