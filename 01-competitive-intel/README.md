# 01 · Competitive Battlecard Generator

A Claude skill that turns two company names into a fully sourced, sales-ready battlecard pack (PDF): competitor profile, live-call card, proof and data card, answer key, and a clickable source log.

**Worked example:** Genspark vs Manus. See [`example-output/genspark-vs-manus-battlecards.pdf`](example-output/genspark-vs-manus-battlecards.pdf). It uses public information only, as a portfolio exercise, and is not affiliated with either company.

## What it does
- Researches both companies from first-party pages, press, review sites and independent reviews.
- Tags every claim: CR company-reported · 3P third-party · RV review-based · UV unverified.
- Builds five A4-landscape pages with colour-coded wins, concessions and red flags.
- Writes answers for every question and objection, so reps are never stuck.
- Ends with a "Verify before use" list, so nothing unchecked is passed off as fact.

## How to use it
1. Add `SKILL.md` as a skill in Claude (Settings, Capabilities, Skills, upload this folder as a zip), or paste its contents into a Claude Project's instructions.
2. Ask: *"Build a battlecard: us = <Company A>, competitor = <Company B>, for AEs selling to <buyer>."*
3. Claude asks up to three questions, researches, builds the PDF and lists what to verify.

## Folder
```
SKILL.md                      the skill (instructions Claude follows)
references/                   design spec, research protocol, best-practice notes
assets/
  build_battlecards_example.py  working template; copy, replace content
  logos/                      example logo files (partners named in a press release)
example-output/               the finished Genspark vs Manus PDF
```

## Run the example script yourself
```
pip install playwright
python3 assets/build_battlecards_example.py out.pdf out.html
```
Set `CHROME` to your Chrome/Chromium path if it is not `/usr/bin/google-chrome`.

## Notes
- Logos are shown only for partners and backers named in the vendor's own press release and belong to their owners. Remove or replace them for your own use.
- Figures in the example were verified on 1 Nov 2026 and will go stale; re-check before reuse.
- Italic text on a card means guidance for sales, not customer-facing copy.
