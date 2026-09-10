# P12 — Windows event logs · build log

**Topic** `T20` Windows Event Logs (49 min) — single-topic page
**Page** `docs/page-12/index.html` — 22 screens, 6 part dividers — shape v2 (`D136`)
**Built** 2026-09-09

| | |
|---|---|
| Stepped figures | **5** — `F1` anatomy of an event · `F2` logon types · `F3` the cleared log · `F4` pass-the-hash pattern · `F5` Security log vs Sysmon |
| SIMSCREEN | **1** — `ss-t20`, the instructor demo: EvtxECmd across six real recordings |
| Lifecycle stage | **3 · ANALYSE** |
| Evidence | `EVS-14` — six real attack recordings, Tier 2 (GPL-3.0), 29 assertions |

## The spine of the page

Event logs are the one artifact Windows writes **on purpose** — testimony, not a side effect. So the page's
turning sentence is that **the attacker's attempt to silence the testimony (clearing the log) is written down as
the loudest testimony of all**. Every finding is quoted as EventID + Provider + UTC time + the one field that
carries the meaning, and mapped to MITRE.

## Every event is from a real recording

Read with `python-evtx`, all six from `EVTX-ATTACK-SAMPLES` (Samir Bousseaden, GPL-3.0):

- **1102** Security log cleared by `EXAMPLE\user01` at **23:35:07**, in a file of **112 records** (110 are 4663
  file-access noise — you filter for the clear, you don't scroll to it).
- **104** System log cleared by the same account **42 seconds earlier**.
- **4732 ×2**: Guest (RID 501) and NetworkService (S-1-5-20) added to Administrators by `IEUser` — the student lab.
- **4624/4625** logon type 2 with a `0xC000006A` bad-password failure, both from a Chrome updater — "interactive
  is not always a person".
- **4624 type 9 (NewCredentials) + seclogo + ::1 + 4672**: the pass-the-hash pattern, opened by a 1102 clear.
- **Sysmon 13**: `a.exe` writes a `Run` value disguised as `"c:\windows\tasks\taskhost.exe"` — persistence the
  Security log never sees.

29 assertions in `verify14.py`, all passing. RegRipper-style tooling was not needed; `EvtxECmd` output layout was
reproduced faithfully in the SIMSCREEN and every value is real.

## Two engine bugs fixed here, both would have hit P13/P14

**(a) Backslashes in SIMSCREEN/figure captions broke the page's JavaScript.** `EXAMPLE\user01` in a caption became
`\u` in the JS source — an invalid Unicode escape — and the render gate caught it as 100+ page errors. The shared
caption builders in `lib.py` (`fig`) and `sims.py` (`simscreen`) now escape backslashes before quotes. P10 and P11
happened to avoid a lowercase `\u`; a Windows path page could not. See `D139`.

**(b) Two false positives from the terminology gate**, both reworded rather than weakening the gate: `الآثار`
(banned as *artifacts*, but here *side effects*) and `المجموعات` (banned as *clusters*, but here security *groups*).
`D132` warned the LITERAL class has an accepted cost; this is the same cost in the other direction, and the honest
fix is to reword the ordinary use, not to un-ban the technical one.

## Gates

```
python3 scripts/density_gate.py docs/page-12/index.html      ALL PASS
node testing/render_gate.js docs/page-12/index.html          PASS — zero findings
```

Twelve pages now pass both.
