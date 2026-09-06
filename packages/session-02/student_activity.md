# Session 2 — Student Activity

**Two investigations, 60 minutes, individual at the keyboard.**
Case 02a — acquire and verify the suspect USB · 35 min
Case 02b — examine the acquired image's structure · 25 min

---

## Case 02a — acquire and verify the suspect USB

**Time box: 35 minutes.**

### Brief

A finance workstation at Meridian Retail Group has been investigated after a suspected data theft. The
workstation is exhibit `EVI-SRC01`, Windows computer name `FIN-WKS-07`, used by the account
`l.bennett`. It was reached still running; volatile data and memory were captured, then the machine
was powered down and the system disk imaged.

A USB storage device was attached to the workstation when it was found. It has been seized as a
separate exhibit. **Your task is to acquire it and prove what you did.**

Nothing about the device's contents has been established. Your job in this case is acquisition and
verification only.

### Scope and authorisation

You are authorised to:

- acquire a forensic image of the seized USB device
- verify the image against its own acquisition record
- record the acquisition in the chain-of-custody record

You are **not** authorised to:

- write to the device in any way
- examine data outside the seized exhibit
- draw conclusions about who used the device

### Evidence

| Item | Exhibit | Format | Manifest |
|---|---|---|---|
| Suspect USB device image | `EVS-04` | E01 + raw | published with **both** digests before the session (`D18`) |

⚠️ **Verify the published hashes before you begin.** A mismatch is a finding, not an inconvenience.

### Environment

`FOR-WS01` on the `CLEAN-TOOLS` snapshot. FTK Imager 8.3. A write blocker, hardware or software.
Mount read-only with OSFMount 3.3.1000 or Arsenal Image Mounter 3.13.368 if you need to look inside.

### The acquisition decision

Before you image anything, work down this path and **write your answer at each step**:

1. Is the host running?
2. Is the data encrypted at rest?
3. Is time short, or is the device too large to image?
4. Which method — and what does it forfeit?

Your written answers are part of the deliverable. The decision is evidence.

### The questions

| # | Question |
|--:|---|
| **Q1** | Verify `EVS-04` against its published manifest. State both digests and the result. *(Q1 is always hash verification.)* |
| **Q2** | Record the write blocker you used, and the exact time it was engaged relative to connecting the source. Why does the order matter? |
| **Q3** | You imaged the device. State precisely what your verification result covers, and what it does not. |
| **Q4** | The device is 8 GB. Your E01 image is smaller than 8 GB. Is that a problem? Explain in one sentence. |
| **Q5** | Which acquisition method did you choose, and what evidence would you have forfeited by choosing logical acquisition instead? |
| **Q6** | Can you establish from your acquisition alone **who** attached this device to the workstation? Answer honestly. |

### Deliverable

Write your answers as numbered findings and interpretations, using the fixed report format:

```
F-01  <fact only, tied to one named artifact at an exact path>
I-01  <interpretation, clearly separated, with its basis>
L-01  <limitation — what this evidence cannot show>
```

### Success criteria

| ☐ | |
|:-:|---|
| ☐ | Q1 answered with **both** digests and an explicit pass or fail |
| ☐ | The write blocker recorded **before** the source was connected |
| ☐ | Every finding tied to one named artifact at an exact path |
| ☐ | Interpretation visibly separated from findings |
| ☐ | At least one honest limitation stated |
| ☐ | Every tool named **with its version** |

### Two things that will cost you marks

1. Writing *"the USB was used to steal data"* as a finding. That is an interpretation, and on this
   evidence it is not even a supported one.
2. Writing *"the image is verified, so the device was not tampered with."* Verification covers the
   copy, not the history of the original.

---

## Case 02b — examine the acquired image's structure

**Time box: 25 minutes.**

### Brief

You now hold a verified image. Before anything inside it is examined, its **structure** has to be
established and recorded: what partitions exist, what file systems they hold, and whether the sizes
reconcile against the device.

### Scope and authorisation

You are authorised to examine the partition and file-system structure of `EVS-04`, and to mount it
**read-only**. You are not authorised to interpret file contents in this case — that is Session 3.

### The questions

| # | Question |
|--:|---|
| **Q1** | Re-verify your working copy against the manifest before you start. State the result. |
| **Q2** | List the partitions: start offset, size, partition type. |
| **Q3** | Which file system is on each partition, and what is the volume size each one reports? |
| **Q4** | Do the partition sizes account for the whole device? If not, how much is unaccounted for? |
| **Q5** | If there is unaccounted space, state what it **could** be — and mark clearly whether your answer is a finding or an interpretation. |
| **Q6** | **Why** is the unaccounted space there? Answer using only the evidence in front of you. |

⚠️ **Q6 is answerable only as a limitation.** The structure shows *that* space is unaccounted for. It
cannot show *why*. A correct answer says so.

### Deliverable

The same three line formats. One `L-` line is required.

### Success criteria

| ☐ | |
|:-:|---|
| ☐ | The image was mounted **read-only** and you can say how you know |
| ☐ | Partition offsets and sizes given as numbers, not descriptions |
| ☐ | Q5 explicitly labelled finding or interpretation |
| ☐ | Q6 answered as a limitation, not guessed |

### If you finish early

Mount the raw image as well as the E01 and confirm the structure reads identically from both. Record
whether the two agree — and note that agreement between two copies is still not a statement about the
source device.
