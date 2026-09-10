# P02 · Student guide — Evidence integrity

Topic `T03` · 38 minutes. Everything on the page, in the order it happens, so you can work through
it again alone.

---

## The one sentence

> **A matching hash proves the copy equals the source as read at that moment — and nothing else.**

You probably arrived believing a hash proves evidence "has not been tampered with". That sentence
appears in professional courseware. It is not right, and the rest of this page is why.

---

## 1 · What a hash is

A one-way function. Any input, any size, in; a fixed-length digest out. Change one bit of the input
and the digest changes completely and unpredictably — the **avalanche** property.

Try it yourself:

```powershell
"H" | Set-Content -NoNewline t.txt ; Get-FileHash t.txt -Algorithm SHA256
"h" | Set-Content -NoNewline t.txt ; Get-FileHash t.txt -Algorithm SHA256
```

Two digests with nothing in common, from a one-bit difference.

**Never copy a digest out of a document, including this one.** A value you did not compute is a
claim about a value.

---

## 2 · The one thing a match proves

That two byte streams are identical, to within the collision resistance of the function.

That is genuinely valuable. It is how you show a 2 TB image equals a 2 TB drive without comparing
them by hand, and how you show months later that nothing in **your** custody changed the image.

---

## 3 · The four things it does not prove

### 3.1 · Not completeness

If a host protected area is never reported by the drive's interface, it is never read — so it is
absent from the source hash **and** from the image hash. They agree perfectly about a partial copy.

> A match is a comparison between two reads. It cannot comment on what was never read.

### 3.2 · A mismatch is not tampering

A failing sector, a cable fault, a text editor rewriting line endings, and an SSD's own garbage
collection after TRIM all produce a mismatch with nobody at fault.

> `FAILED` means *these differ*. It carries no cause, no time, no identity, and **no magnitude** —
> a one-second edit and a total replacement produce the same line.

### 3.3 · Not authenticity, and not provenance

The hash says the copy equals the source. It says nothing about *which drive the source was*, whose
data it held, or whether it had already been altered before you arrived.

### 3.4 · Nothing at all, if one person holds both

Someone who can change the image and can also change the file holding its hash simply recomputes.
The protection was never the function's strength — it is **where the value is stored**.

> This is the correction INE makes to itself: `[U2 p143]` says hashes prove a file has not been
> tampered with; `[U2 p144]` says the hash must be stored securely and **separately**. The second
> slide is the true one, and it is true because of where the value lives.

---

## 4 · So where does authenticity live?

In two records, both written by you, neither recoverable afterwards.

### 4.1 · Chain of custody

The unbroken, contemporaneous record of who held the exhibit, when, and what they did to it.

INE's minimum fields: what the evidence is, how it was acquired, when, by whom, where stored, and
every subsequent action. Physical controls belong with it — antistatic bag, padding, sealed
container, **tape signed across the seal** so re-opening is visible, controlled temperature.

Read one as a timeline and check three things:

1. no unexplained time gap,
2. no transfer without two signatures,
3. hashes recorded at seizure that still match today.

> **The asymmetry matters.** A perfect chain does not by itself win admissibility. A single
> unexplained gap is enough to lose it — the other side only has to raise the *possibility* of
> substitution.

And note what it does *not* carry: continuity of the **exhibit**, not the genuineness of the
**data**. The attacker's wiper ran before you arrived and the chain is still flawless.

### 4.2 · The write-block proof trail

A write blocker filters write commands out of the path before they reach the media. It matters
because attaching a disk to a running Windows box *is* a write — Windows touches the volume,
updates journal state, and can mount and modify unasked.

**Hardware** is an inline dock (WiebeTech Forensic UltraDock; Tableau TD3). **Software** is a
forensic boot disc, or the Windows registry value below. INE is blunt: software is the fallback,
not the equal.

Now the part that matters:

> **An image taken on a write blocker and an image taken without one are byte-identical.**
> There is no field. No tool can tell anyone afterwards.

So the proof lives in four places outside the file:

1. the blocker's own display or log,
2. a photograph of the connected rig with serials legible, taken before anything is disconnected,
3. the custody-form line naming make, model, serial and firmware,
4. your contemporaneous notes.

**And the strongest technical evidence is not any of those four** — it is hashing the **source**
before the imaging run and again after, and recording both. Two matching source hashes across the
run is a measurement. "A write blocker was used" is a claim.

### 4.3 · The software fallback, and how it fails

`HKLM\SYSTEM\CurrentControlSet\Control\StorageDevicePolicies` → `WriteProtect` (`REG_DWORD`) = `1`.

What it is not:

- It is in **your** registry, not the evidence's — it says something about your workstation and
  **nothing about how any particular exhibit was handled**. Not per-device, not timestamped.
- It covers devices enumerated as **USB mass storage** only. Not a SATA disk on an internal port,
  not a dock presenting as a fixed disk, not MTP.
- It usually needs a reboot or at least a re-enumeration.

> **The classic failure:** set the value, do not reboot, plug the evidence in, report "software
> write blocked". Windows writes to it happily. **Always demonstrate the block on a scratch stick
> before touching evidence** — attempt a write, confirm it fails, log the result.

---

## 5 · Reading a tool's own verification

FTK Imager's log ends with `MD5 checksum: … : verified`. What was compared?

The digest computed **while writing** the image against the digest computed **while reading it
back**. The source drive is not re-read.

That is a real check — it proves the write-then-read round trip was clean. It is **not** an
independent check, and it says nothing about the source. `EVS-01`'s acquisition log states this in
its own text; read that note.

Also in that file, and worth knowing: the Case Information block is free text typed by the
operator, and the drive geometry is what the **interface reported** — so an HPA-shortened capacity
is faithfully logged as though it were the whole disk.

---

## 6 · Two lines to keep

For your report, and for the rest of the course:

> **Finding:** `<file>` computed SHA-256 does not match the value recorded in `<manifest>`.
>
> **Not established:** what changed, when, by how much, or by whom.

Say the first. Say the second. Stop.
