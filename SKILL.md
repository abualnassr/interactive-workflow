---
name: interactive-workflow
description: Build an interactive HTML workflow or process diagram (cards on a fixed grid, orthogonal labelled arrows, click-to-highlight with whole-chain trace, right-hand context panel, search, deep links, four switchable colour themes including a dark one) plus a PNG for slides. Use when asked for an interactive workflow, process flow, work process, process map, operating model map, framework map, or to turn a Mermaid flowchart into something clickable.
license: MIT
metadata: {"version": "1.2.5", "author": "Bandar Abualnassr"}
---

# Interactive workflow diagram (v1.2.5)

Produces one self-contained HTML file (no external dependencies, works offline, opens in any browser) that maps a process as cards and labelled arrows. Clicking a card highlights what feeds it and what it feeds (direct links, or the full upstream and downstream chain) and opens a context panel on the right. The page ships with four colour themes the viewer can switch between in the header, a search box, keyboard shortcuts and deep links to a card. A PNG of the canvas is produced for slides.

Writing rules: card titles 2 to 6 words, specific verbs ("Classify severity", not "Process data"); arrow labels name WHAT passes (a record, a decision, a document), never "next" or "then"; avoid long dashes in card and arrow text, they eat width. Card, panel, stage, lane and group text is inserted as HTML: write `&amp;` for `&` and `&lt;` for `<` ("P&amp;IDs"), and inside the JavaScript strings escape double quotes as `\"`.

## 1. Gather the content first

Do not start the HTML until the following is settled. Ask the user for whatever the source material does not give. If the user pastes a Mermaid flowchart, read it for topology and meaning only (nodes become cards, edges become arrows, edge text becomes labels) and author fresh content; do not copy its styling.

1. Stages (columns or swimlanes), left to right, 3 to 5.
2. Optional bottom lane for shared enablers: standards, data stores, forums, tools. Include it only when the process really has shared enablers; otherwise set `LANE=null` and the canvas ends under the lowest card.
3. Cards, maximum 20. Each card needs: id (its first character is the key of its stage or of the lane; keys are one character), type, x and y in pixels (a column origin and a row from section 3), title, one-line subtitle, accountable role, and four context fields for the panel: what happens here, why it matters, what good looks like, KPI it reports. Optionally a twelfth field, the responsible person or entity (who does the work, as opposed to who answers for it); it appears as an italic line on the card and under Accountable in the panel. Use it when the user distinguishes accountable from responsible (RACI thinking) or names individuals; leave it out otherwise.
4. Arrows. Each needs: from, to, label. Decisions need labelled branches ("yes", "no: known failure"). Every card connects to at least one other. A loop back to the trigger is normal and goes along the top corridor; any arrow into a trigger card counts as feedback automatically, and any other return arrow (a rework loop, an escalation back) gets `back:true` so the reach counts and the whole-chain highlight do not run in circles.
5. Optional groups: dashed boundary boxes with a small label, for a sub-loop or a boundary (for example "Learn loop", "Vendor side"). Zero to three.
6. Theme. Offer the four built-in themes and set the chosen one as default in `<html data-theme="...">`. The viewer can still switch; a viewer's own pick is remembered for that page only, so it never overrides the default of another workflow file.

Card types:

| type | meaning | styling |
|---|---|---|
| trigger | what starts the cycle | ink fill, white text, accent role line |
| proc | process step with an accountable owner | soft fill, accent border |
| dec | decision with labelled branches | surface fill, dashed border |
| store | data store or system of record | surface fill, faint border |
| tool | control or standard the step follows (matrix, policy, RACI, job plan) | tint fill, accent2 border |
| out | output, deliverable or forum where people answer for results | outfill, white text |

## 2. Four themes

Every colour in the page is a CSS variable, so a theme is one line. Tokens: `bg` (page), `surface` (canvas, panel, white cards, label pills), `fg` (main text, stage labels, selection ring), `ink` (dark fills: trigger card, panel header), `accent` and `accent2` (highlights, incoming arrows), `deep` (outgoing arrows), `outfill` and `outborder` (output cards), `tint`, `soft`, `soft2` (fills), `text`, `muted`, `faint`, `rule`, `line` (default arrow colour), `hl` (highlighted label fill), `who` (accountable line), `trigger-border`.

| theme | feel | bg | accent | accent2 | deep |
|---|---|---|---|---|---|
| ocean (default) | corporate, calm | white | #2A9D8F | #1F7A6F | #1D4E89 |
| forest | operations, sustainability | white | #5B8C5A | #3F6B3E | #7A4E2D |
| ember | energetic, product or startup | white | #E07A2F | #B85E1C | #6B2E2E |
| graphite | dark mode: black, grey and yellow, for screens and dark decks | #121316 | #F5C518 | #E0B000 | #FFFFFF |

To add a client brand, copy one `[data-theme=...]` block, rename it, replace the hex values and add a button in the `.themes` header. In a light theme keep `fg` and `ink` dark and `deep` clearly darker than `accent`; in a dark theme keep `ink` black, `fg` near white, `line` light grey, and give the six card types visibly different fills (in graphite: black trigger, dark grey process, olive control, mid grey output, surface-coloured store and dashed decision) so the legend swatches can be told apart. Arrowheads are coloured through CSS (`#arr path{fill:var(--line)}` etc.), so they follow the theme automatically. Take the PNG for slides in the theme that matches the deck background (graphite for dark decks).

## 3. Layout on a fixed grid (this is what prevents overlaps)

- Canvas 1680 px wide, 990 px high with a lane, otherwise 50 px under the lowest card, inside a 2160 px page (30 px margin, canvas, 20 px gap, 400 px panel, 30 px margin). `fit()` scales the whole page to the window width. The panel never scrolls: `syncHeights()` makes the canvas and the panel the same height, growing both when a card has long context text, and the lane stretches to the new bottom.
- Cards are 140 px high and `CARD_W` (180) px wide, with `overflow:hidden`. Column x origins: 30, 450, 870, 1290 (stage dividers at 0, 420, 840, 1260); card centres at x 120, 540, 960, 1380.
- A second card side by side in the same column and row sits at column x + `CARD_W` + 20 (x + 200 with 180 px cards). The 20 px between the two has no room for an arrow or a label, so connect them through a row gap instead; to feed both from one card, fan out through the row gap above them. The second card also narrows the vertical gap to its right to 40 px (410 to 450, 830 to 870, 1250 to 1290), and in column 4 (x 1490 to 1670) it closes the right-edge corridor.
- Five stages: set `CARD_W=150`; stage dividers at 0, 336, 672, 1008, 1344; card x origins 30, 366, 702, 1038, 1374 (centres 105, 441, 777, 1113, 1449); vertical gaps 180 to 366, 516 to 702, 852 to 1038, 1188 to 1374, right edge 1524 to 1680. Narrower cards wrap sooner, so keep titles short and let the audit's clipping check confirm.
- Stage widths are free: each `STAGES` x is just where that divider sits. When one stage needs two cards side by side, widen it and narrow the others, for example five stages at 0, 315, 630, 1050, 1365 (the third stage 420 px wide, the others 315) with `CARD_W=150`; cards start 30 px right of their divider. Work out the vertical gaps from the card edges you end up with.
- Rows y: 60, 240, 420, 600 (pitch 180, 40 px gap). Lane starts at y 745; lane cards at y 800. Top corridor y 42 for the loop-back arrow. Inside the lane, above its cards, corridors y 752 to 788 (right of the lane label). Under the lane cards, a bottom corridor y 955 to 985; the template's feedback arrow runs there at y 965.
- Arrows run in the corridors: row gaps 200 to 240, 380 to 420, 560 to 600; lane gap 745 to 800; vertical gaps 210 to 450, 630 to 870, 1050 to 1290 (with four even stages); left edge x 8 and 20, narrow, so use it for short runs or rotated labels only; right edge x 1480 to 1670. Each vertical gap contains a dashed stage divider: keep vertical arrows at least 10 px from it (the audit flags closer ones).
- Labels of horizontal runs sit on the line, centred, 12 px above it (label y = line y - 12). Labels of short vertical arrows (up to about 100 px) go beside the arrow, 10 px to its right with `anchor:"start"`, 18 px above the bottom of the gap (y 222, 402, 582), so horizontal runs in the upper part of the gap do not cross them; such a label grows to the right, so keep the next vertical line clear of it. Labels of longer vertical runs are rotated (`rot:-90`) and sit on the line.
- The lane label sits at x 40, 10 px below the lane top, and is as wide as its text (about 10 px per character, since it is spaced capitals). A vertical arrow coming down into a lane card in column 1 crosses it; enter that card from the left corridor (x 20) or from its right edge instead.
- Groups sit 10 px outside the cards they enclose; their label straddles the top border at the left, so leave the top corridor free above a group or start the group at y 46 as in the example.

## 4. Arrows

- Every arrow is an explicit orthogonal route: `pts` = waypoints starting on the source card edge and ending on the target card edge, 8 px rounded corners. No bezier curves.
- The final segment is trimmed by 3 px and the SVG layer sits above the cards (`z-index:3; pointer-events:none`), so arrowheads are never hidden. Marker `refX=10`, 8 px.
- Labels are SVG groups: a surface-coloured rounded rect behind 11 px semi-bold text, `text-anchor` middle (or `start` / `end` beside a vertical arrow). All paths are drawn first, then all label groups, so labels sit above every line.
- Two arrows may share a run: a fan-in to the same point on a card, or a fan-out from the same point. Give them the same `bus` id. The audit flags arrows that run on top of each other unless they share a `bus` id, and lets a bus's shared run pass the labels of its members.
- Click behaviour: incoming arrows accent2 dashed animated, outgoing arrows deep dashed animated, everything else dimmed. The "whole chain" checkbox in the panel extends this to every upstream and downstream step along the flow, never through feedback arrows. Animation is disabled for viewers who prefer reduced motion.

## 5. Context panel and interaction

Default state explains how to read the diagram, the card types present (with counts in the legend) and the arrow colours. On click it shows: kind and stage, title, subtitle, Accountable (and Responsible when given), What happens here, Why it matters, What good looks like, Fed by, Feeds, Reach along the flow (how many steps have to happen before this card and how many it eventually feeds, computed without feedback arrows, so the numbers change along the flow; cards on parallel branches can share numbers; with the whole-chain toggle), KPI it reports, and a Copy link button that copies a deep link `#card=<id>` (or shows it for copying by hand when the browser blocks the clipboard). Opening such a link, or changing it in an open page, selects the card. Cards are reachable with Tab and selected with Enter or Space. Esc resets; `/` focuses the search box, which dims cards whose title, subtitle, accountable or responsible do not match.

## 6. Skeleton (complete, runs as is)

The file below is a complete working example (purchase request to payment, 13 cards, 16 arrows, one group, one feedback arrow marked `back:true`, four themes). Edit the CONTENT block (`TITLE`, `FOOTER`, `STAGES`, `LANE`, `G`, `CARD_W`, `N`, `E`) and, outside it, only the `<h1>` and the default theme in `<html data-theme="...">`. The browser tab title and the footer line are set from `TITLE` and `FOOTER`; the footer is shown in capitals. The routes in `E` show every pattern: straight horizontal, short vertical with side label, decision branches, dog-leg into a card, lane arrows with rotated labels, an arrow entering a card from below, and a feedback arrow along the bottom corridor. A second example (incident to improvement, with a loop back to the trigger along the top corridor) ships in the `examples` folder of the published skill.

```html
<!DOCTYPE html><html lang="en" data-theme="ocean"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Interactive workflow</title>
<style>
/* ---------- THEMES. Default: <html data-theme="..."> ; viewers switch in the header; ?theme=name forces one ----------
   bg page, surface canvas/panel/white cards, fg main text, ink dark fills (trigger, panel header), accent/accent2 highlights and
   incoming arrows, deep outgoing arrows, outfill/outborder output cards, tint control cards, soft process cards, line default arrows */
:root,[data-theme=ocean]{--bg:#fff;--surface:#fff;--fg:#0F1F33;--ink:#0F1F33;--accent:#2A9D8F;--accent2:#1F7A6F;--deep:#1D4E89;--outfill:#1D4E89;--outborder:#1D4E89;--tint:#CDE6E2;--soft:#F1F8F7;--soft2:#E6F1EF;--text:#2E3A48;--muted:#6E7A8A;--faint:#B9C3CF;--rule:#D5DEE7;--line:#223344;--hl:#F2FBF9;--who:#1D4E89;--trigger-border:#0F1F33}
[data-theme=forest]{--bg:#fff;--surface:#fff;--fg:#1B2A1F;--ink:#1B2A1F;--accent:#5B8C5A;--accent2:#3F6B3E;--deep:#7A4E2D;--outfill:#7A4E2D;--outborder:#7A4E2D;--tint:#D9E6CF;--soft:#F4F8F0;--soft2:#EAF1E3;--text:#2F3B33;--muted:#6F7C72;--faint:#B8C4BA;--rule:#D6DED3;--line:#26332A;--hl:#F6FAF1;--who:#7A4E2D;--trigger-border:#1B2A1F}
[data-theme=ember]{--bg:#fff;--surface:#fff;--fg:#1C1C1E;--ink:#1C1C1E;--accent:#E07A2F;--accent2:#B85E1C;--deep:#6B2E2E;--outfill:#6B2E2E;--outborder:#6B2E2E;--tint:#F5D9C4;--soft:#FBF4EE;--soft2:#F6EBE2;--text:#3A3A3C;--muted:#777780;--faint:#C4C4C8;--rule:#E1DAD3;--line:#2B2B2B;--hl:#FFF7F0;--who:#6B2E2E;--trigger-border:#1C1C1E}
[data-theme=graphite]{--bg:#121316;--surface:#1C1E22;--fg:#F0F0F0;--ink:#000;--accent:#F5C518;--accent2:#E0B000;--deep:#FFFFFF;--outfill:#4A4F58;--outborder:#C9CCD2;--tint:#4A4012;--soft:#262930;--soft2:#2E3036;--text:#D6D6D6;--muted:#9A9EA6;--faint:#55595F;--rule:#3A3D43;--line:#C9CCD2;--hl:#3B3410;--who:#F5C518;--trigger-border:#F5C518}
*{box-sizing:border-box}html,body{margin:0;background:var(--bg);color:var(--text);font-family:"Inter","Segoe UI","Helvetica Neue",Arial,sans-serif}
#scaler{transform-origin:top left;width:2160px;padding:26px 30px 20px}
header{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:12px;gap:20px}header h1{margin:0;font-size:24px;color:var(--fg)}header h1 span{color:var(--accent)}header p{margin:4px 0 0;color:var(--muted);font-size:13px}
.tools{display:flex;gap:14px;align-items:center;flex:none}
.themes{display:flex;gap:6px;align-items:center;font-size:11px;color:var(--muted)}.themes button{font:inherit;font-size:11px;padding:4px 10px;border-radius:3px;border:1px solid var(--rule);background:var(--surface);color:var(--text);cursor:pointer}.themes button.on{background:var(--fg);color:var(--bg);border-color:var(--fg)}.themes i{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px;vertical-align:-1px}
#q{font:inherit;font-size:12px;padding:5px 9px;width:200px;border:1px solid var(--rule);border-radius:3px;background:var(--surface);color:var(--fg)}#q::placeholder{color:var(--muted)}
.layout{display:flex;gap:20px;align-items:flex-start}
.container{position:relative;background:var(--surface);border:1px solid var(--fg);border-radius:4px;width:1680px;height:990px;overflow:hidden;flex:none}
.lane{position:absolute;left:0;right:0;bottom:0;border-top:1px solid var(--rule);background:var(--soft)}.lane-label{position:absolute;left:40px;top:10px;font-size:11px;letter-spacing:.12em;color:var(--fg);text-transform:uppercase}
.stage{position:absolute;top:0;bottom:0;border-left:1px dashed var(--rule)}.stage-label{position:absolute;top:12px;font-size:12px;font-weight:700;letter-spacing:.12em;color:var(--fg);text-transform:uppercase}.stage-label b{color:var(--accent2);margin-right:6px}
.group{position:absolute;border:1.5px dashed var(--faint);border-radius:6px;z-index:1;pointer-events:none}.group-label{position:absolute;top:-8px;left:8px;background:var(--surface);padding:0 5px;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.node{position:absolute;width:180px;height:140px;padding:11px 12px 10px;border-radius:4px;border:1.5px solid;background:var(--soft);cursor:pointer;transition:transform .15s,box-shadow .15s,opacity .2s;z-index:2;overflow:hidden}
.node:hover{transform:translateY(-2px);box-shadow:0 6px 18px rgba(0,0,0,.18)}.node .kind{font-size:9px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:4px}.node .label{font-weight:700;font-size:13px;line-height:1.2;color:var(--fg)}.node .sub{font-size:10.5px;margin-top:4px;line-height:1.25}.node .who{font-size:10px;color:var(--who);margin-top:5px;font-weight:700}.node .resp{font-size:9.5px;color:var(--muted);margin-top:2px;font-style:italic}
.trigger{background:var(--ink);border-color:var(--trigger-border)}.trigger .label,.trigger .sub{color:#fff}.trigger .who{color:var(--accent)}.trigger .kind,.trigger .resp{color:#BDBDBD}
.proc{background:var(--soft);border-color:var(--accent)}.tool{background:var(--tint);border-color:var(--accent2)}.out{background:var(--outfill);border-color:var(--outborder)}.out .label,.out .sub{color:#fff}.out .who{color:var(--tint)}.out .kind,.out .resp{color:#C9C9C9}.store{background:var(--surface);border-color:var(--faint)}.dec{background:var(--surface);border-color:var(--fg);border-style:dashed}
[data-theme=graphite] .out .who{color:var(--accent)}[data-theme=graphite] .panel .pill.in,[data-theme=graphite] .panel .pill.out{color:#000}
.node:focus-visible{outline:3px solid var(--accent);outline-offset:3px}
.dim{opacity:.18}.sel{box-shadow:0 0 0 3px var(--fg),0 8px 22px rgba(0,0,0,.25)}.miss{opacity:.12}
svg{position:absolute;inset:0;width:100%;height:100%;z-index:3;pointer-events:none}
#arr path{fill:var(--line)}#arrIn path{fill:var(--accent2)}#arrOut path{fill:var(--deep)}
.edge{fill:none;stroke:var(--line);stroke-width:1.8;marker-end:url(#arr);transition:stroke .2s,opacity .2s}.edge.in{stroke:var(--accent2);stroke-width:3;marker-end:url(#arrIn);stroke-dasharray:9 5;animation:dash 1s linear infinite}.edge.outg{stroke:var(--deep);stroke-width:3;marker-end:url(#arrOut);stroke-dasharray:9 5;animation:dash 1s linear infinite}.edge.dim{opacity:.1}
.lbl rect{fill:var(--surface);stroke:var(--rule);rx:3}.lbl text{font-size:11px;font-weight:600;fill:var(--fg)}.lbl.hl rect{stroke:var(--fg);fill:var(--hl)}.lbl.dim{opacity:.12}@keyframes dash{to{stroke-dashoffset:-28}}
@media (prefers-reduced-motion:reduce){.edge.in,.edge.outg{animation:none}.node{transition:none}}
.panel{width:400px;flex:none;border:1px solid var(--fg);border-radius:4px;background:var(--surface);overflow:hidden}.panel .head{background:var(--ink);color:#fff;padding:16px 18px;position:relative}.panel .head .kind{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}.panel .head h2{margin:4px 0 2px;font-size:18px;padding-right:70px}.panel .head .stage-tag{font-size:11px;color:#C9C9C9}.panel .head .copy{position:absolute;right:14px;top:14px;font:inherit;font-size:10px;padding:3px 8px;border-radius:3px;border:1px solid #777;background:transparent;color:#ddd;cursor:pointer}.panel .body{padding:14px 18px 18px;font-size:12.5px;line-height:1.45}.panel h3{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent2);margin:14px 0 6px;border-bottom:1px solid var(--rule);padding-bottom:4px}.panel h3:first-child{margin-top:0}.panel .who{font-weight:700;color:var(--fg)}.panel .resp{color:var(--text)}.panel ul{margin:0;padding-left:16px}.panel li{margin:3px 0}.panel li b{color:var(--fg)}.panel .pill{display:inline-block;font-size:10px;padding:2px 7px;border-radius:3px;background:var(--soft2);color:var(--fg);border:1px solid var(--rule);margin:0 4px 4px 0}.panel .pill.in{background:var(--accent2);color:#fff;border-color:var(--accent2)}.panel .pill.out{background:var(--deep);color:#fff;border-color:var(--deep)}.panel .hint{color:var(--muted);font-style:italic}.panel label.tr{display:flex;gap:6px;align-items:center;font-size:11.5px;color:var(--text);margin:6px 0 0;cursor:pointer}.panel .reach{display:flex;gap:8px;margin-top:4px}.panel .reach div{flex:1;border:1px solid var(--rule);border-radius:3px;padding:6px 8px;font-size:11px;color:var(--muted)}.panel .reach b{display:block;font-size:16px;color:var(--fg)}.panel .reach small{display:block;margin-top:2px;font-size:10px;color:var(--muted);line-height:1.3}
.legend{display:flex;gap:16px;margin-top:10px;font-size:11.5px;flex-wrap:wrap;color:var(--text)}.legend span::before{content:"";display:inline-block;width:16px;height:14px;border-radius:3px;margin-right:6px;vertical-align:-3px;background:var(--b);border:2px solid var(--bd)}.legend span.dashed::before{border-style:dashed}.legend span.arrow::before{width:22px;height:0;border-width:0 0 3px;border-radius:0;vertical-align:3px;background:none}.legend span i{font-style:normal;color:var(--muted);margin-left:3px}.footer{margin-top:8px;font-size:10px;color:var(--fg);letter-spacing:.08em;text-transform:uppercase;display:flex;justify-content:space-between}.footer span{color:var(--muted);text-transform:none;letter-spacing:0}
</style></head><body><div id="scaler">
<header><div><h1><span>Purchase request to payment |</span> from a need to a paid invoice</h1><p>Click a card to see what feeds it, what it feeds, and the context behind it. Click the background or press Esc to reset. Press / to search.</p></div>
<div class="tools"><input id="q" type="search" placeholder="Find a card (/)" autocomplete="off">
<div class="themes">Theme <button data-t="ocean"><i style="background:#2A9D8F"></i>Ocean</button><button data-t="forest"><i style="background:#5B8C5A"></i>Forest</button><button data-t="ember"><i style="background:#E07A2F"></i>Ember</button><button data-t="graphite"><i style="background:#F5C518;border:1px solid #333"></i>Graphite</button></div></div></header>
<div class="layout"><div class="container" id="c">
<svg id="svg"><defs>
<marker id="arr" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z"/></marker>
<marker id="arrIn" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z"/></marker>
<marker id="arrOut" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z"/></marker>
</defs></svg>
</div><aside class="panel" id="panel" aria-live="polite"></aside></div>
<div class="legend" id="legend"></div>
<div class="footer"><div id="foot"></div><span>Keys: click a card, or Tab to it and press Enter · click again or Esc to clear · / search</span></div></div>
<script>
// ============================ CONTENT: edit everything in this block ============================
const TITLE="Purchase request to payment";
// Footer line under the diagram: owner, date, process version, or a note.
const FOOTER="Example process · replace with your own title";
// Stages: key (one character; every card id starts with its stage key), label, and x of the divider (cards start 30 px right of it). 3 to 5 stages.
const STAGES=[{key:"a",label:"Request",x:0},{key:"b",label:"Approve",x:420},{key:"c",label:"Buy",x:840},{key:"d",label:"Pay",x:1260}];
// Optional bottom lane for shared enablers (key: one character, not used by a stage). Set LANE=null to remove it (the canvas then ends under the lowest card).
const LANE={key:"s",label:"Controls &amp; systems",top:745};
// Optional dashed groups drawn behind cards: {label,x,y,w,h}. Leave [] for none.
const G=[{label:"Approval chain",x:440,y:46,w:200,h:524}];
// Cards. Grid: columns x = 30, 450, 870, 1290 (second card in a column at +200); rows y = 60, 240, 420, 600; lane cards y = 800.
// Card width in px: 180 for 3 or 4 stages, 150 for 5 stages (see the five-stage grid in SKILL.md).
const CARD_W=180;
// N: [id, type, x, y, title, subtitle, accountable, what, why, good, kpi, responsible?]   (responsible is optional)
const N=[
 ["a1","trigger",30,60,"Need identified","Goods or a service required","Requester","Someone needs goods or a service that is not in stock and not covered by an existing contract.","Every purchase starts here. An unclear need becomes a wrong order later.","The need is written down with a specification, quantity and required date before anything is raised.","Requests returned for clarification","Any employee"],
 ["a2","proc",30,240,"Raise purchase request","Specification, quantity, cost centre","Requester's manager","The request is entered in the ERP with specification, quantity, estimated cost, cost centre and required date.","A complete request lets Finance and Procurement decide without going back and forth.","Mandatory fields complete on first submission; estimated cost within 10 percent of the final order.","Requests complete on first submission","Requester"],
 ["b1","proc",450,60,"Check budget","Against the cost centre budget","Budget owner","Finance confirms the cost centre has budget for the request, or flags it as unbudgeted.","Spending without budget is the first thing an audit finds.","Budget check completed within one working day; unbudgeted spend has a documented justification.","Budget checks within 1 day","Finance business partner"],
 ["b2","dec",450,240,"Within approval limit?","Per the delegation of authority","Budget owner","The value is compared with the approver's limit in the delegation of authority matrix.","Keeps approval at the right level without slowing small purchases down.","No approval above the approver's limit; the matrix decides, not the org chart.","Approvals outside limit"],
 ["b3","proc",450,420,"Escalate to next approver","One level up, same request","Next-level manager","The request goes one level up with the budget check attached, so the approver sees the full history.","High-value spend deserves a second pair of eyes, but not a restart.","Escalations decided within two working days with a reason recorded.","Escalations decided within 2 days","Executive assistant"],
 ["c1","proc",870,60,"Create purchase order","From the approved supplier list","Procurement manager","The buyer turns the approved request into a purchase order with an approved supplier, agreed price and terms.","The order is the contract: what it says is what gets delivered and paid.","Orders placed only with approved suppliers; price and terms match the agreement.","Orders to non-approved suppliers","Buyer"],
 ["c2","proc",870,240,"Receive goods or service","Goods receipt posted in the ERP","Requester","The requester or the warehouse confirms what was delivered, in what quantity and condition, and posts the receipt.","No receipt means no proof of delivery and no basis for payment.","Receipt posted within one day of delivery; discrepancies raised with the supplier the same day.","Receipts posted within 1 day","Warehouse or requester"],
 ["d1","proc",1290,60,"Three-way match","Order, receipt, invoice","Accounts payable lead","Accounts payable checks that the invoice matches the purchase order and the goods receipt in quantity and price.","This is the control that stops paying for what was not ordered or not received.","Invoices matched automatically where possible; exceptions resolved within five working days.","Invoices matched first time","Accounts payable clerk"],
 ["d2","out",1290,240,"Payment released","On the agreed terms","Finance controller","Matched invoices are paid in the next payment run on the agreed terms.","Paying on time keeps suppliers reliable and earns early-payment discounts.","Suppliers paid on the due date; no early or late payments without a reason.","Invoices paid on time","Treasury"],
 ["d3","out",1290,420,"Monthly spend review","Exceptions and supplier performance","Finance controller","Finance and Procurement review spend against budget, approval exceptions, late receipts and supplier performance.","This is where the organisation learns from last month's purchases and adjusts its controls.","Review held monthly with decisions minuted; recurring exceptions get a root cause and an owner.","Recurring exceptions closed","Procurement and Finance analysts"],
 ["s1","tool",30,800,"Delegation of authority","Who approves what amount","Chief financial officer","The matrix that sets approval limits by role and purchase type.","One matrix means the same purchase is approved the same way everywhere.","Reviewed yearly; every approval in the ERP enforces it automatically.","Matrix review completed"],
 ["s2","tool",450,800,"Approved supplier list","Qualified and rated suppliers","Procurement manager","The list of suppliers that passed qualification, with ratings from past performance.","Buying from unknown suppliers is where quality, safety and fraud risks enter.","Every active supplier rated within the last year; poor performers removed or on a plan.","Suppliers rated in the last year","Supplier quality officer"],
 ["s3","store",870,800,"ERP","One record from request to payment","IT application owner","Request, approvals, order, receipt, invoice and payment live in one system.","A single record is what makes the three-way match and the monthly review possible.","No purchases outside the system; mandatory fields complete on more than 95 percent of records.","Purchases outside the ERP"]
];
// Arrows: {f,t,label,pts:[[x,y],...],lab:[x,y],anchor?:"start"|"end",rot?:-90,bus?:"id",back?:true}. pts start on the source edge, end on the target edge.
// back:true marks a feedback arrow that the reach counts and whole-chain highlight do not follow (arrows into a trigger card are treated as feedback automatically).
const E=[
 {f:"a1",t:"a2",label:"requirement",pts:[[120,200],[120,240]],lab:[130,222],anchor:"start"},
 {f:"a2",t:"b1",label:"purchase request",pts:[[210,300],[360,300],[360,130],[450,130]],lab:[285,288]},
 {f:"b1",t:"b2",label:"budget confirmed",pts:[[540,200],[540,240]],lab:[550,222],anchor:"start"},
 {f:"b2",t:"c1",label:"yes: approved",pts:[[630,290],[750,290],[750,130],[870,130]],lab:[690,278]},
 {f:"b2",t:"b3",label:"no: above limit",pts:[[540,380],[540,420]],lab:[550,402],anchor:"start"},
 {f:"b3",t:"c1",label:"approved at next level",pts:[[630,490],[790,490],[790,170],[870,170]],lab:[710,478]},
 {f:"c1",t:"c2",label:"purchase order",pts:[[960,200],[960,240]],lab:[970,222],anchor:"start"},
 {f:"c1",t:"d1",label:"order details",pts:[[1050,130],[1290,130]],lab:[1170,118]},
 {f:"c2",t:"d1",label:"goods receipt",pts:[[1050,310],[1170,310],[1170,170],[1290,170]],lab:[1128,298]},
 {f:"d1",t:"d2",label:"matched invoice",pts:[[1380,200],[1380,240]],lab:[1390,222],anchor:"start"},
 {f:"d2",t:"d3",label:"payment record",pts:[[1380,380],[1380,420]],lab:[1390,402],anchor:"start"},
 {f:"s3",t:"d1",label:"receipt and invoice data",pts:[[1050,870],[1240,870],[1240,220],[1310,220],[1310,200]],lab:[1240,560],rot:-90},
 {f:"s1",t:"b2",label:"approval limits",pts:[[210,840],[300,840],[300,330],[450,330]],lab:[300,600],rot:-90},
 {f:"s2",t:"c1",label:"approved supplier, terms",pts:[[630,840],[820,840],[820,100],[870,100]],lab:[820,600],rot:-90},
 {f:"c2",t:"s3",label:"goods receipt posted",pts:[[960,380],[960,800]],lab:[970,600],anchor:"start"},
 {f:"d3",t:"s2",label:"supplier performance ratings",pts:[[1380,560],[1380,965],[540,965],[540,940]],lab:[960,953],back:true}
];
// ============================ ENGINE: no edits needed below ============================
const KIND={trigger:"Trigger",proc:"Process step",tool:"Control / standard",out:"Output / forum",store:"Data store",dec:"Decision"};
const SW={trigger:["var(--ink)","var(--trigger-border)"],proc:["var(--soft)","var(--accent)"],tool:["var(--tint)","var(--accent2)"],out:["var(--outfill)","var(--outborder)"],store:["var(--surface)","var(--faint)"],dec:["var(--surface)","var(--fg)"]};
const STAGE={};STAGES.forEach((s,i)=>STAGE[s.key]=`${i+1} · ${s.label}`);if(LANE)STAGE[LANE.key]=LANE.label;
document.title=TITLE+' | interactive workflow';document.getElementById('foot').textContent=FOOTER;
const c=document.getElementById('c'),svg=document.getElementById('svg'),panel=document.getElementById('panel');const pos={},byId={};
const H=LANE?990:Math.max(...N.map(n=>n[3]))+190; /* canvas height: fixed with a lane, otherwise ends 50 px under the lowest card */ c.style.height=H+'px';panel.style.height=H+'px';
if(LANE){const l=document.createElement('div');l.className='lane';l.style.top=LANE.top+'px';l.innerHTML=`<div class="lane-label">${LANE.label}</div>`;c.appendChild(l);}
STAGES.forEach((s,i)=>{const d=document.createElement('div');d.className='stage';d.style.left=s.x+'px';c.appendChild(d);const t=document.createElement('div');t.className='stage-label';t.style.left=(s.x+30)+'px';t.innerHTML=`<b>${i+1}</b>${s.label}`;c.appendChild(t);});
G.forEach(g=>{const d=document.createElement('div');d.className='group';d.style.cssText=`left:${g.x}px;top:${g.y}px;width:${g.w}px;height:${g.h}px`;d.innerHTML=`<div class="group-label">${g.label}</div>`;c.appendChild(d);});
N.forEach(n=>{const [id,type,x,y,label,sub,who,,,,,resp]=n;const el=document.createElement('div');el.className='node '+type;el.id='n-'+id;el.style.left=x+'px';el.style.top=y+'px';el.style.width=CARD_W+'px';el.tabIndex=0;el.setAttribute('role','button');el.setAttribute('aria-label',KIND[type]+': '+label);el.innerHTML=`<div class="kind">${KIND[type]}</div><div class="label">${label}</div><div class="sub">${sub}</div><div class="who">${who}</div>${resp?`<div class="resp">Responsible: ${resp}</div>`:''}`;c.appendChild(el);pos[id]={el,x,y,type};byId[id]=n;});
const NS='http://www.w3.org/2000/svg';const edges=[],labelGroups=[];
E.forEach(spec=>{const {f,t,label,pts,lab,rot,anchor,bus}=spec;const P=pts.map(p=>p.slice());const n=P.length;const [ax,ay]=P[n-2],[bx,by]=P[n-1];const len=Math.hypot(bx-ax,by-ay);const k=Math.max(0,len-3)/len;P[n-1]=[ax+(bx-ax)*k,ay+(by-ay)*k];
 const R=8;let d=`M${P[0][0]},${P[0][1]}`;for(let i=1;i<n-1;i++){const [x0,y0]=P[i-1],[x1,y1]=P[i],[x2,y2]=P[i+1];const dx1=Math.sign(x1-x0),dy1=Math.sign(y1-y0),dx2=Math.sign(x2-x1),dy2=Math.sign(y2-y1);const r=Math.min(R,Math.hypot(x1-x0,y1-y0)/2,Math.hypot(x2-x1,y2-y1)/2);d+=` L${x1-dx1*r},${y1-dy1*r} Q${x1},${y1} ${x1+dx2*r},${y1+dy2*r}`;}d+=` L${P[n-1][0]},${P[n-1][1]}`;
 const path=document.createElementNS(NS,'path');path.setAttribute('d',d);path.setAttribute('class','edge');svg.appendChild(path);
 const g=document.createElementNS(NS,'g');g.setAttribute('class','lbl');const rct=document.createElementNS(NS,'rect');const tx=document.createElementNS(NS,'text');tx.textContent=label;tx.setAttribute('x',lab[0]);tx.setAttribute('y',lab[1]);tx.setAttribute('text-anchor',anchor||'middle');tx.setAttribute('dominant-baseline','middle');g.appendChild(rct);g.appendChild(tx);if(rot)g.setAttribute('transform',`rotate(${rot} ${lab[0]} ${lab[1]})`);labelGroups.push(g);svg.appendChild(g);
 const bb=tx.getBBox();rct.setAttribute('x',bb.x-5);rct.setAttribute('y',bb.y-2);rct.setAttribute('width',bb.width+10);rct.setAttribute('height',bb.height+4);edges.push({f,t,label,path,tx:g,bus,back:spec.back});});
labelGroups.forEach(g=>svg.appendChild(g));
// legend with counts
const counts={};N.forEach(n=>counts[n[1]]=(counts[n[1]]||0)+1);
document.getElementById('legend').innerHTML=Object.keys(KIND).filter(k=>counts[k]).map(k=>`<span class="${k==='dec'?'dashed':''}" style="--b:${SW[k][0]};--bd:${SW[k][1]}">${KIND[k]}<i>${counts[k]}</i></span>`).join('')+`<span class="arrow" style="--bd:var(--accent2)">arrows that feed the selected card</span><span class="arrow" style="--bd:var(--deep)">arrows fed by the selected card</span>`;
// reach (full upstream / downstream chains)
const isBack=e=>e.back||pos[e.t].type==='trigger'; // feedback arrows: marked back:true, or any arrow into a trigger card
function reach(id,dir){const seen=new Set();const st=[id];while(st.length){const x=st.pop();edges.forEach(e=>{if(isBack(e))return;const nx=dir==='up'?(e.t===x?e.f:null):(e.f===x?e.t:null);if(nx&&nx!==id&&!seen.has(nx)){seen.add(nx);st.push(nx);}});}return seen;}
let trace=false;
function syncHeights(){panel.style.height='auto';const h=Math.max(H,panel.scrollHeight);c.style.height=h+'px';panel.style.height=h+'px';if(typeof fit==='function')fit();}
function defaultPanel(){panel.innerHTML=`<div class="head"><div class="kind">Context panel</div><h2>Select a card</h2><div class="stage-tag">${TITLE}</div></div><div class="body"><h3>How to read the diagram</h3><p>Stages run left to right.${LANE?' The bottom lane holds the standards, data and forums that every stage shares.':''}</p><h3>What the cards mean</h3><ul>${Object.keys(KIND).filter(k=>counts[k]).map(k=>`<li><b>${KIND[k]}</b>: ${({trigger:'what starts the cycle.',proc:'an action with an accountable owner.',dec:'a branch with labelled outcomes.',store:'where information lives between steps.',tool:'the rule, matrix or plan a step follows.',out:'where people answer for results.'})[k]}</li>`).join('')}</ul><h3>What the arrows mean</h3><p>Each arrow is labelled with what passes between two steps. When a card is selected, <span class="pill in">incoming</span> arrows feed it and <span class="pill out">outgoing</span> arrows are fed by it.</p><p class="hint">Click any card for its purpose, why it matters, what good looks like, who is accountable and responsible, its inputs and outputs, and the KPI it reports. Tick "whole chain" in a card's panel to follow every upstream and downstream step.</p></div>`;syncHeights();}
function showPanel(id){const [,type,,,label,sub,who,what,why,good,kpi,resp]=byId[id];const ins=edges.filter(e=>e.t===id).map(e=>`<li><b>${byId[e.f][4]}</b>: ${e.label}</li>`).join('')||'<li class="hint">none: start of the cycle</li>';const outs=edges.filter(e=>e.f===id).map(e=>`<li><b>${byId[e.t][4]}</b>: ${e.label}</li>`).join('')||'<li class="hint">none: end of the cycle</li>';const up=reach(id,'up').size,dn=reach(id,'down').size;
 panel.innerHTML=`<div class="head"><div class="kind">${KIND[type]}</div><h2>${label}</h2><div class="stage-tag">${STAGE[id[0]]||''} · ${sub}</div><button class="copy" id="copy">Copy link</button></div><div class="body"><h3>Accountable</h3><div class="who">${who}</div>${resp?`<div class="resp">Responsible: ${resp}</div>`:''}<h3>What happens here</h3><p>${what}</p><h3>Why it matters</h3><p>${why}</p><h3>What good looks like</h3><p>${good}</p><h3>Fed by</h3><ul>${ins}</ul><h3>Feeds</h3><ul>${outs}</ul><h3>Reach along the flow</h3><div class="reach"><div><b>${up}</b>upstream step${up===1?'':'s'}<small>everything that has to happen before this card</small></div><div><b>${dn}</b>downstream step${dn===1?'':'s'}<small>everything this card eventually feeds</small></div></div><label class="tr"><input type="checkbox" id="trace" ${trace?'checked':''}> Highlight the whole chain instead of direct links only</label><p class="hint" style="margin:4px 0 0">Feedback and return arrows are not followed, so the counts show how far along the flow this card sits.</p><h3>KPI it reports</h3><span class="pill">${kpi}</span></div>`;
 document.getElementById('copy').onclick=ev=>{ev.stopPropagation();const b=ev.target,u=location.href.split('#')[0]+'#card='+id;const done=()=>{b.textContent='Copied';setTimeout(()=>b.textContent='Copy link',1200);},ask=()=>prompt('Copy this link',u);if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(u).then(done,ask);else ask();};
 document.getElementById('trace').onchange=ev=>{trace=ev.target.checked;select(id,true);};syncHeights();}
let selected=null;
function clear(){Object.values(pos).forEach(p=>p.el.classList.remove('dim','sel'));edges.forEach(e=>{e.path.classList.remove('in','outg','dim');e.tx.classList.remove('hl','dim');});}
function reset(){selected=null;clear();defaultPanel();if(location.hash)history.replaceState(null,'',location.pathname+location.search);}
function select(id,keep){if(!keep&&selected===id){reset();return;}clear();selected=id;const up=trace?reach(id,'up'):new Set(),dn=trace?reach(id,'down'):new Set();const keepSet=new Set([id,...up,...dn]);
 edges.forEach(e=>{const inc=e.t===id||(trace&&!isBack(e)&&up.has(e.t)&&(up.has(e.f)||e.f===id)),out=e.f===id||(trace&&!isBack(e)&&dn.has(e.f)&&(dn.has(e.t)||e.t===id));if(inc){e.path.classList.add('in');e.tx.classList.add('hl');keepSet.add(e.f);}else if(out){e.path.classList.add('outg');e.tx.classList.add('hl');keepSet.add(e.t);}else{e.path.classList.add('dim');e.tx.classList.add('dim');}});
 Object.entries(pos).forEach(([k,q])=>{if(!keepSet.has(k))q.el.classList.add('dim');});pos[id].el.classList.add('sel');showPanel(id);history.replaceState(null,'',location.pathname+location.search+'#card='+id);}
Object.entries(pos).forEach(([id,p])=>{p.el.addEventListener('click',ev=>{ev.stopPropagation();select(id);});p.el.addEventListener('keydown',ev=>{if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();select(id);}});});
c.addEventListener('click',reset);panel.addEventListener('click',ev=>ev.stopPropagation());
// search
const q=document.getElementById('q');q.addEventListener('input',()=>{const v=q.value.trim().toLowerCase();Object.entries(pos).forEach(([id,p])=>{const n=byId[id];const hit=!v||[n[4],n[5],n[6],n[11]||''].join(' ').toLowerCase().includes(v);p.el.classList.toggle('miss',!hit);});});
document.addEventListener('keydown',ev=>{if(ev.key==='Escape'){q.value='';q.dispatchEvent(new Event('input'));q.blur();reset();}else if(ev.key==='/'&&document.activeElement!==q){ev.preventDefault();q.focus();}});
// theme: ?theme=name in the URL, header buttons; a viewer's pick is remembered for this page only, when storage is available
const TKEY='wf-theme:'+location.pathname;function setTheme(t,keep){document.documentElement.setAttribute('data-theme',t);document.querySelectorAll('.themes button').forEach(b=>b.classList.toggle('on',b.dataset.t===t));if(keep)try{localStorage.setItem(TKEY,t);}catch(e){}}
document.querySelectorAll('.themes button').forEach(b=>b.addEventListener('click',()=>setTheme(b.dataset.t,true)));
(function(){let t=new URLSearchParams(location.search).get('theme');if(!t){try{t=localStorage.getItem(TKEY);}catch(e){}}setTheme(t&&document.querySelector(`.themes button[data-t="${t}"]`)?t:document.documentElement.getAttribute('data-theme')||'ocean');})();
// deep link #card=id, on load and when the link changes in an open page
defaultPanel();function fromHash(){const m=location.hash.match(/card=([\w-]+)/);if(m&&pos[m[1]]&&selected!==m[1])select(m[1],true);}fromHash();window.addEventListener('hashchange',fromHash);
function fit(){const s=Math.min(1,(window.innerWidth-8)/2160);document.getElementById('scaler').style.transform=`scale(${s})`;document.body.style.height=(document.getElementById('scaler').offsetHeight*s+10)+'px';}window.addEventListener('resize',fit);fit();syncHeights();
</script></body></html>

```

## 7. Audit before delivery (required)

Evaluate the function below in the rendered page, using whichever of these the session has, in this order:

1. A shell with Python: run `python <skill folder>/scripts/wf_check.py "<file>.html"` (`python3` on macOS and Linux), where `<skill folder>` is the folder this SKILL.md is in. It reads the function below (the only `js` block in this file), runs it in headless Chromium, prints `{"findings": [...], "console_errors": [...]}`, and exits 0 only when both lists are empty. If Playwright is missing, install it first (`pip install playwright` then `python -m playwright install chromium`) when the session allows installs.
2. A browser tool of the agent's own (a Playwright or Chrome MCP server, a built-in browser pane): open the file, evaluate the function in the page, and read the console.
3. Neither: skip the automated audit, check the route coordinates against the grid by hand, and tell the user plainly that the automated audit was not run.

The audit checks the data (duplicate ids, arrows to unknown cards, unconnected cards, unknown stage keys), the geometry (cards, arrows or labels outside the canvas, cards overlapping, vertical arrows on or within 10 px of a stage divider, arrow start and end on the right card edges, arrows crossing other cards, arrows running on top of each other, labels on cards or on each other, lines through labels or through stage, lane and group titles, those titles on cards) and card text clipped at the bottom or the side. Fix every finding by moving a waypoint, a label or a card, then rerun until `findings` and `console_errors` are both empty. Anything else is never a pass.

```js
() => {
  const c = document.getElementById('c').getBoundingClientRect();
  const bad = [];
  // schema: ids unique, arrows reference real cards, every card connected, stage key known, cards inside the canvas
  const ids = N.map(n => n[0]); ids.forEach((id,i) => { if (ids.indexOf(id) !== i) bad.push('duplicate id '+id); if (!STAGE[id[0]]) bad.push('unknown stage key for '+id); });
  E.forEach(e => { if (!byId[e.f]) bad.push('arrow from unknown '+e.f); if (!byId[e.t]) bad.push('arrow to unknown '+e.t); if (e.pts.length < 2) bad.push('arrow '+e.f+'>'+e.t+' needs 2+ points'); });
  ids.forEach(id => { if (!E.some(e => e.f===id || e.t===id)) bad.push('unconnected '+id); });
  const nodes = [...document.querySelectorAll('.node')].map(e => { const r = e.getBoundingClientRect(); return {id:e.id.slice(2), l:r.left-c.left, t:r.top-c.top, r:r.right-c.left, b:r.bottom-c.top}; });
  nodes.forEach(n => { if (n.l < 0 || n.t < 0 || n.r > c.width || n.b > c.height) bad.push('outside canvas '+n.id); });
  nodes.forEach((a,i) => nodes.slice(i+1).forEach(b => { if (a.l < b.r && b.l < a.r && a.t < b.b && b.t < a.b) bad.push('card-card '+a.id+' / '+b.id); }));
  // arrows: outside the canvas, or running on top of each other (unless they share a bus id)
  edges.forEach(e => { const r = e.path.getBoundingClientRect(); if (r.left < c.left || r.top < c.top || r.right > c.right || r.bottom > c.bottom) bad.push('arrow outside canvas '+e.f+'>'+e.t); });
  const segs = E.map(e => e.pts.slice(1).map((q,i) => [e.pts[i], q]));
  const span = (a,b,c2,d) => Math.min(Math.max(a,b),Math.max(c2,d)) - Math.max(Math.min(a,b),Math.min(c2,d));
  E.forEach((a,i) => E.forEach((b,j) => { if (j <= i || (a.bus && a.bus === b.bus)) return;
    segs[i].forEach(([p,q]) => segs[j].forEach(([r,t]) => {
      if (p[1]===q[1] && r[1]===t[1] && Math.abs(p[1]-r[1]) < 3 && span(p[0],q[0],r[0],t[0]) > 6) bad.push('arrow-overlap '+a.f+'>'+a.t+' / '+b.f+'>'+b.t);
      if (p[0]===q[0] && r[0]===t[0] && Math.abs(p[0]-r[0]) < 3 && span(p[1],q[1],r[1],t[1]) > 6) bad.push('arrow-overlap '+a.f+'>'+a.t+' / '+b.f+'>'+b.t); })); }));
  // vertical arrow runs on or beside a dashed stage divider
  STAGES.forEach(st => { if (!st.x) return; E.forEach((e,i) => segs[i].forEach(([p,q]) => { if (p[0]===q[0] && Math.abs(p[0]-st.x) < 10) bad.push('arrow-on-divider '+e.f+'>'+e.t+' / '+st.label); })); });
  const inside = (x,y,n,pad=0) => x>n.l-pad && x<n.r+pad && y>n.t-pad && y<n.b+pad;
  edges.forEach(e => { const L = e.path.getTotalLength(); const p1 = e.path.getPointAtLength(L); const p0 = e.path.getPointAtLength(0); const t = nodes.find(n=>n.id===e.t), f = nodes.find(n=>n.id===e.f);
    if (!t || !f) return; if (!inside(p1.x,p1.y,t,6)) bad.push('end '+e.f+'>'+e.t); if (!inside(p0.x,p0.y,f,6)) bad.push('start '+e.f+'>'+e.t);
    const crossed = new Set(); for (let s=4; s<L-4; s+=3){ const p = e.path.getPointAtLength(s); nodes.forEach(n => { if (n.id!==e.f && n.id!==e.t && inside(p.x,p.y,n,-1)) crossed.add(n.id); }); }
    if (crossed.size) bad.push('cross '+e.f+'>'+e.t+':'+[...crossed]); });
  const labs = [...document.querySelectorAll('.lbl')].map(g => { const r = g.getBoundingClientRect(); return {t:g.textContent, l:r.left-c.left, top:r.top-c.top, r:r.right-c.left, b:r.bottom-c.top}; });
  const ov = (a,b) => a.l < b.r && b.l < a.r && a.top < b.b && b.top < a.b;
  labs.forEach((a,i) => { if (a.l < 0 || a.top < 0 || a.r > c.width || a.b > c.height) bad.push('label outside canvas '+a.t);
    nodes.forEach(n => { if (ov(a,{l:n.l,r:n.r,top:n.t,b:n.b})) bad.push('label-on-card '+a.t+' / '+n.id); });
    labs.slice(i+1).forEach(b => { if (ov(a,b)) bad.push('label-label '+a.t+' / '+b.t); }); });
  edges.forEach(e => { const L = e.path.getTotalLength(); for (let s=0; s<L; s+=4){ const p = e.path.getPointAtLength(s); labs.forEach(a => { if (a.t !== e.label && !(e.bus && edges.some(o=>o.bus===e.bus && o.label===a.t)) && p.x>a.l && p.x<a.r && p.y>a.top && p.y<a.b) bad.push('line-through-label '+e.f+'>'+e.t+' / '+a.t); }); } });
  [...document.querySelectorAll('.lane-label,.stage-label,.group-label')].forEach(el => { const r = el.getBoundingClientRect(); const box={l:r.left-c.left,top:r.top-c.top,r:r.right-c.left,b:r.bottom-c.top};
    edges.forEach(e => { const L = e.path.getTotalLength(); for (let s=0; s<L; s+=4){ const p = e.path.getPointAtLength(s); if (p.x>box.l && p.x<box.r && p.y>box.top && p.y<box.b) { bad.push('line-through-text '+e.f+'>'+e.t+' / '+el.textContent); break; } } });
    labs.forEach(a => { if (ov(a,box)) bad.push('label-on-text '+a.t+' / '+el.textContent); });
    nodes.forEach(n => { if (ov(box,{l:n.l,r:n.r,top:n.t,b:n.b})) bad.push('text-on-card '+el.textContent+' / '+n.id); }); });
  [...document.querySelectorAll('.node')].forEach(e => { if (e.scrollHeight > e.clientHeight+1 || e.scrollWidth > e.clientWidth+1) bad.push('clipped '+e.id.slice(2)); });
  return [...new Set(bad)];
}
```

Also check the console for errors (a missing constant silently empties the diagram), press Tab until a card is focused and Enter to select it, click at least two cards to confirm the panel, the highlight and the whole-chain toggle work, confirm the reach numbers differ between an early and a late card (if every card shows the same numbers, a return arrow is missing `back:true`), select the card with the most panel text (what, why and what good looks like together) and confirm the panel and canvas stay the same height, and switch through all four themes once; the audit result does not change with theme, but contrast does, so look at graphite separately.

## 8. Deliver

1. The HTML file, named `<Topic> - workflow (interactive).html`, saved in the user's working folder (or the output folder the environment designates).
2. A PNG of the canvas for slides, in the theme that matches the deck (one per theme if the user has not chosen): `python <skill folder>/scripts/wf_check.py "<file>.html" ocean graphite` writes `<name> - <theme>.png` next to the HTML for each theme named (`<name>` is the HTML file name without `.html`); with another browser tool, screenshot the `#c` element at device scale factor 2 in a 2180 x 1180 viewport, with `?theme=<name>` on the URL. On a 16:9 slide place it about 4.9 in high, centred, with a caption line explaining the card colours.
3. Tell the user the page is a single file with no dependencies; that the theme can be switched in the header or forced with `?theme=graphite` in the URL; that Esc resets, `/` searches and Copy link gives a link straight to a card; that cards work from the keyboard (Tab, then Enter); that it is made for a laptop or desktop screen (on a phone it scales down, so pinch to zoom); and that it falls back to Segoe UI or Arial where Inter is not installed.

## Changelog

- 1.2.5: the page is 2160 px wide instead of 2120, so the context panel keeps a right margin and no longer touches or pokes past the window edge (at 1920 px it added a sideways scrollbar); PNG export viewport 2180 x 1180 so the canvas is captured at full size; demo animation in the README.
- 1.2.4: audit review fixes. Template: readable incoming/outgoing labels in graphite, and white outgoing arrows there so they stand apart from the grey default arrows; generic `<title>`; Copy link falls back to showing the link when the clipboard is blocked (it used to say "Copied" anyway); cards reachable with Tab and selected with Enter or Space; a viewer's theme pick is remembered per page, so it no longer overrides other files' defaults; deep links also work when changed in an open page; tab title and footer come from `TITLE` and `FOOTER`; `CARD_W` for five stages; panel hint corrected. Audit: also flags arrows or labels outside the canvas, arrows on top of each other, arrows on a stage divider, stage, lane or group titles on cards, and text clipped at the side; `wf_check.py` waits for fonts and layout and finds the audit by its code block. Instructions: x and y are pixels, keys are one character, label rows 222/402/582, documented corridors (bottom y 955 to 985, right edge), second-card and five-stage grids, widening a stage, label placement rules, the lane-label trap, what `bus` does, HTML escaping.
- 1.2.3: new example screenshots (one with a card selected and the context panel open); README cleanup.
- 1.2.2: works in any agent that reads SKILL.md (Claude Code, Codex, Cursor, OpenCode, Hermes Agent, OpenClaw and others): bundled `scripts/wf_check.py` runs the audit and exports PNGs from a shell; audit step lists the options in order; audit no longer crashes on an arrow to an unknown card (it reports it); metadata on one line for loaders that only read single-line frontmatter.
- 1.2.1: skeleton example swapped to a purchase request to payment flow (generic across industries); licence and author metadata in the frontmatter; audit step says what to do when no browser is available.
- 1.2: panel no longer scrolls, canvas and panel always share one height; reach and whole-chain highlight follow the flow only (feedback arrows into the trigger, or marked `back:true`, are skipped) so the numbers and the highlighted path differ per card; graphite fills reworked and legend swatches enlarged, dashed for decisions and drawn as lines for the two arrow entries, so the legend reads in dark mode.
- 1.1: fourth theme (graphite, dark), lane optional, optional responsible per card, optional dashed groups, legend counts, reach counts and full-chain trace, search, Esc and / shortcuts, deep links with Copy link, reduced-motion support, audit extended with data checks, card overlap and clipped text, canvas height follows content without a lane.
- 1.0: first public version with three themes.
