# 11 X (Twitter) Hook Formulas - 2026 Edition

X rewards a different shape than LinkedIn. A single tweet has to land a
complete punch in the first line, because there is no "see more" fold to buy
you a second sentence. A thread rewards a strong promise plus an open loop in
tweet 1, so the reader taps "Show this thread."

Each formula below has a skeleton, why it works, and a primary goal. The goals
are the ones X's published ranking code pays for (weights and sources in
`x-ranking-signals.md`, rules in `algorithm-heuristics.md`):

| Goal | Ranked actions (weight) | What the post has to make likely |
|---|---|---|
| **Conversation** | reply 5, quote 5 (reply 20 on an original from a mutual follow) | the right reader answering or adding a take |
| **Send** | share via copy link 20, via DM 5, share 2 | the reader forwarding it to one specific person |
| **Follow** | follow author 4 | the reader wanting your next post |
| **Read-through** | click dwell time 0.4/s, dwell, read-through retrieval | the reader opening it and finishing it |

Reposts (1) and likes (0.66) are side effects, never the goal. Bookmarks have
no ranking weight: a "save-worthy" post earns its rank as Send or Read-through.

Formulas X1-X6 and X11 are **single-tweet** shapes (the whole idea fits in one
tweet, or a 2-3 tweet micro-thread). X7-X10 are **thread** shapes (tweetstorms).
Publora auto-splits any long `content` into a numbered `(1/N)` thread at
sentence boundaries, so you can write a thread as flowing prose or break it
yourself with `---` separators.

## Contents

- X1 - One-Liner Contrarian
- X2 - Data-Point Hook
- X3 - Build-in-Public Confession
- X4 - Value-Add Quote
- X5 - Mini-List Tweet
- X6 - Relatable Cold-Open
- X7 - Listicle-Thread Promise
- X8 - Story Thread
- X9 - Curiosity-Gap Thread Opener
- X10 - How-I Teardown Thread
- X11 - Third-Person Case-Study Flex
- Engagement-goal split
- Single tweet vs thread: pick the container first
- Hook micro-rules (X-specific)
- Never do

---

## X1 - One-Liner Contrarian

**Goal: Conversation** (quotes and replies). Single tweet. The whole value is one
sharp, defensible, against-the-grain claim about your own field.

```
Most {group} think {common belief}.

The ones who {win} do the opposite: {contrarian move}.
```

Or the even tighter one-line form:

```
{Unpopular truth stated flatly, no hedge, no "I think".}
```

**Why:** A complete, screenshot-ready opinion invites the two actions the ranker
weights at 5: a reply that pushes back and a quote that stakes a position. No setup, no thread, no
fold. The claim has to be true enough to defend in the replies and sharp enough
to make a quote-tweet worth writing.

**Warning:** A contrarian take you cannot back up gets ratio'd, and a take
outside your field mostly earns mutes and "not interested" (-58.8, -52.3) from
people who never followed you for it. Only ship the ones you would defend in
person, about the field you post in.

---

## X2 - Data-Point Hook

**Goal: Send.** Single tweet built around one concrete, odd-precision number
that reframes how the reader sees a thing.

```
{Specific number, not rounded} {what it measures}.

{One line of context that makes the number land.}
```

Worked shape:

```
A landing page that loads in 1.3s converts 2.4x better than one at 3.2s.

Speed is not a UX nicety. It is a revenue line item.
```

A corpus-corroborated variant (validated across ~450 top tweets, July 2026): a
**big brand's specific spend plus a same-day consequence**. This shape traveled
across several unrelated accounts, not one lucky post:

```
{Named company} spends {specific $ figure} a year on {thing}.

{Yesterday / this week} they announced {the consequence}.
```

("Starbucks spends $400 million a year on software. Yesterday they announced
they are moving off IBM and Microsoft." "Rockstar didn't spend $7.6 billion
building a game. They built a world where the biggest audiences get paid first.")

**Why:** A single hard number is the unit people forward: "look at this" to a
colleague is a copy-link or DM share, the heaviest positive weight in the ranker. Odd, non-rounded figures (1.3s, $873.47, 2.4x) read as real
measurement, not a vibe. The second line tells the reader why to care.

**Warning:** Never invent the number. A figure that gets fact-checked in the
replies costs you more reach than the post earned.

---

## X3 - Build-in-Public Confession

**Goal: Conversation, then Follow.** Single tweet or 2-3 tweet micro-thread.
You share a real number from your own work, including the ugly ones.

```
{Time marker}: {your project} did {real metric, good or bad}.

Here is the part nobody tweets: {the honest cost, mistake, or surprise}.
```

**Why:** Founders and builders over-index on X, and raw transparency out-pulls
polish. A real failure or an unflattering metric earns replies because it gives
other builders permission to compare notes. The confession is the conversation
starter.

**Warning:** It has to be a true number from your real work. Manufactured
vulnerability is obvious and gets punished.

---

## X4 - Value-Add Quote

**Goal: Conversation.** You quote someone else's take and add a layer, NOT a
cheap dunk. The quote shows the original above your comment, and it counts as
your own original post: no reply discount, eligible for the small-account boost.

```
{One line that reframes or respectfully challenges the quoted take.}

{The added value: the missing nuance, the counter-example, the "and here is why".}
```

**Why:** Quote tweets borrow the reach and context of the original while letting
you stake your own position. The ones that travel add genuine value or a sharper
frame, not contempt. A value-add quote tweet often out-reaches a standalone post
because it rides an existing conversation.

**Warning:** Punching down or quote-dunking on a small account reads as
bullying and backfires. Add value or skip it. A quote tweet is public, so assume
the original author will see it.

---

## X5 - Mini-List Tweet

**Goal: Send.** A single tweet that packs a tight, scannable list. The whole
list fits in 280 chars (or a roomy single post on Premium).

```
{N} {things} that {payoff}:

1. {item}
2. {item}
3. {item}
4. {item}
5. {item}
```

**Why:** A self-contained list is the thing people send to the one person who
needs it. A bookmark alone carries no ranking weight; the send does. Keep each item to a few words
so the whole thing reads in one glance. If the list needs more than a line per
item, it is a thread (use X7), not a single tweet.

**Warning:** Padding the list with filler items to hit a round number dilutes
it. Five real items beat ten weak ones.

---

## X6 - Relatable Cold-Open

**Goal: Conversation, light.** A single tweet that names a feeling or a small
universal moment with no setup. The reader sees themselves in it. It mostly
earns likes, the action the ranker weights least (0.66), so use it for presence,
not growth.

```
{One short line that drops the reader straight into a shared, specific moment.}
```

Worked shape:

```
that 4pm feeling when the code finally compiles and you are scared to touch anything.
```

**Why:** Relatable observations are the cheapest likes on X and the most
shareable to a reader's own followers. They work because recognition is instant.
Specific beats generic: a named moment ("4pm", "the code compiles") lands harder
than a vague mood.

**Warning:** This is the most copied genre on X, so a generic version disappears.
The specificity is the whole job. Do not reach for ALL CAPS to add intensity, it
reads as trying too hard.

**Two corpus-observed variants of the cold-open** (both recurred among top
performers, July 2026):

- **Ironic day-in-the-life list.** A quoted aspirational archetype, then deadpan
  bullets where the last one punctures it. `"Come with me on my 5am morning as a
  24 year old in B2B SaaS sales" - run / grounding / performative meditation / ...`
  This reads relatable but the format (quoted premise + comedy bullets) is
  distinct. The mechanic is satire of a recognizable online genre.
- **Meme juxtaposition.** One line whose whole payload is an unexpected pairing:
  `What Viktor Gyokeres taught me about B2B sales`. `Marathon and B2B sales`.
  The mechanic is incongruity, not recognition, and it over-indexes on reposts.

---

## X7 - Listicle-Thread Promise

**Goal: Read-through, then Send.** Thread, or one long post on Premium. The
opener promises a numbered payoff; each item gets room to breathe.

```
{N} {things} that {big specific payoff}.

Most people get {number} of them wrong.
```

Then one tweet per item:

```
1. {Item name}

{2-3 lines that actually teach the item, with a concrete example.}
```

**Why:** The promise plus the "most people get X wrong" line opens a loop the
reader has to resolve, so they expand the thread. A teaching thread with real
examples is read to the end, which the ranker now trains on. Only the opener is
distributed to non-followers, so the strongest item goes at position 1 or 2.

**Warning:** If tweet 1 over-promises and the body under-delivers, you train
followers to skip your threads. The promise is a contract.

---

## X8 - Story Thread

**Goal: Read-through, then Follow.** Thread or long post. It starts in the
middle of a real story at the moment of tension. No warm-up.

```
{One line dropped into the peak of a real story: the moment it nearly broke, or the impossible odds.}

{One line that raises the stakes and promises the turn is coming.}
```

Then the thread carries the scene forward, one beat per tweet, ending on the
turn and a single line of meaning.

**Why:** Starting in the action (in medias res) skips the setup the scroll
punishes. Story threads earn read-through, and a reader who
finishes a good story is the likeliest to follow. The open loop in tweet 1 ("here is the moment it nearly
broke") is what makes the reader tap to see how it resolves.

**Warning:** Only use a true story. Readers punish manufactured stakes, and a
fabricated arc that gets caught destroys trust fast.

---

## X9 - Curiosity-Gap Thread Opener

**Goal: Read-through, then Conversation.** Thread or long post. The opener
names a surprising result and withholds the mechanism.

```
{Surprising outcome stated as fact, with a number if you have one.}

I did not expect why. Here is what actually happened.
```

**Why:** Line 1 is a complete, intriguing claim; line 2 deepens the gap and
promises the explanation lives below. The reader expands the thread to close the
loop, and the "I did not expect why" framing invites replies guessing the
reason. Pair the reveal with a real, specific cause, not a platitude.

**Warning:** Pure clickbait with a thin payoff gets a fast tap-away: the reader
does not finish, and "not dwelled" is a negative weight. The reveal has to be worth the tap.

---

## X10 - How-I Teardown Thread

**Goal: Send, then Follow.** Thread, long post or Article. The opener frames a
specific result you got; the body is the exact, repeatable steps.

```
How I {specific result with a number} in {timeframe}.

The exact steps, nothing held back.
```

Then one tweet per step, each actionable:

```
Step {n}: {step name}

{What to do, the specific tool or ratio, and the one mistake to avoid.}
```

**Why:** "How I" beats "How to" on X because first-person results carry proof. A
no-paywall teardown of a real result is what people send to a teammate to run
later, and it shows the reader what following you gets them. The number in tweet 1 ("in 14 days", "to 10k") is the credibility
anchor.

**Corpus caveat (July 2026):** among ~450 top tweets, first-person "How I"
teardowns were *rare* in real over-performers. What actually dominated was the
third-person result flex (X11): narrating someone else's outcome. Reach for X10
when the result is genuinely yours and provable; otherwise the same material
travels further framed as X11. This reverses the LinkedIn-inherited rule.

**Warning:** Vague steps ("be consistent", "add value") kill the save. Every
step needs a concrete instruction someone could execute tomorrow.

---

## X11 - Third-Person Case-Study Flex

**Goal: Send.** Single tweet (or 2-3 tweet micro-thread). You
narrate someone else's absurd, specific result, framed as an unfair advantage
anyone could copy. This was the single most common winning shape in a ~450-tweet
corpus (July 2026), and it sat in a blind spot between X2 (abstract stat) and
X10 (first-person how-I).

```
{A person or faceless thing} {achieved an absurd, specific $ outcome} {doing something ordinary or sneaky}.

{One line that sharpens the "how" into an anyone-could-do-this frame.}
```

Worked shapes (real corpus hooks):

```
A cruise channel with 59 videos makes $5,000/month from AdSense alone.

He stopped paying $1,000/month for AI and built his own instead.
```

**Why:** The emotional pull is aspiration, not vulnerability. A third party's
result lets the reader imagine the same win without the poster having to expose
their own numbers. The specific, non-round figure ($10,400/month, 59 videos)
does the credibility work; the second line converts it into a template the
reader feels they could run.

**Warning:** Many corpus examples tail into an engagement-bait CTA ("like this
and I'll DM the breakdown", "repost to help your network"). The *hook* works;
the CTA does not fit these skills' voice rules. Use the shape, skip the bait. And
never invent the result or the person. A fabricated case study that gets
checked in the replies costs more reach than it earned.

---

## Engagement-goal split

Pick the formula by what you want the post to earn, then narrow by topic.

| Goal | Earned by | Formulas |
|---|---|---|
| **Conversation** | confessions, takes worth arguing, value-add quotes, questions only this post could ask | X1 One-Liner Contrarian, X3 Build-in-Public, X4 Value-Add Quote, X9 Curiosity-Gap |
| **Send** | hard numbers, lists, repeatable how-tos, case studies a reader forwards | X2 Data-Point, X5 Mini-List, X10 How-I Teardown, X11 Third-Person Case-Study |
| **Follow** | proof of what the account reliably delivers | X3 Build-in-Public, X8 Story Thread, X10 How-I Teardown |
| **Read-through** | depth people finish: teaching lists, stories, mechanisms | X7 Listicle-Thread, X8 Story Thread, X9 Curiosity-Gap |

X6 Relatable Cold-Open is presence, not growth: it mostly earns likes.

## Single tweet vs thread: pick the container first

| If the idea is... | Use | Why |
|---|---|---|
| One claim, one number, one moment | single tweet (X1, X2, X6) | a thread on a one-line idea reads as padding |
| Someone else's absurd, specific result | single tweet (X11) | the number plus an anyone-could-do-this frame is the whole punch |
| A scannable list, each item one line | single tweet (X5) | fits in 280, easy to forward |
| A list where each item needs teaching | long post on Premium, else thread (X7) | a long post is one original; thread tweets 2+ are replies, discounted and never shown to non-followers |
| A narrative with a build and a turn | thread (X8) | one beat per tweet controls pacing |
| A surprising result with a mechanism | thread (X9) | gap in tweet 1, payoff in the body |
| A repeatable process you ran yourself | long post, Article or thread (X10) | one step per beat, send-worthy |
| Anything that needs headers, images or tables | Article (`x-article`) | one original card, minutes of dwell |

## Hook micro-rules (X-specific)

- **First line carries everything.** There is no fold. If the first tweet does
  not stop the scroll on its own, nothing downstream matters.
- **"How I" beats "How to", but third-person beats "How I".** First-person
  results carry proof over generic instruction, yet in a ~450-tweet corpus
  (July 2026) narrating *someone else's* result (X11) out-pulled first-person
  "How I" teardowns. Reach for the case study unless the win is provably yours.
- **One specific number in tweet 1** gives the reader something to answer or
  forward. 1.3s beats "fast". $873.47 beats "cheap".
- **Open the loop in the thread opener, never close it.** Tweet 1 promises;
  the body delivers. If tweet 1 answers its own question, no one expands. It is
  also the only tweet non-followers will ever be shown.
- **Lead a story with the tension, not the context.** In medias res beats the
  warm-up the scroll punishes.

## Never do

- Pad a one-line idea into a thread. Readers do not finish it, and read-through is what the ranker now trains on.
- Open a thread with "A thread:" and nothing else. The promise has to be in the
  words, not the label.
- Stack hashtags. Zero or one. The ranker ignores them; readers read two or more as spam.
- Put the link where the value should be. A link is not penalised (opening one is
  weighted +0.2), but a reader who leaves does not reply, send or finish. Value in
  the post, link second. Never through a shortener or redirect.
- Quote-dunk on a small account. Add value or skip it: dunks collect the blocks and
  reports that `agatha/` counts against the account.
- Copy the like-for-DM / repost-to-help CTA that many viral case-study tweets
  tail into. The hook shape (X11) travels; the engagement-bait closer violates
  these skills' voice rules and reads as spam. Use the shape, drop the bait.
