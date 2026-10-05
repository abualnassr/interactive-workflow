#!/usr/bin/env python3
"""Nyx packet lane — drive nyx_packet_builder.py over an approved set.

Reads the owner-approved platform→image map (PLATFORM-IMAGE-MAP.md §2 table),
derives the tier-allowed app list per image, and invokes the existing packet
builder once per image with the allowed apps. Nothing is invented here: the
tier matrix and the voice/format policy come from the map; the packet shape
comes from nyx_packet_builder.py + posting-packet-v1.

HARD RULES enforced by this driver (not negotiable, no flag turns them off):
  * tier rule   — SFW → all socials · suggestive → Telegram only ·
                  explicit → Fanvue only (never a social packet)
  * meta rule   — instagram/facebook packets are human-manual-lane only:
                  status never leaves READY_FOR_HUMAN_REVIEW here, so no
                  agent-side posting path can pick them up
  * venue rule  — discord packets are emitted but venue is disabled fleet-wide
                  (platforms.discord.enabled=false); account stays UNBOUND
  * gates       — every human gate stays pending, posting_authorized=false,
                  scheduler NOT_AUTHORIZED. Approval is a human act.

Usage:
  python3 nyx_packet_lane.py --map <PLATFORM-IMAGE-MAP.md> [--dry-run]
  python3 nyx_packet_lane.py --map <...> --execute [--only PROD2_s2pots]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

BUILDER = Path.home() / ".hermes/scripts/nyx_packet_builder.py"
SOCIAL_APPS = ["instagram", "threads", "facebook", "reddit", "snapchat",
               "telegram", "x", "discord"]

# Tier → allowed social apps (PLATFORM-IMAGE-MAP.md §2 "Tier rule applied").
TIER_APPS: dict[str, list[str]] = {
    "SFW": SOCIAL_APPS,
    "suggestive": ["telegram"],
    "explicit": [],  # Fanvue only — never a social packet
}
META_APPS = {"instagram", "facebook"}


def parse_map(path: Path) -> tuple[dict[str, dict], list[str]]:
    """Parse §2's markdown table into {image: {tier, apps}} + warnings."""
    text = path.read_text()
    section = text.split("## 2.")[-1].split("## 3.")[0]
    rows: dict[str, dict] = {}
    warnings: list[str] = []
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("| Image"):
            continue
        cells = [c.strip().strip("`") for c in line.strip("|").split("|")]
        if len(cells) < 4:
            continue
        image, tier = cells[0], cells[1]
        if not image or set(image) <= {"-", ":"} or image.lower() == "image":
            continue  # table separator row
        if tier not in TIER_APPS:
            warnings.append(f"unknown tier {tier!r} for {image} — skipped")
            continue
        apps = [a for a in SOCIAL_APPS if a in cells[2:]]
        allowed = TIER_APPS[tier]
        derived = [a for a in apps if a in allowed]
        dropped = [a for a in apps if a not in allowed]
        if dropped:
            warnings.append(
                f"{image}: map marks {dropped} but tier={tier} forbids it — dropped")
        rows[image] = {"tier": tier, "apps": derived or [a for a in allowed]}
    return rows, warnings


def slug(image: str) -> str:
    """id-safe batch slug: lowercase, no digits suffix from the capture stamp."""
    base = re.sub(r"-capture_\d+_\.png$", "", Path(image).name, flags=re.I)
    base = re.sub(r"-capture_\d+_\.jpg$", "", base, flags=re.I)
    slug = re.sub(r"[^a-z0-9._-]+", "-", base.lower()).strip("-.")
    return slug if re.match(r"^[a-z0-9][a-z0-9._-]{2,127}$", slug) else f"img-{slug}"


def caption_for(image: str, tier: str, batch: str) -> str:
    """Neutral scaffold, not persona voice. The caption gate is human."""
    return (f"[DRAFT — owner caption gate open] {image} ({tier}) · batch {batch}. "
            f"Voice pass + CTA + disclosure placement are owner decisions; "
            f"this line is a placeholder scaffold, not Nyx copy.")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Nyx packet lane driver")
    ap.add_argument("--map", type=Path, required=True, help="PLATFORM-IMAGE-MAP.md")
    ap.add_argument("--assets", type=Path, default=None, help="approved asset dir")
    ap.add_argument("--only", default=None, help="single image name (smoke test)")
    ap.add_argument("--execute", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv[1:])

    map_text = args.map.read_text()
    assets = args.assets
    if assets is None:
        m = re.search(r"\*\*Canonical folder:\*\* `([^`]+)`", map_text)
        assets = Path(m.group(1)) if m else args.map.parent
    if not assets.is_dir():
        print(f"assets dir not found: {assets}")
        return 2

    rows, warnings = parse_map(args.map)
    if args.only:
        rows = {k: v for k, v in rows.items() if k == args.only}
    if not rows:
        print("no rows parsed from the map — refusing to guess")
        return 2

    receipt = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "driver": "nyx_packet_lane",
        "map": str(args.map),
        "assets": str(assets),
        "mode": "EXECUTE" if args.execute else "DRY",
        "tier_rule": "SFW=all socials; suggestive=telegram only; explicit=fanvue only",
        "meta_rule": "instagram/facebook emitted for the human manual lane only",
        "venue_rule": "discord venue disabled fleet-wide; account UNBOUND",
        "gate_rule": "all human gates pending; posting_authorized=false",
        "warnings": warnings,
        "batches": {},
    }

    total_packets = 0
    failures: list[str] = []
    for image, spec in sorted(rows.items()):
        src = assets / image
        if not src.exists():
            matches = sorted(assets.glob(f"{image.split('-capture')[0]}*"))
            if not matches:
                failures.append(f"{image}: master not found in {assets}")
                receipt["batches"][image] = {"error": "master missing"}
                continue
            src = matches[0]
        batch = slug(image)
        apps = spec["apps"]
        entry = {"tier": spec["tier"], "apps": apps, "master": str(src),
                 "batch_id": batch, "meta_manual_lane": [a for a in apps if a in META_APPS],
                 "discord_venue_disabled": "discord" in apps}
        cmd = [sys.executable, str(BUILDER), "--master", str(src),
               "--apps", ",".join(apps), "--batch-id", batch,
               "--caption", caption_for(image, spec["tier"], batch)]
        if not args.execute:
            cmd.append("--dry-run")
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        entry["builder_rc"] = proc.returncode
        entry["builder_out"] = (proc.stdout or "").strip()[-600:]
        if proc.returncode != 0:
            entry["builder_err"] = (proc.stderr or "").strip()[-400:]
            failures.append(f"{image}: builder rc={proc.returncode}")
        total_packets += len(apps)
        receipt["batches"][image] = entry
        print(f"{'EXEC' if args.execute else 'DRY'} {image} [{spec['tier']}] "
              f"-> {len(apps)} packet(s) rc={proc.returncode}")

    receipt["packets_planned"] = total_packets
    receipt["ok"] = not failures
    receipt["failures"] = failures

    out_dir = Path("/data/AI-OFM-Operations/operations/nyx-launch-001/receipts/packet-lane")
    if args.execute:
        out_dir.mkdir(parents=True, exist_ok=True)
        rp = out_dir / f"packet-lane-{time.strftime('%Y%m%d-%H%M%S')}.json"
        rp.write_text(json.dumps(receipt, indent=2))
        receipt["receipt_path"] = str(rp)
        print(f"receipt: {rp}")
    for w in warnings:
        print(f"WARN {w}")
    print(f"packet-lane {'EXECUTE' if args.execute else 'DRY'}: "
          f"{len(rows)} image(s), {total_packets} packet(s), failures={failures or 'none'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))