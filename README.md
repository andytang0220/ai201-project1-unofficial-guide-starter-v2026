# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

I picked the city_guides corpus. The system answers questions about specific 
towns/villages relating to getting there, getting around, eating and drinking, 
what to see, where to stay, when to go, and practical notes. It also answers 
questions about general accessibility, seasonality, walking, and eating in the 
region. 

## Chunking Strategy

**Chunk size: 800**
**Overlap: 120**

The chunking strategy does not use an arbitrary chunk size and overlap. These are 
reserved for the fallback strategy. The primary strategy chunks based on sections.
Since the documents in the city_guides corpus are all sectioned out with headers, 
it was advantageous to chunk based on these since it guarantees no cut off 
sentences and thus complete thoughts. Additionally, document headers are injected 
into the chunks to provide them with context on what town is being referenced.

## Sample Chunks

**Chunk 1** — source: guide_accessibility.md#0 `` — produced by: chunker.py::split_documents``
Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.
```
```

**Chunk 2** — source: guide_corry_vale.md#5 `` — produced by: chunker.py::split_documents``
Corry Vale — Where to stay

Perhaps thirty beds in the entire valley, spread across two pubs and a handful of farmhouse rooms. In summer these are booked months ahead. Camping is permitted on two marked fields and nowhere else.
```
```

**Chunk 3** — source: guide_givens_mill.md#2 `` — produced by: chunker.py::split_documents``
Givens Mill — Getting around

Everything is on one street along the river. The mill is at one end and the church at the other, eight minutes apart. The riverside path continues in both directions for as far as you want to walk.
```
```

**Chunk 4** — source: guide_kestrelford.md#4 `` — produced by: chunker.py::split_documents``
Kestrelford — What to see

The market square on a Saturday morning is the main event and has run continuously since the 1400s. The parish church has a 13th-century tower you can climb for £2. The old trackbed walk runs six miles to the next village along an easy gradient and is the best half-day here.
```
```

**Chunk 5** — source: guide_pellew_sands.md#6 `` — produced by: chunker.py::split_documents``
Pellew Sands — When to go

June and September for the beach without the crowds. July and August are busy and the town is at its most itself, for better and worse. Winter is bleak, largely closed, and has a following among people who like that sort of thing.
```
```

## Sample Answer

**Question:**
python .\app.py --variant headings ask "What is the most accessible town in the region on foot?"

**Answer:**
   (best distance 0.481, cutoff 0.65)

According to `guide_walking.md`, Thornby Wells is the region's most accessible town on foot, featuring flat, formal gardens and level streets.

Sources retrieved: guide_accessibility.md, guide_corry_vale.md, guide_walking.md

1 model calls this session, 703 tokens (671 in, 32 out)

```
```

**My relevance cutoff:**

Threshold set to 0.65. Adjust up from the starter 0.6 since original was too 
close to the closest distance of test questions 1 and 5. 0.65 was a value that 
was closer to the middle point of the two groupings.

| Question | In corpus? | Best distance |
|---|---|---|
|"What is the most accessible town in the region on foot?"|Yes|0.481|
|"When is the busiest time for Halden Bay?"|Yes|0.277|
|"What hours do the Kestrelford pubs serve food in the evening?"|Yes|0.172|
|"How many rooms does the Elder Ness pub have?"|Yes|0.177|
|"What regions are difficult to get around for those with limited mobility"|Yes|0.4268|
|"What is the capital of Mongolia?"|No|0.808|
|"How do I change the oil in a diesel engine?"|No|0.881|
|"Who won the 1994 World Cup?"|No|0.982|
|"What is the recommended dosage of ibuprofen for a headache?"|No|0.835|
|"How do I write a for loop in Rust?"|No|0.859|

## How I Used AI

**1.**
I asked Claude to check over my idea to chunk by sections. It identified to me 
the issue of section chunks not having any context on which town they are about. 
This led to the addition of headers to each section chunk.
**2.**
I used Claude to implement the chunking by sections strategy.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
