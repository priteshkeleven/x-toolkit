"""parse_markdown.py output is pasted straight into X's editor.

An unescaped '<' swallows text, a numbered list that comes back as bullets
changes the meaning of "step 3", and an image silently swapped for a same-named
file from Downloads uploads something the user never chose. Offline.
"""
from __future__ import annotations

import importlib.util
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "x-article" / "scripts" / "parse_markdown.py"

spec = importlib.util.spec_from_file_location("parse_markdown", SCRIPT)
parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser)

ARTICLE = """---
title: frontmatter is skipped
---
# Why deploys take 6 minutes

![cover](cover.png)

Costs < $50 & falling. See [the repo](https://github.com/x/y?a=1&b=2).

## Steps

1. Cache the base layer
2. Skip the *full* rebuild

- bullet

---

```
docker build --cache-from <image>
```

![missing](nope.png)
"""


class ParseArticle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        root = pathlib.Path(cls.tmp.name)
        (root / "cover.png").write_bytes(b"png")
        (root / "article.md").write_text(ARTICLE, encoding="utf-8")
        cls.result = parser.parse_markdown_file(str(root / "article.md"))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_title_from_h1_and_removed_from_body(self):
        self.assertEqual(self.result["title"], "Why deploys take 6 minutes")
        self.assertNotIn("Why deploys", self.result["html"])

    def test_text_is_escaped_once(self):
        html = self.result["html"]
        self.assertIn("Costs &lt; $50 &amp; falling", html)
        self.assertIn('href="https://github.com/x/y?a=1&amp;b=2"', html)
        self.assertNotIn("&amp;amp;", html)

    def test_ordered_lists_stay_ordered(self):
        self.assertIn("<ol><li>Cache the base layer</li><li>Skip the <em>full</em> rebuild</li></ol>", self.result["html"])
        self.assertIn("<ul><li>bullet</li></ul>", self.result["html"])

    def test_code_becomes_an_escaped_blockquote(self):
        self.assertIn("<blockquote>docker build --cache-from &lt;image&gt;</blockquote>", self.result["html"])

    def test_cover_and_dividers(self):
        self.assertTrue(self.result["cover_exists"])
        self.assertEqual(len(self.result["dividers"]), 1)
        self.assertNotIn("<hr", self.result["html"])

    def test_a_missing_image_is_reported_not_substituted(self):
        missing = self.result["content_images"][0]
        self.assertFalse(missing["exists"])
        self.assertTrue(missing["path"].endswith("nope.png"))
        self.assertEqual(self.result["missing_images"], 1)

    def test_the_script_never_searches_personal_folders(self):
        source = SCRIPT.read_text(encoding="utf-8")
        for folder in ('"Downloads"', '"Desktop"', '"Pictures"'):
            self.assertNotIn(folder, source)

    def test_paths_outside_the_article_folder_are_rejected(self):
        """A Markdown file can come from anyone; its image paths get uploaded."""
        root = pathlib.Path(self.tmp.name)
        (root / "notes.txt").write_text("secret", encoding="utf-8")
        outside = pathlib.Path(self.tmp.name).parent / "outside.png"
        for src, reason in (("/etc/passwd", "absolute"),
                            ("../outside.png", "outside"),
                            ("notes.txt", "not an image")):
            path, usable, problem = parser.resolve_image(src, root)
            self.assertFalse(usable, src)
            self.assertIn(reason, problem, src)
        self.assertFalse(outside.exists())

    def test_an_image_inside_the_folder_is_usable(self):
        path, usable, problem = parser.resolve_image("cover.png", pathlib.Path(self.tmp.name))
        self.assertTrue(usable)
        self.assertEqual(problem, "")

    def test_after_text_hides_internal_markers(self):
        self.assertNotIn("___CODE_BLOCK", self.result["content_images"][0]["after_text"])


if __name__ == "__main__":
    unittest.main()
