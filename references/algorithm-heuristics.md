# 2026 X posting rules, derived from the ranking code

Every rule in the first part of this file follows from a line of X's published
For You code. The facts, weights and file citations live in
`x-ranking-signals.md`; this file says what to do about them. The second part
lists product facts (limits) and habits that are **not** in the code, labelled
as such, so a skill never presents folklore as the algorithm.

## Contents

- The goals the ranker pays for
- Rules from the code
- Threads, long posts and Articles
- Replies on other people's posts
- Spam traps
- Not in the code: limits, timing and style
- Pre-publish checklist

## The goals the ranker pays for

Every skill in this bundle picks **one primary goal** per post from this list.
The weights are what the ranker multiplies each predicted action by
(`x-ranking-signals.md`, The action weights).

| Goal | Actions and weights | Write for it by |
|---|---|---|
| **Conversation** | reply 5, quote 5; reply 20 on an original from a mutual follow | a claim the right reader has an answer to, a question only this post could ask, a take they want to add to |
| **Send** | share via copy link 20, share via DM 5, share 2 | something a reader would forward to one person: a fix, a number, a template, a checklist, a "this is exactly our problem" |
| **Follow** | follow author 4 | a post that shows what the account reliably delivers, so the reader wants the next one |
| **Read-through** | click dwell time 0.4 per predicted second, dwell; retrieval trained on read-through | depth that is finished, not padded: a long post, a thread or an Article people read to the end |
| Reposts, likes | repost 1, like 0.66 | secondary. Never the primary goal of a post |

**Bookmarks are not a ranking goal.** The ranker has no bookmark weight. A
"save this" post earns its rank through Send and Read-through, so plan it as
one of those.

The negative side outweighs everything: report -234, mute -58.8, not interested
-52.3, block -31.2. A post that makes the wrong reader likely to mute you can
cost more than its likes earn. Write for your audience, not for everyone.

## Rules from the code

1. **Write for the reply, the quote and the send, not the like.** A reply is
   worth about 7.6 likes and a copy-link share about 30, as predicted
   probabilities. Pick the goal before the hook.
2. **Originals carry the reach.** Replies and reposts are discounted (× 0.75)
   even for your followers, and replies and reposts from you are filtered out
   for non-followers. Your growth comes from original posts, including quote
   posts, which count as originals.
3. **Post less, and only what would rank first.** Among one viewer's candidates
   your second post is worth × 0.625 of its score, your third × 0.44, and it
   falls to × 0.25. A filler post does not ride on your strong one, it competes
   with it. One to three strong originals a day beats six.
4. **Small accounts: the first two hours matter.** Up to 50,000 followers, an
   original post under 2 hours old with fewer than 200 impressions can be
   lifted to about position 15 in a viewer's feed. Post originals when your
   audience is awake, not at 3 a.m. to "beat the rush".
5. **Everything expires at 48 hours.** For You does not recommend a post after
   two days. Evergreen material gets a new post with a new angle, not a bump.
6. **Mutual follows multiply replies.** On your original posts, a viewer you
   mutually follow has their reply weighted 20 instead of 5. Real two-way
   relationships with peers in your niche are worth more than raw follower
   count. Follow-for-follow schemes are what `bdsm/` looks for; do not.
7. **Do not say what ten others just said.** The diversity rerank pushes down a
   post that sits close to its neighbours. Take the trending topic, not the
   trending take.
8. **Never repeat yourself verbatim.** Near-identical text across posts or
   replies gets labelled `COPYPASTA_SPAM`; duplicate content is dropped for
   everyone but you; and people who saw it once are filtered from seeing it
   again.
9. **Links are not penalised, leaving is.** Opening a link is weighted +0.2.
   The cost is that a reader who leaves is not replying, sharing or dwelling.
   Put the value in the post and the link second (a reply or the last tweet).
   Never use shorteners or redirect chains: a low-quality hop in the chain plus
   @mentions of non-followers trips a spam drop.
10. **Avoid the mute.** Off-topic rage bait, dunks on small accounts and
    hot takes outside your niche raise predicted mute and not-interested for
    the people who see them. Contrarian is fine; contrarian for your audience,
    about your field.

## Threads, long posts and Articles

The code changes the old thread advice:

- Tweets 2..N of a thread are replies to yourself. Non-followers only get tweet
  1 through For You; followers get the rest at × 0.75 and one branch per
  conversation. **Tweet 1 is the only part that is distributed.** It has to
  earn the click on its own.
- A **long post** (Premium) is one original: no reply discount, eligible for
  the small-account boost, and readers who click "Show more" and stay feed
  click dwell time (0.4 per predicted second). When the account can post long,
  prefer one long post over a thread for depth.
- An **Article** is the same bet at full length: one original card, a click,
  and minutes of dwell. Use it for anything that needs headers or images.
- Use a thread when the account cannot post long, or when each tweet genuinely
  stands alone and the sequence is the point (a numbered list, a timeline).
  Keep it to what readers finish: read-through is a training target, padding is
  not.
- Front-load. The strongest item goes in tweet 1 or 2.

## Replies on other people's posts

- They do **not** reach non-followers through For You (filtered) and reach your
  followers at × 0.75. Their value is in the conversation itself: the author and
  their readers see you, and a good reply earns profile visits and follows.
- Replies to accounts with 125,000+ followers are scored by an LLM for reply
  spam and ranking. Generic agreement, emoji-only replies and the same reply
  pasted under five big accounts rank at the bottom, or trip `COPYPASTA_SPAM`.
- The best replies add one specific thing the post did not have: a number, a
  counter-example, the step that was skipped.

## Spam traps

- The same sentence in more than one reply or post.
- Links through shorteners, trackers or redirects, especially combined with
  @mentions of people who do not follow you.
- Mass-mentioning accounts.
- A burst of follows, likes or replies that looks automated.
- Content that collects blocks and reports out of proportion to its likes
  (`agatha/`): it labels the account, not just the post.

Check your account's labels any time in Under the Hood:
`https://x.com/i/jf/under_the_hood`.

## Not in the code: limits, timing and style

These are product facts and observed habits, not ranking rules.

| Item | Standard | X Premium |
|---|---|---|
| Post text | 280 weighted chars | 25,000 chars |
| Images per post | 4 | 4 |
| Image size | 5 MB | 5 MB |
| Video length | 2 min 20 s | longer, plan-dependent |

- **Weighted length.** X counts most Latin text as 1 per character, but emoji
  and CJK characters as 2, and any URL as 23. `../skills/x-humanizer/scripts/precheck.py`
  computes it.
- **Timing (observed, not in the code).** Weekday mornings in the audience's
  timezone and an early-afternoon bump work for most B2B and tech audiences;
  8-11 p.m. for build-in-public developers. What the code does say is narrower:
  for small accounts the first two hours count, and nothing lives past 48.
- **Hashtags (style, not ranking).** Zero or one, at the end. The ranker
  ignores them; readers do not.
- **Engagement bait (unpublished).** "RT if you agree" and "reply YES" are not
  in the published rules, and some rules are unpublished. They also invite
  "not interested". Do not use them.

## Pre-publish checklist

- [ ] One primary goal: Conversation, Send, Follow or Read-through.
- [ ] Tweet 1 / line 1 earns the click on its own (it is the only part distributed).
- [ ] An original post, not a reply, when the aim is reach.
- [ ] Would a reader send this to one specific person, or answer it? If neither, rework.
- [ ] Not the take everyone posted today; your angle, your number.
- [ ] Not a near-copy of anything you posted before.
- [ ] Value in the post; any link second, no shorteners, no mass @mentions.
- [ ] Nothing that makes your own audience want to mute you.
- [ ] Inside 280 weighted characters on a standard account (`precheck.py`), or a deliberate long post / thread / Article.
- [ ] At most one em dash per tweet; no AI vocabulary cluster (3+ markers in one tweet).
- [ ] At least one odd-precision number with a named referent where the claim allows it.
- [ ] 0-1 hashtag, 0-1 emoji.
- [ ] Close is a landing or a specific question, not "what do you think?".
- [ ] Today's other posts are not competing with this one (author decay).
