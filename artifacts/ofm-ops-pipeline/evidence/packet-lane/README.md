# Evidence · Packet lane wired + executed (2026-10-05)

Proves wiring backlog item **§4c-4** (`packet builder → packets/social/*.json → owner
approve → daily plan + stager consume`) is no longer "discussed but not wired" —
the builder leg now runs end-to-end and its receipts are on disk.

## The decision

Atlas asked: build `packets/social` for the next set, or fix the readback checklist?
**Built the packet lane; the readback checklist was left untouched.** The checklist was
correct — `packets/social` is a non-optional critical artifact of the live cycle. Editing
the checklist to silence an accurate alert would have destroyed the signal.

## What ran

```
python3 ~/.hermes/scripts/nyx_packet_lane.py \
  --map "<approved>/2026-10-03-launch/PLATFORM-IMAGE-MAP.md" --execute
```

`tools/nyx_packet_lane.py` (committed here) is a new driver over the existing
`nyx_packet_builder.py`. It reads the **owner-approved** §2 platform→image matrix, applies
the tier rule per row, and invokes the builder once per image with the tier-allowed apps.
The tier matrix and voice/format policy are not re-invented here — they are read from the
approved map.

| Result | Value |
|---|---|
| Images processed | 11 |
| Packets written to `packets/social/*.json` | **20** |
| Schema validation | 20/20 **PASS** against `posting-packet-v1` |
| Public-copy (EXIF strip + AI provenance + SHA-256 receipt) | 20/20 ok |
| Lane receipt | `packet-lane-receipt-20261005.json` (batch/dry-run/warnings/failures) |
| Plan receipt | `daily-plan-receipt-2026-10-06.json` |

Per-app counts: `s2pots` 8 (SFW → all socials), `s3kneel` 8 (SFW → all socials),
`02bed`/`04pottery`/`kitchenmorn`/`apron` 1 each (suggestive → Telegram only).

## Gates held — no gate was executed

Every one of the 20 packets, verified by reading them back:

```
status              READY_FOR_HUMAN_REVIEW      (never APPROVED_*)
posting_authorized  false
scheduler.status    NOT_AUTHORIZED
platform.account_id UNBOUND
human_gates         caption, cta, disclosure, account, item — all pending
```

Additional constraints the driver enforces with no flag to disable them:

- **Tier rule** — SFW → all socials; suggestive → Telegram only; explicit → Fanvue only,
  never a social packet. Zero explicit-tier images produced a packet.
- **Meta rule** — instagram/facebook packets exist only for the human manual lane; their
  status never leaves `READY_FOR_HUMAN_REVIEW`, so no agent-side path can pick them up
  (consistent with the standing IG/Meta human-only hard rule).
- **Venue rule** — discord packets are emitted but the venue is disabled fleet-wide
  (`platforms.discord.enabled: false` on every profile); account stays `UNBOUND`.

## Downstream legs now verifiable

1. **`ofm-backup-readback.py` → rc=0.** Before: `MISSING packets-social` (ALERT, streak 2).
   After: silent, only informational drift (`receipts: file count 91 -> 100`,
   `staging-ledger: hash changed`). The alert class is closed by building the artifact,
   not by editing the checklist.
2. **`ofm_daily_plan.py` → rc=0, and it is silent for the right reason.** Its receipt reads
   `approved_packets: 0` / `no APPROVED_TO_POST_MANUALLY packets — nothing to plan
   (pre-release)`. It now reads a populated dir and correctly declines to plan packets
   whose gates are open. That is the chain working, not the chain broken.
3. **Owner approval is now the only missing leg** in
   builder → packets → owner approve → daily plan → stager → post evidence.
   Approving means flipping status to `APPROVED_TO_POST_MANUALLY` with the five gates
   recorded as human decisions — a human act; not performed here.

## New finding — manifest vs disk drift (unowned, needs a name)

The approved-set manifest `manifest-2026-10-03-launch.jsonl` records **21** approvals, but
only **11** masters exist in `assets/approved/2026-10-03-launch/`. Missing entirely from disk:
`PRODs2_door`, `PROD2_s1window`, `PROD4_03rollers`, `PROD4_05cat`, `PRODn3_terrace`.
They are also missing across the whole `nyx-launch-001` tree.

This is the same class of defect as the readback alert — a manifest claims an artifact that
the filesystem cannot produce — but it sits in the **asset intake lane**, not the packet
lane, so it is not fixed by this work and has no fix owner assigned. Two candidate causes
(evidence does not yet separate them): post-approval deletion, or an intake bug that
appends the approval row without completing the copy.

- `PROD4_05cat` matters beyond inventory: it is Fanvue post #1 **LIVE** (`cd31c66b…`,
   free teaser) whose only local master is gone — recoverable from the platform itself.
- `PLATFORM-IMAGE-MAP.md` §4 already excludes `PROD4_05v2catfeet` + `PROD4_10stocking` as
  truncated/corrupt — so the asset lane has a known weak spot.

Flagging, not fixing: recovering the masters is an intake-lane decision (re-pull from the
podium volume = spend approval = human gate), not a packet-lane change.

## Reproduce / re-run

```
# dry run (no writes)
python3 tools/nyx_packet_lane.py --map "<approved-set>/PLATFORM-IMAGE-MAP.md" --dry-run
# execute
python3 tools/nyx_packet_lane.py --map "<approved-set>/PLATFORM-IMAGE-MAP.md" --execute
```

`--only <image>` smoke-tests one image (8 packets for an SFW image, 1 for suggestive).