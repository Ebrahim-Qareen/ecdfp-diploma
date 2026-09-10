# P04 · Guided lab — collect volatile state in order

`T06` · 15 minutes at the keyboard · pairs with SIMSCREEN `ss-t06` on `docs/page-04/index.html#p11`

**Scenario.** `FIN-WKS-07` is found powered on, user session locked, network cable still in. You have
about ten minutes before someone senior asks for it to be shut down.

**Setup.** One Windows VM per pair, snapshotted. One USB (or a second virtual disk) as the examiner
drive. Live Response Collection and WinPmem on the examiner drive, never on the target.

---

## Step 1 — write the note (2 min, no tool)

Before anything is plugged in, each pair writes, on paper or in a file **on the examiner drive**:

```
Case              <case id>
Host              <hostname>
Arrived           <yyyy-mm-dd hh:mm>
Responder         <name>
My USB            <make, model, SERIAL>
Tooling           <collector version, imager version>
Machine state     powered on / locked / network cable in|out
```

> **Instructor:** do not let anyone skip this to "get to the tools". Step 1 is the assessed step —
> steps 2–6 are worthless without it, and the exercise on screen 14 is unanswerable without it.

## Step 2 — choose the collection mode (1 min)

Run the collector. Six options; take **Memory Dump**, not Complete.
Ask the room *why not Complete* before revealing it: Complete images the disk too, and the disk is
not going anywhere.

## Step 3 — watch the order (2 min)

The collector works **down** the RFC 3227 list: memory → connections → processes → logged-on users →
ARP and routing → copied files. Say out loud that the tool has the rule encoded so a responder
cannot get it wrong under pressure.

## Step 4 — read the tree (3 min)

```
<HOST>_<yyyymmdd>_<hhmmss>\
  ForensicImages\Memory\        the RAM capture
  LiveResponseData\
    BasicInfo\                  host identity, OS build, uptime
    NetworkInfo\                connections, ARP, routing
    PersistenceMechanisms\      autoruns, services, tasks
    CopiedFiles\event logs\     the .evtx set
  Processing_Details.txt        every command, with its timestamp
  <HOST>_hashes.txt             a digest for every file collected
```

## Step 5 — read `Processing_Details.txt` (3 min) ★

**This is Section 6 of the report, written for you.** Have each pair copy the first and last lines
into their report template right now, while the file is open.

## Step 6 — hash before power-down (4 min)

```powershell
Get-FileHash .\ForensicImages\Memory\mem.raw -Algorithm SHA256
```

Recorded on the examiner drive, **before** the machine is powered down.

> **The point of step 6.** This is the one exhibit in the case that can never be re-taken. After
> power-down there is nothing left to compare a later hash against, so the hash has to exist *now*.

---

## Debrief — four questions

1. How many artifacts did your collection create on the target? *(at least four: a process, a driver
   load, a prefetch entry, a USBSTOR key)*
2. Which of those would look identical to an exfiltration device in `T17`? *(the USBSTOR key)*
3. What separates yours from an attacker's? *(only your step-1 note)*
4. Your capture took four minutes. Name one thing in it that was already false when the file closed.
   *(any process that exited during the capture — the smear)*

## Common failures

| What happens | Say this |
|---|---|
| a pair writes the image to `C:` | 16 GB into free space is 16 GB over the deleted files `T15` will ask them to carve |
| a pair skips step 1 and starts the collector | stop them; the lab is not recoverable from here and that is the lesson |
| "the process list is inconsistent — anti-forensics!" | that is the smear. It is a lead, never a finding |
| a pair hashes after power-down | ask what they would compare it against |
