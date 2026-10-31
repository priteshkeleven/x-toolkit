#!/usr/bin/env python3
"""
precheck.py - check an X draft against the parts of X's ranking code a script can see.

Every check names the rule it comes from (references/x-ranking-signals.md):

  FAIL  over the weighted length limit (X counts emoji and CJK as 2, URLs as 23)
  FAIL  near-duplicate of a recent post or reply      -> COPYPASTA_SPAM / DUPLICATE_CONTENT
  FAIL  link through a URL shortener or redirect      -> SPAM_HIGH_RECALL redirect-chain rule
  WARN  a link together with @mentions                -> same rule, when they do not follow you
  WARN  3+ @mentions, 2+ hashtags, 2+ emoji, bait phrases, em dashes over the cap
  INFO  link in the distributed part, thread / reply reach facts

Weighted length follows twitter-text's v3 rules (code points 0-4351 and a few
punctuation ranges weigh 1, everything else 2; a URL is 23; an emoji sequence
is 2). Complex emoji sequences are approximated.

Standard library only. Nothing leaves the machine.

Usage
  python3 precheck.py draft.txt
  python3 precheck.py thread.txt --thread            # tweets split on lines of ---
  python3 precheck.py reply.txt --reply --history my_recent_replies.txt
  python3 precheck.py post.txt --premium --json
"""

import argparse
import json
import re
import sys
import unicodedata

LIMIT_STANDARD = 280
LIMIT_PREMIUM = 25_000
URL_WEIGHT = 23
DUPLICATE_THRESHOLD = 0.7   # share of 3-word phrases in common; one changed word stays above it

WEIGHT_1_RANGES = ((0, 4351), (8192, 8205), (8208, 8223), (8242, 8247))

URL_RE = re.compile(
    r"https?://[^\s<>\"']+|www\.[^\s<>\"']+"
    r"|\b[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:com|io|ai|dev|co|org|net|app|so|xyz|me|gg|ly|sh|to|tv)\b(?:/[^\s<>\"']*)?",
    re.IGNORECASE,
)
MENTION_RE = re.compile(r"(?<![\w@])@\w{1,15}\b")
HASHTAG_RE = re.compile(r"(?<![\w#])#[^\s#.,!?;:]+")
SHORTENERS = {
    "bit.ly", "tinyurl.com", "ow.ly", "buff.ly", "lnkd.in", "goo.gl", "rebrand.ly", "is.gd",
    "cutt.ly", "shorturl.at", "rb.gy", "tiny.cc", "s.id", "t.ly", "bl.ink", "short.io",
    "trib.al", "dlvr.it", "ift.tt", "shorturl.com", "v.gd", "qr.ae",
}
BAIT_RE = re.compile(
    r"\b(?:rt|retweet|repost|like) if\b|\breply (?:yes|no|with (?:a|an) [\w ]{1,12} emoji)\b"
    r"|\bfollow for follow\b|\bf4f\b|\bfollow back\b|\btag (?:someone|a friend)\b"
    r"|\bcomment [\"'“]?\w+[\"'”]? (?:below )?(?:and|&) i'?ll (?:dm|send)\b"
    r"|\brepost to help\b|\bdrop a [\"'“]?\w+[\"'”]? below\b|\bwho else\b\??$",
    re.IGNORECASE | re.MULTILINE,
)
WORD_RE = re.compile(r"[a-z0-9']+")


def _is_emoji_start(cp: int) -> bool:
    return (0x1F000 <= cp <= 0x1FAFF or 0x2600 <= cp <= 0x27BF or 0x2B00 <= cp <= 0x2BFF
            or cp in (0x203C, 0x2049, 0x2122, 0x2139, 0x231A, 0x231B, 0x2328, 0x23CF)
            or 0x23E9 <= cp <= 0x23FA)


def _emoji_cluster_end(text: str, i: int) -> int:
    """Index after the emoji sequence starting at i (ZWJ, VS16, skin tones, flags, keycaps)."""
    n = len(text)
    first = ord(text[i])
    i += 1
    if 0x1F1E6 <= first <= 0x1F1FF and i < n and 0x1F1E6 <= ord(text[i]) <= 0x1F1FF:
        return i + 1                                   # regional-indicator flag pair
    while i < n:
        cp = ord(text[i])
        if cp == 0xFE0F or 0x1F3FB <= cp <= 0x1F3FF or cp == 0x20E3 or 0xE0020 <= cp <= 0xE007F:
            i += 1
        elif cp == 0x200D and i + 1 < n:
            i += 2                                     # ZWJ plus the next code point
        else:
            break
    return i


def weighted_length(text: str) -> int:
    """X's weighted character count for one post."""
    text = unicodedata.normalize("NFC", text)
    total, last = 0, 0
    pieces = []
    for m in URL_RE.finditer(text):
        pieces.append(text[last:m.start()])
        total += URL_WEIGHT
        last = m.end()
    pieces.append(text[last:])
    for piece in pieces:
        i = 0
        while i < len(piece):
            cp = ord(piece[i])
            if _is_emoji_start(cp):
                i = _emoji_cluster_end(piece, i)
                total += 2
                continue
            total += 1 if any(a <= cp <= b for a, b in WEIGHT_1_RANGES) else 2
            i += 1
    return total


def emoji_count(text: str) -> int:
    count, i = 0, 0
    while i < len(text):
        if _is_emoji_start(ord(text[i])):
            i = _emoji_cluster_end(text, i)
            count += 1
        else:
            i += 1
    return count


def _domain(url: str) -> str:
    host = re.sub(r"^https?://", "", url, flags=re.I).split("/")[0].split("?")[0].lower()
    return host[4:] if host.startswith("www.") else host


def _shingles(text: str) -> set:
    words = WORD_RE.findall(URL_RE.sub(" ", text.lower()))
    return {" ".join(words[i:i + 3]) for i in range(max(0, len(words) - 2))} or set(words)


def similarity(a: str, b: str) -> float:
    sa, sb = _shingles(a), _shingles(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def split_units(text: str) -> list[str]:
    """Split on lines that contain only --- (the bundle's thread separator)."""
    parts = re.split(r"(?m)^\s*---\s*$", text)
    return [p.strip() for p in parts if p.strip()]


def check_unit(text: str, index: int, kind: str, limit: int) -> list[dict]:
    issues = []

    def add(level, rule, msg):
        issues.append({"level": level, "rule": rule, "message": msg})

    length = weighted_length(text)
    if length > limit:
        add("FAIL", "length", f"{length} weighted characters, over the {limit} limit")

    urls = URL_RE.findall(text)
    mentions = MENTION_RE.findall(text)
    for url in urls:
        if _domain(url) in SHORTENERS:
            add("FAIL", "SPAM_HIGH_RECALL",
                f"{_domain(url)} is a shortener; link chains are rated hop by hop, use the real URL")
        if "utm_" in url.lower():
            add("WARN", "link hygiene", "tracking parameters in a link; strip them")
    if urls and mentions:
        add("WARN", "SPAM_HIGH_RECALL",
            f"a link plus {len(mentions)} @mention(s): if they do not follow you and the link is rated "
            "low quality, the post is dropped for everyone but you")
    if len(mentions) >= 3:
        add("WARN", "mentions", f"{len(mentions)} @mentions; mass-mentioning reads as spam")
    tags = HASHTAG_RE.findall(text)
    if len(tags) >= 2:
        add("WARN", "hashtags", f"{len(tags)} hashtags; zero or one, at the end")
    emo = emoji_count(text)
    if emo >= 2:
        add("WARN", "emoji", f"{emo} emoji; zero or one")
    bait = BAIT_RE.findall(text)
    if bait:
        add("WARN", "bait", "engagement-bait phrasing (" + ", ".join(sorted({b.strip() for b in bait})) +
            "); it invites 'not interested' (weight -52.3)")
    words = len(WORD_RE.findall(text.lower()))
    dashes = text.count("—")
    cap = max(1, words // 100)
    if dashes > cap:
        add("WARN", "em dash", f"{dashes} em dashes, cap is {cap} here")
    if urls and index == 0 and kind in ("post", "thread"):
        add("INFO", "links", "link in the part that gets distributed: opening a link is weighted +0.2, "
            "but a reader who leaves does not reply or share; make sure the value is in the post")
    return issues


def run(text: str, kind: str = "post", premium: bool = False, history: list[str] = ()) -> dict:
    units = split_units(text) if kind == "thread" else [text.strip()]
    limit = LIMIT_PREMIUM if premium else LIMIT_STANDARD
    report = {"kind": kind, "limit": limit, "units": [], "notes": []}

    for i, unit in enumerate(units):
        issues = check_unit(unit, i, kind, limit)
        best = max(((similarity(unit, h), h) for h in history), default=(0.0, ""))
        if best[0] >= DUPLICATE_THRESHOLD:
            issues.append({"level": "FAIL", "rule": "COPYPASTA_SPAM",
                           "message": f"{best[0]:.0%} similar to an earlier post: \"{best[1][:60]}...\"; "
                                      "near-identical text is labelled spam and seen posts are not re-shown"})
        report["units"].append({"index": i + 1, "weighted_length": weighted_length(unit), "issues": issues})

    if kind == "thread" and len(units) > 1:
        report["notes"].append("Tweets 2..N are replies: non-followers are only shown tweet 1, followers see "
                               "the rest at x0.75. Tweet 1 has to stand alone.")
        if premium:
            report["notes"].append("On Premium, one long post is one original: no reply discount. Consider it.")
    if kind == "reply":
        report["notes"].append("Replies are not shown to non-followers in For You and reach your followers at "
                               "x0.75. If the point deserves reach, make it a quote post.")
    report["verdict"] = "FAIL" if any(x["level"] == "FAIL" for u in report["units"] for x in u["issues"]) else "PASS"
    return report


def render(report: dict, out=sys.stdout) -> None:
    print(f"\nX PRECHECK  ({report['kind']}, limit {report['limit']})", file=out)
    print("=" * 60, file=out)
    for unit in report["units"]:
        label = f"#{unit['index']}" if len(report["units"]) > 1 else "post"
        print(f"  {label:<6} {unit['weighted_length']:>6} weighted chars", file=out)
        for issue in unit["issues"]:
            print(f"         {issue['level']:<4} [{issue['rule']}] {issue['message']}", file=out)
    for note in report["notes"]:
        print(f"  NOTE   {note}", file=out)
    print("-" * 60, file=out)
    print(f"  {report['verdict']}\n", file=out)


def main() -> None:
    ap = argparse.ArgumentParser(description="Check an X draft against the ranking code's visible rules.")
    ap.add_argument("input", nargs="?", default="-", help="file, or - for stdin")
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--thread", action="store_true", help="split into tweets on lines of ---")
    group.add_argument("--reply", action="store_true", help="the draft is a reply (or several, split on ---)")
    ap.add_argument("--premium", action="store_true", help="25,000-character limit")
    ap.add_argument("--history", help="file of the user's recent posts or replies, split on lines of ---")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.input == "-":
        text = sys.stdin.read()
    else:
        with open(args.input, encoding="utf-8") as fh:
            text = fh.read()
    history = []
    if args.history:
        with open(args.history, encoding="utf-8") as fh:
            history = split_units(fh.read())

    kind = "thread" if args.thread else "reply" if args.reply else "post"
    if kind == "reply":
        report = run_replies(split_units(text), args.premium, history)
    else:
        report = run(text, kind, args.premium, history)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        render(report)
    sys.exit(1 if report["verdict"] == "FAIL" else 0)


def run_replies(units: list[str], premium: bool, history: list[str]) -> dict:
    """Several replies at once: each is checked, and against the others."""
    reports = [run(u, "reply", premium, list(history) + [o for o in units if o is not u]) for u in units]
    merged = {"kind": "reply", "limit": reports[0]["limit"] if reports else LIMIT_STANDARD,
              "units": [], "notes": reports[0]["notes"] if reports else []}
    for i, rep in enumerate(reports):
        unit = rep["units"][0]
        unit["index"] = i + 1
        merged["units"].append(unit)
    merged["verdict"] = "FAIL" if any(r["verdict"] == "FAIL" for r in reports) else "PASS"
    return merged


if __name__ == "__main__":
    main()
