# Session 1 — Guided Lab

**Forensic Foundations, Evidence Integrity & Chain of Custody**

Two labs, run in order. **Lab A** builds the workstation you will use for the rest of the diploma.
**Lab B** is the integrity work this whole course rests on.

Every step has an **expected result** and a **verification line**. A step without a passing
verification line is not complete — do not move on.

---

## Objective

Build and baseline a forensic workstation, then verify a supplied evidence set against its signed
manifest and record the result as a finding.

By the end you will have completed the arc this course runs on every session:

> **acquire → verify (hash) → analyse → interpret → document**

---

## Environment

| | |
|---|---|
| **VM** | `FOR-WS01` — clean Windows base, no forensic tooling |
| **Start from snapshot** | `CLEAN-BASE` |
| **Network** | offline. Installers are supplied locally |
| **Evidence** | `EVS-01` — ⚠️ **unverified** at time of writing. Four files plus manifests |
| **Deliverable** | one custody line, signed |

> ✅ **`EVS-01` was generated and hash-verified on 2026-08-30.** The manifests ship with the set as
> `EVS-01.sha256` and `EVS-01.md5`. **Read every digest from the manifest — never type one.**

---

## Lab A — build the workstation and baseline it

### Step A1 — confirm your starting point

Open the snapshot manager and confirm `FOR-WS01` is running from `CLEAN-BASE` with nothing after
it.

**Expected result:** exactly one snapshot in the tree, named `CLEAN-BASE`.

**Verification line:**

```
A1 PASS — FOR-WS01 running from CLEAN-BASE, no later snapshots.
```

> **Why this step exists:** if you install onto a machine whose starting state you cannot describe,
> nothing you do afterwards is reproducible — and reproducibility is half of what makes a method a
> method.

---

### Step A2 — record the baseline

Before installing anything, capture what the machine is:

```powershell
# Windows build and the PowerShell version that will run every later command
Get-ComputerInfo -Property OsName,OsVersion,OsBuildNumber
$PSVersionTable.PSVersion
```

**Expected result:** an OS name, version and build number, and a PowerShell version.
Write all four into your notes.

**Verification line:**

```
A2 PASS — baseline recorded: OS <name> <version> build <build>, PowerShell <version>.
```

> Every command in this diploma is only correct against a stated version. This is where you get
> yours.

---

### Step A3 — install the tool set

Install from the supplied local media, in any order. Record the version of each as you go.

| Tool | Version to install |
|---|---|
| FTK Imager | 8.3 |
| Autopsy | 4.23.1 |
| Wireshark | 4.6.8 |
| Volatility 3 | 2.28.0 **plus its symbol pack** |
| ExifTool | 13.59 |
| HxD | 2.5.0.0 |
| OSFMount | 3.3.1000 |
| Arsenal Image Mounter | 3.13.368 |
| TestDisk / PhotoRec | **7.2 stable** — not the 7.3 work-in-progress build |
| RegRipper | **3.0 only** |
| NetworkMiner | 3.1 |
| Get-ZimmermanTools | current |
| plaso / log2timeline | current |
| CyberChef | offline copy |

**Expected result:** every tool launches once and closes cleanly.

**Verification line:**

```
A3 PASS — 14 tools installed; each launched once; versions recorded in notes.
```

> **Volatility 3 downloads symbol files on first run.** On an offline machine that does not wait —
> **it fails.** The symbol pack is supplied with the installer for exactly this reason.

**Three tools are deliberately absent, and you should know why:**

| Not installed | Reason |
|---|---|
| RegRipper 4.0 | licensed for personal and academic use only; barred from vendor training and any distribution |
| 010 Editor | commercial, 30-day evaluation, no free tier. HxD covers this course's needs |
| Xiao Steganography | no working vendor site; every available copy is a third-party mirror from 2010 or earlier |

---

### Step A4 — take the `CLEAN-TOOLS` snapshot

Shut the VM down cleanly first. Then take a snapshot named **exactly**:

```
CLEAN-TOOLS
```

**Expected result:** the snapshot tree reads `CLEAN-BASE → CLEAN-TOOLS`.

**Verification line:**

```
A4 PASS — snapshot CLEAN-TOOLS created from a clean shutdown; tree is CLEAN-BASE -> CLEAN-TOOLS.
```

> **This is the point of Lab A.** From here on, any session that goes wrong is one revert away
> from a known-good workstation with a known tool set. Later sessions refer to this snapshot by
> name — the spelling matters.

**Common mistake:** snapshotting a *running* VM. It works, but it captures memory state as well
and the snapshot becomes machine-specific and much larger. Shut down first.

---

## Lab B — verify an evidence set

### Step B1 — see the avalanche for yourself

```powershell
"Evidence file, original." | Set-Content -NoNewline evidence.txt
Get-FileHash .\evidence.txt -Algorithm SHA256
```

**Expected result:** a 64-hex-character digest and the path to `evidence.txt`.

Now change exactly one character — the capital `E` becomes lowercase:

```powershell
"evidence file, original." | Set-Content -NoNewline evidence.txt
Get-FileHash .\evidence.txt -Algorithm SHA256
```

**Expected result:** a digest with **no visible resemblance** to the first. Not "mostly the same" —
unrecognisable.

**Verification line:**

```
B1 PASS — one character changed; both digests recorded in notes; they share no leading characters.
```

> Generate these yourself and write both into your notes. **Never transcribe a digest from a
> slide, a document or a screenshot** — a copied digest is a digest you cannot defend.

---

### Step B2 — hash the evidence set

Change into the directory holding your downloaded `EVS-01` files.

**Windows:**

```powershell
Get-FileHash * -Algorithm SHA256 | Format-List Path,Hash
```

**Linux:**

```bash
sha256sum *
```

**Expected result:** four digests, one per file:

| File |
|---|
| `seizure_notes.txt` |
| `EVI-SRC01_acquisition_log.txt` |
| `custody_form_EVI-SRC01.txt` |
| `evidence_inventory.csv` |

**Verification line:**

```
B2 PASS — 4 files hashed with SHA-256; digests recorded.
```

---

### Step B3 — verify against the signed manifest

**Linux — the manifest is in `sha256sum` format, so the tool does the comparison:**

```bash
sha256sum -c EVS-01.sha256
```

**Windows:**

```powershell
Get-Content EVS-01.sha256 | ForEach-Object {
    $expected, $name = ($_ -split '\s+', 2)
    $name = $name.TrimStart('*').Trim()
    $actual = (Get-FileHash $name -Algorithm SHA256).Hash
    '{0}: {1}' -f $name, $(if ($actual -eq $expected) { 'OK' } else { 'FAILED' })
}
```

**Expected result — read this carefully:**

```
seizure_notes.txt: OK
EVI-SRC01_acquisition_log.txt: FAILED
custody_form_EVI-SRC01.txt: OK
evidence_inventory.csv: OK
```

🔴 **One file fails. That is correct — it is the exercise, not an error in your download.**

**Verification line:**

```
B3 PASS — manifest checked: 3 OK, 1 FAILED. The failing file is named in my notes.
```

**Common mistakes at this step:**

| Mistake | What happens | Fix |
|---|---|---|
| Verifying against a hash you typed by hand | a false FAILED on a good file | always read the manifest from the file |
| Opening the files in an editor first, then hashing | an editor may rewrite line endings and change every digest | hash before you read |
| Running the check from the wrong directory | *"No such file or directory"* on all four | `cd` to the evidence directory first |
| Assuming `FAILED` means the download broke | you re-download and lose the exercise | a mismatch is a **finding**, and finding it is the job |

---

### Step B4 — record the mismatch as a finding, not a conclusion

Write it in the report format. Two separate boxes.

**✅ This is a finding:**

> **F-01** — `EVI-SRC01_acquisition_log.txt`, received in `EVS-01`, computes to SHA-256
> `7eda34b3…f4bfb3c6`. The value recorded for that filename in `EVS-01.sha256` is
> `f05bfee8…457171d7`. The two do not match. The other three files in the set match their
> recorded values.
>
> *(Quote both digests in full in your own report — they are truncated here only to fit the page.)*

**✅ This is the interpretation, and it belongs in a different section:**

> **I-01** — The content of `EVI-SRC01_acquisition_log.txt` differs from the content that was
> present when the manifest was produced. Assessed with high confidence, since the remaining
> three files verify and a transport fault affecting exactly one file of four without detection is
> unlikely. Considered and not excluded: an editor that rewrote line endings on open, and
> corruption during transfer.

**❌ This is neither, and it will lose marks:**

> ~~The acquisition log was tampered with to hide the real acquisition time.~~

Three separate failures in one sentence: *tampered with* asserts intent, *to hide* asserts motive,
and *the real acquisition time* asserts a fact no artifact you hold states.

**Verification line:**

```
B4 PASS — one finding and one interpretation written as separate numbered entries;
          the interpretation cites F-01 and names an alternative.
```

---

### Step B5 — state what this cannot show

Every investigation carries at least one. For this one:

> **Cannot prove** — which of the two versions is the original. The manifest records what the file
> hashed to when the manifest was made; it does not establish that the manifest was made before
> the change. Nor does the mismatch identify who altered the file, when, or with what — nothing in
> `EVS-01` records that.

**Verification line:**

```
B5 PASS — one limitation stated, in its own section, not mixed into the finding.
```

---

## Chain of custody — close the lab

Complete one line. Handwritten on the printed form, then transcribed into your notes.

| Field | Your entry |
|---|---|
| **Who** | your full name and role |
| **What** | `EVS-01` — four files and two manifests |
| **When** | date and time, **with the time zone**, in UTC |
| **From where** | where you obtained it, and how |
| **Hash** | SHA-256 as verified in **B3**, and the MD5 alongside it |
| **Where stored** | the exact path on `FOR-WS01`, and the medium |
| **Result** | `3 verified, 1 mismatch — see F-01` |

**Sign it.**

```
CoC PASS — one custody line completed and signed; the mismatch is recorded on the form,
           not left in my notes only.
```

> **The mismatch goes on the form.** A custody record that only says what went right is not a
> custody record. This one has to say that one of four files did not verify at the moment it came
> into your hands — otherwise the next person to hold it inherits a problem with no history.

---

## Lab complete — check yourself

| ☐ | |
|:-:|---|
| ☐ | `CLEAN-TOOLS` snapshot exists and is spelled exactly |
| ☐ | Every tool version is written down, not remembered |
| ☐ | Both avalanche digests are in your notes |
| ☐ | The manifest check produced 3 `OK` and 1 `FAILED` |
| ☐ | One finding, written with no verb of inference |
| ☐ | One interpretation, citing the finding and naming an alternative |
| ☐ | One limitation, in its own section |
| ☐ | One custody line, signed, recording the mismatch |

If any box is empty, that is the box the report will lose a mark on.
