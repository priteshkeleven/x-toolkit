# What X's ranking code actually rewards

Source: [`xai-org/x-algorithm`](https://github.com/xai-org/x-algorithm), the
code behind the For You feed, read at commit
[`9106e9f`](https://github.com/xai-org/x-algorithm/tree/9106e9f33ee9cc6a92929fc798ae6c566e2841cb)
(31 Oct 2026). Every claim below cites the file it comes from. X states that a
cron job keeps the defaults in this code equal to the main production values,
and that experiments on a small share of traffic can differ. Re-check this file
when the repo changes: the weights have moved before (see the bidirectional
boost history in [docs/BIDIRECTIONAL_BOOST_CHANGE](https://github.com/xai-org/x-algorithm/blob/9106e9f33ee9cc6a92929fc798ae6c566e2841cb/docs/BIDIRECTIONAL_BOOST_CHANGE.md)).

This file is facts. `algorithm-heuristics.md` turns them into posting rules.

## Contents

- How a post is scored
- The action weights
- Adjustments after the weighted sum
- What gets a post filtered out
- Spam and visibility labels a creator can trip
- What is not in the code
- How to read the weights without fooling yourself

## How a post is scored

1. Candidates come from accounts the viewer follows (Thunder), from accounts
   they do not follow (Phoenix retrieval, SimClusters) and from a shared list of
   popular recent posts. (x-algorithm README, Overview)
2. Phoenix, a transformer, reads the **viewer's own recent actions** and
   predicts, per post, the probability that this viewer takes each action.
3. Those probabilities are multiplied by fixed weights and summed:
   `score = Σ weight_i × P(action_i)`. (`xai-value-model/scoring.rs`,
   `compute_weighted_score`)
4. Multipliers follow (out-of-network discount, repeated-author decay), then a
   small-account boost, then a diversity rerank. (`vm-ranker/`)
5. Visibility filtering can still drop the post after it is ranked.

The model scores **this viewer's predicted reaction**, not the post's total
engagement. Ten thousand likes do not add up to anything here; they only
matter through what Phoenix learns about who reacts to posts like yours.

## The action weights

From `home-mixer/params/param.rs` (lines ~402-520). These are the weights in
effect: home-mixer computes each post's weighted score
(`home-mixer/scorers/vm_ranker.rs`, `local_scores`) and sends it to the
`vm-ranker` service, which reuses it and only applies the multipliers below.
`vm-ranker/params.rs` carries its own copy with a few different values (like
0.5, not interested -47.52, video open 0.07, continuous dwell time 0.004, post
unexplored 0.02), used only when that service recomputes the score itself. The
order of magnitude, and every conclusion in this file, is the same under either.

Positive actions:

| Predicted action | Weight | What it means for a writer |
|---|---|---|
| Share via copy link | **20.0** | the reader sends your post somewhere else |
| Reply | **5.0** | the reader writes back |
| Reply, on an **original** post by someone the viewer **mutually follows** | **5.0 + 15.0 = 20.0** | `BidirectionalFollowReplyWeightBoost`; applies only to originals, not replies or reposts (`xai-value-model/inputs.rs`, `bidirectional_boost_eligible`) |
| Quote | **5.0** | the reader adds their own take on top of yours |
| Share via DM | **5.0** | the reader sends it to one person |
| Follow author | **4.0** | the post makes the reader want more of you |
| Share (generic) | 2.0 | |
| Repost | 1.0 | |
| Favorite (like) | 0.66 | |
| Click dwell time (predicted seconds after clicking into the post) | 0.4 | the reader opened it and stayed |
| Click | 0.3 | |
| Open link | 0.2 | positive, not a penalty |
| Dwell (probability of a dwell) | 0.05 | |
| Photo expand | 0.05 | |
| Quoted-post click | 0.05 | |
| Video open | 0.02 | |
| Post unexplored | 0.015 | in-network only |
| Continuous dwell time (predicted seconds) | 0.006 | |
| Profile click, video quality view, post video | **0.0** | currently switched off |

Negative actions:

| Predicted action | Weight |
|---|---|
| Report | **-234.0** |
| Mute author | **-58.8** |
| Not interested | **-52.272** |
| Block author | **-31.2** |
| Not dwelled (scrolled past) | -0.02 |

## Adjustments after the weighted sum

Production values from `vm-ranker/params.rs` and `home-mixer/params/param.rs`:

- **Out-of-network discount: × 0.75.** Posts from accounts the viewer does not
  follow are multiplied by `OonWeightFactor = 0.75`. With
  `EnableOonRescoreForInNetworkRepliesRetweets = true`, **replies and reposts
  from accounts the viewer does follow get the same × 0.75**. Only an original
  post, shown to a follower, escapes it. (`xai-value-model/scoring.rs`,
  `oon_applies`)
- **Repeated-author decay.** `EnableAuthorDiversity = true`, decay 0.5, floor
  0.25: among the candidates for one feed request, your best post keeps its
  score, your second is × 0.625, your third × 0.4375, your fourth × 0.34, then
  it flattens toward × 0.25. (`diversity_multiplier`: `(1 - floor) × decay^k + floor`)
- **Small-account boost (cold start).** `home-mixer/scorers/author_cold_start.rs`:
  an **original** post (not a reply, not a repost) from an author with **at most
  50,000 followers**, **under 2 hours old** and with **fewer than 200
  impressions** can be lifted to about **position 15-16** of a viewer's feed
  (`ColdStartSlotMin/Max = 15/16`). One such post per request is chosen, by
  Thompson sampling.
- **Diversity rerank.** `DppEnabled = true`, `DppTheta = 0.65`: a determinantal
  point process trades a little score for less similarity between neighbouring
  posts, using their embeddings. A post that says what ten others just said is
  the one that gets pushed down.
- **Read-through is a training target.** Since 8 Oct 2026 the ranking model
  predicts time spent better (`phoenix/xrex/models/loss_recsys.py`); since 13
  Oct 2026 retrieval is also trained to surface posts people **read all the way
  through** (x-algorithm README, Notable Updates).

## What gets a post filtered out

Pre-scoring filters (x-algorithm README, Filtering; `home-mixer/filters/`):

- **Older than 48 hours** (`AgeFilter`). For You does not recommend a post past
  two days, however good. SimClusters candidates are capped at 48 hours too.
- **Already seen or already served** to that viewer (`PreviouslySeenPostsFilter`,
  `PreviouslyServedPostsFilter`). Reposting the same thing does not get it a
  second look from people who saw it.
- **Replies and reposts from accounts the viewer does not follow**
  (`OONRetweetReplyFilter`). Your replies on a stranger's post do not travel
  to non-followers through For You. They live in the conversation.
- **Muted keywords** match post text (`MutedKeywordFilter`).
- **One branch per conversation** after ranking (`DedupConversationFilter`).
- For brand-new viewer accounts only, out-of-network posts under an engagement
  threshold (`NewUserMinEngagementFilter`, currently disabled).

## Spam and visibility labels a creator can trip

Visibility filtering runs after ranking and can drop a post for everyone but
its author. Rules in `visibility-filtering/rules/tweet_rules.rs`; the labels
come from `botmaker-rules/`, `grox/` and `agatha/`.

| Label or system | What triggers it (public part) | Effect |
|---|---|---|
| `COPYPASTA_SPAM` | the same or near-same text posted across many posts or replies (`BBQDuplicateTextProd.bot`, `BBQDuplicateTextRepliesProd.bot`, unigram and CJK character jobs) | labelled with a downrank note; high-PageRank and grey-verified accounts are exempt |
| `DUPLICATE_CONTENT` | duplicate content | dropped for non-authors (`DUPLICATE_CONTENT_DROP_UNSPECIFIED`) |
| `SPAM_HIGH_RECALL` | among other rules, a post whose link redirect chain includes a URL rated `LOW_QUALITY`, posted with @mentions of accounts that do not follow the author (`LQ_Tweets_With_LQ_URL_Verdict_At_Mention_To_NonFollower_v2.bot`) | dropped for non-authors |
| Reply spam scoring | replies to accounts with **125,000+ followers** are scored by an LLM for reply spam and reply ranking (`grox/flows/reply_spam/constants.py`, `GEMMA_REPLY_SPAM_MIN_FOLLOWERS`) | low-scored replies rank low in that conversation |
| Account labels | `agatha/`: blocks, reports and spam reports **relative to likes** your posts collect; `bdsm/`: inauthentic action patterns over time; `user-cred-v2/`: PageRank over follows and engagement | labels on the account limit its posts |

The prompts for the LLM classifiers and some botmaker rules are deliberately
unpublished (x-algorithm README, What's not in this repo). You can see which labels
your own account carries in the **Under the Hood** report at
`https://x.com/i/jf/under_the_hood`.

## What is not in the code

Checked against the ranking path (`home-mixer/`, `xai-value-model/`,
`vm-ranker/`, `phoenix/`):

- **No bookmark weight.** Bookmarks appear only as an input describing the
  viewer's history (`home-mixer/util/viewer_history.rs`) and as a hydrated count.
  Nothing multiplies P(bookmark).
- **No link penalty.** Opening a link is weighted +0.2. The cost of a link is
  indirect: a reader who leaves is a reader who does not dwell, reply or share,
  and a link to a low-quality or redirecting URL can trip the spam rule above.
- **No Premium or verification boost** in the published weights or multipliers.
  (Grey-verified and high-PageRank accounts are exempt from some spam rules.)
- **No video boost.** Video quality view and post-video weights are 0.0; video
  open is 0.02. Video earns what any post earns: dwell, replies, shares.
- **No hashtag rule** in ranking. Hashtags only matter through muted keywords
  and readers.
- **No "first 30 minutes" second test.** The code has no rule that re-tests a
  post after early replies. What it has is the 2-hour, 200-impression window for
  small accounts and a 48-hour hard limit.
- **No reply-back multiplier.** The author replying to replies is not weighted
  as such; it matters because it creates more replies and mutual follows.

## How to read the weights without fooling yourself

X added this warning to the code itself (`param.rs` comments, x-algorithm README): the
weights scale **predicted probabilities**, not counts. A report is weighted
-234 because its base rate is more than 1000x lower than a like's, so the
weight lets a rare prediction move the ranking at all. "One report cancels 468
likes" is wrong.

What the table does tell you is which reactions the ranker values **when a
viewer is predicted to take them**. A post that makes the right readers likely
to reply, quote, send it to someone or follow you outranks one that only makes
them likely to like it. A post that makes them likely to mute you or tap "not
interested" loses more than any like can return.

Personalisation cuts both ways: reports from a hostile cluster mostly move
rankings for viewers who resemble that cluster, and engagement only counts if
the post was served in the Home timeline, not if people were sent to it
directly.
