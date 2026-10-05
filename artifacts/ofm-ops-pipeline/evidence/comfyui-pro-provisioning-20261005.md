# comfyui-pro provisioning — evidence receipt

Date: 2026-10-05 · Owner: @deanna · Assignee: @atlas (§4c-6)

## States (per profile-clone-persistent-environment evidence vocabulary)

| Layer | State | Proof |
|---|---|---|
| `SAVED` | ✅ | SOUL.md 2517 B at `~/.hermes/profiles/comfyui-pro/SOUL.md`; config.yaml `mcp_servers` added, lint ok |
| `PARSED` | ✅ | `hermes -p comfyui-pro config check` → ok |
| `LOADED` | ✅ | `hermes profile list` → `comfyui-pro  stealth/space-bunny-alpha  running`; gateway log 07:44:52 `Now serving profile 'comfyui-pro'` |
| **Identity smoke** | ✅ | Live run `20261005_074613_eb3a69` answered lane + tranche prerequisites + ComfyUI URL **from its own doctrine**, unprompted. Cites owner-approved asset set, @lore contract, `spec_id`/pillar rule. |
| MCP capability | ✅ | `comfyui-merged` handshake → `Unified server online: 69 total tools` (40 comfyui-mcp + 29 ds_) against live ComfyUI `http=200` |
| `PERSISTENCE_TESTED` | ➖ | n/a — no external mutable state owned yet (no tranche run) |

## What the stub actually was

The pre-existing `comfyui-pro/` directory was an **orphan**, not a registered profile:
- not present in `hermes profile list`; `hermes profile create` refused with "already exists"
- contents: bare `config.yaml` (33 B, `plugins: [turbofit]` only), empty `skills/`, `mnemosyne/`, `runtime/`
- **no SOUL.md, no model/route, no .env, no profile.yaml**
- preserved (not destroyed) at `~/.hermes/profiles/.deanna-stash/comfyui-pro-orphanstub-20261005/`

Critically, `~/.hermes/config.yaml` already binds a Discord room to it:
`room-comfyui-pro` → `chat_id 1540113287784701984` → `profile: comfyui-pro`.
**The room existed; the agent behind it did not.** That is why §4c-6 read "no SOUL, no model config."

## Provisioning decisions

| Field | Value | Reason |
|---|---|---|
| Clone source | `forge` | Role-adjacent ComfyUI lane; route verified live *before* cloning (not a config read) |
| Model | `stealth/space-bunny-alpha` (commandcode) | Free-tier-first. Doctrine: never recommend a paid model while a free one reliably does the job. The historical `kimi-k3`/tokenhungry config is **not** restored. |
| Fallback | `deepseek-v4-flash` | Inherited; cheap second leg |
| MCP | `comfyui-merged` enabled, `comfy-draftsman` disabled | 69 tools verified live; draftsman stays off until a draft-authoring need is real (capability loaded only when needed) |
| Discord | not cloned | Forge's token would collide; two gateways cannot hold one bot |

Not touched: `atlas`/default (untouchable), `@forge` source profile (baseline md5 `3a7fce41…` / `eb0d706a…` unchanged).

## Model-impact statement

**No spend change.** Route is a free commandcode model, same class as Forge and Cadence. The *capability* change is large (0 → 69 MCP tools), the *cost* change is zero. No paid endpoint introduced.

## Owner gates — untouched

- Discord bot token for `room-comfyui-pro` → **still owner-gated** (agent cannot claim a bot without a token)
- First real production tranche → 🚪 spend gate, owner-only
- No gate was crossed to reach this state.