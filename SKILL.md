---
name: interactive-workflow
description: Build an interactive HTML workflow or process diagram (cards on a fixed grid, orthogonal labelled arrows, click-to-highlight with whole-chain trace, right-hand context panel, search, deep links, four switchable colour themes including a dark one) plus a PNG for slides. Use when asked for an interactive workflow, process flow, work process, process map, operating model map, framework map, or to turn a Mermaid flowchart into something clickable.
license: MIT
metadata: {"version": "1.4.1", "author": "Bandar Abualnassr"}
---

# Interactive workflow diagram (v1.4.1)

Produces one self-contained HTML file (no external dependencies, works offline, opens in any browser) that maps a process as cards and labelled arrows. Clicking a card highlights what feeds it and what it feeds (direct links, or the full upstream and downstream chain) and opens a context panel on the right. The page ships with four colour themes the viewer can switch between in the header, a search box, keyboard shortcuts and deep links to a card. A PNG of the canvas is produced for slides.

Writing rules: card titles 2 to 6 words, specific verbs ("Classify severity", not "Process data"); arrow labels name WHAT passes (a record, a decision, a document), never "next" or "then"; avoid long dashes in card and arrow text, they eat width; leave a little room in every card, because text sets wider where Inter is installed or on a Mac than in a headless check. Card, panel, stage, lane and group text is inserted as HTML: write `&amp;` for `&` and `&lt;` for `<` ("P&amp;IDs"), and inside the JavaScript strings escape double quotes as `\"`.

## 1. Gather the content first

Do not start the HTML until the following is settled. Ask the user for whatever the source material does not give. If the user pastes a Mermaid flowchart, read it for topology and meaning only (nodes become cards, edges become arrows, edge text becomes labels) and author fresh content; do not copy its styling.

1. Stages (columns or swimlanes), left to right, 3 to 5.
2. Optional bottom lane for shared enablers: standards, data stores, forums, tools. If the request does not say, ask whether the user wants it, and suggest it when the process has shared standards, systems or forums. When the user does not want it ("no bottom lane", "no enablers", "just the stages") or the process has no shared enablers, set `LANE=null`, leave out the lane cards and their arrows, and the canvas ends under the lowest card. An enabler the user still wants on the map, such as the CMMS, becomes a normal card (a data store or control) inside the stage that uses it most, connected like any other card.
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
- Labels of horizontal runs sit on the line, centred, 12 px above it (label y = line y - 12), except on the top corridor (y 42) and the bottom corridor under the lane cards, where the label sits on the line itself (label y = line y) to stay clear of the stage titles and the cards. Labels of short vertical arrows (up to about 100 px) go beside the arrow, 10 px to its right with `anchor:"start"`, 18 px above the bottom of the gap (y 222, 402, 582), so horizontal runs in the upper part of the gap do not cross them; such a label grows to the right, so keep the next vertical line clear of it. Labels of longer vertical runs are rotated (`rot:-90`) and sit on the line; keep a rotated label shorter than its run. To size a label, allow about 6.5 px per character plus 10 px of padding (11 px semi-bold).
- The lane label sits at x 40, 10 px below the lane top, and is as wide as its text (about 7 to 8 px per character, since it is spaced capitals). A vertical arrow coming down into a lane card in column 1 crosses it; enter that card from the left corridor (x 20) or from its right edge instead.
- Groups sit 10 px outside the cards they enclose; their label straddles the top border at the left, so leave the top corridor free above a group or start the group at y 46 as in the example.

## 4. Arrows

- Every arrow is an explicit orthogonal route: `pts` = waypoints, 8 px rounded corners, no bezier curves.
- Write the first and last point with `at(id, side, offset)`, never as typed numbers: `side` is `"top"`, `"bottom"`, `"left"` or `"right"`, `offset` is px along that edge from its left or top end (leave it out for the middle). This puts the ends exactly on the card's edge; hand-typed ends are how arrows end up stopping short, overshooting into a card, or sliding along its border.
- The first segment leaves its card at right angles and the last segment arrives at right angles from outside: into a top edge from above, a bottom edge from below, a left edge from the left, a right edge from the right. Never end with a segment that runs along the edge (for an arrow coming up from the lane into the side of a card, turn so the last segment comes in sideways). Keep ends 12 px or more from a corner; spread several arrows on one edge by giving them different offsets. When several arrows come up into the same edge from below, let the vertical closest to the card take the lowest entry, so the runs do not cross.
- Arrowheads are 12 px at every line width. The engine stops the tip 1 px short of the card and tightens the last corner so the head always sits on a straight run, which needs a final segment of 16 px or more (the top corridor's 18 px drop into a row-1 card is enough; the 10 px gap between the left-edge corridor and a column-1 card is not, so enter those cards another way). The SVG layer sits above the cards (`z-index:3; pointer-events:none`), so arrowheads are never hidden.
- Labels keep 4 px or more clear of every card. They are SVG groups: a surface-coloured rounded rect behind 11 px semi-bold text, `text-anchor` middle (or `start` / `end` beside a vertical arrow). All paths are drawn first, then all label groups, so labels sit above every line.
- Two arrows may share a run: a fan-in to the same point on a card, or a fan-out from the same point. Give them the same `bus` id. The audit flags arrows that run on top of each other unless they share a `bus` id, and lets a bus's shared run pass the labels of its members.
- Click behaviour: incoming arrows accent2 dashed animated, outgoing arrows deep dashed animated, everything else dimmed. The "whole chain" checkbox in the panel extends this to every upstream and downstream step along the flow, never through feedback arrows. Animation is disabled for viewers who prefer reduced motion.

## 5. Context panel and interaction

Default state explains how to read the diagram, the card types present (with counts in the legend) and the arrow colours. On click it shows: kind and stage, title, subtitle, Accountable (and Responsible when given), What happens here, Why it matters, What good looks like, Fed by, Feeds, Reach along the flow (how many steps have to happen before this card and how many it eventually feeds, computed without feedback arrows, so the numbers change along the flow; cards on parallel branches can share numbers; with the whole-chain toggle), KPI it reports, and a Copy link button that copies a deep link `#card=<id>` (or shows it for copying by hand when the browser blocks the clipboard). Opening such a link, or changing it in an open page, selects the card. Cards are reachable with Tab and selected with Enter or Space. Esc resets; `/` focuses the search box, which dims cards whose title, subtitle, accountable or responsible do not match.

## 6. Build from the template

`templates/workflow.html` in this skill's folder is a complete working page (purchase request to payment, 13 cards, 16 arrows, one group, one feedback arrow marked `back:true`, four themes). Copy it to the output file, never retype it, then edit the copy:

- The CONTENT block, between the `CONTENT: edit everything in this block` and `ENGINE: no edits needed below` marker comments: `TITLE`, `FOOTER`, `STAGES`, `LANE`, `G`, `CARD_W`, `N`, `E`. The browser tab title and the footer line are set from `TITLE` and `FOOTER`; the footer is shown in capitals.
- Outside it, only the `<h1>` (`<h1><span>Title |</span> short subtitle</h1>`; the span takes the accent colour) and the default theme in `<html data-theme="...">`. Leave the ENGINE and the CSS alone.

The CONTENT formats:

```
STAGES = [{key:"a", label:"Request", x:0}, ...]        key: one character; x: the divider
LANE   = {key:"s", label:"Controls &amp; systems", top:745}   or null
G      = [{label, x, y, w, h}, ...]                       dashed groups, or []
CARD_W = 180                                              150 for five stages
N      = [[id, type, x, y, title, subtitle, accountable, what, why, good, kpi, responsible?], ...]
E      = [{f, t, label, pts:[at(f,side,offset?), [x,y], ..., at(t,side,offset?)], lab:[x,y], anchor?:"start"|"end", rot?:-90, bus?:"id", back?:true}, ...]
```

`type` is one of trigger, proc, dec, store, tool, out. `pts` start on the source card edge and end on the target card edge. Read the template's `E` before routing: it shows every pattern (straight horizontal, short vertical with side label, decision branches, dog-leg into a card, lane arrows with rotated labels, an arrow entering a card from below, a feedback arrow along the bottom corridor). `examples/incident-to-improvement.html` adds a loop back to the trigger along the top corridor and a dashed group around two output cards.

## 7. Audit before delivery (required)

The audit is the function in `scripts/audit.js`. Evaluate it in the rendered page, using whichever of these the session has, in this order:

1. A shell with Python: run `python <skill folder>/scripts/wf_check.py "<file>.html"` (`python3` on macOS and Linux), where `<skill folder>` is the folder this SKILL.md is in. It runs `scripts/audit.js` in headless Chromium, prints `{"findings": [...], "console_errors": [...]}`, and exits 0 only when both lists are empty. If Playwright is missing, install it first (`pip install playwright` then `python -m playwright install chromium`) when the session allows installs.
2. A browser tool of the agent's own (a Playwright or Chrome MCP server, a built-in browser pane): open the page at any window size, evaluate the whole of `scripts/audit.js` in it (the file runs itself and returns the list of findings), and read the console.
3. Neither: skip the automated audit, check the route coordinates against the grid by hand, and tell the user plainly that the automated audit was not run.

The audit checks the data (duplicate ids, arrows to unknown cards, unconnected cards, unknown stage keys), the geometry (cards, arrows or labels outside the canvas, cards overlapping, vertical arrows on or within 10 px of a stage divider, arrow ends exactly on the right card edges, arriving and leaving at right angles from outside and clear of corners, final segments long enough for the arrowhead, arrows crossing any card including their own, arrows running on top of each other, labels on or within 4 px of cards, labels on each other, lines through labels or through stage, lane and group titles, those titles on cards) and card text clipped at the bottom or the side. Fix every finding by moving a waypoint, a label or a card, then rerun until `findings` and `console_errors` are both empty. Anything else is never a pass.

Also check the console for errors (a missing constant silently empties the diagram), press Tab until a card is focused and Enter to select it, click at least two cards to confirm the panel, the highlight and the whole-chain toggle work, confirm the reach numbers differ between an early and a late card (if every card shows the same numbers, a return arrow is missing `back:true`), select the card with the most panel text (what, why and what good looks like together) and confirm the panel and canvas stay the same height, and switch through all four themes once; the audit result does not change with theme, but contrast does, so look at graphite separately.

## 8. Deliver

1. The HTML file, named `<Topic> - workflow (interactive).html`, saved in the user's working folder (or the output folder the environment designates).
2. A PNG of the canvas for slides, in the theme that matches the deck (one per theme if the user has not chosen): `python <skill folder>/scripts/wf_check.py "<file>.html" ocean graphite` writes `<name> - <theme>.png` next to the HTML for each theme named (`<name>` is the HTML file name without `.html`); with another browser tool, screenshot the `#c` element at device scale factor 2 in a 2180 x 1180 viewport, with `?theme=<name>` on the URL. On a 16:9 slide place it about 4.9 in high, centred, with a caption line explaining the card colours.
3. Tell the user the page is a single file with no dependencies; that the theme can be switched in the header or forced with `?theme=graphite` in the URL; that Esc resets, `/` searches and Copy link gives a link straight to a card; that cards work from the keyboard (Tab, then Enter); that it is made for a laptop or desktop screen (on a phone it scales down, so pinch to zoom); and that it falls back to Segoe UI or Arial where Inter is not installed.

## Changelog

- 1.4.1: the bottom lane is the user's choice: the agent asks when the request does not say, leaves it out on "no bottom lane", and moves an enabler the user still wants into a stage as a normal card.
- 1.4.0: arrow ends. New `at(id, side, offset)` helper in the template puts arrow ends exactly on a card's edge, so agents no longer type end coordinates by hand. The audit now requires each end to sit on the edge, meet it at right angles from outside and stay 12 px from corners, flags arrows that pass through their own source or target and final segments too short for an arrowhead, and keeps labels 4 px clear of cards. Arrowheads are now a fixed 12 px (they scaled with line width, up to 24 px when highlighted), sit on a straight run even after a tight corner, and touch their card; the old check accepted an end anywhere inside the card or up to 6 px short, which let arrows overshoot, stop short or slide along a border. Examples rewritten with `at()` (rendering unchanged) and two labels moved clear of cards.
- 1.3.0: the page template moved to `templates/workflow.html` and the audit to `scripts/audit.js`, so SKILL.md holds only the rules (about a third of its former size) and agents copy the template instead of retyping it; section 6 lists the CONTENT formats; `wf_check.py` reads `scripts/audit.js` and saves PNGs only after a clean audit. The audit now works at any window size (it used to report dozens of false findings unless the page was shown at full size, which hit agents auditing in a normal browser window) and runs itself when evaluated.
- 1.2.5: the page is 2160 px wide instead of 2120, so the context panel keeps a right margin and no longer touches or pokes past the window edge (at 1920 px it added a sideways scrollbar); PNG export viewport 2180 x 1180 so the canvas is captured at full size; demo animation in the README.
- 1.2.4: audit review fixes. Template: readable incoming/outgoing labels in graphite, and white outgoing arrows there so they stand apart from the grey default arrows; generic `<title>`; Copy link falls back to showing the link when the clipboard is blocked (it used to say "Copied" anyway); cards reachable with Tab and selected with Enter or Space; a viewer's theme pick is remembered per page, so it no longer overrides other files' defaults; deep links also work when changed in an open page; tab title and footer come from `TITLE` and `FOOTER`; `CARD_W` for five stages; panel hint corrected. Audit: also flags arrows or labels outside the canvas, arrows on top of each other, arrows on a stage divider, stage, lane or group titles on cards, and text clipped at the side; `wf_check.py` waits for fonts and layout and finds the audit by its code block. Instructions: x and y are pixels, keys are one character, label rows 222/402/582, documented corridors (bottom y 955 to 985, right edge), second-card and five-stage grids, widening a stage, label placement rules, the lane-label trap, what `bus` does, HTML escaping.
- 1.2.3: new example screenshots (one with a card selected and the context panel open); README cleanup.
- 1.2.2: works in any agent that reads SKILL.md (Claude Code, Codex, Cursor, OpenCode, Hermes Agent, OpenClaw and others): bundled `scripts/wf_check.py` runs the audit and exports PNGs from a shell; audit step lists the options in order; audit no longer crashes on an arrow to an unknown card (it reports it); metadata on one line for loaders that only read single-line frontmatter.
- 1.2.1: skeleton example swapped to a purchase request to payment flow (generic across industries); licence and author metadata in the frontmatter; audit step says what to do when no browser is available.
- 1.2: panel no longer scrolls, canvas and panel always share one height; reach and whole-chain highlight follow the flow only (feedback arrows into the trigger, or marked `back:true`, are skipped) so the numbers and the highlighted path differ per card; graphite fills reworked and legend swatches enlarged, dashed for decisions and drawn as lines for the two arrow entries, so the legend reads in dark mode.
- 1.1: fourth theme (graphite, dark), lane optional, optional responsible per card, optional dashed groups, legend counts, reach counts and full-chain trace, search, Esc and / shortcuts, deep links with Copy link, reduced-motion support, audit extended with data checks, card overlap and clipped text, canvas height follows content without a lane.
- 1.0: first public version with three themes.
