---
name: competitive-battlecard-generator
description: Build a researched, fully sourced head-to-head sales battlecard pack (profile card, live-call card, proof card, answer key, source log) as a PDF for any two competing companies. Use when asked for a battlecard, competitive card, or "us vs them" sales enablement.
---

# Competitive Battlecard Generator

Produces a 5-page A4-landscape PDF for one head-to-head: **"us" vs one competitor**. Every claim carries a numbered, clickable source and a confidence tag. Built for sales reps who have about 15 seconds to scan during a call.

## 1. Before you start: confirm four things (ask at most three questions)

1. **Us and Them.** Which company is "us" (the side the reps sell) and which is the competitor.
2. **Audience.** Who uses the card (AEs, SDRs, CSMs) and typical buyer (role, company size).
3. **Real or exercise.** Real internal use, or a portfolio exercise on public information only. For an exercise, say so on every page.
4. **Today's date.** Stamp "Verified <date>" and "next review <date + 30 days>" on every page.

If the user already answered, don't ask again. Start with one sentence saying what you are about to do.

## 2. Research (public sources first, record as you go)

For both companies, collect and keep a running table of `fact | URL | date seen | tag`.

Look for: HQ and headcount; funding and revenue claims; ownership or regulatory news; product launches with dates; pricing and credit or usage rules; review-site scores and review counts; verbatim user quotes; named partners and customers; security certifications; public roadmap.

Source priority:
1. First-party pages (pricing, docs, press releases, security page).
2. Wire releases and major press.
3. Review sites (Trustpilot, G2, Capterra, app stores): open the page itself, not a summary.
4. Independent reviews and comparison articles.
5. Vendor-written "alternative to X" pages count as marketing. Use them only to see what the vendor concedes.

Tools: web search and scrape. If a site is blocked, say so and move on. Never work around a block.

### Confidence tags (put one on every figure or claim)
- **CR**: company-reported (press release, own site, founder statement). Not audited.
- **3P**: third-party analysis or reporting.
- **RV**: review-based (user reviews, ratings, quotes).
- **UV**: unverified or conflicting. Appears in one source only, or sources disagree.

### Hard rules
- **Never print a URL you did not open or see in a result.** Do not guess links.
- **Quotes must be verbatim**, with site, star rating if shown, and month. Do not paraphrase inside quote marks.
- **Check each review page for banners.** A platform may withhold or flag a rating (this happened with Trustpilot for one company in the worked example). If so, do not compare scores on that platform.
- **Conflicting numbers**: show both, tag UV, and add the item to the Verify list. Do not average them.
- **Different dates are not comparable.** Never write "we're bigger" from figures dated months apart.
- **One-source claims** (a single tear sheet, a social post) stay out of the cards. Mention them in a small footnote tagged UV, or in the Verify list.
- **Be honest where "us" is weaker.** Each weakness of ours gets a "Concede" or "Careful" stance, never a made-up counterpoint.
- **No invented customers, logos, quotes or testimonials.** Show logos only for partners or backers named in a primary source, using real brand files from an icon library. Never draw a logo by hand. If no customers are public, say so on the card.
- Mark judgement ("Read:", win/lose bullets) as analyst inference.
- Label text meant for sales (coaching, instructions) in *italics*, and add the note "Italic text is guidance for sales, not customer-facing." Spoken lines are plain text in quotes.

## 3. The five pages

Follow `references/design-spec.md` for layout and tokens, and use `assets/build_battlecards_example.py` as the working template (copy it, replace the source table and page content, keep the CSS and structure).

| Page | Name | Contents |
|---|---|---|
| 1 | **Card A: Competitor profile** (backup layer) | Five snapshot tiles (HQ, headcount, revenue, ownership, entry price). What they have shipped (dated, with a 4–5 word gloss where useful). Pricing table plus "the catch". Review scores as bars. What users like and dislike, each with two verbatim quotes. Momentum split into green "Working for them" and red "Red flags". |
| 2 | **Card B front: live-call card** | Three boxes: **Win on / Be careful on / Watch for**. Table "Their weakness, our counterpoint" with stance chips (Press / Careful / Concede). Table "Their strength, our response". Landmine questions (3). Discovery questions (2). Objections to expect (names only, scripts on page 4). **When we win** and **When we lose**, 3–4 evidence-backed bullets each. |
| 3 | **Card B back: proof and data** | Four score tiles (revenue run-rate, G2, Trustpilot or equivalent, app store). Pricing side by side. Top use cases. Social-proof strip (named partners and backers with real logos, headline customer count tagged CR, 2–3 verbatim user quotes from review sites). "Verify before this card is used" list. |
| 4 | **Answer key** | For each discovery question: what to say for each likely answer and what to listen for. For each of 4 objections: Acknowledge, Reframe (with a sourced fact), Ask. Include an ownership/security objection if relevant. |
| 5 | **Source log** | Every numbered citation with title, publisher, clickable URL. Numbering follows first appearance. |

Content limits that keep it scannable: no cell over about 25 words; body text at least 7pt; one idea per bullet; at most 3 landmines, 2 discovery questions, 4 objections.

## 4. Build

1. Write all content with its citations first. Then render with the template script using headless Chrome via Playwright (`pip install playwright`; any Chrome/Chromium binary, set `CHROME`).
2. Render to PDF at A4 landscape with backgrounds on.
3. Rasterize each page (`pdftoppm -r 80 -png`) and look at every page.

## 5. QA checklist (do not skip)

- [ ] Every figure and claim on pages 1–4 has a citation number, and each number exists in the source log.
- [ ] Every source URL was opened or seen in a result.
- [ ] Every quote is verbatim and attributed to a real review.
- [ ] No page clips or overflows; footers are clear; text is legible.
- [ ] Dates on compared figures are shown, and not-comparable pairs are warned.
- [ ] Each of our weaknesses has a Concede or Careful stance.
- [ ] Verify list names everything that is unverified, conflicting, or could not be opened.
- [ ] Page-2 questions all have answers on page 4.

## 6. Deliver

Send the PDF. In one short message: what the pack is, what could not be done (e.g. no public customers, blocked sites), and the items on the Verify list. Offer next steps: a Google Slides or Docs version, or a refresh in 30 days.

## Lessons from the worked example (Genspark vs Manus, Nov 2026)

- A platform withheld one company's Trustpilot rating after removing fake reviews. The first draft's "our score is higher" line would have been wrong. Always open the page.
- The same company showed two different G2 scores from different listings. Tag UV and verify.
- A comparison article's URL looked plausible but was never opened. It was removed. Never keep a guessed link.
- Enterprise logos were not available; the strip shows only partners named in the vendor's own press release. That is the honest ceiling for public-only work.
- Pricing pages could not be opened directly, so plan prices came from third-party pages and are tagged 3P.
