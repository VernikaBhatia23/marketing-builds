# Design spec

Derived from best-in-class battlecard patterns (sources at the bottom of `battlecard-best-practices.md`).

## Format
A4 landscape (297 × 210 mm), 5 pages, 10 mm side margins. Print backgrounds on. Inter (with Inter Display for headline numbers); fall back to a clean sans-serif.

## Principles
- One screen, scanned in ~15 seconds: strongest facts first, tables over paragraphs.
- Talk-track language, not archive prose.
- Colour carries meaning, never decoration: indigo = us, teal = them, green = we win/positive, amber = careful/unverified, red = lose/red flag.
- Every claim carries a small numbered citation `[n]` linking to the source, plus a CR/3P/RV/UV tag.
- "Last verified" date and "next review" date in each page header.
- Italic = guidance for sales. Plain text in quotes = words to say.

## Tokens
```
ink #101828   muted #566074   line #DDE2EA   surface #F4F6F9
us #3A3FD6 (tint #ECEDFD)   them #0E7C86 (tint #E1F2F3)
win #17794A (tint #E2F4EA)  care #8F5400 (tint #FFF0D1)  lose #B3261E (tint #FCE7E4)
```
Body 8.2pt, never below 6.5pt. Headline numbers 13–14pt Inter Display bold. Section titles 9.2pt bold.

## Components
- **Header**: title, one italic guidance line, right-aligned meta (verified date, scope note, italic-guidance note, tag key).
- **Tiles** (5 across): big value, small caption with citation and tag.
- **Section with left rule**: coloured left border by meaning (teal neutral, green positive, red negative, amber careful).
- **Stance chip**: Press (green), Careful (amber), Concede (red).
- **Score bar**: label, bar scaled to /5, value, small sub-line with count and citation.
- **Quote box**: verbatim text, source line (site, stars, month, citation), left border in section colour.
- **Wordmark chips / logos**: real logo files only, uniform 10 mm tall boxes. Text chips where no logo is available.

## Page-fit rules
Check each page visually; no scroll or clipped text. If a page overflows, cut words before shrinking type. Leave breathing room rather than filling the page.
