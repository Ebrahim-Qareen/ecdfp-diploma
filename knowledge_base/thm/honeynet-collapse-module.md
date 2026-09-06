---
module: Honeynet Collapse — six connected TryHackMe rooms telling one incident
rooms: initialaccesspot · elevatingmovement · lostinramslation · crmsnatch · shockandsilence ·
       thelasttrial
scope: **This is not a room note.** It is the analysis the six extractions were done for: the arc as
       a single design — how state carries, what each room may assume, how difficulty ramps, and
       what we take.
feeds: **D40** (how our six-session carry-through is structured) and **D41** (what a question's
       answer may not be). Both appended to `DECISIONS.md` from this note.
extracted: 2026-08-29
companion notes: `initialaccesspot.md` · `elevatingmovement.md` · `lostinramslation.md` ·
                 `crmsnatch.md` · `shockandsilence.md` · `thelasttrial.md`
currency: blocks **K**, **L**, **M**, **N**, **O**, **P** of `_TOOL_CURRENCY_2026-08-28.md`
---

# The Honeynet Collapse module, as one design

## 1. What it is

Six premium challenge rooms, each **Hard · 60 min · 2 tasks**, telling one intrusion at DeceptiTech —
a honeypot vendor that does not use its own product. Each room names its position: *"This room is
about the Nth attack stage (#N on the network diagram)."*

| # | room | host | subnet | platform | scored Qs | completions | recommends |
|---|---|---|---|---|---|---|---|
| ① | Initial Access Pot | `deceptipot-demo` 172.16.8.239 | DMZ | **Linux** | 6 | 3,562 | 78 |
| ② | Elevating Movement | `SRV-IT-QA` 172.16.8.216 | DMZ | Windows | 6 | 2,643 | 50 |
| ③ | Lost in RAMslation | `SRV-DMZ-GW` 172.16.8.15 | DMZ | Windows (memory) | 6 | 1,500 | 38 |
| ④ | CRM Snatch | `SRV-CRM-01` 172.16.2.9 | **CORE** | Windows (disk) | 6 | 1,246 | 31 |
| ⑤ | Shock and Silence | `DC-01` 172.16.2.4 | CORE | Windows (file system) | 5 | 1,209 | 23 |
| ⑥ | The Last Trial | Lucas Rivera's laptop | *remote user* | **macOS** | 6 | 1,236 | 23 |

**The arc:** an exposed honeypot in the DMZ → a QA server → the DMZ gateway → across the subnet
boundary to the CRM server → the domain controller → and out to a remote developer's laptop. **Five
host stages, then a person.** Ransomware, wiped logs, corrupted backups and a deleted SIEM are the
outcome, stated in every room's opening.

🟢 **Dating the module from its own assets** (the filenames carry millisecond timestamps): the shared
topology diagram was uploaded **2025-06-26**, the room icons and banners **2025-09-08**. **So the
module is roughly eleven months old at extraction** — young by the standards of this corpus, where
room 22 shipped Autopsy 4.21.0, three years stale.

## 2. How state carries between rooms

**Four mechanisms, and they are worth ranking by cost, because we have to build the equivalent.**

| mechanism | what it does | cost to build | verdict |
|---|---|---|---|
| **One shared diagram, reused byte-identically** | Establishes topology, names every host, and **numbers all six stages** so each room's scope is visible | **One SVG, drawn once** | 🟢🟢 **Adopt.** Verified empirically: rooms 23 and 24 serve the *same asset ID*, `678ecc92c80aa206339f0f23-1750969983020.svg` |
| **A stage number in one sentence** | *"This room is about the Nth attack stage (#N on the network diagram)"* | One sentence per room | 🟢🟢 **Adopt** — it is what makes the diagram a *scope statement* rather than decoration |
| **An identical recap paragraph** | The *"One ordinary morning…"* outcome paragraph, repeated verbatim in all six | Copy-paste | 🟢 **Adopt the idea, not the execution** — §7 |
| **Character continuity** | Emily (stages 1–2), Matthew (2, 3, 4), Logan (5), Lucas (6) recur as colleagues, victims and investigators | Free, if the scenario is written once | 🟢🟢 **Adopt — the cheapest continuity there is**, and the module's most underrated device |

🟢🟢 **The diagram is the finding.** It is one asset, reused unchanged, that simultaneously supplies
context to a newcomer and a *"you built this"* summary to someone who has done the previous five.
**That is the answer to the problem room 22 §5.5 posed** — how to keep sessions chained (**D8/D19**)
without making session five unusable to a student who missed session four.

⚠️ **Two things it does not do, and both are fixable for free:**

1. **It never highlights the current stage.** The reader must find the number themselves. **Ours
   should highlight.**
2. **It uses RFC 1918 addresses** (`172.16.x.x`), where **D19 requires documentation ranges**
   (RFC 5737). Trivial, and exactly the kind of thing that gets copied by accident.

⚠️ **And the character continuity has an unexamined edge the module never picks up:** **Matthew's
domain credentials are stolen in stage 2, and Matthew is the investigator in stage 3.** No room
comments on it. 🟢🟢 **That is a free exercise — *"who should not be running this investigation, and
why?"*** — and it is a question real engagements ask in their first hour.

## 3. What each room is allowed to assume — the dependency ledger

**Every room is independently completable.** None requires a prior room's answer as an input; each
supplies its own evidence and its own machine. **What carries is narrative, not data.**

| room | assumes from earlier | supplies to later | hard dependency? |
|---|---|---|---|
| ① | nothing | the foothold; Emily's credentials stolen | — |
| ② | *"the entry point secured and Emily's domain credentials stolen"* | Matthew's domain hash | **no** — stated as given |
| ③ | *"the threat actor has managed to move laterally"* | the 3389 destination (④) | **no** |
| ④ | *"the attacker had already slipped into the server with Matthew's stolen credentials"* | the stolen customer export | **no** |
| ⑤ | the encryption outcome | — | **no** |
| ⑥ | *"amidst this primary attack"* — and then **explicitly disconnects itself** | — | **no** |

🟢🟢 **The design rule the module follows: state the previous stage's conclusion as given context, and
supply fresh evidence for the current one.** That is what makes six chained rooms survivable.

🔴 **But it creates the module's most consistent flaw: given context is not visually distinguished
from findings.** A student reads *"the attacker had already slipped into the server with Matthew's
stolen credentials"* in the same voice as everything else, and **inherits a conclusion they did not
establish.** ⚠️ Over six rooms that is six inherited conclusions, and **it is a D20 criterion-4 habit
failure in slow motion.**

🟢🟢 **The fix is typographic and costs nothing: mark the carried-forward block as *given context*.**
Ours already has a place for it — the D19 case brief — and **`ecdfp-session-package` should render it
as a distinct block, not as prose.**

**One dependency the module does have, and it is the good kind:** ③ establishes a connection to
172.16.2.9:3389 from the *source* side and **cannot prove it succeeded**; ④ is the destination.
🟢🟢 **A stated limitation in one session, closed by the next.** **That is exactly the shape our
`S6-09` should have**, and it only works because the limitation is stated.

## 4. How the difficulty ramps — and where students stop

**It does not ramp. All six are labelled Hard, all six are 60 minutes, five of six have six scored
questions.** The *content* varies by artifact family — Linux logs, Windows event logs, memory, disk,
NTFS, macOS — but **the declared difficulty is flat.**

🟢🟢 **The completion counts are a real dataset, and they say something the labels do not:**

| stage | completions | of previous | of stage ① | recommend rate |
|---|---|---|---|---|
| ① Initial Access Pot | 3,562 | — | 100.0 % | 2.19 % |
| ② Elevating Movement | 2,643 | 74.2 % | 74.2 % | 1.89 % |
| ③ **Lost in RAMslation** | 1,500 | **56.8 %** | 42.1 % | 2.53 % |
| ④ CRM Snatch | 1,246 | 83.1 % | 35.0 % | 2.49 % |
| ⑤ Shock and Silence | 1,209 | 97.0 % | 33.9 % | 1.90 % |
| ⑥ The Last Trial | 1,236 | **102.2 %** | 34.7 % | 1.86 % |

**Three readings, and the third is the useful one:**

1. **The module loses two thirds of its starters by stage 3**, and **the single largest drop is at
   memory forensics** — a 43 % fall between ② and ③, far steeper than any other step.
2. **After stage 3 it plateaus at about a third and stays there** — ④, ⑤ and ⑥ are within 3 % of one
   another, and **stage ⑥ is slightly *higher* than stage ⑤**. **Whoever survives memory finishes the
   module.**
3. 🟢🟢 **The recommend rate is flat at roughly 2 % throughout** — it does not fall as completions
   fall. **So the attrition is not dissatisfaction; it is difficulty.** People who finish a room like
   it about equally, whichever room it is.

⚠️ **Caveat, stated because it matters:** these are cumulative snapshots taken on one day. If the six
rooms were released simultaneously the curve is attrition; if released in sequence, part of it is age.
**The asset timestamps (§1) suggest a single release**, but that is inference, not proof.

**What we take from it:**

- 🔴🔴 **Memory is the wall.** Our own map already compresses memory into `S2-03` (acquisition) and
  `S6-10` (analysis) with a Volatility **homework track** — and **this data supports that structure
  rather than undermining it**, because the homework track is what stops memory being a single
  cliff-edge session. 🟢 **Worth saying in the instructor brief: expect the memory session to be the
  one students struggle with, and protect it with the most scaffolding.**
- ⚠️ **A flat "Hard" label across six sessions is not a ramp**, and our six sessions do ramp — S1
  fundamentals through S6 capstone. **The module is a chained case, not a curriculum**, and that
  distinction is worth keeping clear when we borrow from it.

## 5. The platform arc, and what it costs us

**Linux → Windows → Windows → Windows → Windows → macOS.**

🔴🔴 **Under D38, stages ① and ⑥ are out of scope.** **The module is four usable rooms of six**, and
that should be recorded in one place rather than rediscovered.

🟢🟢 **But the platform spread turned out to be the module's largest single contribution to our
material**, because it produced the **three-platform contrast** that **D38**'s figure **F1** is built
on. The clearest row:

| | Windows | macOS | Linux |
|---|---|---|---|
| **where a download's URL is recorded** | in a `Zone.Identifier` **ADS on the file** (**O2**) | a **UUID on the file**, the URL in a **per-user SQLite DB** (**P1**) | **nowhere** (**J7**, by analogy) |
| **delete one record** | affects **one file** | **strips provenance from every downloaded file at once** | n/a |
| **file deleted** | the ADS dies with it | **the DB row survives** | n/a |

**Each platform preserves what the others lose**, and **reading that table is a better argument for a
Windows-weighted syllabus than "24 hours does not stretch"** — which is what **D38** already
concluded, now with a third column to prove it.

⚠️ **The honest cost:** two of six rooms cannot be used as exercises at all, and the two out-of-scope
rooms are the *first* and the *last* — **the module's entry point and its resolution.** A student
following our course could not do this module end to end.

## 6. The evidence architecture — six for six

🔴 **Not one of the six rooms yields a reusable evidence set.** Every stage is a live lab VM: an SSH
target, an RDP target, or an image sitting inside a machine you cannot download from.

| stage | evidence | reusable? |
|---|---|---|
| ① | live Ubuntu honeypot over SSH | no |
| ② | live Windows server over RDP | no |
| ③ | `SRV-DMZ-GW-evidence.mem` inside the VM | no |
| ④ | disk snapshot + EZ Tools on the Desktop | no |
| ⑤ | `DC-01-NTFS-Logs.ad1` + tools on the Desktop | no |
| ⑥ | `Lucas_Disk.img` + `apfs-fuse` / `mac_apt` | no |

🟢🟢 **This closes a question that has been open since room 22: no, the Priority-2 set will not supply
our Windows intrusion image.** `EVS-10` remains unallocated after seven consecutive rooms. **The image
must be staged on `EVI-SRC01` (D19) or sourced from CFReDS (D36).** **No further extraction changes
this.**

⚠️ **And none of the six publishes an acquisition record** — no hash, no tool, no operator, no capture
time — which against **D20 criterion 1** would fail on arrival. **Deliberately not counted as a
defect** (`lostinramslation.md` §4): it is near-universal across the corpus, and counting it in room
25 rather than room 6 would be arbitrary. 🟢🟢 **It is worth far more as an exercise than a
complaint** — hand students the same dump *with* an acquisition record and have them compute the
smear window from the elapsed capture time.

🟢 **The formats are themselves a curriculum contribution**, and an unexpected one. Across three
stages the module uses a **memory dump**, a **disk snapshot** and an **AD1 logical image** — and the
last of those (**O1**) fixes an `S2-05` row we had only half-specified, along with the fact that
**Autopsy cannot open an AD1 at all.**

## 7. Question design across the module — the aggregate scorecard

**35 scored questions across six rooms.** The pattern is consistent enough to score.

| dimension | result | verdict |
|---|---|---|
| **stems that assert their own conclusion** | **6 of 6 rooms** | 🔴 house style, not accident |
| **answer formats specified** | 3 of 6 rooms, and only on some questions | ⚠️ inconsistent |
| **timezone specified** | **0 of 6** | 🔴 on a module built on timelines |
| **"cannot be determined" questions** | **0 of 6** | 🔴 |
| **stems that warn against the obvious** | **2 of 6** (⑤ *"Go beyond the obvious"*, ⑥ *"Not every attack is targeted"*) | 🟢🟢 rare and excellent |
| **conceptual figures** | **0 of 6** | 🔴 one shared topology diagram, nothing else |
| **credentials published in the task body** | **5 of 6** (all but ⑥) | 🔴 **R8** |
| **questions whose answer is a secret or PII** | **3 questions in 2 rooms** (②, ④) | 🔴🔴 **D41** |
| **anti-forensics stated up front** | ④ and ⑤ | 🟢🟢 the module's best framing decision |
| **safety/handling defects** | **2 of 6** (①, ②) | 🟢 and the reason is structural — §8 |

### 🔴🔴 The finding that outgrew its category

The project has been counting *"rooms with a 'cannot be determined' question: 0"* since room 1. **Over
this module that stopped being a stylistic observation and became a correctness finding**, because in
four of the six rooms **the honest answer to a question the room actually asks is "not determinable
from this evidence":**

| room | its own question | why it cannot be answered as asked |
|---|---|---|
| ② | *"Which full command line was used to dump the OS credentials?"* | *Audit Process Creation* is **"Default: Not configured"** and the command-line policy **"Not Configured (not enabled)"** — **L1** |
| ③ | *"For how many seconds did the attacker maintain their PowerShell session active?"* | 400/403 bracket an **engine instance**; *"this event cannot be strictly correlated to a logon session"* — **N2** |
| ⑤ | *"Which executable file initiated the encryption process?"* | `USN_RECORD_V2` has **no process field**; the journal *"logs only the fact of a change … and the reason for the change"* — **O4** |
| ⑥ | *"When was the malicious application installed?"* | a drag-and-drop app *"bypasses the mechanisms built into OS X for recording installation"* — **P3** |

🟢🟢 **Three of those four are the same underlying shape, and it is worth naming: the event was never
recorded, rather than destroyed.** No anti-forensics was required to produce any of them. **That is a
more important idea than "the attacker cleared the logs", and the course should teach it as its own
category.**

⚠️ **And note the platform constraint that makes this excusable for TryHackMe and inexcusable for
us:** a challenge platform needs a string in a box, so it *cannot* accept *"not determinable"* as an
answer. **Our assessment is a written report graded on a fixed rubric (D20/D21), so we can.** 🟢🟢
**That is a concrete, defensible advantage of report-based assessment over answer-checking, and it
should be said to students in `S1`.**

### 🔴🔴 Secrets and PII as answers

Two rooms, three questions: ② asks for **an NTLM hash**, ④ for **a cloud-storage password** and for
**a named individual's email address taken from the exfiltrated customer data.**

**An NT hash is an authenticator, not evidence** — NTLM takes it directly, and NTLMv2 is still enabled
by default (**L3**). **And exfiltrated customer data is the victim's most sensitive material**; an
answer key containing a data subject's email is a breach of the thing the analyst was hired to
protect. 🔴 **D22 makes this a release-gate concern for us, not a matter of taste.**

🟢🟢 **The replacements are strictly better forensics.** *"How many customer records were in the
staged export, and how do you know?"* exercises archive enumeration (**N4** — names, sizes,
timestamps and CRC32 are readable **without** the password), a CRC comparison against the original,
and a stated limitation. *"What is Lucas's email?"* exercises `Ctrl+F`. **This becomes D41.**

### 🟢 The two safety defects, and why there are only two

Rooms ① and ② have evidence-handling defects — a pre-mounted ext4 filesystem with no mount mode
stated, and students running EZ Tools on the live host, contaminating the very Prefetch and Amcache
they are about to read. **Rooms ③–⑥ have none.**

🟢🟢 **The reason is structural, not editorial, and it is the module's best unstated lesson: stages
1–2 are live response by nature; stages 3–6 are offline analysis of captured artifacts.** The correct
handling rule **depends on where in the incident you are standing** — and by stage ⑥ the room ships a
mount command that is **read-only by design** (`apfs-fuse` cannot write, **P4**).

⚠️ **The module walks through both halves in order and never says so.** **We should say it** — it is
the strongest argument in the corpus for teaching acquisition and analysis as separate disciplines
with separate rules.

## 8. What we adopt, what we reject

### Adopt — and all of it is free

| # | idea | where it lands | cost |
|---|---|---|---|
| 1 | **One numbered map, six sessions, current stage highlighted** (§2) | figure **F7**, every session page | one figure |
| 2 | **Prior stages as a visibly marked *given context* block** (§3) | `ecdfp-session-package` | typographic |
| 3 | **A stated limitation in one session, closed by the next** (§3) | `S6-09`, and the S4→S5→S6 chain | free |
| 4 | **Anti-forensics stated in the brief, graded on what is correctly reported unrecoverable** (④, ⑤) | `S6-09` + **D20** criterion 4 | free |
| 5 | **One strand that turns out to be unrelated** (⑥) | `S6-09` | free |
| 6 | **Character continuity, including the compromised investigator** (§2) | D19 scenario | free |
| 7 | **A stem that warns against the obvious** (⑤, ⑥) | question-design guidance | free |
| 8 | **A control failure, not a user error, as the entry point** (①) | D19 opening | free |

### Reject

- ❌ **Flat difficulty across six stages** (§4). Ours ramps; the module is a case, not a curriculum.
- ❌ **Credentials in the task body** (5 of 6 rooms). Ours are issued out of band.
- ❌ **Secrets and PII as answers** (§7). **D41.**
- ❌ **Narrating the attack in the brief** (①–⑤). We narrate the **discovery**, as ⑤ does best.
- ❌ **A `.ad1` as course evidence** — Autopsy cannot open it (**O1**), and our students work in
  Autopsy. 🟢 It stays as a **teaching object** in `S2-05`, not as an exercise medium.

### Two decisions, appended to `DECISIONS.md`

**D40 — how the six-session carry-through is structured.** Items 1–5 above, together: the numbered
map, the marked given-context block, the deliberate cross-session limitation, anti-forensics stated in
the brief, and one unrelated strand in the capstone.

**D41 — no eCDFP question may have a secret or a data subject's personal information as its answer.**
§7.

⚠️ **D40 has a prerequisite that is still open:** **D19 describes a chain of techniques, not a
topology.** Figure **F7** cannot be drawn until our incident is expressed as *six numbered stages
across named hosts*. **That must be resolved before any session page is built, since F7 appears on
all six.**

## 9. Verdict

**As a teaching object, the module is better than any single room in the corpus and worse than its
best individual room deserves.**

🟢🟢 **What it gets right is architectural.** One diagram carries six sessions. Every room stands
alone while belonging to one story. Two briefs actively warn against the obvious reading. The
anti-forensics is declared rather than hidden, which turns *"find the log entry"* into *"the log entry
does not exist — now what"*. And the final stage refuses the narrative link the student most wants to
draw. **Those five decisions are worth more to us than the thirty-five questions combined.**

🔴 **What it gets wrong is at the level of the individual question.** Stems assert conclusions in all
six rooms; three questions want a secret or a person's data; no room states a timezone; and in four
rooms the honest answer to a graded question is *"not determinable from this evidence."*

🟢🟢 **And the most useful thing it gave us is not in any of that.** Across rooms ②, ③, ⑤ and ⑥ the
same idea surfaces from four unrelated directions — **some evidence is not destroyed, it is simply
never recorded.** No command line without auditing (**L1**), no process in the change journal
(**O4**), no receipt for a drag-and-drop install (**P3**), no attribution in a login record. **That is
the difference between an artifact an attacker removed and an artifact that never existed**, and it is
the single most valuable idea to come out of the whole extraction.

⚠️ **One last note on method, and it is about this analysis rather than the module.** In room ④ I
inferred that the stolen customer export supplied the targeting for room ⑥ — a tidy chaining device I
was pleased to find. **Room ⑥ refutes it explicitly.** The inference rested on **proximity plus a
shared name**, with no artifact connecting them, and I made it **one room before writing the warning
about exactly that failure mode.** The correction stands in `crmsnatch.md` §5.2, recorded rather than
deleted. 🟢🟢 **It belongs in this verdict because it is the module's own lesson, demonstrated on the
person analysing it:** a plausible story assembles itself out of proximity, and the only defence is
asking which artifact connects the two facts.
