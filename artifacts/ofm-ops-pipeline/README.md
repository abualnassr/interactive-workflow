# OFM Ops Pipeline — Wiring Map, Ownership & Execution Audit

**Date:** 2026-10-05 · **Built by:** Atlas (Hermes agent) for Asmoday · **Version:** v1
**Diagram:** [`OFM Ops Pipeline - workflow (interactive).html`](OFM%20Ops%20Pipeline%20-%20workflow%20(interactive).html) — one self-contained HTML file, click any card for its context panel. PNGs: [ocean](OFM%20Ops%20Pipeline%20-%20workflow%20(interactive)%20-%20ocean.png) · [graphite](OFM%20Ops%20Pipeline%20-%20workflow%20(interactive)%20-%20graphite.png).
**Build source:** [`sources/build_html.py`](sources/build_html.py) (assembles the page from the interactive-workflow template) · **Audit:** `wf_check.py` (headless Chromium) — **findings: 0, console errors: 0** · HTML sha256 `8da9058ab7916784d7ec922911ae2aeab52500b81d131c992f6abd6df046e3ec`.

This artifact maps the full AI-OFM operations pipeline across every agent profile, classifies every job (**wired and working / degraded / discussed but not wired / needs a new connection**), specifies the connections and group chats required, assigns execution ownership end-to-end, flags the human-gated steps (identified, not executed), and carries the receipts proving execution has begun.

---

## 0 · TL;DR

| Dimension | State |
|---|---|
| Agents inventoried | **16 live profiles** + 4 chartered-but-absent roles (Senter, Hephaestus, Nike, Prompt-Engineer) — see §2 |
| Jobs inventoried | **28 in the shared registry** (19 OFM-lane, 2 disabled by design) + 1 in the steward profile — see §4 |
| Wired & working | 12 OFM-lane jobs green with receipts; content→staging→posting→analytics chain live |
| Needs attention | **7 jobs** (provider-credit cluster + one readback-expectation bug); 1 platform job failing — see §4b |
| Discussed but not wired | 9 named items, each with its exact missing connection — see §4c |
| New connections needed | 7 named agent-to-agent seams — see §4d, §5a |
| New group chats | **3** (Production · Distribution · Fleet & Governance) — see §5b |
| Executed in this session | Phone staging verified live on `apollo` (2 byte-readback receipts), fanvue pool status, cron fleet check, cadence SOUL path pin — see §8 |
| Owner-gated (not executed) | Spend, posting, canon, DMs/pricing, account actions — see §7 |
| Owner decisions open | 5 — see §9 |

---

## 1 · The artifact set

| File | What it is |
|---|---|
| `OFM Ops Pipeline - workflow (interactive).html` | 20-card interactive workflow: 5 stages (Plan → Produce → Qualify → Distribute → Operate), 24 labelled arrows, 3 red-dashed exception routes (rescope, KILL-rework, staging-mismatch), bottom lane of shared controls. Four switchable themes, search, deep links, `?exceptions=off` for presenting the normal path. |
| `… - ocean.png` / `… - graphite.png` | Canvas exports for slides (light + dark). |
| `sources/build_html.py` | How the page was generated from the interactive-workflow template (content block only; engine untouched). |
| `evidence/` | Receipts captured 2026-10-05 (§8). |
| `README.md` | This document. |

**Reading the diagram:** click a card → right panel shows accountable owner, what happens, why it matters, what good looks like, fed-by/feeds, reach, KPI. Red dashed = exception routes (rejection/rework/mismatch); the header switch hides them. Human gates are marked in card subtitles (`human gate: …`).

---

## 2 · Agent roster & responsibilities matrix

All 16 profiles live on this machine. "Jobs" = jobs registered in that profile's own cron registry (the shared OFM registry runs under the default profile).

| # | Profile | Role / persona | In room? | OFM pipeline contribution | Own jobs | Status notes |
|---|---|---|---|---|---|---|
| 1 | `default` (**Atlas**) | Orchestrator, control plane, final routing; production/visual approvals route to owner | ✅ | Owns the shared job registry; runs tranche/staging/release scripts; verification | 28 (shared) | Live; this audit |
| 2 | `agora` | Western social & community operator; AI-influencer post engine (drafts only) | ✅ | Pillar briefs, post engine, banned-list/critic passes | 0 | Added 2026-10-05; routing wired; swipe-file list BLOCKED_ON_OWNER |
| 3 | `cadence` | Content & calendar scheduler | ✅ | Briefs, calendar, packet/plan build; schedule-only, never releases | 0 | Digest job not yet wired (§4c-1); SOUL path pin applied 2026-10-05 (§8) |
| 4 | `lore` | ComfyUI R&D + prompt engineering (absorbed `prompt-engineer`) | ✅ | Prompt forge owner; model/workflow contracts from source | 0 | Change-notice-to-room standing rule accepted |
| 5 | `deanna` | HR / crew alignment; profile configs (not default) | ✅ | Staffing, SOUL/config hygiene, role boundaries | 0 | Authored cadence SOUL fix; audits crews |
| 6 | `forge` | Local infra + runbook audit (RTX 2060 lane) | ✅ | Smoke tests, deterministic validation, hygiene audits | 0 | QA conscience; smoke receipts loop pending (§4d-1) |
| 7 | `fleetop` | 80-account social fleet operator; device/account logistics | ➖ | Phone staging (ADB), run sheets, fleet state | 0 | Staging lane verified live 2026-10-05 (§8); needs a seat in Distribution (§5b) |
| 8 | `mint` | Fanvue monetization operator ("Coin"); publish/pricing within policy | ➖ | Fanvue drain (3×/week), chatter/offers as drafts only | 0 | Holds Fanvue MCP tokens; chatter job degraded on provider credits (§4b) |
| 9 | `steward` | Control-room curator; Discord producers; lane oversight | ➖ | Stewardship cycles lead; lane objectives/transitions | 2 | Daily propose-pass 09:30 live |
| 10 | `comfyui-pro` | ComfyUI operations (production gen) per manifest | ➖ | Production execution — *but the profile is a stub today* | 0 | ⚠ No SOUL, no model/route config — cannot hold a room seat until provisioned (§4c-6) |
| 11 | `architect` | Principal software architect (design before code) | ➖ | Not in OFM loop; assigned via Atlas when needed | 0 | Support pool |
| 12 | `coder` | Software builder (dry-run interview → plan → execute) | ➖ | Not in OFM loop | 0 | Support pool |
| 13 | `burner` | Scratch profile (Atlas persona clone) | ➖ | Excluded from OFM by charter | 0 | Support pool |
| 14 | `makima` | Local-model co-pilot (Qwen 3.8-27B, OrcaRouter) | ➖ | Not in OFM loop | 0 | Support pool |
| 15 | `sirvir` | Turbofit customer service | ➖ | Different product line (Turbofit) | 0 | Not OFM |
| 16 | `maintenance` | Fleetgraph repository maintainer | ➖ | Dev repo ops (github.com/asmodaydoescoding/fleetgraph) | 0 | Not OFM |

**Chartered but not present on this machine** (named in the fleet manifest / Discord / docs — do not treat as dispatchable peers):
- `senter` — wiki/comprehension surface; referenced by voice-control channels; not a local profile here.
- `hephaestus` — LoRA engineering role, now executed by scripts (`lora_forge_cron.py`, lora forge lane); no live profile.
- `nike` — rented-GPU runtime role, now executed by `nyx_lane_runner.py` scripts; no live profile.
- `prompt-engineer` — decommissioned 2026-09-09; mandate consolidated into `lore`.
- Factory role codes **M1/R2/R3** (Calliope/Athena/Apollo) are roles *inside* one skill (`generation-factory-specialist-orchestration`) — not agents.

---

## 3 · The pipeline as one loop

```
signals → brief → prompt forge → (spend + KEEP gate) → contract/smoke → tranche →
deterministic validation → owner visual QA → release + derivatives → packets/plan →
phone staging (apollo) → manual posts (socials) / agent posts (Fanvue) →
post evidence → 24h metrics → weekly classification → next batch
              ▲                                                    │
              └────────────────── signals / trend feedback ────────┘
```
Oversight: stewardship cycles watch the lanes; cron fires the read-only work; every stage closes with a receipt. Human gates sit at: spend/KEEP, visual QA, release of explicit content, manual posting, DMs/pricing, account actions.

---

## 4 · Wiring audit

### 4a · Wired and working (green, receipts-backed)

| Job | Schedule | Last run | Notes |
|---|---|---|---|
| context / skills / agents / loops factories | every 3h | 2026-10-05 03:19–05:19 | proposal-only wiki factories |
| ofm-daily-briefing | 09:00 | 2026-10-04 09:17 ok | read-only ops brief → Discord #daily-briefing |
| ofm-missing-metrics | 09:10 | 2026-10-04 09:25 ok | lists receipts lacking analytics rows |
| ofm-stewardship-cycles | 08:45 | 2026-10-04 08:46 ok | lane objectives; transitions only |
| ofm-prompt-forge | 10:30 | 2026-10-04 10:39 ok | inspiration → Nyx brief + prompts + receipt |
| ofm-daily-plan | 08:15 | 2026-10-04 08:24 ok | silent when no approved packets (currently: pre-release) |
| ofm-fanvue-billing | 09:30 | 2026-10-04 09:31 ok | read-only earnings sync |
| ofm-analytics-rows | 09:40 | 2026-10-04 09:40 ok | prefills 24h rows |
| ofm-comment-scan | 10:00 | 2026-10-04 10:01 ok | flags comments needing human review |
| lora-forge-biweekly | every 360m | 2026-10-05 01:11 ok | LORA FORGE onboarding ticks |
| studio-library-index | 08:20 | 2026-10-04 08:25 ok | studio library index |
| ofm-engagement-research | Mon 11:00 | 2026-10-01 05:13 ok | weekly campaign research |
| ofm-fanvue-drop | Tue/Thu/Sat 03:00 | 2026-10-03 08:26 ok | pool drain (1 posted; 6 pending; next fire Tue 2026-10-06 03:00) |

Re-verified live this session: `check_ofm_jobs.py` + drop dry-run + phone staging (§8).

### 4b · Needs attention / degraded (verified 2026-10-05 06:4x)

`check_ofm_jobs.py jobs` → `ofm-cron-jobs=attention 9/16`.

| Job | Symptom | Root cause (evidence) | Fix owner |
|---|---|---|---|
| ofm-weekly-analytics | last run 09-28 error, streak 1 | cron worker dispatch failed in the fleet-wide provider outage window; next run Mon 09:20 | Atlas (watch) + provider fix (§4c-5) |
| ofm-policy-digest | last run 09-28 error, streak 1 | same window; next run Mon 09:30 | Atlas (watch) |
| ofm-asset-hygiene | 2026-10-05 03:20 error | `HTTP 429: usage limit reached` (runner quota — provider cluster) | provider fix (§4c-5) |
| ofm-fanvue-chatter | 2026-10-04 error | `HTTP 400: insufficient credits` — draft pass can't call its model | provider fix (§4c-5) |
| ofm-backup-readback | streak 2, ALERT | **`MISSING packets-social: …/packets/social`** — the packet dir was never built for the launch cycle (phone-staging lane bypassed it); readback expectation vs lane reality | Cadence/Atlas — build the packet lane or update the checklist (§4c-4) |
| ig-daily-fetch | disabled, streak 20 | parked by design after the 2026-09-30 IG suspension (pause verified 09-30) | owner — unpark decision |
| ofm-ig-health | disabled | same park | owner — unpark decision |
| hermes-bug-loop *(platform)* | exit 2 `read-issue`, streak 14 | platform tooling (separate lane) | maintenance/coder |

### 4c · Discussed but not wired (named — this is the work backlog)

1. **Cadence daily digest job** (07:00 EEST, fires only when slots exist) — blocked on: (a) channel target pick (#content-batches exists; #content-calendar does not; text-to-Atlas is the honest default), (b) `platforms.discord.enabled: false` on every profile. *Missing connection: Cadence job → chosen surfacing target.*
2. **Agora swipe-file account list** — **BLOCKED_ON_OWNER** (standing blocker declared in room).
3. **Lore change-notice rule** — accepted as a standing rule (no silent model/workflow swaps); *mechanism not yet written into any checklist/automation.*
4. **Packet lane for the live cycle** — the manual lane (staging tree + platform map) posted the launch set; `packets/social/` was never built, so (a) backup-readback alerts, (b) daily plan stays silent, (c) phone stager's packet mode goes unused. *Missing connection: packet builder → `packets/social/*.json` → owner approve → daily plan + stager consume.* Also note handle binding (step 19, `UNBOUND` accounts) is the upstream owner-blocked step.
5. **Fallback provider repair (fleet-wide)** — `deepseek-v4-flash` is a dead id and the deepseek account is 402; b.ai 403; experiential 401; codex lane quota-locked (resets Oct 10). **11 profiles carry a failover chain that cannot produce a token.** Options: fund (rec: small top-up + id correction) / drop (fail loud) / **repoint to the free ladder ($0 — fleet-router ready; pool probed live)**. *Owner decision — route changes are gated.*
6. **`comfyui-pro` provisioning** — stub profile (no SOUL, no model config). Production currently executes via scripts under Atlas. *Needs Deanna/owner provisioning before the profile can serve as the lane owner.*
7. **Kanban handoff bus** — 4 boards exist (`ofm-content-pipeline`, `ofm-cron-ops`, `ofm-factory-evidence`, `ofm-fleetop-pilot`), **all empty**; handoffs run on receipts/scripts instead. *Decision: wire it (assign boards to lanes) or retire it formally.*
8. **Sweep keeps → posting pool** — `assets/approved/2026-10-04-sweep/` (56 masters) not wired into any posting lane; fanvue pool has 6 pending + 7 unapproved-owner; drop script drains the pool only. *Missing connection: approved sweep → pool/packet selection (owner-approved set).*
9. **V2 test-drive venue decision** — explicit-media venue still parked from the 2026-10-01 incident (Discord home was wrong; Telegram/local candidate). *Owner decision.*

### 4d · Needs a new connection between agents (the seams)

| # | Connection | What passes | Status |
|---|---|---|---|
| 1 | **Lore ↔ Forge** | validated contract → smoke pass/fail receipt back to the KB | agreed in room 2026-10-05; not mechanized |
| 2 | **Agora ↔ Lore** | brief (persona/pillar/platform/anchors) → tested spec + failure modes + GAP list | agreed; **Agora side written** → [`interfaces/brief-to-spec-interface-v1.md`](interfaces/brief-to-spec-interface-v1.md) + `social-command` skill; Lore counter-sign pending |
| 3 | **Agora/Cadence ↔ Deanna** | canon/voice blessing loop on briefs & copy | agreed; not mechanized |
| 4 | **FleetOp ↔ Distribution room** | packets → run sheet → staging receipts → post evidence | staging live; room missing (§5b) |
| 5 | **Mint ↔ human approval queue** | chatter/offer/pricing drafts → owner queue (never auto-send) | drafts exist; queue surface not wired |
| 6 | **Steward ↔ rooms/channels** | producer rule: every channel a live producer; new-agent channel sync | rule stated; not executed for the 3 new rooms |
| 7 | **Alert class → fix owner routing** | job failures route to a named owner (readback→Cadence, provider→Atlas/owner, IG→owner) | ad-hoc today |

---

## 5 · Connection & group-chat plan

### 5a · Connections to make (execute order)

1. **Fallback repair** (owner picks A/B/C from §4c-5) → Atlas executes fleet-wide, verifies per-profile live probe.
2. **Cadence digest** → channel pick + Discord enable (owner) → Cadence job created → first fire verified.
3. **Packet lane** → Cadence builds packets for the next approved set (after handle-binding decision) → backup alert clears.
4. **Lore↔Forge receipts loop** → tiny spec: forge smoke writes receipt to KB path; Lore validates on next contract pass.
5. **Agora↔Lore + Deanna loops** → written into both profiles' operating docs (same pattern as the change-notice rule). *Agora↔Lore: Agora side done 2026-10-05 (contract + skill); Lore and Deanna halves pending.*
6. **Mint draft queue** → define the queue surface (kanban or receipts/chatter + daily digest line).
7. **Steward + new rooms** → channels/producers for the 3 rooms below; roundtable charter update.

### 5b · Group chats — existing and to be created

| Room | Members | Purpose | First agenda |
|---|---|---|---|
| **Existing:** "Atlas, Agora, Lore, Deanna, Forge" (+ Cadence) | atlas, agora, cadence, lore, deanna, forge | Content & QA-prep lane: briefs → prompts → contracts, canon blessing, change notices | close §4d-1/2/3 loops; swipe-file decision |
| **New:** OFM Production | atlas, lore, forge, comfyui-pro (after provisioning) | Generation lane war room: contracts → smoke → tranches → validation; tranche receipts & failure modes | comfyui-pro provisioning; first tranche after next KEEP |
| **New:** OFM Distribution | atlas, cadence, fleetop, mint | Packets → phone staging → manual posting evidence → Fanvue drain; pacing vs cadence windows | packet lane kickoff; wave-2 Fanvue decision; staging receipts |
| **New:** Fleet & Governance | atlas, deanna, steward, fleetop | Staffing, routes/creds, Discord producer rule, device fleet state; executes the fallback repair once decided | fallback repair execution plan; room/channel sync |

*(A legacy room "Atlas, Deanna, FleetOP, Steward, Hephaestus, ComfyUI Pro" was deleted earlier — the new rooms rehome those guards; Hephaestus as a member is replaced by the Forge lane.)*

---

## 6 · Execution ownership map (start → finish, minus human gates)

| Stage | Step | Executes | Trigger | Output / receipt | Gate |
|---|---|---|---|---|---|
| Plan | Inspiration & engagement signals | Atlas registry jobs (research) | daily/Mon | ledger + briefs | — |
| Plan | Pillar brief & batch scope | **Cadence** (+Agora) | per batch | brief doc | — |
| Plan | Prompt forge | **Lore** (job 10:30) | daily | brief + prompts + receipt | — |
| Plan | Spend + KEEP verdict | **Asmoday** | per batch | verdict + envelope | 🚪 |
| Produce | Contracts & smoke | **Lore** drafts / **Forge** smokes | per contract | smoke receipt | — |
| Produce | Generation tranche | **comfyui-pro lane** (runner by Atlas) | per approved batch | renders + receipts | 🚪 spend |
| Produce | Deterministic validation | **Forge** | per output | validation / quarantine | — |
| Qualify | Owner visual QA | **Asmoday** | per batch | KEEP / KILL | 🚪 |
| Qualify | Release & derivatives | **Atlas** (scripts) | per KEEP | derivatives + public copy + hashes | 🚪 disclosure confirm |
| Qualify | Hygiene audit | system (03:00) | daily | anomaly list | — |
| Distribute | Packet & plan build | **Cadence** (builder) | per release | packets + plan | 🚪 handle binding |
| Distribute | Phone staging | **FleetOp** (ADB) | per packet | staging receipts | — |
| Distribute | Manual posting (socials) | **Asmoday** (from apollo) | per window | post evidence | 🚪 |
| Distribute | Fanvue drain | **Mint** | Tue/Thu/Sat 03:00 | drop receipts | within approved pool |
| Distribute | Chatter / offers / pricing | **Mint** (drafts only) | daily | draft queue | 🚪 to send |
| Distribute | Comment & DM watch | system → human | daily | flag list | 🚪 resolves |
| Operate | Evidence & 24h metrics | **Atlas** + owner input | 24h after post | analytics rows | — |
| Operate | Weekly classification | **Atlas** | Mon | digest | — |
| Operate | Billing sync | system (mint tokens) | daily | ledger | — |
| Operate | Stewardship cycles | **Steward** + Atlas | daily 08:45 | lane states | — |
| Operate | Backup readback | system (03:30) | daily | alert if missing | — |
| Operate | LoRA forge | **Forge** lane scripts | 360m | onboarding units | 🚪 spend |
| Operate | Wiki factories | system | 3h | proposals only | — |

---

## 7 · Human-gated steps — flagged, NOT executed

Per the operation's gate doctrine (rented GPU/spend · external routes with spend exposure · public posting/scheduling · DMs/mass messages/PPV/pricing · explicit publishing venue · canon/identity changes · account creation/login recovery · handle binding · platform-policy calls · complaint/chargeback handling). None were executed in producing this artifact. Open gates right now: **spend envelope** (fallback repair + next tranche), **handle binding** (blocks packets), **manual posts** (owner from apollo), **wave-2 Fanvue confirm**, **v2 venue**, **swipe-file list**.

---

## 8 · Evidence that execution has begun (2026-10-05)

| Evidence file | Proves |
|---|---|
| `evidence/phone-stage-mkdir-20261005.json` | `nyx_phone_stage.py --mkdir-only --execute` on `apollo` (serial 16a71a80): all 8 app dirs present, readback OK |
| `evidence/phone-stage-push-20261005.json` | Byte-verified push (size + md5 match on-device) through the same lane — the staging leg that was blocked on device connection now runs |
| `evidence/fanvue-drop-*.txt` | Pool state: 1 posted / 6 pending / 7 unapproved-owner; dry-run shows next post + no side effects |
| `evidence/cron-health-check-20261005.txt` | Live fleet check `attention 9/16` with per-job detail |
| `evidence/cron-registry-20261005.md` | All 28 jobs with last-run status — the audit's source table |
| `evidence/sessions-inventory-20261005.md` | Agent session history ~2026-10-01→05 (305 sessions / 26,895 msgs; subagent waves, factories, room threads) |
| `evidence/cadence-soul-pathpin-20261005.md` | The one residual room-approved SOUL fix, applied (file + old/new strings for audit) |
| This repo commit | The artifact itself: diagram (audit pass), document, evidence — published to `github.com/abualnassr/interactive-workflow` |

**Publication:** [PR #1](https://github.com/abualnassr/interactive-workflow/pull/1) — fork `asmodaydoescoding` → `abualnassr:main`, mergeable (verified via API). Direct push with automation credentials is pull-only on that repo, so the PR is the publication path; merge to land it.

---

## 9 · Open decisions for the owner

1. **Fallback repair** — (A) fund deepseek + fix the id, (B) drop the chain to fail loud, (C) repoint 11 profiles to the live free ladder ($0, ready). *Recommendation: C now, A-lite at leisure.*
2. **Cadence queue target** — #content-batches / new #content-calendar / text-to-Atlas, + fleet-wide `platforms.discord.enabled` flip.
3. **Fanvue wave-2** — confirm the 7 `unapproved-owner` items; 6 pending drain automatically starting Tue 03:00.
4. **Create the 3 new group chats** (§5b).
5. **V2 test-drive venue** — decide the explicit-media surface (still parked from 2026-10-01).

---

## 10 · Method & provenance

Sources: live `~/.hermes/cron/jobs.json` + executions, agent profile SOULs/configs, group-room transcripts (2026-10-05), `/data/AI-OFM-Operations` tree (receipts, packets, pools), `~/.hermes/scripts/` runners, and the vault docs (*OFM Recurring Job Inventory 2026-09-15*, *OFM Automation Job Map 2026-09-14*, *Fleet Profile Manifest 2026-09-09*, *Human Approval Gates*, *Automation Control Map*). Diagram generated with the **interactive-workflow** skill (v1.5.0) via `sources/build_html.py`; layout audit passed with zero findings and zero console errors; interaction checks (card panel, keyboard select, exception toggle, search, theme, reach numbers) verified in headless Chromium.
*Boundary: this artifact mirrors operations; Go-Live Plan v2 and the authority docs keep doctrine authority. Nothing here overrides a gate.*
