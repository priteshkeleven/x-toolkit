# Article structure

What an X Article has to do, in the order the reader meets it. The ranking
facts behind each part are in `../../../references/x-ranking-signals.md`.

## 1. Title: earn the click

The title is most of what the feed shows. A click is weighted 0.3; nothing
after it counts unless it happens.

- Name the payoff, with a number when the material has one: "How we cut deploys
  from 40 minutes to 6", not "Thoughts on CI".
- Under about 70 characters so it does not truncate on mobile.
- Promise only what the Article delivers. A reader who clicks and leaves fast
  is a "not dwelled" signal.

## 2. Cover: readable at thumbnail size

- One idea, large: a chart, a before/after, a single phrase. Not a stock photo.
- High contrast; it is seen at a few hundred pixels wide.
- The first image in the Markdown becomes the cover.

## 3. Opening: earn the stay (first three lines)

Click dwell time is weighted 0.4 per predicted second, the most valuable
attention signal in the ranker. The opening decides whether it accrues.

- Deliver something immediately: the result, the number, or the one-line
  answer. Then promise how the Article earns it.
- No throat-clearing ("In this article I will..."), no definitions of things the
  reader already knows.

## 4. Sections: one payoff each

- H2 headers that read as a table of contents: a reader skimming the headers
  should get the argument.
- One idea per section, with a concrete example, number or screenshot.
- Front-load: the most useful section comes first or second.
- Short paragraphs (2-4 sentences). Lists where the content is a list.
- Images where they replace words (a chart, a diff, a screenshot), not as
  decoration.

## 5. Length: what gets finished

Retrieval is trained to surface posts people read all the way through. Length
the material earns, then stop.

| Material | Typical length |
|---|---|
| One process with steps | 800-1,500 words |
| An argument with evidence | 1,200-2,500 words |
| A reference guide | as long as the reference, with headers that make it skimmable |

If a section could be cut without the reader missing it, cut it.

## 6. Ending: give the next step

- End on the most useful line or a short summary of the steps.
- One ask at most: follow for the next one (say what it will be), or a specific
  question to reply to. A follow is weighted 4.

## Before handing off

- [ ] Title names the payoff and fits about 70 characters.
- [ ] Cover reads at thumbnail size.
- [ ] First three lines deliver something.
- [ ] Every H2 section pays off; nothing to cut.
- [ ] Numbers and names come from the user or the Story Bank, none invented.
- [ ] Humanizer pass done; em dashes about 1 per 100 words.
- [ ] Every image exists locally (`missing_images` is 0).
