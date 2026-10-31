#!/usr/bin/env python3
"""
Parse a Markdown article for the X Articles editor.

Adapted from wshuyi's parse_markdown.py (x-article-publisher-skill, MIT). Changes:
text is HTML-escaped before conversion, ordered lists stay ordered, H4 is
supported, a word count is reported, and a missing image is reported as missing
instead of being replaced by a same-named file found in Downloads, Desktop or
Pictures (which could upload the wrong, possibly private, image).

Extracts:
- Title (first H1, else first H2, else first line)
- Cover image (first image)
- Content images and dividers, each with the block index it follows
- HTML for rich-text paste (images and dividers stripped; X ignores <hr>)

Usage:
    python3 parse_markdown.py article.md              # JSON
    python3 parse_markdown.py article.md --html-only  # HTML only

The block_index is the 0-based block element an image or divider goes after.
Insert from the highest index to the lowest so earlier positions do not shift.
"""

import argparse
import html as html_lib
import json
import os
import re
import sys
import urllib.parse
from pathlib import Path

UL_ITEM = re.compile(r"^\s*[-*] ")
OL_ITEM = re.compile(r"^\s*\d+\. ")


def split_into_blocks(markdown: str) -> list[str]:
    """Split markdown into logical blocks (paragraphs, headers, quotes, code, ...)."""
    blocks, current, code = [], [], []
    in_code = False

    def flush():
        if current:
            blocks.append("\n".join(current))
            current.clear()

    for line in markdown.split("\n"):
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_code:
                in_code = False
                if code:
                    blocks.append("___CODE_BLOCK_START___" + "\n".join(code) + "___CODE_BLOCK_END___")
                code = []
            else:
                flush()
                in_code = True
            continue
        if in_code:
            code.append(line)
            continue
        if not stripped:
            flush()
            continue
        if re.match(r"^---+$", stripped):
            flush()
            blocks.append("___DIVIDER___")
            continue
        if stripped.startswith(("#", ">")):
            flush()
            blocks.append(stripped)
            continue
        if re.match(r"^!\[.*\]\(.*\)$", stripped):
            flush()
            blocks.append(stripped)
            continue
        current.append(line)

    flush()
    if code:
        blocks.append("___CODE_BLOCK_START___" + "\n".join(code) + "___CODE_BLOCK_END___")
    return blocks


def _after_text(clean_blocks: list[str]) -> str:
    if not clean_blocks:
        return ""
    block = re.sub(r"___CODE_BLOCK_(START|END)___", "", clean_blocks[-1])
    lines = [l for l in block.strip().split("\n") if l.strip()]
    return lines[-1][:80] if lines else ""


def extract_images_and_dividers(markdown: str, base_path: Path):
    """Return (images, dividers, markdown_without_them, total_blocks)."""
    images, dividers, clean = [], [], []
    img_pattern = re.compile(r"^!\[([^\]]*)\]\(([^)]+)\)$")

    for block in split_into_blocks(markdown):
        stripped = block.strip()
        if stripped == "___DIVIDER___":
            dividers.append({"block_index": len(clean), "after_text": _after_text(clean)})
            continue
        match = img_pattern.match(stripped)
        if match:
            alt, src = match.group(1), match.group(2)
            if re.match(r"^https?://", src):
                path, exists = src, False   # remote: download it yourself before upload
            else:
                local = urllib.parse.unquote(src)
                path = local if os.path.isabs(local) else str(base_path / local)
                exists = os.path.isfile(path)
            if not exists:
                print(f"[parse_markdown] WARNING: image not found locally: {path}", file=sys.stderr)
            images.append({"path": path, "exists": exists, "alt": alt,
                           "block_index": len(clean), "after_text": _after_text(clean)})
        else:
            clean.append(block)

    return images, dividers, "\n\n".join(clean), len(clean)


def extract_title(markdown: str) -> tuple[str, str]:
    """Title from the first H1 (removed from the body), else first H2, else first line."""
    lines = markdown.strip().split("\n")
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("# "):
            title = stripped[2:].strip()
            lines.pop(idx)
            return title, "\n".join(lines)
        if stripped.startswith("## "):
            return stripped[3:].strip(), markdown
        if not stripped.startswith("!["):
            return stripped[:100], markdown
    return "Untitled", markdown


def _inline(text: str) -> str:
    """Escape, then apply bold / italic / links. Text is escaped first so a literal
    '<' or '&' in the article survives the paste."""
    text = html_lib.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", text)
    # The URL is already escaped with the rest of the text; only quotes remain.
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
                  lambda m: '<a href="%s">%s</a>' % (m.group(2).replace('"', "&quot;"), m.group(1)), text)
    return text


def markdown_to_html(markdown: str) -> str:
    """Convert block-split markdown to HTML for the X Articles editor."""
    out = []
    for part in markdown.split("\n\n"):
        part = part.strip()
        if not part:
            continue
        code = re.fullmatch(r"___CODE_BLOCK_START___(.*?)___CODE_BLOCK_END___", part, re.S)
        if code:
            # X Articles has no code blocks; a blockquote keeps it visually apart.
            lines = [html_lib.escape(l, quote=False) for l in code.group(1).strip().split("\n") if l.strip()]
            out.append("<blockquote>" + "<br>".join(lines) + "</blockquote>")
            continue
        heading = re.fullmatch(r"(#{1,4}) (.+)", part)
        if heading:
            level = max(2, len(heading.group(1)))   # a second H1 in the body becomes H2
            out.append("<h%d>%s</h%d>" % (level, _inline(heading.group(2)), level))
            continue
        if part.startswith(">"):
            body = "<br>".join(_inline(re.sub(r"^>\s?", "", l)) for l in part.split("\n"))
            out.append("<blockquote>" + body + "</blockquote>")
            continue
        lines = part.split("\n")
        for marker, tag in ((UL_ITEM, "ul"), (OL_ITEM, "ol")):
            if all(marker.match(l) for l in lines):
                items = "".join("<li>" + _inline(marker.sub("", l, count=1)) + "</li>" for l in lines)
                out.append("<%s>%s</%s>" % (tag, items, tag))
                break
        else:
            out.append("<p>" + "<br>".join(_inline(l) for l in lines) + "</p>")
    return "".join(out)


def parse_markdown_file(filepath: str) -> dict:
    path = Path(filepath)
    with open(filepath, encoding="utf-8") as fh:
        content = fh.read()

    if content.startswith("---"):          # YAML frontmatter
        end = content.find("---", 3)
        if end != -1:
            content = content[end + 3:].strip()

    title, content = extract_title(content)
    images, dividers, clean, total = extract_images_and_dividers(content, path.parent)
    words = len(re.findall(r"[A-Za-z0-9']+|[一-鿿]", re.sub(r"___CODE_BLOCK_(START|END)___", " ", clean)))
    missing = [i for i in images if not i["exists"]]

    return {
        "title": title,
        "cover_image": images[0]["path"] if images else None,
        "cover_exists": images[0]["exists"] if images else True,
        "content_images": images[1:],
        "dividers": dividers,
        "html": markdown_to_html(clean),
        "total_blocks": total,
        "word_count": words,
        "reading_minutes": round(words / 230, 1),
        "source_file": str(path.absolute()),
        "missing_images": len(missing),
    }


def main():
    parser = argparse.ArgumentParser(description="Parse Markdown for X Articles")
    parser.add_argument("file", help="Markdown file to parse")
    parser.add_argument("--html-only", action="store_true", help="print only the HTML")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    result = parse_markdown_file(args.file)
    if args.html_only:
        print(result["html"])
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
