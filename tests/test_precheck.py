"""precheck.py has to say what X's ranking code says, and only that.

The skills tell the agent to fix every FAIL it reports, so a FAIL on something
the code does not penalise (a plain link) would teach the agent a rule that is
not there, and a missed duplicate would let a reply through that the code labels
spam. Offline, standard library only.
"""
from __future__ import annotations

import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "x-humanizer" / "scripts" / "precheck.py"

spec = importlib.util.spec_from_file_location("precheck", SCRIPT)
precheck = importlib.util.module_from_spec(spec)
spec.loader.exec_module(precheck)


def levels(report, rule=None):
    return [i["level"] for u in report["units"] for i in u["issues"] if rule is None or i["rule"] == rule]


class WeightedLength(unittest.TestCase):
    """twitter-text v3: Latin 1, CJK 2, emoji sequence 2, URL 23."""

    def test_latin_counts_one(self):
        self.assertEqual(precheck.weighted_length("hello"), 5)

    def test_accents_count_one(self):
        self.assertEqual(precheck.weighted_length("café"), 4)

    def test_cjk_counts_two(self):
        self.assertEqual(precheck.weighted_length("日本語"), 6)

    def test_an_emoji_sequence_counts_two(self):
        for emoji in ("\U0001F44D", "\U0001F44D\U0001F3FD", "\U0001F468‍\U0001F469‍\U0001F467", "\U0001F1FA\U0001F1F8"):
            self.assertEqual(precheck.weighted_length(emoji), 2, repr(emoji))

    def test_any_url_counts_twenty_three(self):
        self.assertEqual(precheck.weighted_length("https://example.com/a/very/long/path/indeed"), 23)
        self.assertEqual(precheck.weighted_length("see example.com"), 4 + 23)

    def test_over_280_fails_on_standard_but_not_premium(self):
        text = "a" * 281
        self.assertEqual(precheck.run(text)["verdict"], "FAIL")
        self.assertEqual(precheck.run(text, premium=True)["verdict"], "PASS")


class RulesFromTheCode(unittest.TestCase):
    def test_a_plain_link_is_not_a_failure(self):
        """Opening a link is weighted +0.2. The code has no link penalty."""
        report = precheck.run("We cut deploys to 6 minutes. Write-up: https://example.com/deploys")
        self.assertEqual(report["verdict"], "PASS")
        self.assertNotIn("FAIL", levels(report))
        self.assertIn("INFO", levels(report, "links"))

    def test_a_shortener_fails(self):
        report = precheck.run("Write-up here https://bit.ly/x1")
        self.assertIn("FAIL", levels(report, "SPAM_HIGH_RECALL"))

    def test_link_plus_mentions_warns(self):
        report = precheck.run("cc @alice https://example.com/post")
        self.assertIn("WARN", levels(report, "SPAM_HIGH_RECALL"))

    def test_near_duplicate_of_history_fails(self):
        earlier = "we hit this exact retry issue last quarter and fixed it with exponential backoff"
        report = precheck.run("we hit this exact retry issue last quarter and fixed it with backoff", history=[earlier])
        self.assertIn("FAIL", levels(report, "COPYPASTA_SPAM"))

    def test_different_text_is_not_a_duplicate(self):
        earlier = "we hit this exact retry issue last quarter and fixed it with exponential backoff"
        report = precheck.run("our deploys went from 40 minutes to 6 after caching the base image", history=[earlier])
        self.assertNotIn("FAIL", levels(report))

    def test_replies_are_checked_against_each_other(self):
        a = "great point, we hit this exact retry issue last quarter and fixed it with backoff"
        b = "great point, we hit this exact retry issue last quarter and fixed it with jitter"
        report = precheck.run_replies([a, b], False, [])
        self.assertEqual(report["verdict"], "FAIL")

    def test_bait_hashtags_and_emoji_warn_but_do_not_fail(self):
        """None of these is a published ranking rule, so they are warnings."""
        report = precheck.run("RT if you agree #a #b \U0001F680\U0001F525")
        self.assertEqual(report["verdict"], "PASS")
        for rule in ("bait", "hashtags", "emoji"):
            self.assertIn("WARN", levels(report, rule))

    def test_a_thread_is_split_and_explained(self):
        report = precheck.run("tweet one\n---\ntweet two\n---\ntweet three", kind="thread")
        self.assertEqual(len(report["units"]), 3)
        self.assertTrue(any("non-followers" in n for n in report["notes"]))

    def test_every_rule_name_is_documented(self):
        """A FAIL the agent cannot look up is a rule it cannot explain."""
        signals = (ROOT / "references" / "x-ranking-signals.md").read_text(encoding="utf-8")
        for rule in ("COPYPASTA_SPAM", "SPAM_HIGH_RECALL"):
            self.assertIn(rule, signals)


if __name__ == "__main__":
    unittest.main()
