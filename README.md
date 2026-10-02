# interactive-workflow

An agent skill for Claude Code, OpenAI Codex, Cursor, OpenCode, Hermes Agent, OpenClaw and other agents that read `SKILL.md`. It turns a process description into a self-contained, clickable HTML diagram: cards on a fixed grid, labelled orthogonal arrows, a context panel on the right, search, deep links, four colour themes (one dark), and a PNG for slides. One file, no dependencies, works offline, opens in any browser.

Built for process maps, operating models, governance frameworks and work flows where every step has an accountable owner, an input, an output and a KPI. It is not a general drawing tool.

## What it looks like

Purchase request to payment, Ocean theme (default), with the decision "Within approval limit?" selected. Arrows that feed it light up in the accent colour, arrows it feeds in the second colour, everything else fades back, and the panel on the right shows its context:

![Purchase request to payment, Ocean theme, card selected](examples/purchase-request-to-payment%20-%20ocean.png)

The same diagram in the Forest theme, nothing selected:

![Purchase request to payment, Forest theme](examples/purchase-request-to-payment%20-%20forest.png)

A second example, incident to improvement, in Graphite (dark):

![Incident to improvement, Graphite theme](examples/incident-to-improvement%20-%20graphite.png)

And in Ember:

![Incident to improvement, Ember theme](examples/incident-to-improvement%20-%20ember.png)

Open either HTML file in the `examples` folder in a browser and click a card. The panel shows who is accountable and responsible, what happens, why it matters, what good looks like, what feeds the card, what it feeds, how far its reach goes along the flow, and the KPI it reports. Tick "whole chain" to follow every upstream and downstream step. Esc resets, `/` searches, Copy link gives a link straight to a card, and the buttons top right switch theme. Cards also work from the keyboard: Tab to a card, Enter to select it.

## Install

The skill is a plain `SKILL.md` folder in the open [Agent Skills](https://agentskills.io) format, so it works in any agent that reads skills, not only Claude.

### Any agent, with the skills CLI (recommended)

```
npx skills add abualnassr/interactive-workflow -g -a <agent>
```

`-g` installs it for your user account (leave it out to install into the current project only). Pass one or more agent ids after `-a`, separated by spaces, or `-a '*'` for every agent the CLI supports:

| Agent | `-a` id |
|---|---|
| Claude Code | `claude-code` |
| OpenAI Codex | `codex` |
| Cursor | `cursor` |
| OpenCode | `opencode` |
| Hermes Agent | `hermes-agent` |
| OpenClaw | `openclaw` |
| GitHub Copilot | `github-copilot` |
| Gemini CLI | `gemini-cli` |
| Windsurf | `windsurf` |
| Cline | `cline` |
| Roo Code | `roo` |
| Kilo Code | `kilo` |
| OpenHands | `openhands` |
| Goose | `goose` |
| Amp | `amp` |
| Continue | `continue` |
| Zed | `zed` |
| Warp | `warp` |
| Qwen Code | `qwen-code` |
| Kiro CLI | `kiro-cli` |
| Junie | `junie` |
| Trae | `trae` |
| Augment | `augment` |
| Droid (Factory) | `droid` |
| AiderDesk | `aider-desk` |

For example, Claude Code, Codex and Hermes Agent in one go:

```
npx skills add abualnassr/interactive-workflow -g -a claude-code codex hermes-agent
```

Run `npx skills add --help` for the full, current list of agents.

### Claude apps (claude.ai, Claude Desktop, Cowork)

Download `interactive-workflow-v*.zip` from the [latest release](https://github.com/abualnassr/interactive-workflow/releases/latest), then in Claude go to Settings, then Skills (Capabilities on some plans), choose Add skill and upload the zip.

### Aider

Aider has no skills folder, so load the file as read-only context for the session:

```
aider --read path/to/interactive-workflow/SKILL.md
```

or add it under `read:` in `.aider.conf.yml` to load it every time.

### By hand

Clone this repository into your agent's skills folder; the repository root is the skill folder:

```
git clone https://github.com/abualnassr/interactive-workflow
```

Keep `SKILL.md` and `scripts/` together. The `examples` folder is only for you to look at.

## Use

Ask in plain language, for example:

- "Make an interactive process flow of our change management procedure."
- "Turn this Mermaid flowchart into a clickable workflow with a dark theme."
- "Map our hiring process as an interactive diagram: stages, owners, decisions, systems, plus a PNG for the deck."

The agent will ask for whatever the source does not give (stages, cards, arrows, who is accountable), build the page, run a collision audit in a headless browser, and hand back the HTML and PNG.

## Audit and PNG export

The skill checks every diagram for collisions before handing it over, and renders a PNG for slides. Both need a headless browser. The bundled script does both from any shell:

```
pip install playwright
python -m playwright install chromium
python <skill folder>/scripts/wf_check.py "My process - workflow (interactive).html" ocean graphite
```

Use `python3` on macOS and Linux. It prints the audit findings as JSON (an empty list is a pass) and saves one PNG per theme named. The agent runs it for you when it has a shell; agents with their own browser tool (a Playwright or Chrome MCP server, a built-in browser) can use that instead. With neither, the skill still builds the page and says plainly that the audit was not run.

## What the skill enforces

- A fixed grid (180 x 140 px cards, four columns, four rows, an optional enablers lane) so nothing overlaps.
- Explicit orthogonal arrow routes with labels that say what passes, never "next".
- Six card types: trigger, process step, decision, data store, control or standard, output or forum.
- An audit (`scripts/wf_check.py`) that fails the build on duplicate ids, arrows to unknown cards, unconnected cards, cards, arrows or labels off the canvas, arrows through cards, arrows on top of each other, labels on cards or on each other, lines through text, titles on cards, clipped card text, and console errors.
- Four themes as CSS variables: Ocean, Forest, Ember, Graphite. Add a client brand by copying one block.

## Notes

- Made for a laptop or desktop screen. On a phone the whole page scales down to fit, so pinch to zoom.
- The page uses the Inter font when installed and falls back to Segoe UI or Arial.
- A viewer's theme choice is remembered for that page only; `?theme=graphite` (or any theme name) in the URL forces one.
- In a plain chat with no shell or browser (claude.ai without code execution, for example) the skill builds the page and tells you the audit was not run.
- Feedback arrows (into the trigger, or marked `back:true`) are drawn but not followed when counting reach, so the numbers mean something.

## Licence

MIT. Copyright 2026 Bandar Abualnassr.
