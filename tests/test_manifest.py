from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(rel):
    with open(str(ROOT / rel), encoding="utf-8") as fh:
        return json.load(fh)


class ManifestTests(unittest.TestCase):
    def test_plugin_manifest(self):
        plugin = load(".claude-plugin/plugin.json")
        self.assertEqual(plugin["name"], "prred")
        self.assertEqual(plugin["license"], "MIT")

    def test_marketplace_manifest(self):
        market = load(".claude-plugin/marketplace.json")
        self.assertEqual(market["plugins"][0]["source"], "./")
        self.assertEqual(market["name"], "prred")
        self.assertEqual(market["plugins"][0]["name"], "prred")

    def test_skill_names_match_folders(self):
        for skill in (ROOT / "skills").glob("*/SKILL.md"):
            text = skill.read_text(encoding="utf-8")
            m = re.match(r"---\r?\n(.*?)\r?\n---", text, re.S)
            self.assertIsNotNone(m, skill)
            name = re.search(r"^name:\s*(\S+)\s*$", m.group(1), re.M)
            self.assertIsNotNone(name, skill)
            self.assertEqual(name.group(1), skill.parent.name)


if __name__ == "__main__":
    unittest.main()
