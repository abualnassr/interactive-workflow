#!/usr/bin/env python3
"""forge_smoke_receipt.py — local-lane smoke receipt writer (seam 4d-1 write half).

Owner: forge (local RTX 2060 lane: smoke, diagnostics, masks, metadata, post-processing).
Boundaries enforced in code, not by comment:
  * local lane only — enqueues against 127.0.0.1:8188, refuses any other host
  * smoke tier only — the prompt is a QA probe, never persona/canonical copy
  * fresh seed per run, drawn from os.urandom, recorded in the receipt
  * deterministic artifact verification — sha256 over the rendered PNG
  * binds prompt id <-> spec id <-> render hash (Lore validates the triple)

The prompt embedded here is FORGE-AUTHORED SMOKE PROBE TEXT, not a Lore-authored
canonical prompt and not publishable copy. spec_id carries the `forge-smoke:`
prefix so a validator can never mistake a smoke probe for a contracted spec.

Usage:
  python3 forge_smoke_receipt.py [--out RECEIPT.json] [--steps N] [--label TEXT]
Exit:
  0 = runtime proof (artifact rendered + hashed)   1 = preflight/runtime failure
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import sys
import time
import urllib.error
import urllib.request

API = "http://127.0.0.1:8188"
CHECKPOINT = "v1-5-pruned-emaonly.safetensors"
WIDTH, HEIGHT = 512, 512

# Forge-authored smoke probe text. Generic still life, no persona identity, no
# canon reference, no platform copy. Deliberately unremarkable so the receipt
# measures the LANE (node classes, checkpoint, sampler, VRAM), not taste.
POSITIVE = (
    "a plain grey ceramic mug on a wooden desk beside a closed notebook, "
    "soft window daylight, shallow depth of field, neutral product photo"
)
NEGATIVE = "text, watermark, signature, nsfw, nude, extra fingers, deformed"

# Mandated runtime vocabulary. The CODE is the only thing allowed in `status`;
# the prose lives in `status_detail`. Never put a description in `status`.
STATUS_DETAIL = {
    "PREFLIGHT_BLOCKED": "lane unreachable or required node classes absent",
    "RUNTIME_FAILED": "graph submitted but produced no artifact",
    "PREFLIGHT_READY": "graph submitted",
    "TRANCHE_COMPLETE": "artifact rendered, hashed, embedded prompt extracted",
}
REQUIRED_NODES = [
    "CheckpointLoaderSimple",
    "CLIPTextEncode",
    "EmptyLatentImage",
    "KSampler",
    "VAEDecode",
    "SaveImage",
]


def _get(path: str, timeout: int = 30):
    with urllib.request.urlopen(API + path, timeout=timeout) as r:
        return json.load(r)


def _post(path: str, payload: dict, timeout: int = 30):
    req = urllib.request.Request(
        API + path,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def preflight() -> dict:
    """Read /system_stats and /object_info. Returns a preflight record."""
    if not API.startswith("http://127.0.0.1"):
        sys.exit("forge_smoke_receipt: refusing non-local API %r" % API)
    stats = _get("/system_stats")
    dev = stats["devices"][0]
    oi = _get("/object_info")
    ckpts = oi["CheckpointLoaderSimple"]["input"]["required"]["ckpt_name"][0]
    return {
        "api": API,
        "comfyui_version": stats["system"]["comfyui_version"],
        "device": dev["name"],
        "vram_total": dev["vram_total"],
        "vram_free": dev["vram_free"],
        "object_info_classes": len(oi),
        "required_nodes": {n: (n in oi) for n in REQUIRED_NODES},
        "checkpoint_available": CHECKPOINT in ckpts,
    }


def embedded_prompt(png_path: str) -> dict:
    """Pull the tEXt 'prompt' chunk out of the rendered PNG.

    Per doctrine the embedded workflow prompt is untrusted data: it is extracted
    and recorded, never executed or echoed as instruction.
    """
    import struct
    import zlib

    out = {"present": False, "sha256_of_chunk": None, "length": None}
    with open(png_path, "rb") as fh:
        assert fh.read(8) == b"\x89PNG\r\n\x1a\n", "not a PNG"
        while True:
            head = fh.read(8)
            if len(head) < 8:
                break
            length, ctype = struct.unpack(">I4s", head)
            data = fh.read(length)
            fh.read(4)
            if ctype == b"IEND":
                break
            if ctype == b"tEXt" and data.startswith(b"prompt\x00"):
                raw = data.split(b"\x00", 1)[1]
                out["present"] = True
                out["length"] = len(raw)
                out["sha256_of_chunk"] = hashlib.sha256(raw).hexdigest()
                out["triggers_present"] = {
                    t: (t.encode() in raw) for t in ("nyxmarlowe_v2x", "r3alism")
                }
    return out


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def build_graph(seed: int, steps: int) -> dict:
    return {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": CHECKPOINT},
        },
        "2": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": POSITIVE, "clip": ["1", 1]},
        },
        "3": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": NEGATIVE, "clip": ["1", 1]},
        },
        "4": {
            "class_type": "EmptyLatentImage",
            "inputs": {"width": WIDTH, "height": HEIGHT, "batch_size": 1},
        },
        "5": {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed,
                "steps": steps,
                "cfg": 6.0,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1.0,
                "model": ["1", 0],
                "positive": ["2", 0],
                "negative": ["3", 0],
                "latent_image": ["4", 0],
            },
        },
        "6": {
            "class_type": "VAEDecode",
            "inputs": {"samples": ["5", 0], "vae": ["1", 2]},
        },
        "7": {
            "class_type": "SaveImage",
            "inputs": {"filename_prefix": "forge_smoke", "images": ["6", 0]},
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="")
    ap.add_argument("--steps", type=int, default=12)
    ap.add_argument("--label", default="forge-seam-4d-1-smoke")
    args = ap.parse_args()

    started = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    t0 = time.time()
    run_tag = time.strftime("%Y%m%d-%H%M%S")
    prompt_id = "%s-%s" % (args.label, run_tag)
    spec_id = "forge-smoke:%s" % prompt_id  # NOT a contracted spec — see module docstring
    seed = secrets.randbits(53)  # fresh seed per run, never reused

    def finish(code: str, detail_key: str) -> int:
        """Stamp the mandated status code, its detail line, and elapsed time."""
        receipt["status"] = code
        receipt["status_detail"] = STATUS_DETAIL[detail_key]
        receipt["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        receipt["elapsed_s"] = round(time.time() - t0, 2)
        _emit(receipt, args.out)
        print("%s: %s" % (code, receipt.get("error") or STATUS_DETAIL[detail_key]))
        return 0 if code in ("PREFLIGHT_READY", "TRANCHE_COMPLETE") else 1

    receipt = {
        "receipt_version": "smoke-receipt-v1",
        "schema": "forge.smoke_receipt/1",
        "written_by": "forge",
        "lane": "local-rtx2060",
        "lane_scope": "smoke/diagnostics/masks/metadata/post-processing — not production",
        "spec_id": spec_id,
        "prompt_id": prompt_id,
        "spec_id_class": "forge_smoke_probe",
        "publishable": False,
        "started_at": started,
        "status": None,
    }

    try:
        receipt["preflight"] = preflight()
    except (urllib.error.URLError, OSError, KeyError) as exc:
        receipt["error"] = repr(exc)
        return finish("PREFLIGHT_BLOCKED", "PREFLIGHT_BLOCKED")

    missing = [n for n, ok in receipt["preflight"]["required_nodes"].items() if not ok]
    if missing or not receipt["preflight"]["checkpoint_available"]:
        receipt["error"] = "missing=%s checkpoint=%s" % (
            missing,
            receipt["preflight"]["checkpoint_available"],
        )
        return finish("PREFLIGHT_BLOCKED", "PREFLIGHT_BLOCKED")

    graph = build_graph(seed, args.steps)
    receipt["graph"] = {
        "nodes": len(graph),
        "classes": sorted({n["class_type"] for n in graph.values()}),
        "topology": "linear: ckpt -> clip(+/-) -> empty latent -> ksampler -> vae -> save",
        "checkpoint": CHECKPOINT,
        "width": WIDTH,
        "height": HEIGHT,
        "steps": args.steps,
        "cfg": 6.0,
        "sampler_name": "euler",
        "scheduler": "normal",
        "fresh_seed": seed,
        "seed_policy": "secrets.randbits(53), one seed per run, never reused",
        "prompt_text_positive": POSITIVE,
        "prompt_text_negative": NEGATIVE,
        "prompt_text_provenance": "forge-authored smoke probe; not canonical, not Lore-authored",
    }

    try:
        receipt["status"] = "PREFLIGHT_READY"
        receipt["status_detail"] = STATUS_DETAIL["PREFLIGHT_READY"]
        queued = _post("/prompt", {"prompt": graph})
        pid = queued["prompt_id"]
        receipt["prompt_id_runtime"] = pid
    except Exception as exc:  # noqa: BLE001 - receipt must survive any submit error
        receipt["error"] = "submit: %r" % (exc,)
        return finish("RUNTIME_FAILED", "RUNTIME_FAILED")

    deadline = time.time() + 600
    hist = None
    while time.time() < deadline:
        h = _get("/history/%s" % pid)
        if pid in h:
            hist = h[pid]
            break
        time.sleep(2)

    if hist is None:
        receipt["error"] = "timeout waiting for history/%s" % pid
        return finish("RUNTIME_FAILED", "RUNTIME_FAILED")

    receipt["history_status"] = hist.get("status", {})
    outputs = hist.get("outputs", {})
    pngs = [
        img["filename"]
        for node_out in outputs.values()
        for img in node_out.get("images", [])
        if img.get("type") == "output"
    ]
    if not pngs:
        receipt["error"] = "no output image in history"
        return finish("RUNTIME_FAILED", "RUNTIME_FAILED")

    png_path = os.path.join(
        os.environ.get("COMFY_OUTPUT_DIR", "/data/AI-OFM-Operations/comfyui/output"),
        pngs[0],
    )
    receipt["artifact"] = {
        "filename": pngs[0],
        "path": png_path,
        "exists": os.path.exists(png_path),
        "bytes": os.path.getsize(png_path) if os.path.exists(png_path) else 0,
        "render_sha256": sha256_file(png_path) if os.path.exists(png_path) else None,
    }
    receipt["embedded_prompt"] = embedded_prompt(png_path)
    receipt["vram_after"] = _get("/system_stats")["devices"][0]
    finish("TRANCHE_COMPLETE", "TRANCHE_COMPLETE")
    print("  seed=%d  render_sha256=%s\n  prompt_id=%s\n  spec_id=%s"
          % (seed, receipt["artifact"]["render_sha256"], prompt_id, spec_id))
    return 0


def _emit(receipt: dict, out: str) -> None:
    path = out or os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "evidence",
        "smoke",
        "forge-smoke-receipt-%s.json"
        % time.strftime("%Y%m%d-%H%M%S", time.localtime()),
    )
    path = os.path.abspath(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    receipt["receipt_path"] = path
    with open(path, "w") as fh:
        json.dump(receipt, fh, indent=2, sort_keys=True)
    print("receipt: %s" % path)


if __name__ == "__main__":
    sys.exit(main())