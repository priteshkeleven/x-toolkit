---
name: x-content-planner
description: "Generate a weekly X (Twitter) content plan from a theme, audience, and content pillars, paced by what X's ranking code rewards: 1-3 originals a day (author decay), originals in the 2-hour small-account window, depth as long posts or Articles. Per-day format, formula, angle, time and ranked goal (conversation, sends, follows, read-through), plus daily reply targets. Not for drafting a single post (use x-post-writer)."
---

# X Content Planner

Produce a weekly X plan built around a pillar discipline and the cadence X's
ranking code actually rewards (`../../references/algorithm-heuristics.md`): a few
strong originals a day rather than many, posted while the audience is awake,
with depth packaged as one long post or Article, and a daily reply block.

## When to use

- User asks "plan my week on X" or "what should I post this week"
- User wants to escape ad-hoc posting and establish a rhythm
- Before a launch week (the plan aligns a product pillar)

## Input

- **Theme** (optional): e.g. "shipping our AI agent in public"
- **Audience description:** e.g. "indie builders, AI engineers, early founders"
- **Pillar mix** (optional): defaults to 40% Build-in-Public / 30% Insight /
  20% Engagement / 10% Promotion
- **Posting cadence** (optional): defaults to 1-2 originals/day on weekdays
- **Account tier and follower count**: Premium unlocks long posts; under 50,000
  followers gets the 2-hour small-account boost on originals
- **Voice samples** (optional): past tweets for voice calibration

## Output

A markdown plan with:

### 7-day calendar

| Day | Slot | Type | Pillar | Formula | 1-line angle | Goal | Time |
|---|---|---|---|---|---|---|---|
| Mon | AM | single | Insight | X1 One-Liner Contrarian | "speed is a revenue line item" | Conversation | 9:30 AM |
| Mon | PM | reply block | Engagement | R-templates | 5 builder threads | Conversation | 2:00 PM |
| Tue | AM | long post | Build-in-Public | X10 How-I Teardown | "how we cut deploy 40m to 6m" | Send | 10:00 AM |
| Wed | AM | single | Insight | X2 Data-Point | "1.3s page = 2.4x conversion" | Send | 9:30 AM |
| Thu | AM | single | Build-in-Public | X3 Confession | "the metric we hid for a month" | Conversation | 10:00 AM |
| Fri | AM | Article | Insight | X7 Listicle | "9 landing-page mistakes, with screenshots" | Read-through | 9:30 AM |

(The skill fills real angles from the theme. Weekends are optional and skew to
story threads or relatable singles.)

### Daily reply and quote-tweet targets

For each day:
- **5-10 accounts to engage** (names or archetypes: "peer builders at 2-20k",
  "AI founders shipping in public", "the 3-4 larger creators in the niche")
- **Template to apply** (R1 answer, R2 concede-sharpen, R3 extend, R5 value-add quote)
- **Target:** 5-10 substantive replies per day, each written for its post. In the
  ranking code replies are not shown to non-followers and reach followers at
  × 0.75; their value is the conversation and the mutual follows it builds
  (a mutual follow's reply on your originals is weighted 20, not 5).

### Weekly balance check

- [ ] At most 2-3 originals on any day (your extra posts compete with your best one)
- [ ] Originals timed to the audience's awake hours (2-hour small-account window)
- [ ] At least 1 build-in-public post (real number from your work)
- [ ] At least 1 piece of finished depth (long post, Article or thread)
- [ ] At least 1 engagement/reply-heavy day
- [ ] No pillar over 60% of the week's posts
- [ ] No formula repeated more than twice, no two near-identical takes
- [ ] Goal mix spread across Conversation, Send, Follow, Read-through

## Goal mix (balance the week)

Every formula targets one of the four goals X's ranking code pays for. A week
that chases one signal reads as engineered:

| Goal | Formulas | Weekly target |
|---|---|---|
| Conversation | X1, X3, X4, X9 | at least 2 |
| Send | X2, X5, X10, X11 | at least 2 |
| Follow | X3, X8, X10 | at least 1 |
| Read-through | X7, X8, X9 as a long post, Article or thread | at least 1 |

Likes and reposts are side effects. Bookmarks have no ranking weight, so they
get no target.

## Rules

- **1-3 originals a day, only strong ones.** For one viewer your second post in
  48 hours scores × 0.625, your third × 0.44, flattening at × 0.25. A filler
  post competes with your best one.
- **Time originals to the audience.** Accounts under 50,000 followers get a boost
  for originals in their first 2 hours. Weekday mornings in the audience's
  timezone are the usual window for B2B and tech (observed, not in the code).
- **Nothing lives past 48 hours.** Re-use material as a new angle, never as a
  repost of the same text.
- **Depth as one piece.** On Premium, plan depth as a long post or an Article;
  threads only when the beats stand alone.
- **Replies are a content type, not an afterthought.** Block reply time daily;
  aim them at peers who talk back.
- **Promotion pillar max 1-2 posts/week.** Ads earn mutes.
- **One formula per slot, varied across the week.** Similar posts get pushed
  down by the diversity rerank.

## Formula -> pillar mapping

| Pillar | Preferred formulas |
|---|---|
| Build-in-Public | X3 Confession, X10 How-I Teardown, X8 Story Thread |
| Insight | X1 Contrarian, X2 Data-Point, X7 Listicle-Thread, X9 Curiosity-Gap |
| Engagement | X6 Relatable, X4 Quote-Tweet, reply templates |
| Promotion | X10 (results that imply the product), X2 (your own data) |

## Steps

1. Gather inputs. Ask for theme, audience, pillar preferences if not provided.
2. Validate the pillar mix sums to 100%; warn if any pillar is over 60%.
3. For each day and slot, pick: type (single / long post / thread / Article /
   reply block), pillar, formula (do not over-repeat), angle, posting time
   (audience timezone), goal.
4. Add daily reply/quote-tweet targets with a suggested template.
5. Run the weekly balance check and the goal-mix check; flag anything missing.
6. Return as markdown, plus optional JSON for import.

## Example

See `references/example-week.md` for a filled-in 7-day plan.

## Files

- `SKILL.md` - this file
- `references/example-week.md` - worked 7-day plan
- `references/pillars-framework.md` - the X pillar discipline and the cadence the code rewards
- `../../references/algorithm-heuristics.md` - posting rules derived from X's ranking code

## Related skills

- `x-post-writer` - draft each single tweet from the plan
- `x-thread-builder` - draft each thread from the plan
- `x-reply-drafter` - execute the daily reply targets
- `x-hook-extractor` - study competitors' posts while planning
- `x-research` - find what the niche is discussing this week before picking angles
- `x-article` - draft the week's Article
