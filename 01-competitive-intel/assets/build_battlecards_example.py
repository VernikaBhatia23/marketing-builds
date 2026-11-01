#!/usr/bin/env python3
"""Worked example: builds the 5-page Genspark vs Manus battlecard PDF (A4 landscape).
Copy this file, replace the content (S sources dict + the five page_* functions), keep the CSS and structure.
Usage: python3 build_battlecards_example.py out.pdf out.html
Needs: pip install playwright && a Chrome/Chromium binary (set CHROME below)."""
import sys, asyncio, re, base64, os
from playwright.async_api import async_playwright

OUT_PDF, OUT_HTML = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = os.environ.get("CHROME", "/usr/bin/google-chrome")

def L(name):
    """Inline an SVG logo from assets/logos as a data URI. Only use logos you are entitled to show."""
    with open(os.path.join(HERE, "logos", name + ".svg"), "rb") as f:
        return "data:image/svg+xml;base64," + base64.b64encode(f.read()).decode()

# ---- SOURCES: key -> (title, publisher, url). Only add URLs you actually opened or saw in results.

S = {
 'ph':      ("Manus launch history", "Product Hunt", "https://www.producthunt.com/products/manus/launches"),
 'ph_mm':   ("Manus launches (2025-26)", "Product Hunt", "https://www.producthunt.com/products/manus/launches/manus-meeting-minutes"),
 'ciw':     ("Manus: $500M to $2B in 8 months", "CIW News", "https://www.ciw.news/p/manus-100m-arr"),
 'scmp':    ("Manus hits US$100M revenue milestone", "SCMP", "https://www.scmp.com/tech/tech-trends/article/3336925/manus-hits-us100-million-revenue-milestone-global-competition-ai-agents-heats"),
 'sacra':   ("Manus company profile", "Sacra", "https://sacra.com/research/manus"),
 'sacra90': ("Manus at $90M/year", "Sacra", "https://sacra.com/research/manus-at-90m-year/"),
 'latka':   ("Manus revenue and team size", "Latka", "https://getlatka.com/companies/manus.im"),
 'svic_m':  ("Manus tear sheet", "Silicon Valley Invest Club", "https://siliconvalleyinvestclub.com/hi/companies/manus/tear-sheet.pdf"),
 'aie':     ("Manus organisation page", "AI Engineer", "https://www.ai.engineer/orgs/manus"),
 'bbg':     ("China blocks Meta's $2B Manus deal", "Bloomberg", "https://www.bloomberg.com/news/articles/2026-04-27/china-blocks-meta-s-2-billion-acquisition-of-ai-startup-manus"),
 'tnw':     ("Meta cuts Manus off from internal systems", "The Next Web", "https://thenextweb.com/news/meta-manus-data-split-china-unwind-acquisition"),
 'ground':  ("Manus to resume independent operations", "Ground News", "https://ground.news/article/manus-to-resume-independent-operations-in-unwind-of-meta-deal"),
 'm_bo':    ("What is Manus Browser Operator?", "Manus docs (first-party)", "https://www.manus.im/docs/integrations/manus-browser-operator"),
 'altto':   ("Manus unveils Wide Research mode", "AlternativeTo", "https://alternativeto.net/news/2025/7/manus-unveils-new-wide-research-mode-enabling-100-parallel-ai-agents-for-scalable-tasks"),
 'm_help':  ("Current membership pricing for Manus", "Manus Help Center (first-party)", "https://help.manus.im/en/articles/11711111"),
 'mck':     ("Manus pricing", "Justin McKelvey", "https://justinmckelvey.com/blog/manus-pricing"),
 'carly':   ("Manus pricing (2026)", "Carly", "https://www.usecarly.com/blog/manus-pricing/"),
 'spec':    ("Manus AI pricing plans guide 2026", "SpectrumAI Lab", "https://spectrumailab.com/blog/manus-ai-pricing-plans-cost-guide-2026"),
 'aitr':    ("Manus AI review 2026", "AI Tools Radar", "https://ai-tools-radar-3ly.pages.dev/blog/reviews/manus-ai-review-2026/"),
 'usage':   ("Cloud Computer basic tier dropped", "UsagePricing", "https://www.usagepricing.com/blueprint/activity/manus-2026-10-15-cloud-computer-basic-tier-dropped"),
 'zem':     ("Manus AI reviews 2026", "Zemith", "https://www.zemith.com/en/learn/manus-review"),
 'preuve_m':("Manus AI review (2026)", "Preuve", "https://preuve.ai/blog/manus-ai-review"),
 'g2_m':    ("Manus AI agent reviews", "G2", "https://g2.com/products/manus-ai-agent/reviews"),
 'tp_m':    ("Manus reviews", "Trustpilot", "https://www.trustpilot.com/review/manus.im?page=1"),
 'superapp':("Manus AI review 2026", "Superapp", "https://www.superappp.com/blog/manus-ai-review-2026-pricing-reviews-is-it-worth-it"),
 'aipedia': ("Manus vs Genspark vs ChatGPT Tasks", "Aipedia", "https://aipedia-en.pages.dev/compare/manus-vs-genspark-vs-chatgpt-tasks"),
 # Genspark
 'svic_g':  ("Genspark company profile", "Silicon Valley Invest Club", "https://siliconvalleyinvestclub.com/zh-TW/companies/genspark/"),
 'bw_g':    ("Genspark funding and ARR announcement", "Business Wire", "https://www.businesswire.com/news/home/20260617758937/en/"),
 'inkl':    ("Genspark valued at $2.6B", "Reuters via inkl", "https://www.inkl.com/news/ai-startup-genspark-valued-at-2-6-billion-in-latest-funding-round"),
 'tip':     ("Genspark launches AI Workspace 6.0", "TechIntelPro (Business Wire)", "https://techintelpro.com/news/ai/agentic-ai/genspark-launches-ai-workspace-60-with-persistent-memory"),
 'gs_blog': ("Introducing Genspark AI Workspace 6.0", "Genspark blog (first-party)", "https://genspark.ai/blog/genspark-ai-workspace-6"),
 'cw':      ("Genspark AI Workspace 6.0 and SecondBrain Note", "Computer Weekly", "https://www.computerweekly.com/blog/Inspect-a-Gadget/Genspark-AI-Workspace-60-SecondBrain-Note"),
 'dt':      ("Genspark unveils AI Workspace 6.0", "Digital Today", "https://www.digitaltoday.co.kr/en/view/84794/genspark-unveils-persistent-memory-based-ai-workspace-6-0-launches-first-hardware"),
 'preuve_g':("Genspark review (2026)", "Preuve", "https://preuve.ai/blog/genspark-review"),
 'eesel':   ("Genspark AI pricing (2026)", "eesel", "https://www.eesel.ai/blog/genspark-ai-pricing"),
 'tp_g':    ("Genspark reviews (3.5 / 310)", "Trustpilot", "https://www.trustpilot.com/review/genspark.ai?page=10"),
 'tp_g_uk': ("Genspark reviews (2.9 / 226)", "Trustpilot UK", "https://uk.trustpilot.com/review/genspark.ai?page=9"),
 'tp_g_nz': ("Genspark reviews, slides feedback", "Trustpilot NZ", "https://nz.trustpilot.com/review/genspark.ai?page=3"),
 'app_g':   ("Genspark AI Workspace app listing", "App Pricing Lab", "https://apppricinglab.com/app/apple/6739554054"),
 'claw':    ("Genspark extends Series B, launches AI employee", "Let's Data Science", "https://letsdatascience.com/news/genspark-extends-series-b-launches-ai-employee-7996040f"),
 'rank':    ("Genspark vs Manus", "AI Agent Rank", "https://aiagentrank.io/compare/genspark-vs-manus"),
}

CSS0 = """
@page { size: 297mm 210mm; margin: 0; }
:root{--ink:#101828;--mut:#566074;--line:#DDE2EA;--sur:#F4F6F9;
--us:#3A3FD6;--ust:#ECEDFD;--them:#0E7C86;--tht:#E1F2F3;
--win:#17794A;--wint:#E2F4EA;--care:#8F5400;--caret:#FFF0D1;--lose:#B3261E;--loset:#FCE7E4}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff}
body{font-family:'Inter',sans-serif;color:var(--ink);font-size:8.2pt;line-height:1.36;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:9mm 10mm 7mm;display:flex;flex-direction:column;gap:3.2mm;page-break-after:always;overflow:hidden;position:relative}
.page:last-child{page-break-after:auto}
a{color:inherit;text-decoration:none}
sup.c{font-size:5.6pt;line-height:0;vertical-align:super;margin-left:1px;font-weight:600;color:var(--us);white-space:nowrap}
sup.c a{color:var(--us)}
b,strong{font-weight:650}
/* header */
.hd{display:flex;justify-content:space-between;align-items:flex-end;gap:8mm;padding-bottom:2.6mm;border-bottom:1.6pt solid var(--ink)}
.hd .t1{font-family:'Inter Display','Inter',sans-serif;font-weight:700;font-size:27pt;line-height:1;letter-spacing:-.02em}
.hd .t1 span{font-weight:500;color:var(--mut)}
.hd .t2{margin-top:1.6mm;color:var(--mut);font-size:8.6pt;max-width:165mm}
.hd .meta{text-align:right;font-size:7.2pt;color:var(--mut);line-height:1.5;flex:none}
.hd .meta b{color:var(--ink)}
.keyrow{display:flex;gap:2mm;justify-content:flex-end;margin-top:1.4mm}
/* tags */
.tg{display:inline-block;font-size:5.8pt;font-weight:700;padding:.4pt 3pt;border-radius:2pt;margin-left:2px;vertical-align:1px;letter-spacing:.02em}
.tg.cr{background:var(--ust);color:var(--us)}
.tg.3p{background:#E8EBF0;color:#3B4659}
.tg.rv{background:#EFE7FB;color:#5B2DA8}
.tg.uv{background:var(--caret);color:var(--care);outline:.6pt solid #E3B25A}
/* tiles */
.tiles{display:grid;grid-template-columns:repeat(5,1fr);gap:2.4mm}
.tile{background:var(--sur);border-radius:2mm;padding:2.4mm 3mm;border-top:2pt solid var(--them)}
.tile .v{font-family:'Inter Display','Inter';font-size:14.5pt;font-weight:700;letter-spacing:-.01em;line-height:1.1}
.tile .l{margin-top:.8mm;color:var(--mut);font-size:7.2pt;line-height:1.35}
/* sections */
.grid3{display:grid;gap:3mm;flex:1;min-height:0}
.sec{border-left:2.2pt solid var(--them);padding:0 0 0 2.6mm;min-height:0;overflow:hidden}
.sec h3{font-size:9.2pt;font-weight:700;margin-bottom:1.4mm;letter-spacing:-.005em}
.sec.win{border-color:var(--win)} .sec.risk{border-color:var(--lose)} .sec.care{border-color:#D69A2D} .sec.us{border-color:var(--us)}
ul.l{list-style:none} ul.l li{position:relative;padding-left:3mm;margin-bottom:1.1mm}
ul.l li:before{content:"";position:absolute;left:.2mm;top:1.5mm;width:1.4mm;height:1.4mm;border-radius:50%;background:var(--them)}
.sec.win ul.l li:before{background:var(--win)} .sec.risk ul.l li:before{background:var(--lose)}
.tl{display:grid;grid-template-columns:15mm 1fr;gap:.8mm 2mm}
.tl .d{color:var(--them);font-weight:650;font-size:7.4pt}
.tl .x{margin-bottom:.4mm}
.note{margin-top:1.6mm;background:var(--sur);border-radius:1.6mm;padding:1.6mm 2.2mm;font-size:7.4pt;color:#33405a}
table.pr{width:100%;border-collapse:collapse;font-size:7.7pt}
table.pr td{padding:1.1mm 1mm;border-bottom:.5pt solid var(--line);vertical-align:top}
table.pr td:first-child{font-weight:650;white-space:nowrap;padding-left:0;width:19mm}
/* bars */
.bar{display:grid;grid-template-columns:23mm 1fr 11mm;align-items:center;gap:2mm;margin-bottom:1.5mm}
.bar .nm{font-size:7.5pt;font-weight:600}
.bar .tr{height:3.6mm;background:#E7EBF1;border-radius:1mm;position:relative;overflow:hidden}
.bar .fl{position:absolute;left:0;top:0;bottom:0;border-radius:1mm}
.bar .nv{font-weight:700;font-size:8.4pt;text-align:right}
.bar .sub{grid-column:2/4;font-size:6.9pt;color:var(--mut);margin-top:-1mm;margin-bottom:.4mm}
/* card B */
.top3{display:grid;grid-template-columns:repeat(3,1fr);gap:2.4mm}
.top3 div{border-radius:2mm;padding:2mm 3mm;font-size:8pt}
.top3 .k{font-weight:700;font-size:8.6pt;display:block;margin-bottom:.4mm}
.top3 .w{background:var(--wint);color:#0C4A2B} .top3 .cc{background:var(--caret);color:#5A3500} .top3 .ww{background:var(--loset);color:#6E150F}
.cols{display:grid;grid-template-columns:1.62fr 1fr;gap:4mm;flex:1;min-height:0}
.blk{margin-bottom:2.6mm}
.blk>h3{font-size:9.2pt;font-weight:700;margin-bottom:1.2mm;display:flex;align-items:center;gap:1.6mm}
.blk>h3 i{font-style:normal;font-weight:500;color:var(--mut);font-size:7.4pt}
.row{display:grid;grid-template-columns:1fr 3.2mm 1.25fr 13mm;gap:1.8mm;align-items:start;padding:1.5mm 0;border-top:.5pt solid var(--line)}
.row:first-of-type{border-top:none}
.row .th{color:#3B4659}
.row .ar{color:#9AA3B2;font-size:9pt;line-height:1.1;text-align:center}
.row .us{color:var(--ink)}
.chip{font-size:6.6pt;font-weight:700;border-radius:8pt;padding:.7mm 0;text-align:center;display:block}
.chip.p{background:var(--wint);color:var(--win)} .chip.cr2{background:var(--caret);color:var(--care)} .chip.co{background:var(--loset);color:var(--lose)}
.colh{display:grid;grid-template-columns:1fr 3.2mm 1.25fr 13mm;gap:1.8mm;font-size:6.9pt;color:var(--mut);font-weight:600;padding-bottom:.8mm;border-bottom:1pt solid var(--ink)}
.box{border-radius:2mm;padding:2.2mm 3mm;margin-bottom:2.4mm}
.box h4{font-size:8.6pt;margin-bottom:1mm}
.box.q{background:var(--ust)} .box.o{background:var(--sur)} .box.w{background:var(--wint)} .box.l{background:var(--loset)}
.box ol{padding-left:3.6mm} .box ol li{margin-bottom:1mm}
.say{font-style:italic;color:#1d2a44}
.al{display:grid;grid-template-columns:11mm 1fr;gap:.4mm 1.5mm;margin-bottom:1.1mm}
.al b{color:var(--us);font-size:7.4pt}
.small{font-size:7.1pt;color:var(--mut)}
.ft{margin-top:auto;display:flex;justify-content:space-between;font-size:6.6pt;color:var(--mut);border-top:.5pt solid var(--line);padding-top:1.4mm}
.ft b{color:var(--ink)}
.cmp{width:100%;border-collapse:collapse;font-size:7.8pt}
.cmp th{font-size:7.4pt;text-align:left;padding:1mm 1.4mm;border-bottom:1pt solid var(--ink);font-weight:700}
.cmp th.g{color:var(--us)} .cmp th.m{color:var(--them)}
.cmp td{padding:1.1mm 1.4mm;border-bottom:.5pt solid var(--line);vertical-align:top}
.cmp td:first-child{font-weight:650;width:22mm;color:var(--mut)}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:3mm}
.dash{border:.8pt dashed #9AA3B2;border-radius:2mm;padding:2.2mm 3mm;color:var(--mut)}
.warn{background:var(--caret);color:#5A3500;border-radius:1.6mm;padding:1.6mm 2.4mm;font-size:7.4pt;margin-top:1.4mm}
/* source log */
.slog{columns:2;column-gap:8mm;font-size:6.8pt;line-height:1.25}
.slog div{break-inside:avoid;display:grid;grid-template-columns:6mm 1fr;margin-bottom:.8mm}
.slog .n{color:var(--us);font-weight:700}
.slog .u{color:var(--mut);font-size:5.6pt;word-break:break-all}
"""

S.update({
 'tp_m_main': ("Manus reviews: 1.2 from 210", "Trustpilot", "https://www.trustpilot.com/review/manus.im"),
 'superapp':  ("Manus AI review (2026)", "Superapp", "https://superapp.dev/blog/manus-ai-review-2026-pricing-reviews-is-it-worth-it"),
 'tp_g_main': ("Genspark reviews: 483, rating withheld", "Trustpilot", "https://www.trustpilot.com/review/genspark.ai"),
 'g2_g':      ("Genspark AI: 4.3 from 20 reviews", "G2", "https://www.g2.com/sellers/genspark-ai"),
 'lindy':     ("Genspark AI review 2026", "Lindy", "https://www.lindy.ai/blog/genspark-review"),
 'bw_ms':     ("Genspark and Microsoft strategic partnership", "Business Wire", "https://www.businesswire.com/news/home/20260429907387/en/Genspark-Announces-Global-Strategic-Partnership-with-Microsoft-to-Embed-AI-Agents-Across-Microsoft-365-and-Agent-365"),
 'gs_biz':    ("Genspark for Business", "Genspark (first-party)", "https://www.genspark.ai/business"),
 'aiide':     ("Genspark vs Manus", "AI IDE List", "https://aiidelist.com/blog/genspark-vs-manus"),
})

ORDER = []
def c(*keys):
    out = []
    for k in keys:
        if k not in ORDER: ORDER.append(k)
        out.append(f'<a href="{S[k][2]}">{ORDER.index(k)+1}</a>')
    return '<sup class="c">[' + ','.join(out) + ']</sup>'
def tg(kind): return f'<span class="tg {kind.lower()}">{kind}</span>'
def g(t): return f'<span class="g">{t}</span>'

CSS = CSS0 + """
.g{font-style:italic;color:#4A5876}
.say{font-style:normal;color:#1d2a44}
.q{font-size:7.6pt;line-height:1.35;background:#fff;border-radius:1.4mm;padding:1.4mm 2mm;margin-top:1.3mm;border-left:2pt solid var(--them)}
.q .by{display:block;font-size:6.5pt;color:var(--mut);margin-top:.4mm}
.sec.win .q{border-color:var(--win);background:#F3FAF6} .sec.risk .q{border-color:var(--lose);background:#FDF4F3}
.q.us2{border-color:var(--us);background:#F4F4FE}
.good li:before{background:var(--win)!important} .bad li:before{background:var(--lose)!important}
.good li b{color:var(--win)} .bad li b{color:var(--lose)}
.pill{display:inline-block;border-radius:8pt;padding:.3mm 2.4mm;font-size:6.6pt;font-weight:700;margin-bottom:1.2mm}
.pill.gr{background:var(--wint);color:var(--win)} .pill.rd{background:var(--loset);color:var(--lose)}
.cols2{display:grid;grid-template-columns:1.18fr 1fr;gap:4mm;flex:1;min-height:0}
.row2{display:grid;grid-template-columns:1fr 3mm 1.25fr 12.5mm;gap:1.6mm;align-items:start;padding:1.25mm 0;border-top:.5pt solid var(--line);font-size:7.7pt}
.score{display:grid;grid-template-columns:repeat(4,1fr);gap:2.2mm;margin-bottom:2.4mm}
.sc{border-radius:2mm;background:var(--sur);padding:2mm 2.4mm}
.sc .h{font-size:6.8pt;color:var(--mut);font-weight:600}
.sc .a{display:flex;justify-content:space-between;align-items:baseline;margin-top:.6mm}
.sc .a b{font-family:'Inter Display','Inter';font-size:13pt;color:var(--us);letter-spacing:-.01em}
.sc .a i{font-style:normal;font-family:'Inter Display','Inter';font-weight:700;font-size:13pt;color:var(--them)}
.sc .a span{font-size:6pt;color:var(--mut)}
.sc .n{font-size:6.6pt;color:var(--mut);margin-top:.6mm;line-height:1.3}
.wm{display:flex;flex-wrap:wrap;gap:1.6mm;margin:1.2mm 0}
.wm span{border:.8pt solid var(--line);border-radius:1.4mm;padding:1.3mm 3mm;font-weight:700;font-size:8.6pt;letter-spacing:-.01em;background:#fff}
.wm.lg span{display:flex;align-items:center;justify-content:center;min-width:24mm;height:10mm;padding:1mm 3mm}
.wm.inv span.tx{font-size:7.6pt}
.wm.inv span{background:var(--sur);color:#3B4659;font-weight:600}
.qb{background:var(--ust);border-radius:2mm;padding:2.2mm 3mm;margin-bottom:1.8mm}
.qb p{font-size:8pt;line-height:1.38}.qb .by{font-size:6.6pt;color:var(--mut);margin-top:.6mm}
.ak{display:grid;grid-template-columns:1fr 1fr;gap:3.2mm}
.ak .card{border:.8pt solid var(--line);border-radius:2mm;padding:2.4mm 3mm}
.ak h4{font-size:8.8pt;margin-bottom:1.3mm}
.ak .st{display:grid;grid-template-columns:15mm 1fr;gap:.4mm 2mm;margin-bottom:1mm;font-size:7.7pt}
.ak .st b{font-size:6.9pt;color:var(--us);text-transform:none}
"""

KEY = f'{tg("CR")} company-reported {tg("3P")} third-party {tg("RV")} review-based {tg("UV")} unverified'
def hd(title_html, sub, size=27, extra=''):
    return f"""<div class="hd"><div><div class="t1" style="font-size:{size}pt">{title_html}</div>
   <div class="t2">{sub}</div></div>
  <div class="meta"><b>Verified 1 Nov 2026</b> &nbsp;&middot;&nbsp; next review 1 Dec 2026<br>Public sources only. Portfolio exercise, not affiliated with either company.<br>{g('Italic text is guidance for sales, not customer-facing.')}
   <div class="keyrow">{KEY}</div></div></div>"""

# ------------------------------------------------------------ page 1
def page_a():
    return f"""
<section class="page" id="pA">
 {hd('Manus <span>profile</span>', g('This is the backup layer. Read it before the call, and keep the head-to-head card open during it.'))}
 <div class="tiles">
  <div class="tile"><div class="v">Singapore</div><div class="l">HQ. Moved from Beijing in mid-2025.{c('ciw')}{tg('3P')}</div></div>
  <div class="tile"><div class="v">About 105 people</div><div class="l">Dec 2025. Sources range from 78 to 137.{c('sacra','latka')}{tg('UV')}</div></div>
  <div class="tile"><div class="v">$100M+ ARR</div><div class="l">Run-rate above $125M incl. usage (Dec 2025). Unaudited.{c('scmp','ciw')}{tg('CR')}</div></div>
  <div class="tile"><div class="v">Independent again</div><div class="l">China ordered Meta's ~$2B deal unwound (Apr 2026).{c('aie','bbg','ground')}{tg('3P')}</div></div>
  <div class="tile"><div class="v">From $20 / month</div><div class="l">Credit-based, so cost per task varies.{c('mck')}{tg('3P')}</div></div>
 </div>

 <div class="grid3" style="grid-template-columns:1.2fr .95fr 1fr">
  <div class="sec"><h3>What they have shipped</h3>
   <div class="tl" style="grid-template-columns:14mm 1fr">
    <div class="d">Mar 2025</div><div class="x">Public launch {g('(general-purpose AI agent)')}{c('ph')}</div>
    <div class="d">May 2025</div><div class="x">Slides and Browser Operator {g('(agent works in your browser)')}{c('ph')}</div>
    <div class="d">Jul 2025</div><div class="x">Wide Research {g('(100+ agents on one job)')}{c('altto')}</div>
    <div class="d">Oct 2025</div><div class="x">Manus 1.5{c('ph_mm')}</div>
    <div class="d">Jan 2026</div><div class="x">Meeting Minutes {g('(AI meeting notes)')}{c('ph')}</div>
    <div class="d">Mar 2026</div><div class="x">My Computer {g('(desktop app)')}{c('ph_mm')}</div>
    <div class="d">May 2026</div><div class="x">Cloud Computer {g('(always-on cloud machine)')} and Scheduled Tasks 2.0 {g('(recurring jobs)')}{c('ph_mm')}</div>
   </div>
   <div class="note"><b>Signature move:</b> Browser Operator uses the customer's own logged-in browser, including paid tools like Crunchbase or Semrush.{c('m_bo')}{tg('CR')}</div>
  </div>

  <div class="sec"><h3>Pricing</h3>
   <table class="pr">
    <tr><td>Free</td><td>300 credits a day, 1,500 a month cap{c('aitr')}{tg('3P')}</td></tr>
    <tr><td>Pro $20</td><td>4,000 credits a month{c('mck','m_help')}{tg('3P')}</td></tr>
    <tr><td>Pro $40</td><td>8,000 credits, 7-day trial{c('mck','m_help')}{tg('3P')}</td></tr>
    <tr><td>Team</td><td>From $20 a seat; annual saves ~17%{c('spec')}{tg('3P')}</td></tr>
    <tr><td>Add-on</td><td>Cloud Computer, $30 or $50{c('usage')}{tg('UV')}</td></tr>
   </table>
   <div class="note"><b>The catch:</b> one task can cost 200 to 9,000 credits,{c('carly')} and unused monthly credits are cleared at renewal.{c('tp_m_main')}</div>
  </div>

  <div class="sec"><h3>How reviewers rate it <span style="font-weight:500;color:var(--mut);font-size:7.2pt">(out of 5)</span></h3>
   <div class="bar"><div class="nm">App Store</div><div class="tr"><div class="fl" style="width:94%;background:var(--win)"></div></div><div class="nv">4.7</div><div class="sub">About 39K ratings{c('preuve_m')}{tg('RV')}</div></div>
   <div class="bar"><div class="nm">G2 (two views)</div><div class="tr"><div class="fl" style="width:86%;background:#6AA78B"></div></div><div class="nv">4.3</div><div class="sub">vs 2.5 from 6 on the listing I read{c('zem','g2_m')}{tg('UV')}</div></div>
   <div class="bar"><div class="nm">Trustpilot</div><div class="tr"><div class="fl" style="width:24%;background:var(--lose)"></div></div><div class="nv">1.2</div><div class="sub">210 reviews, 94% one-star, 176 in last 12 months{c('tp_m_main','preuve_m')}{tg('RV')}</div></div>
   <div class="note">{g('Read: app users like it; billing and support reviewers do not. Analyst inference.')}</div>
  </div>
 </div>

 <div class="grid3" style="grid-template-columns:1fr 1fr 1fr">
  <div class="sec win"><h3>What users like</h3><ul class="l good">
   <li>Autonomous browsing and multi-step extraction when a task succeeds{c('zem')}{tg('RV')}</li>
   <li>Works in your own logged-in browser{c('m_bo')}{tg('CR')}</li>
   <li>Runs long sessions without hand-holding{c('aipedia')}{tg('3P')}</li></ul>
   <div class="q">&ldquo;I've been a pro user for a few months now. Built some really cool web CRM systems.&rdquo;<span class="by">Trustpilot reviewer, 1 star overall{c('tp_m_main')}</span></div>
   <div class="q">&ldquo;I was able to find a genuine differentiation with Manus from the other AIs.&rdquo;<span class="by">Trustpilot reviewer, 1 star overall{c('tp_m_main')}</span></div></div>
  <div class="sec risk"><h3>What users dislike</h3><ul class="l bad">
   <li>Credits drain on failed or looping tasks{c('zem')}{tg('RV')}</li>
   <li>Unused credits expire; one review lost 31,132 after upgrading{c('tp_m_main')}{tg('RV')}</li>
   <li>Support is mostly bots; refund fights drag on{c('tp_m_main')}{tg('RV')}</li></ul>
   <div class="q">&ldquo;I ran a prompt and spent 10k (yes, TEN THOUSAND) credits.&rdquo;<span class="by">Trustpilot reviewer, Sep 2026{c('tp_m_main')}</span></div>
   <div class="q">&ldquo;Upgrading your tier on Manus AI is instant, but downgrading is practically impossible.&rdquo;<span class="by">Trustpilot reviewer, Sep 2026{c('tp_m_main')}</span></div></div>
  <div class="sec"><h3>Momentum and watch-list</h3>
   <span class="pill gr">Working for them</span><ul class="l good">
   <li><b>$100M+ ARR</b> about 8 months after launch{c('scmp')}{tg('CR')}</li>
   <li><b>8 product releases</b> from May 2025 to May 2026, up to a cloud computer{c('ph_mm')}</li></ul>
   <span class="pill rd" style="margin-top:1mm">Red flags</span><ul class="l bad">
   <li><b>Ownership unsettled.</b> Founders reportedly want a $1B buyback{c('tnw')}{tg('3P')}</li>
   <li><b>Trust gap:</b> 1.2 on Trustpilot, 94% one-star{c('tp_m_main')}</li>
   <li><b>No public roadmap</b> found</li></ul>
   <div class="small" style="margin-top:.8mm">Unverified, not used on the card: $400 to $500M run-rate (Jun 2026){c('svic_m')}{tg('UV')}</div></div>
 </div>
 <div class="ft"><span><b>Card A of 2.</b> Numbers in brackets link to the source log on page 5.</span><span>Page 1 of 5</span></div>
</section>"""

# ------------------------------------------------------------ page 2
def page_b1():
    return f"""
<section class="page" id="pB1">
 {hd('<span style="color:var(--us)">Genspark</span> <span>vs</span> <span style="color:var(--them)">Manus</span>', g('Live-call card, written from Genspark&rsquo;s side. Scan the three boxes first, then the tables. Answers to every question on the right are on page 4.'), 25)}

 <div class="top3">
  <div class="w"><span class="k">Win on</span>Finished slides, sheets and docs from one workspace, plus native Microsoft 365 plugins.{c('lindy','bw_ms')}</div>
  <div class="cc"><span class="k">Be careful on</span>Credits and support complaints on both sides. Trustpilot currently withholds our rating.{c('tp_g_main','tp_m_main')}</div>
  <div class="ww"><span class="k">Watch for</span>Buyers who need hours-long autonomous runs or an agent inside their logged-in tools.{c('aipedia','m_bo')}</div>
 </div>

 <div class="cols2">
  <div>
   <div class="blk"><h3>Their weakness, our counterpoint</h3>
    <div class="colh" style="grid-template-columns:1fr 3mm 1.25fr 12.5mm"><span>What they struggle with</span><span></span><span>What we say</span><span>Stance</span></div>
    <div class="row2"><div>Credits drain on failed or looping tasks{c('tp_m_main')}</div><div class="ar">&rarr;</div>
     <div>We get credit complaints too.{c('lindy')} Safer line: chat and images cost 0 credits on paid plans through 31 Dec 2026.{c('eesel')}</div><span class="chip cr2">Careful</span></div>
    <div class="row2"><div>Cost per task is unpredictable (200 to 9,000 credits){c('carly')}</div><div class="ar">&rarr;</div>
     <div>Pilot on their real task. One 10-slide deck test used about 244 credits.{c('preuve_g')}</div><span class="chip p">Press</span></div>
    <div class="row2"><div>Trustpilot 1.2; 94% one-star{c('tp_m_main')}</div><div class="ar">&rarr;</div>
     <div>Don't compare scores: Trustpilot withholds ours.{c('tp_g_main')} Use G2 4.3 from 20 reviews.{c('g2_g')}</div><span class="chip cr2">Careful</span></div>
    <div class="row2"><div>Support is mostly bots; refunds drag{c('tp_m_main')}</div><div class="ar">&rarr;</div>
     <div>Reviewers praise our response time,{c('tp_g_main')} but we have suspension and refund complaints too.</div><span class="chip p">Press</span></div>
    <div class="row2"><div>Ownership uncertain after the Meta unwind{c('bbg','ground')}</div><div class="ar">&rarr;</div>
     <div>Raise it as a procurement question only. Our own origins draw scrutiny.{c('rank')}</div><span class="chip cr2">Careful</span></div>
   </div>

   <div class="blk"><h3>Their strength, our response</h3>
    <div class="colh" style="grid-template-columns:1fr 3mm 1.25fr 12.5mm"><span>Where they are good</span><span></span><span>What we do</span><span>Stance</span></div>
    <div class="row2"><div>Hours-long autonomous sessions{c('aipedia')}</div><div class="ar">&rarr;</div>
     <div>Concede. Redirect to time-to-finished-deliverable.</div><span class="chip co">Concede</span></div>
    <div class="row2"><div>Works in the customer's own logins{c('m_bo')}</div><div class="ar">&rarr;</div>
     <div>We have an AI browser with autopilot {g('(from your brief; no public link yet)')}. Say &ldquo;comparable&rdquo;.</div><span class="chip cr2">Careful</span></div>
    <div class="row2"><div>Wide Research: 100+ parallel agents{c('altto','aiide')}</div><div class="ar">&rarr;</div>
     <div>No public equivalent found. Don't claim parity.</div><span class="chip co">Concede</span></div>
    <div class="row2"><div>Cheaper entry: $20 vs our $24.99{c('mck','preuve_g')}</div><div class="ar">&rarr;</div>
     <div>We're 25% higher at entry, 50 to 75% at team level.{c('spec','gs_biz','lindy')} Reframe to cost per finished deck.</div><span class="chip cr2">Careful</span></div>
   </div>
  </div>

  <div>
   <div class="box q" style="margin-bottom:1.8mm;padding:1.8mm 2.6mm"><h4>Landmine questions to plant early</h4><ol>
    <li class="say">&ldquo;How do you forecast what a task will cost before it runs?&rdquo;{c('carly')}</li>
    <li class="say">&ldquo;What happens to unused credits at renewal?&rdquo;{c('tp_m_main')}</li>
    <li class="say">&ldquo;Who owns the vendor today, and does that pass procurement?&rdquo;{c('ground')}</li></ol></div>
   <div class="box o" style="margin-bottom:1.8mm;padding:1.8mm 2.6mm"><h4>Discovery: ask, then listen <span class="small">&rarr; answers p.4</span></h4>
    <div class="say" style="margin-bottom:.8mm">&ldquo;Is your output mostly decks and docs, or open-ended research?&rdquo;</div>
    <div class="say">&ldquo;Does the agent need to work inside tools you're logged into?&rdquo;</div></div>
   <div class="box o" style="margin-bottom:1.8mm;padding:1.8mm 2.6mm"><h4>Objections to expect <span class="small">&rarr; scripts p.4</span></h4>
    <div class="say" style="margin-bottom:.6mm">&ldquo;Manus is cheaper.&rdquo; &nbsp;&ldquo;Your reviews are bad too.&rdquo;</div>
    <div class="say">&ldquo;Manus runs longer tasks.&rdquo; &nbsp;&ldquo;Who owns you?&rdquo;</div></div>

   <div class="box w" style="margin-bottom:1.8mm;padding:2mm 2.6mm"><h4>When we win</h4><ul class="l good" style="font-size:7.6pt">
    <li><b>Decks and reports.</b> &ldquo;Presentations are well designed and 80-85% accurate.&rdquo;{c('tp_g_main')} Lindy's top-saved-time feature.{c('lindy')}</li>
    <li><b>Multi-format, one workspace.</b> Slides, sheets, docs, media; G2 reviewers praise AI Slides and multi-step research.{c('lindy','g2_g')}</li>
    <li><b>Work inside Office.</b> Native PowerPoint, Excel and Word plugins; no Manus equivalent found.{c('bw_ms')}</li>
    <li><b>Enterprise checks.</b> SOC 2 Type II, ISO 27001, SSO listed on our business page.{c('gs_biz')}{tg('CR')}</li></ul></div>
   <div class="box l" style="margin-bottom:0;padding:2mm 2.6mm"><h4>When we lose</h4><ul class="l bad" style="font-size:7.6pt">
    <li><b>Big parallel research.</b> Manus Wide Research is built for tens or hundreds of items.{c('aiide')}</li>
    <li><b>Predictable cost.</b> Lindy's main drawback; Call for Me alone is 500 credits a call.{c('lindy')}</li>
    <li><b>Sticker price.</b> $24.99 vs $20 at entry.{c('mck','preuve_g')}</li>
    <li><b>Creative editing and export polish.</b> One 2-star review says edits were ignored; Lindy had two exports lose formatting.{c('tp_g_main','lindy')}</li></ul></div>
  </div>
 </div>
 <div class="ft"><span><b>Card B, front.</b> {g('Win/lose is judgement drawn from the cited evidence.')} Proof is on page 3.</span><span>Page 2 of 5</span></div>
</section>"""

# ------------------------------------------------------------ page 3
def page_b2():
    return f"""
<section class="page" id="pB2">
 {hd('<span style="color:var(--us)">Genspark</span> <span>vs</span> <span style="color:var(--them)">Manus</span>: proof', g('Use this side to back up a claim, not to open a conversation.'), 22)}

 <div class="score">
  <div class="sc"><div class="h">Revenue run-rate</div><div class="a"><b>$250M</b><i>$125M</i></div><div class="n">Genspark Jul 2026; Manus Dec 2025. Different dates, so don't say &ldquo;bigger&rdquo;.{c('tip','scmp')}{tg('CR')}</div></div>
  <div class="sc"><div class="h">G2 rating</div><div class="a"><b>4.3</b><i>2.5 to 4.3</i></div><div class="n">Ours: 20 reviews, 95% four or five stars. Manus: two conflicting views.{c('g2_g','g2_m','zem')}{tg('UV')}</div></div>
  <div class="sc"><div class="h">Trustpilot</div><div class="a"><b>withheld</b><i>1.2</i></div><div class="n">Trustpilot hides our score after removing fake reviews (483 total).{c('tp_g_main','tp_m_main')}{tg('RV')}</div></div>
  <div class="sc"><div class="h">App Store</div><div class="a"><b>4.8</b><i>4.7</i></div><div class="n">Ours about 1.8K ratings; Manus about 39K.{c('app_g','preuve_m')}{tg('RV')}</div></div>
 </div>
 <div class="small" style="margin:-1mm 0 1.2mm"><span style="color:var(--us);font-weight:700">Blue = Genspark</span> &nbsp; <span style="color:var(--them);font-weight:700">Teal = Manus</span> &nbsp;&middot;&nbsp; Funding: Genspark has raised $645M+ at a $2.6B valuation (Jun 2026).{c('inkl','preuve_g')}</div>

 <div class="cols" style="grid-template-columns:1fr 1fr;gap:5mm">
  <div>
   <div class="blk"><h3>Pricing side by side</h3>
    <table class="cmp">
     <tr><th></th><th class="g">Genspark</th><th class="m">Manus</th></tr>
     <tr><td>Free</td><td>100 credits a day{c('lindy','aiide')}</td><td>300 a day, 1,500 a month cap{c('aitr')}</td></tr>
     <tr><td>Entry</td><td>Plus $24.99 ($19.99 annual), 10,000 credits{c('preuve_g')}</td><td>Pro $20, 4,000 credits{c('mck')}</td></tr>
     <tr><td>Heavy use</td><td>Pro $249.99 ($199.99 annual), 125,000 credits{c('preuve_g')}</td><td>Pro $40, 8,000 credits{c('mck')}</td></tr>
     <tr><td>Team</td><td>$30 a seat{c('lindy')}; our business page says $35 billed annually{c('gs_biz')}{tg('UV')}</td><td>From $20 a seat{c('spec')}</td></tr>
     <tr><td>Credit rules</td><td>Don't roll over.{c('lindy')} Chat and images cost 0 on paid plans to 31 Dec 2026.{c('eesel')}</td><td>Unused monthly credits cleared at renewal.{c('tp_m_main')}</td></tr>
    </table></div>

   <div class="blk"><h3>Top use cases <i>(indicative, from reviews and docs)</i></h3>
    <table class="cmp">
     <tr><th class="g">Genspark</th><th class="m">Manus</th></tr>
     <tr><td style="font-weight:400;color:var(--ink);width:auto">Report and deck drafts, summarising large files, research, data analysis{c('tp_g_main','lindy')}{tg('RV')}</td>
         <td>Data extraction to CSV, market research through logged-in premium tools, researched decks{c('m_bo','zem')}</td></tr>
    </table></div>

   <div class="box o" style="margin-bottom:0"><h4>Verify before this card is used</h4><ol class="small" style="color:var(--ink);font-size:7.4pt">
    <li>Manus G2 score: 4.3 vs 2.5 may be two different listings.</li>
    <li>Genspark's Trustpilot status. It was withheld on 1 Nov 2026; a Sep 2026 review site quoted 3.8.{c('lindy')}</li>
    <li>Genspark Team price ($30 vs $35) and G2 review count (20 vs 11).</li>
    <li>Both live pricing pages; I couldn't open them directly.</li>
    <li>Capterra: no Genspark or Manus listing found, so none is quoted.</li></ol></div>
  </div>

  <div>
   <div class="blk"><h3>Social proof strip</h3>
    <div class="small" style="margin-bottom:.4mm"><b style="color:var(--ink)">Partners and ecosystem named in Genspark's own press release</b>{c('bw_ms')}{tg('CR')}</div>
    <div class="wm lg"><span><img src="{L('microsoft')}" alt="Microsoft" style="height:5.2mm"></span><span><img src="{L('openai')}" alt="OpenAI" style="height:5.2mm"></span><span><img src="{L('anthropic')}" alt="Anthropic" style="height:4.2mm"></span><span><img src="{L('aws')}" alt="AWS" style="height:5.2mm"></span></div>
    <div class="small" style="margin-bottom:.4mm"><b style="color:var(--ink)">Backers named in the same release</b></div>
    <div class="wm inv lg"><span><img src="{L('lg')}" alt="LG" style="height:5.2mm"></span><span class="tx">Emergence Capital</span><span class="tx">SBI</span><span class="tx">Pavilion Capital</span></div>
    <div class="small"><b style="color:var(--ink)">Trusted by 7,000+ teams</b> (company-reported){c('gs_biz','bw_g')}{tg('CR')}. {g('Genspark names no individual customers publicly, so these are partners and backers, not customers. Logos for three backers weren\'t available. Add customer logos only with Genspark marketing\'s permission.')}</div></div>

   <div class="blk"><h3>What users say about Genspark</h3>
    <div class="qb"><p>&ldquo;Producing decks used to be my own private piece of purgatory. It has become a task I LOVE because of how the output would be phenomenal each and every time.&rdquo;</p><div class="by">Trustpilot, 5 stars, Oct 2026{c('tp_g_main')}</div></div>
    <div class="qb"><p>&ldquo;Genspark gives me the best research at low cost of credits.&rdquo;</p><div class="by">Trustpilot, 4 stars, Oct 2026{c('tp_g_main')}</div></div>
    <div class="qb" style="margin-bottom:0"><p>&ldquo;A key advantage is that it automates complex processes.&rdquo;</p><div class="by">G2, verified user in accounting, Oct 2026{c('g2_g')}</div></div></div>
  </div>
 </div>
 <div class="ft"><span><b>Card B, back.</b></span><span>Page 3 of 5</span></div>
</section>"""

# ------------------------------------------------------------ page 4: answer key
def page_ans():
    return f"""
<section class="page" id="pAK">
 {hd('Answer key', g('What to say after each question on page 2. Say it in your own words; the facts and sources are what matter. Do not read this aloud.'), 24)}
 <div class="ak">
  <div>
   <div class="card"><h4>Discovery: Q1. &ldquo;Is your output mostly decks and docs, or open-ended research?&rdquo;</h4>
    <div class="st"><b>If decks, docs</b><span>&ldquo;That's where we're strongest. Let's build one real deck from your own material and compare.&rdquo; Backed by Trustpilot and Lindy feedback on AI Slides.{c('tp_g_main','lindy')}</span></div>
    <div class="st"><b>If research</b><span>&ldquo;What does the research end up as: a report, a sheet, a deck?&rdquo; We win if it ends as a deliverable. For very large parallel research, be honest that Manus has Wide Research.{c('aiide')}</span></div>
    <div class="st"><b>Listen for</b><span>{g('Decks, recurring reports and client-ready output point to us. Hundreds of items researched in parallel points to Manus.')}</span></div></div>
   <div class="card" style="margin-top:3.2mm"><h4>Discovery: Q2. &ldquo;Does the agent need to work inside tools you're logged into?&rdquo;</h4>
    <div class="st"><b>If yes</b><span>&ldquo;Manus's Browser Operator does this. We have an AI browser with autopilot; let's test your exact tools.&rdquo;{c('m_bo')} {g('Don\'t claim we are better.')}</span></div>
    <div class="st"><b>If no</b><span>&ldquo;Then the question is the finished output, and that's our strength.&rdquo;</span></div>
    <div class="st"><b>Also ask</b><span>&ldquo;Do your people live in PowerPoint, Excel and Word?&rdquo; We have native plugins for all three.{c('bw_ms')}</span></div></div>
  </div>
  <div>
   <div class="card"><h4>Objection 1. &ldquo;Manus is cheaper.&rdquo;</h4>
    <div class="st"><b>Acknowledge</b><span>&ldquo;On sticker price, yes: $20 against our $24.99 at entry.&rdquo;{c('mck','preuve_g')}</span></div>
    <div class="st"><b>Reframe</b><span>&ldquo;The real cost is per finished deck. One task on Manus can run 200 to 9,000 credits.&rdquo;{c('carly')}</span></div>
    <div class="st"><b>Ask</b><span>&ldquo;Can we run one real task on each and compare the credits and the result?&rdquo;</span></div></div>
   <div class="card" style="margin-top:2.6mm"><h4>Objection 2. &ldquo;Your reviews are bad too.&rdquo;</h4>
    <div class="st"><b>Acknowledge</b><span>&ldquo;Fair. Credit complaints appear for both products.&rdquo;{c('lindy')}</span></div>
    <div class="st"><b>Reframe</b><span>&ldquo;On G2 we're 4.3 from 20 reviews, and users single out AI Slides and research.&rdquo;{c('g2_g','lindy')} {g('Never quote Trustpilot against Manus: it withholds our score.')}{c('tp_g_main')}</span></div>
    <div class="st"><b>Ask</b><span>&ldquo;Which task would worry you most? Let's test that first.&rdquo;</span></div></div>
   <div class="card" style="margin-top:2.6mm"><h4>Objection 3. &ldquo;Manus runs longer tasks.&rdquo;</h4>
    <div class="st"><b>Acknowledge</b><span>&ldquo;For long autonomous runs, that's right.&rdquo;{c('aipedia')}</span></div>
    <div class="st"><b>Reframe</b><span>&ldquo;If the goal is a polished deliverable, that is where we're strongest.&rdquo;</span></div>
    <div class="st"><b>Ask</b><span>&ldquo;How long do your tasks run today?&rdquo;</span></div></div>
   <div class="card" style="margin-top:2.6mm"><h4>Objection 4. &ldquo;Who owns you? Is this safe?&rdquo;</h4>
    <div class="st"><b>Answer</b><span>&ldquo;We're based in Palo Alto,{c('bw_ms')} and list SOC 2 Type II, ISO 27001 and SSO on our business page.{c('gs_biz')} Happy to share details in procurement.&rdquo; {g('Some third parties note China-founded but US-based, so expect the question.')}{c('rank')}</span></div></div>
  </div>
 </div>
 <div class="ft"><span><b>Answer key.</b> {g('Practise each answer once aloud before the first call.')}</span><span>Page 4 of 5</span></div>
</section>"""

# ------------------------------------------------------------ page 5
def page_src():
    items=[]
    for i,k in enumerate(ORDER,1):
        t,p,u=S[k]
        items.append(f'<div><span class="n">{i}</span><span><a href="{u}"><b>{t}</b></a>, {p}<br><span class="u">{u}</span></span></div>')
    return f"""
<section class="page" id="pS">
 <div class="hd"><div><div class="t1" style="font-size:22pt">Source log</div>
  <div class="t2">Every numbered tag points here. CR company-reported, 3P third-party analysis, RV review-based, UV unverified or conflicting.</div></div>
  <div class="meta"><b>Compiled 1 Nov 2026</b><br>Links are clickable.</div></div>
 <div class="slog">{''.join(items)}</div>
 <div class="ft"><span>Figures change. Re-check pricing and ratings on live pages before each use.</span><span>Page 5 of 5</span></div>
</section>"""

body = page_a() + page_b1() + page_b2() + page_ans()
body += page_src()
html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Genspark vs Manus battlecards</title><style>{CSS}</style></head><body>{body}</body></html>'
open(OUT_HTML,'w').write(html)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
        pg = await b.new_page()
        await pg.set_content(html, wait_until='load')
        await pg.evaluate("document.fonts.ready")
        rep = await pg.evaluate("""() => [...document.querySelectorAll('.page')].map(p => {
            const pr = p.getBoundingClientRect(); let worst = 0;
            p.querySelectorAll('*').forEach(e => { const r = e.getBoundingClientRect(); if (r.height>0) worst = Math.max(worst, r.bottom-pr.bottom + 0); });
            const ft = p.querySelector('.ft').getBoundingClientRect();
            let overlap = 0; p.querySelectorAll('.page > *:not(.ft)').forEach(e => { const r=e.getBoundingClientRect(); overlap = Math.max(overlap, r.bottom - ft.top); });
            return {id:p.id, over_px:Math.round(worst), into_footer_px:Math.round(overlap)}; })""")
        for r in rep: print(r)
        await pg.pdf(path=OUT_PDF, width='297mm', height='210mm', print_background=True, prefer_css_page_size=True)
        await b.close()
asyncio.run(main())
print('sources', len(ORDER))
