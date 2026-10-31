---
name: x-thread-builder
description: "Build an X (Twitter) thread using a 2026 thread formula (listicle, story, curiosity gap, how-I teardown), picked by the goal X's ranking code pays for (read-through, sends, follows, conversation). Writes tweet 1 to stand alone, since it is the only tweet non-followers see, and recommends one long post or an Article instead when that fits. Publishes via Publora on approval. Not for single tweets (use x-post-writer) or auditing a draft (use x-humanizer --mode audit)."
---

# X Thread Builder

Build tweetstorms that get read all the way down. On X, tweet 1 is the entire
funnel: it has to promise a payoff and open a loop, or no one taps "Show this
thread." Everything after only matters if tweet 1 earns the tap.

## When to use

- User says "turn this into a thread" or "write me a thread about X"
- The idea is a list where each item needs teaching, a story with a build, a
  surprising result with a mechanism, or a repeatable process
- User has a single tweet that is trying to do too much and should be a thread

## Formulas this skill uses (thread shapes)

| Code | Formula | Primary goal | Best for |
|---|---|---|---|
| X7 | Listicle-Thread Promise | Read-through, Send | numbered teaching thread, one item per tweet |
| X8 | Story Thread | Read-through, Follow | a real narrative with a build and a turn |
| X9 | Curiosity-Gap Opener | Read-through, Conversation | a surprising result, mechanism withheld |
| X10 | How-I Teardown | Send, Follow | a repeatable process you ran yourself |

Full skeletons in `../../references/hook-formulas.md`. For single tweets
(X1-X6), use `x-post-writer`.

### Pick by goal first

| Goal | Reach for |
|---|---|
| Read-through | X7, X8, X9 |
| Send | X10, X7 |
| Follow | X8, X10 |
| Conversation | X9 |

Goals come from `../../references/algorithm-heuristics.md`. Bookmarks, likes and
reposts are not goals: the first has no ranking weight, the other two the least.

## Thread, long post or Article?

What X's ranking code does with a thread (`references/thread-structure.md`):
tweets 2..N are replies, so non-followers are only ever shown tweet 1, and
followers see the rest at × 0.75. Decide the container before writing:

| Account and material | Container |
|---|---|
| Premium, depth in one arc | **one long post**: a single original, no reply discount, readers who expand it feed click dwell time |
| Needs headers, images, tables, or runs past ~1,500 words | **Article** (`x-article`) |
| Standard account, or each beat genuinely stands alone (numbered list, timeline) | **thread** |

Write the same material either way; only the packaging changes. Tell the user
which one you picked and why in one line.

## How Publora splits a thread

Pass the full thread as one `content` string. Publora auto-splits it:

- at paragraph breaks (`\n\n`) first,
- then at sentence endings,
- then at word boundaries as a fallback,
- and adds `(1/N)` markers, reserving ~8 chars per tweet for the marker.

For full control of where each tweet breaks, hand-split with a `---` separator
on its own line between tweets. The skill defaults to hand-splitting with `---`
so the user sees exactly how the thread will land before approving.

## Steps

**Voice profile first (all drafts).** If `../../references/voice-profile.md` has `filled: yes`, load it and match the user's voice fingerprint, hard rules, and CTA/link style throughout. If it is not filled, mention once that `x-humanizer --mode profile` can learn their voice from a few posts, then proceed with the generic voice rules.

**Story bank next.** If `../../references/story-bank.md` has `filled: yes`, load it and take every concrete detail (numbers, dates, named projects, positions) from there instead of asking mid-draft. **Never invent a figure, a date or a client name that is not in the bank or supplied by the user in this conversation.** If the bank has nothing that fits, ask the user, or say once that `x-humanizer --mode interview` fills it in 20 to 40 minutes. A draft with a plausible invented number is worse than a draft with none: one is vague, the other is a retraction.

1. **Gather inputs.** Topic, the raw material (notes, a transcript, a result),
   target audience, the goal (Read-through / Send / Follow / Conversation), and
   the account tier (decides thread vs long post).
2. **Pick the formula** from the goal table, confirm it fits the material.
3. **Write tweet 1.** It is the only tweet non-followers are ever shown, so it
   is most of the work:
   - Promise a specific payoff (a number, a named result, a clear list count).
   - Open a loop the reader has to resolve ("most people get 3 of them wrong",
     "I did not expect why").
   - Keep it under 280 chars on a standard account. It must stop the scroll
     alone.
4. **Pace the body.** One beat or one item per tweet. Front-load the strongest
   item or beat at position 1-2. Target 5-9 tweets for teaching/list threads;
   longer only for a strong story. Read-through is a training target: cut any
   tweet a reader would skip.
5. **Make each tweet stand alone.** A reader landing mid-thread from a quote
   tweet should still get something.
6. **Write the closer.** End on the most quotable line, then at most one ask:
   a follow with a reason, or "reply with yours". No bookmark or repost asks.
7. **Humanizer pass** on every tweet. Scrub 2026 AI vocab by density, cap em
   dashes (at most one per tweet, never swap one for a period), break stacked
   triads and reveal bridges. Let tweet length vary only as the material
   varies: never insert a 3-word punch tweet for rhythm, never alternate
   long/short, and touch rhythm only if the whole thread reads machine-flat.
   Canonical rules: `x-humanizer` V3.
8. **Algorithm check.** Run `python3 ../x-humanizer/scripts/precheck.py
   thread.txt --thread` (with `--history` when the user's recent posts are
   available). Fix every FAIL. For a full review, `x-humanizer --mode audit`.
9. **Approval card.** Show the container decision, the thread tweet-by-tweet
   with weighted lengths, total tweet count, the formula, the goal, and the
   precheck result. Confirm any `---` breaks.
10. **On approval.** Call `lib.publish(kind="thread", draft_text=<full thread
    with --- breaks>, target_url="https://x.com/compose/tweet",
    platforms=[<X_PLATFORM_ID>], scheduled_time=<iso_or_None>)`. Publora posts
    the chain in one call and returns a `postGroupId`.

## Hard rules

Global voice rules: see root `SKILL.md` Voice rules. Additional skill-specific
rules:

- Tweet 1 must contain a real promise and an open loop. A bare "A thread:" label
  is not a hook.
- Keep each tweet under 280 chars on a standard account (emoji = 2 chars).
- Front-load value. Never bury the best item at the end of a teaching thread.
- No link in tweet 1: it is the part that gets distributed, and a reader who
  leaves there never reaches tweet 2. Links go in a later tweet or a reply,
  never through a shortener.
- Natural rhythm, not manufactured variance. A long thread where every tweet
  is the same length and none carries a real clause reads machine-flat; fix
  that one thing. Never pad or chop tweets to create variance, and never
  insert a punch tweet: the inserted punch is the humanizer fingerprint.
- Only ship a Story Thread (X8) built on a true story. Readers punish
  manufactured stakes.

## Anti-patterns (skill will refuse)

- Tweet 1 that closes its own loop (no reason to expand).
- Over-promising in tweet 1 and under-delivering in the body.
- Vague how-to steps ("be consistent", "add value") in an X10 teardown.
- Padding to hit a round number of tweets.
- Em dashes above the cap (more than one in a tweet), AI vocab clusters, ALL CAPS openers.
- "The result?" reveals, "No X. No Y. Just Z." staccato stacks, one-word tweets for drama.
- Announced candor ("Let me be honest", "not gonna lie") with no dated fact behind it.
- Engagement-bait closers ("RT if this helped").

## Resources

- `../../references/hook-formulas.md` - X7-X10 thread skeletons with worked shapes
- `../../references/algorithm-heuristics.md` - posting rules derived from X's ranking code
- `../../references/x-ranking-signals.md` - why only tweet 1 is distributed, with file citations
- `references/thread-structure.md` - per-position pacing and the closer playbook

## Related skills

- `x-post-writer` - when the idea is really just one tweet
- `x-humanizer` - scrub each tweet, or `--mode audit` the whole thread
- `x-hook-extractor` - lift the structure from a viral thread you admire
- `x-content-planner` - schedule threads into a weekly cadence
- `x-article` - when the material needs headers, images or full length
