# Thread Structure: Pacing and the Closer

A thread is a funnel. Each tweet's only job is to earn the tap to the next one.
Design for the drop-off, not the ideal reader who reads every word.

## What X's ranking code does with a thread

Tweets 2..N are replies to tweet 1. In the For You code (`../../../references/x-ranking-signals.md`):

- Non-followers are never shown tweets 2..N in For You (`OONRetweetReplyFilter`).
  For them, **tweet 1 is the whole thread** until they tap.
- Followers see replies at × 0.75 and only one branch per conversation.
- Tweet 1 is an original, so it gets the full score and, for accounts under
  50,000 followers, the 2-hour small-account boost.
- Retrieval is trained to surface posts people read all the way through. A
  thread people abandon at tweet 3 teaches it the wrong thing about you.

So: everything rides on tweet 1, and length is only worth what gets finished.
On Premium, a single long post usually beats a thread: one original, no reply
discount, and readers who expand it feed click dwell time.

## Per-position roles

| Position | Role | Rule |
|---|---|---|
| Tweet 1 | The hook. Promise + open loop. | The only tweet non-followers are ever shown. Must stop the scroll alone, under 280 weighted chars. |
| Tweet 2 | The strongest payoff or first beat. | Front-load value here; do not save it. Tap-through is highest at 2. |
| Tweets 3 to N-1 | The body. One item or beat each. | Each stands alone. Concrete examples, real numbers. |
| Tweet N | The closer. | Most quotable line + one clear ask. Earns the repost and follow. |

## Tap-through decay

Readers leak out at every tweet (an observed pattern, not a rule in the code),
and the ranker now trains on read-through. Consequences:

- Put the best item at position 1 or 2, never the finale.
- 5-9 tweets is the sweet spot for teaching and list threads.
- A story thread can run longer if every beat raises the stakes, but tap-through
  still falls, so the turn should not be buried at tweet 15.

## Opening a loop (tweet 1 patterns)

- A count with a catch: "7 X that Y. Most people get 3 wrong."
- A withheld mechanism: "{result}. I did not expect why."
- A first-person result: "How I {number result} in {timeframe}. The exact steps."
- A story tension: "{the moment it nearly broke}. Here is what happened."

The loop must stay open. If tweet 1 answers itself, nobody expands.

## The closer playbook

The last tweet does two things and stops:

1. The single most quotable line of the whole thread (this is what gets
   screenshotted and quoted).
2. One ask, not three, and only the ones the ranker weights. Pick one:
   - A follow with a reason: "I post one teardown like this every Tuesday."
   - A reply: "Reply with the one you would add." (Conversation, weight 5)
   - Nothing: a strong last line is its own ask.

   Do not ask for bookmarks (no ranking weight) or reposts (weight 1, and
   "repost if" reads as bait).

Never stack all three asks. Never end on "that's it" or "hope this helps".

## Per-tweet scrub (apply to every tweet)

- [ ] Under 280 weighted chars on a standard account (emoji and CJK = 2, URLs = 23). `precheck.py --thread` checks every tweet.
- [ ] At most one em dash per tweet (replace the excess with a comma, colon
      or `..`, never a period). No en dashes between clauses, no double dashes.
- [ ] No cluster of 2026 AI vocab (3+ markers in one tweet = rewrite it; one
      is fine): significant, crucial, notably, comprehensive, insights,
      robust, leverage, foster, landscape, nuanced, streamline, elevate,
      fundamentally, essentially; "-ing" clause openers; nominalisations.
- [ ] No reveal bridge ("The result?", "Here's what"), no "It's not X, it's
      Y", no sincerity opener ("not gonna lie", "let me be honest").
- [ ] Stands alone if read in isolation.
- [ ] At least one concrete detail (a number with a referent, a name, an
      example) in the body tweets.

## Rhythm across the thread

Let tweet length follow the material. A teaching tweet runs long because it
teaches; a transition runs short because it transitions. That natural variance
is fine on a long thread (our X corpus: variance helps at about 430 words and
is neutral at 200). What reads as machine-made is the opposite in both
directions: every tweet the same length with no clause doing work, or a
manufactured seesaw with a 3-word "punch tweet" dropped in for rhythm. The
inserted punch is the humanizer fingerprint; do not add one. If the thread
reads flat, let the tweet carrying the most content take one real clause, and
stop there.

## Hand-splitting with `---`

Default to hand-splitting so the user approves the exact breaks:

```
Tweet 1 text here, the hook.

---

Tweet 2 text, the strongest payoff.

---

Tweet 3 text, the next beat.
```

Publora treats each `---`-delimited block as one tweet and numbers them `(1/N)`.
If you instead pass flowing prose with no separators, Publora auto-splits at
paragraph then sentence boundaries.
