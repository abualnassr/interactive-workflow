# Brief-to-Spec Interface v1 — Agora ↔ Lore (pillar-first input contract)

> Fleet copy. Vault canonical: `Projects/AI OFM 2026 Ecosystem/Content Pipeline/Brief-to-Spec Interface v1.md`. Committed 2026-10-05 for the artifact's seam §4d-2 wiring (Agora side + Lore side written; counter-signed 2026-10-05).

Wires the **Agora ↔ Lore** seam from this map (§4d-2, §5a-5) — same pattern as the change-notice rule: each side writes the contract into its operating docs. Authority: **Content Quality Playbook — Posts v1** (pillar-first, staged workflow, visual gate). This contract does not override any gate.

## A · Inbound — every brief entering the post engine carries this (pillar-first)

| Field | Rule |
|---|---|
| persona | `Nyx Marlowe` or `Elin Svan`. Elin canon status is `blocked` (no face authority) — drafts park with `GAP: elin-face-remaster`, no filler. |
| pillar | **exactly one** from the signed set. Nyx candidates (pending owner sign-off): Night City Frame · Controlled Distance · Real Life Cinematic · Style Craft. Missing → **rejected before drafting** ("no pillar, no draft"). |
| platform + format | target surface + post format (single image / carousel / Reel / story). |
| goal | what the post must do in the funnel (calibration, engagement, story beat, launch support). |
| angle seed | ≥1 candidate angle, one line + hook sketch. Ideation stays in the engine (Stage A = 3+ angles). |
| anchors | continuity anchors (place, motif, outfit, time) + identity refs (face-lock path, approved reference stack). |
| tier | SFW / suggestive / explicit lane. |
| concrete-detail seed | ≥1 candidate concrete detail (place, object, time, opinion, small conflict). Absent → `GAP:` flag raised; **never** filled with generic filler. |
| source refs | swipe/inspiration references + manifest provenance. Pattern-level only; engagement only from manifests, never invented. |

A brief that arrives as a pre-written draft still passes A → B → C; the seed is the input, the spec is the output.

### Hard rules

- No pillar → no draft (playbook rule zero).
- Missing concrete detail → GAP flag, draft paused.
- Voice: emotional posture + visual storytelling only while the phrase-level voice guide is `BLOCKED_KNOWN_UNKNOWN`; no claimed canonical vocabulary, slang register, or CTA style.
- Stage C gates: banned-list scan, humanizer pass, ≥1 concrete detail, no em dashes. Any miss → rewrite.
- Disclosure is built in (bio + platform labels + packet line); never the public hook.
- Human gate: nothing advances to publish without owner approval.

## B · Outbound — spec → Lore (prompt request)

Built from the spec's *Scene or shot* + anchors, sent as the four-block ping (per the prompt-generation-routing lane):

1. **ENVIRONMENT** — lane + model/workflow: `Krea 2 — ComfyUI lane` / `Nano Banana — Gemini web app` / `MiniMax H3` / `Seedance`.
2. **INPUTS** — scene/shot from the spec; continuity anchors; identity refs (approved stack paths); tier; platform; visual banned-list items to avoid.
3. **OUTPUT wanted** — finished prompt, verbatim-usable, with notes (negatives, text-settling, camera).
4. **AUTHORIZATION SCOPE** — only pre-approved gated actions; everything else parks.

Binding: every ping carries its **`spec_id`**. Prompt craft stays with Lore — the post engine never authors or rewrites prompts locally.

## C · Return — Lore → spec (closes seam §4d-2)

- Verbatim prompt + notes → used as-is in the target lane.
- **Failure modes + GAP list** → attached to the same `spec_id`.
- The spec returns to the brief owner **tested**: filled spec + prompt status + failure modes + GAP list.
- Render QA failures (prompt drift, artifacts) → re-ping carrying prompt id + failed output path; failure modes accumulate on the spec.
- Smoke pass/fail receipts (Forge loop, seam §4d-1) bind `prompt id ↔ spec id ↔ render hash`.
- Failure modes feed the playbook visual gate + banned list via the QA-reports lane — calibration first, doctrine only when owner-approved.

## D · Cross-refs & status

- Seam §4d-3: briefs/copy touching canon or voice route to **Deanna** for blessing before advancing.
- Roles: brief source = Cadence (pillar brief & batch scope) · drafts = Agora · prompts = Lore · smoke = Forge · approval = owner.
- **Status:** Both sides wired 2026-10-05 — Agora: `social-command` skill v1.1.0; Lore: `SOUL.md` §"Brief→spec interface" (intake + return shape + smoke-receipt validation). **Seam §4d-2 closed.**
