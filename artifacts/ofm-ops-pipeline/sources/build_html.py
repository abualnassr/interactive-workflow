#!/usr/bin/env python3
"""Build the OFM Ops Pipeline interactive workflow HTML from the interactive-workflow template.

Reads templates/workflow.html from the repo and replaces ONLY the content block
(TITLE, FOOTER, STAGES, LANE, G, CARD_W, N, E), the <title> and the <h1>.
The engine/CSS is untouched. Asserts every anchor matches exactly once.
"""
import pathlib
import re
import sys

repo = pathlib.Path("/home/xenofon/src/interactive-workflow")
tpl = (repo / "templates" / "workflow.html").read_text(encoding="utf-8")
out_dir = repo / "artifacts" / "ofm-ops-pipeline"
out_dir.mkdir(parents=True, exist_ok=True)

s = tpl

def rep(old: str, new: str) -> None:
    global s
    n = s.count(old)
    assert n == 1, f"anchor count {n} (expected 1): {old[:80]!r}"
    s = s.replace(old, new)

# static <title>
rep("<title>Interactive workflow</title>",
    "<title>OFM Ops Pipeline | interactive workflow</title>")

# h1
rep("<h1><span>Purchase request to payment |</span> from a need to a paid invoice</h1>",
    "<h1><span>OFM Ops Pipeline |</span> plan to post, with the human gates visible</h1>")

# TITLE / FOOTER
rep('const TITLE="Purchase request to payment";',
    'const TITLE="OFM Ops Pipeline";')
rep('const FOOTER="Example process \u00b7 replace with your own title";',
    'const FOOTER="Asmoday fleet \u00b7 2026-10-05 \u00b7 v1 \u00b7 built by Atlas (Hermes) \u00b7 audited from live jobs, receipts and sessions";')

# STAGES (five stages, CARD_W 150)
rep('const STAGES=[{key:"a",label:"Request",x:0},{key:"b",label:"Approve",x:420},{key:"c",label:"Buy",x:840},{key:"d",label:"Pay",x:1260}];',
    'const STAGES=[{key:"a",label:"Plan",x:0},{key:"b",label:"Produce",x:336},{key:"c",label:"Qualify",x:672},{key:"d",label:"Distribute",x:1008},{key:"e",label:"Operate",x:1344}];')

# groups: none
rep('const G=[{label:"Approval chain",x:440,y:46,w:200,h:524}];', 'const G=[];')

# card width
rep('const CARD_W=180;', 'const CARD_W=150;')

NEW_N = '''const N=[
 ["a1","proc",30,60,"Pillar brief","batch scope from canon","Cadence","A scoped brief is agreed with Agora: persona, pillar, platform and batch size, pulled from Nyx Canon v2 and the content calendar.","No pillar means no draft. Agreeing scope first keeps every downstream step honest.","First-draft brief ready in the same touch; gaps flagged, never filled with filler.","briefs on time","Agora"],
 ["a2","proc",30,240,"Prompt forge","daily 10:30 brief + prompts","Lore","The daily forge turns the inspiration stream into a Nyx generation brief and prompt set, guardrails clean, with a receipt.","Prompts are specifications. A daily forge keeps batches fed without stale ideas.","Guardrail-clean batch with receipt; failure modes and GAP lists attached.","batch guardrails clean","prompt-forge job"],
 ["a3","dec",30,420,"Spend &amp; KEEP gate","human gate: verdict + budget","Asmoday","Owner reviews the batch and approves the KEEP set and the spend envelope before any rented GPU or new route moves.","Spend and taste are owner decisions. Bypassing them corrupts both the budget and the canon.","Every tranche carries an explicit KEEP and spend approval; nothing renders without one.","unapproved spend: zero"],
 ["b1","proc",366,60,"Contracts &amp; smoke","validated graph, smoke receipts","Forge","Lore drafts model and workflow contracts from current source; Forge smoke-tests on the local RTX 2060 lane and returns pass or fail receipts to the KB.","Contracts go stale silently. Smoke receipts keep the knowledge base true and the graph admissible.","No production run on an unvalidated contract; a receipt for every smoke pass.","smoke receipts filed","Lore"],
 ["b2","proc",366,240,"Generation tranche","bounded batch, $1-per-job ceiling","ComfyUI Pro","A bounded render batch runs on the admitted graph, local or rented pod, under the $1-per-job ceiling: kill at ceiling, volume preserved.","Bounded tranches keep cost and quality predictable; the runner refuses without approval.","Renders land with receipts, spend stays under ceiling, pod destroyed after pull.","cost per batch","lane runner (Atlas)"],
 ["b3","proc",366,420,"Deterministic validation","hash, dims, provenance","Forge","Every output passes fail-closed checks: hash, dimensions, MIME and provenance. Failures go to quarantine, never to release.","A release path without validation is how corrupt files reach the feed.","Zero unvalidated releases; the quarantine list stays explicit.","validation failures caught","validation scripts"],
 ["c1","dec",702,240,"Owner visual QA","human gate: KEEP or KILL","Asmoday","The owner reviews renders against canon. KEEP releases the batch; KILL sends it back for rework with a reason.","The owner's judgment is the product. Auto-accept would corrupt the identity.","Every released master carries an explicit KEEP; every kill carries a reason.","KEEP rate"],
 ["c2","proc",702,420,"Release &amp; derivatives","masters to app copies + public copy","Atlas","Kept masters are released: eight app derivatives plus a metadata-stripped public copy with AI disclosure, each with a hash receipt.","One release path keeps derivatives byte-exact and disclosure consistent.","Receipt per copy; strip and disclosure verified before anything ships.","receipts per master","derivative scripts"],
 ["c3","tool",702,600,"Asset hygiene audit","daily 03:00 hash readback","Forge","The nightly audit re-verifies registered artifact hashes against the factory control plane; anomalies raise lane alerts.","Silent bit-rot or drift breaks posting quietly; the audit makes it loud.","Anomaly list empty or explicitly triaged; every alert gets a follow-up card.","hash drift caught"],
 ["d1","proc",1038,60,"Packet &amp; plan build","packets per cadence windows","Cadence","Released masters become schema-valid posting packets and land in the per-day plan against the eight-app cadence.","Packets are the contract between content and posting; schema-red packets never reach the phone.","Packets validate clean; the plan is silent when nothing is plannable.","schema-valid packets"],
 ["d2","proc",1038,240,"Phone staging","ADB copy + byte readback","FleetOp","Approved packets are pushed to apollo /sdcard/Download/OFM/Nyx with size and md5 readback. User 0 only; slots 10-15 stay dormant.","Byte-exact staging on a verified device is the last controlled step before a human posts.","Readback matches 100%; a mismatch reopens the card, not the post.","staging readback pass"],
 ["d3","proc",1038,420,"Manual posting","human gate: owner posts","Asmoday","The owner posts from the phone per the platform map: SFW to socials, suggestive to Telegram only. Evidence is captured after each post.","Platform terms and account risk: launch doctrine forbids auto-post. Posting stays human.","Every post gets URL or ID evidence; failures log as POST_FAILED_WITH_EVIDENCE.","posts with evidence"],
 ["d4","proc",1038,600,"Fanvue lane","approved drain + drafts only","Mint","Approved Fanvue posts drain three times a week on schedule; chatter, offers and pricing drafts stop at the human queue.","Monetization follows the same gate doctrine: automate the account, never the conversation.","Drop receipts per post; zero auto-sends; credits or policy issues surface loudly.","drop receipts"],
 ["e1","proc",1374,60,"Evidence &amp; 24h metrics","receipts to analytics rows","Atlas","Post evidence and receipts feed schema-valid analytics rows 24 hours after each post; anything missing is listed daily.","If it is not measured the loop cannot learn. Evidence is the unit of truth.","Rows complete within 24h; the missing-metrics list is empty or owned.","metrics coverage"],
 ["e2","proc",1374,240,"Weekly classification","reach, conversion, revenue, risk","Atlas","The week's receipts are classified into reach, engagement, conversion, revenue and risk, with sources cited; signals route back to planning.","Weekly truth beats daily noise; classification drives the next batch, not vibes.","Numbers cite receipts; no estimated revenue; signals land as briefs.","weekly digest out"],
 ["e3","out",1374,420,"Stewardship cycles","lane objectives, transitions only","Steward","Daily cycles check lanes and objectives: feed freshness, brief freshness, cron health, factory evidence. Only transitions and failures alert.","An unwatched automated pipeline rots silently. Stewardship is the watch.","Lanes green or red with named owners; alerts stay rare and real.","lanes green"],
 ["s1","tool",30,800,"Human gates","spend, canon, release, posts","Asmoday","The hard-gate doctrine: rented GPU and spend, canon changes, release QA, public posting, DMs, pricing, account actions.","Gates are doctrine, not gaps. Every gate has a card on this map and an owner.","No gate bypassed; each gate has an evidence field.","gates bypassed: zero"],
 ["s2","store",366,800,"Handoff &amp; receipts","close with evidence, not claims","Atlas","Stage handoffs name the input artifact, the output path and a receipt; a worker's done is verified on disk, failures open evidence cards.","Self-reported done stalls stacks; receipts keep the chain honest.","No card closes on a claim; every close cites a path or a hash.","claims verified"],
 ["s3","tool",702,800,"Cron &amp; runners","daily ticks, read-only first","Atlas","Twenty-eight registered jobs tick the loop: read-only audits daily, deliveries to Discord channels, silent when healthy.","The loop runs on schedule, not on mood. Silence is a feature here.","Ticker fresh; jobs green or visibly red, no silently stale lanes.","job health"],
 ["s4","store",1038,800,"Canon &amp; disclosure","Nyx Canon v2 + AI disclosure","Deanna","The persona canon, banned list and disclosure rules every caption and derivative binds to.","Identity drift and missed disclosure are the two ways an AI persona loses an account.","Every caption passes banned-list and disclosure checks; canon changes only via the owner.","canon violations: zero","Agora"]
];'''

NEW_E = '''const E=[
 {f:"a1",t:"a2",label:"scoped brief",pts:[at("a1","bottom"),at("a2","top")],lab:[115,222],anchor:"start"},
 {f:"a2",t:"a3",label:"prompt batch",pts:[at("a2","bottom"),at("a3","top")],lab:[115,402],anchor:"start"},
 {f:"a3",t:"b2",label:"approved tranche",pts:[at("a3","right",50),[280,470],[280,310],at("b2","left")],lab:[280,390],rot:-90},
 {f:"a3",t:"a2",label:"no: rescope",pts:[at("a3","left",50),[12,470],[12,320],at("a2","left",80)],lab:[12,395],rot:-90,exc:true,back:true},
 {f:"b1",t:"b2",label:"smoke-passed graph",pts:[at("b1","bottom"),at("b2","top")],lab:[451,222],anchor:"start"},
 {f:"b2",t:"b3",label:"renders",pts:[at("b2","bottom"),at("b3","top")],lab:[451,402],anchor:"start"},
 {f:"b3",t:"c1",label:"validated candidates",pts:[at("b3","right",50),[580,470],[580,310],at("c1","left")],lab:[580,440],rot:-90},
 {f:"c1",t:"c2",label:"KEEP + release",pts:[at("c1","bottom"),at("c2","top")],lab:[787,402],anchor:"start"},
 {f:"c1",t:"b2",label:"KILL: rework",pts:[at("c1","top",40),[742,200],[660,200],[660,330],at("b2","right",90)],lab:[660,255],rot:-90,exc:true,back:true},
 {f:"c2",t:"d1",label:"released masters",pts:[at("c2","right",50),[950,470],[950,130],at("d1","left")],lab:[950,300],rot:-90},
 {f:"c2",t:"d4",label:"eligible set",pts:[at("c2","right",100),[965,520],[965,660],at("d4","left",60)],lab:[900,505]},
 {f:"c2",t:"c3",label:"hash registry",pts:[at("c2","bottom"),at("c3","top")],lab:[787,582],anchor:"start"},
 {f:"c3",t:"e3",label:"drift alerts",pts:[at("c3","right",70),[980,670],[980,580],[1449,580],at("e3","bottom",75)],lab:[980,600],rot:-90},
 {f:"d1",t:"d2",label:"approved packets",pts:[at("d1","bottom"),at("d2","top")],lab:[1123,222],anchor:"start"},
 {f:"d2",t:"d3",label:"staged + readback",pts:[at("d2","bottom"),at("d3","top")],lab:[1123,402],anchor:"start"},
 {f:"d2",t:"d1",label:"readback mismatch",pts:[at("d2","right",30),[1240,270],[1240,130],at("d1","right",70)],lab:[1240,200],rot:-90,exc:true,back:true},
 {f:"d3",t:"e1",label:"post evidence",pts:[at("d3","right",50),[1290,470],[1290,130],at("e1","left")],lab:[1290,300],rot:-90},
 {f:"d4",t:"e1",label:"post IDs + receipts",pts:[at("d4","right",40),[1650,640],[1650,130],at("e1","right",70)],lab:[1650,385],rot:-90},
 {f:"e1",t:"e2",label:"analytics rows",pts:[at("e1","bottom"),at("e2","top")],lab:[1459,222],anchor:"start"},
 {f:"e2",t:"a2",label:"trend signals",pts:[at("e2","right",30),[1600,270],[1600,42],[300,42],[300,285],at("a2","right",45)],lab:[900,42],back:true},
 {f:"s1",t:"a3",label:"spend + canon gates",pts:[at("s1","right",70),[240,870],[240,620],[105,620],at("a3","bottom")],lab:[240,720],rot:-90},
 {f:"s2",t:"b3",label:"validation handoff",pts:[at("s2","top"),at("b3","bottom")],lab:[441,680],rot:-90},
 {f:"s3",t:"c3",label:"daily 03:00 tick",pts:[at("s3","top"),at("c3","bottom")],lab:[787,782],anchor:"start"},
 {f:"s4",t:"d4",label:"canon + disclosure",pts:[at("s4","top"),at("d4","bottom")],lab:[1123,782],anchor:"start"}
];'''

m = re.search(r"const N=\[.*?\n\];", s, re.S)
assert m, "N block not found"
s = s[:m.start()] + NEW_N + s[m.end():]

m = re.search(r"const E=\[.*?\n\];", s, re.S)
assert m, "E block not found"
s = s[:m.start()] + NEW_E + s[m.end():]

out = out_dir / "OFM Ops Pipeline - workflow (interactive).html"
out.write_text(s, encoding="utf-8")
print(f"wrote {out} ({len(s)} bytes)")
print(f"cards: {NEW_N.count('['+chr(34)) if False else s.count(chr(10)+' ['+chr(34))}, arrows: {s.count('{f:'+chr(34))}")
