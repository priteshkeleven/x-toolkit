# X Toolkit

**11 Claude Code and Codex skills for X (Twitter), written for what X's published ranking code actually rewards.** They draft posts, threads, long posts, Articles, replies and quotes in your voice, research what your niche is saying, plan your week, rewrite your profile, and check every draft against the spam traps in X's code before you post. Nothing is posted until you approve it, and by default nothing is posted at all: you paste the approved text yourself.

This bundle merges three projects and checks all of them against a fourth:

- **[sergebulaev/x-skills](https://github.com/sergebulaev/x-skills)** (MIT) is the base: 9 skills, the V3 humanizer, 11 hook formulas, the Story Bank, the Apify read layer and the repo checks.
- **[wshuyi/x-article-publisher-skill](https://github.com/wshuyi/x-article-publisher-skill)** (MIT) supplies the Markdown-to-Articles tools, ported with fixes.
- **[rohunvora/x-research-skill](https://github.com/rohunvora/x-research-skill)** inspired the research workflow. That repo has no license, so none of its code or text is used; `x-research` is written from scratch on this bundle's read layer.
- **[xai-org/x-algorithm](https://github.com/xai-org/x-algorithm)**, the code behind X's For You feed, is the yardstick. Every ranking claim in the skills was checked against it, and the ones the code contradicts were rewritten.

Copyright and credit for each are in [`LICENSE`](LICENSE).

## What the ranking code says, and what changed because of it

The facts, with file and line citations at a pinned commit, are in [`references/x-ranking-signals.md`](references/x-ranking-signals.md). The posting rules derived from them are in [`references/algorithm-heuristics.md`](references/algorithm-heuristics.md).

| The code says | So the skills now |
|---|---|
| Predicted actions are weighted: copy-link share **20**, reply **5** (20 from a mutual follow, on originals), quote **5**, DM share **5**, follow **4**, repost 1, like 0.66 | pick one goal per post from **Conversation, Send, Follow, Read-through** instead of "replies / reposts / likes / bookmarks" |
| There is **no bookmark weight** in ranking | stop optimising for saves; "save-worthy" content is planned as Send or Read-through |
| Report -234, mute -58.8, not interested -52.3, block -31.2 | warn against off-niche rage bait and dunks, which earn mutes from the wrong readers |
| Replies and reposts are **× 0.75** even for followers, and **filtered out** for non-followers | treat originals (and quotes, which are originals) as the reach format; replies as conversation |
| A thread's tweets 2..N are replies | build tweet 1 to stand alone, and recommend **one long post** on Premium or an **Article** for depth |
| Your 2nd post for the same viewer is × 0.625, 3rd × 0.44, floor × 0.25 | plan 1-3 strong originals a day instead of 2-4 |
| Originals from accounts ≤ 50,000 followers, < 2 h old, < 200 impressions, are lifted to ~position 15 | time originals to the audience's waking hours |
| Nothing older than **48 hours** is recommended; seen posts are not re-shown | rebuild evergreen material as new angles, never repost the same text |
| Near-duplicate text is labelled `COPYPASTA_SPAM`; low-quality redirect links plus @mentions of non-followers trip `SPAM_HIGH_RECALL` | check every draft and every batch of replies with `precheck.py` |
| Opening a link is weighted **+0.2**; there is no link penalty | drop the "links suppress reach" rule; keep the value in the post, never use shorteners |
| Video quality view, post video and profile click weights are **0** | drop "native video is favoured" and "profile clicks are high-value" |
| Retrieval is trained on posts people **read all the way through** | cut padding; length is only worth what gets finished |
| A diversity rerank pushes down posts similar to their neighbours | research the gaps; copy structure, never the take |

## Install

### Claude Code (CLI, Desktop, IDE)

```
/plugin marketplace add priteshkeleven/x-toolkit
/plugin install x-toolkit@x-toolkit
```

Or from a terminal:

```bash
claude plugin marketplace add priteshkeleven/x-toolkit
```

```bash
claude plugin install x-toolkit@x-toolkit
```

Or clone and open the folder as your working directory; the `.claude/skills/` mirror makes all 11 skills available with no install.

### claude.ai and Claude Desktop

**Customize** → **Plugins** → **Add** → **Add marketplace** → **Add from a repository**, paste `priteshkeleven/x-toolkit`, sync, then add the plugin from **Discover**.

### Codex CLI

```bash
codex plugin marketplace add priteshkeleven/x-toolkit
```

```bash
codex plugin add x-toolkit@x-toolkit
```

## Set up your voice first

1. **Voice profile:** ask *"build my voice profile"* and paste a few of your own posts (`x-humanizer --mode profile`).
2. **Story Bank:** ask *"interview me"* (`x-humanizer --mode interview`). Your real numbers, turning points and positions, so drafts never invent one.

Both ship blank and are kept out of commits.

## The 11 skills

| Skill | What it does | From |
|---|---|---|
| `x-post-writer` | A single tweet or a Premium long post, on a formula picked by ranked goal, with a precheck | Serge, realigned |
| `x-thread-builder` | A thread, or the call to make it a long post or Article instead | Serge, realigned |
| `x-article` | Write or adapt an X Article; Markdown to rich text, tables to images, an insertion list; you paste and publish | wshuyi + new |
| `x-reply-drafter` | Replies and value-add quotes, checked for duplicate wording across your replies | Serge, realigned |
| `x-humanizer` | Removes AI tells (V3); `--mode audit` with `precheck.py`; `--mode profile`; `--mode interview` | Serge + new precheck |
| `x-research` | A sourced briefing on what X is saying: themes, contested points, voices, gaps | new |
| `x-audience-insights` | Your or a competitor's tweets and repliers, ranked by what the ranker values | Serge, realigned |
| `x-hook-extractor` | The formula behind a strong post, as a blank template | Serge, realigned |
| `x-content-planner` | A week paced by author decay and the 2-hour window, with daily reply targets | Serge, realigned |
| `x-repurposer` | LinkedIn posts, blogs, videos rebuilt as native X posts | Serge, realigned |
| `x-profile-optimizer` | Bio, name, header, pin, link, plus a check of your visibility labels | Serge, realigned |

## Check a draft before you post

```bash
cd skills/x-humanizer
python3 scripts/precheck.py draft.txt                               # a single post
python3 scripts/precheck.py thread.txt --thread                     # tweets split on lines of ---
python3 scripts/precheck.py replies.txt --reply --history mine.txt  # replies vs each other and your history
python3 scripts/precheck.py post.txt --premium --json
```

It reports X's weighted length (emoji and CJK count 2, URLs 23) and every rule it can see in the code, by name: `COPYPASTA_SPAM` near-duplicates, `SPAM_HIGH_RECALL` shortener links and link-plus-mention chains, plus style warnings (bait phrasing, hashtags, emoji, em dashes). Standard library only, runs locally, uploads nothing. If your reach drops suddenly, check X's own report of labels on your account first: [Under the Hood](https://x.com/i/jf/under_the_hood).

## Optional layers

| Layer | Default | What it adds | Setup |
|---|---|---|---|
| Draft only | On | Everything | none |
| Apify read layer | Off | `x-research`, `x-audience-insights`, `x-hook-extractor` and `x-reply-drafter` read real tweets instead of asking you to paste (about $0.15 per 1,000 tweets) | `APIFY_TOKEN` in `.env`, or the filtered Apify MCP connector on claude.ai (`references/mcp-read-layer.md`) |
| Publora auto-post | Off | Posts approved tweets and threads | uncomment `PUBLORA_API_KEY` and `X_PLATFORM_ID` in `.env` |
| Pixfaro images | Off | Generated post images | `PIXFARO_TOKEN` in `.env` |
| Article clipboard | Off | Rich-text paste into the Articles editor | macOS `pip install pyobjc-framework-Cocoa`; tables need `Pillow` |

`x-article` never publishes. If you explicitly ask it to fill a draft in your logged-in browser it can, stopping at a saved draft, and it will remind you that this drives X's website rather than an official API.

## Development

```bash
python3 -m unittest discover -s tests
python3 scripts/check_frontmatter.py
python3 scripts/check_markdown_references.py
python3 scripts/check_untrusted_rule.py
python3 scripts/check_text_encoding.py
python3 scripts/check_security_boundaries.py
python3 scripts/check_mcp_mapping.py
python3 scripts/check_no_secrets.py
python3 scripts/sync_codex_marketplace.py
```

`CLAUDE.md` and `AGENTS.md` hold the conventions. The one this bundle adds: **every ranking claim traces to `references/x-ranking-signals.md` or is labelled as not in the code.** When `xai-org/x-algorithm` changes, update that file and its pinned commit first, then the skills that cite it.

## License

MIT. Copyright (c) 2026 Pritesh K., Sergey Bulaev and wshuyi. See [`LICENSE`](LICENSE).
