# P02 · Guided lab — verify a set you did not create

Topic `T03` · **12 minutes** · evidence `EVS-01` · workstation `FOR-WS01`.

Everything you type is in a code block. Every step has a **verification line** — how you know the
step worked. Do not move on without it.

---

## Why this lab exists

In `P01` you hashed tools **you installed**, against a manifest **your own lab produced**. Here the
set arrives from someone else: four documents and two manifests from case `ITG-2026-014`.

This is the normal case. You will almost never hash something you made.

---

## Step 0 — start from a known state

Restore the `CLEAN-TOOLS` snapshot you took in `P01`, or confirm you are still on it.

**Verify:** the VMware snapshot manager shows `CLEAN-TOOLS` as the current state.

> You are about to make a statement about someone else's evidence. The first thing anyone will ask
> is what your machine was doing at the time. `P01` is why you can answer.

---

## Step 1 — find the set and read the manifest first

```powershell
cd C:\Forensics\Cases\ITG-2026-014\EVS-01
dir
```

You should see four documents and two manifests: `EVS-01.md5` and `EVS-01.sha256`.

```powershell
Get-Content EVS-01.sha256
```

**Verify:** four lines, each a 64-character digest followed by two spaces and a file name.

> **Read the manifest before you verify against it.** A manifest is a claim about four files made
> at some past moment by someone you are trusting. Knowing what it claims is step one; whether it
> is true is step three.

---

## Step 2 — compute one digest yourself

```powershell
Get-FileHash .\seizure_notes.txt -Algorithm SHA256 | Format-List
```

**Verify:** a 64-character hex string. Compare it by eye to the `seizure_notes.txt` line in the
manifest. They match.

Now do the same file with MD5:

```powershell
Get-FileHash .\seizure_notes.txt -Algorithm MD5 | Format-List
```

**Verify:** a 32-character hex string, matching the `EVS-01.md5` line.

> Two functions, two lengths, same file, both correct. You record **both** because MD5 and SHA-1
> are broken for collision resistance — a challenge to one should not take the exhibit with it.

---

## Step 3 — verify the whole set at once

```powershell
wsl sha256sum -c EVS-01.sha256
```

(or, on the Linux side of the lab, `sha256sum -c EVS-01.sha256` directly.)

**Verify:** four lines of output. **Three say `OK`. One says `FAILED`.**

```
seizure_notes.txt: OK
EVI-SRC01_acquisition_log.txt: FAILED
custody_form_EVI-SRC01.txt: OK
evidence_inventory.csv: OK
sha256sum: WARNING: 1 computed checksum did NOT match
```

---

## Step 4 🔑 — say only what the command told you

**Stop typing. This is the step the lab exists for.**

Write down, in one sentence, what you now know about `EVI-SRC01_acquisition_log.txt`.

The honest sentence is:

> **The file as it exists on disk does not match the digest the manifest records for it.**

That is the whole finding. Notice what is *not* in it:

| You do **not** know | Why not |
|---|---|
| **what** changed | a digest has no structure — it cannot be partially compared |
| **how much** changed | one byte and the whole file produce the same `FAILED` |
| **when** it changed | the digest carries no time |
| **who** changed it | the digest carries no identity |
| **whether it was deliberate** | a bad sector, a text editor rewriting line endings, and an edit all look identical here |
| **which side is wrong** | the file may have changed — or the manifest may have been computed on a different file |

> `FAILED` is a **question**, not a verdict. Anyone who writes "the file was tampered with" here has
> stated an interpretation in the Findings section, and lost rubric criterion 4 in one sentence.

---

## Step 5 — now do the thing the hash cannot

The hash told you *that*. To learn *what*, you have to look.

```powershell
Get-Content .\EVI-SRC01_acquisition_log.txt | Select-String "Acquisition started"
```

**Verify:** one line — `Acquisition started : 2026-03-04 09:14:03 UTC`.

Compare that against the acquisition window recorded on the custody form:

```powershell
Get-Content .\custody_form_EVI-SRC01.txt | Select-String "Imaging started"
```

**Verify:** `2026-03-04 09:14  Imaging started, hardware write blocker inline.`

The difference between this file and the one the manifest was computed from is **one second** in
one timestamp. That is it. That is the entire change that produced a completely different digest.

> **The avalanche property, seen from the other side.** In Step 2 you were told a one-character
> change destroys a digest. Here you met the consequence: the digest cannot tell you that the
> change was one second rather than the whole file. Sensitivity and information are not the same
> thing.

---

## Step 6 — read the note the acquisition log makes about itself

```powershell
Get-Content .\EVI-SRC01_acquisition_log.txt | Select-String -Context 0,4 "NOTE ON SCOPE"
```

**Verify:** the log states that verification compared the digest computed while **writing** the
image against the digest computed while **reading it back** — and that the source drive was not
re-read.

> This is the most misread line in forensic tooling. `verified` in an imager's log is the tool
> checking **its own round trip**. It is a real and useful check. It is not an independent check,
> and it says nothing whatsoever about the source drive.

---

## Step 7 — find the write blocker in the evidence

Search the image and its log for any record that a write blocker was used.

```powershell
Select-String -Path .\EVI-SRC01_acquisition_log.txt -Pattern "blocker","block","write-protect"
```

**Verify:** the only hit is the examiner's free-text `Notes` field — which says the blocker details
are recorded **on the custody form, not in this file**.

Now look where it actually lives:

```powershell
Get-Content .\custody_form_EVI-SRC01.txt | Select-String -Context 0,3 "Imaging started"
```

**Verify:** make/model/serial/firmware on notebook page 41, photographed with the rig, frames
011–013, before anything was disconnected.

> **An image taken on a write blocker and an image taken without one are byte-identical.** There is
> no field. The proof lives in four places, all of them outside the file: the blocker's own log or
> display, a photograph of the rig with serials legible, the custody-form line, and your
> contemporaneous notes. Write it down at the time or it does not exist.

---

## Step 8 — the pair that is the real technical proof

```powershell
Get-Content .\custody_form_EVI-SRC01.txt | Select-String -Context 0,3 "re-hashed"
```

**Verify:** the source was hashed **before** the imaging run and **again after**, and the two match.

> Two matching **source** hashes taken across an imaging run are the strongest technical evidence
> available that nothing was written to the source. Stronger than the sentence "a write blocker was
> used" — because it is a measurement, and that is a claim.

---

## Chain of custody — the line this lab produces

Add this to your own record before you close the lab. Fill the bracketed parts yourself.

```
[YYYY-MM-DD HH:MM UTC]  EVS-01 received and verified by [your name] on FOR-WS01
                        (state: CLEAN-TOOLS snapshot).
                        sha256sum -c EVS-01.sha256 -> 3 OK, 1 FAILED.
                        FAILED file: EVI-SRC01_acquisition_log.txt.
                        Finding: file does not match the manifest digest.
                        Cause not established from the hash. Difference located
                        by inspection: one timestamp, 09:14:02 vs 09:14:03.
                        Not reported as tampering. Referred to the set's owner.
```

**Verify:** your line says what you observed and stops. If it contains the word *tampered*,
*altered by* or *someone*, delete that word and re-read it.
