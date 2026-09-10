# P02 · Independent work — you judge

Topic `T03` · **9 minutes**, individual, at your own keyboard.

---

## (a) Sort five results · 4 minutes

Each line is a real hash result from a real situation. Put each into **one** bucket.

> **Integrity intact** — I can state the copy equals what was recorded.
> **Integrity broken** — I can state they differ.
> **Cannot tell from this** — the hash result does not answer the question being asked.

Read the **question** in each scenario, not just the result. Two of these five ask something a
hash cannot answer at all.

| # | Scenario | Your bucket |
|---:|---|---|
| 1 | You image a 500 GB disk. Source hash before and after the run match each other, and the image hash matches the source. **Was anything written to the source during the run?** | |
| 2 | An image verifies perfectly against the hash recorded at acquisition three years ago. The hash was stored in a file **on the same evidence server as the image**, which an administrator has had write access to throughout. **Is the image unaltered since acquisition?** | |
| 3 | You re-hash an exhibit before this week's analysis session. It does not match the value on the custody form. The exhibit is a 2 TB SSD that has been powered on twice since. **Has someone altered the evidence?** | |
| 4 | A disk image verifies against its acquisition hash. The drive had a host protected area that the imaging tool's interface never reported. **Do you have a complete copy of the media?** | |
| 5 | Two identical drives were seized from the same office. Neither was labelled at seizure. Both images verify perfectly against their acquisition hashes. **Which desk did each come from?** | |

**Success criteria.** You have used **"cannot tell from this"** at least twice, and for each of
those two you can say in one sentence what evidence *would* answer the question.

---

## (b) The defect hunt · 5 minutes

You will be shown two consecutive pages from TryHackMe's **Forensic Imaging** room — a free room
with over 18,000 completions.

**Page 1 (Task 4)** computes an MD5 of a disk image and confirms it matches the expected value.

**Page 2 (Task 5)** then runs:

```bash
sudo mount -o loop example1.img /mnt/example1
```

### The question

**What has just happened to the hash that was verified on the previous page?**

### Write three things

1. **What the command does** to the image file — be specific about what gets written.
2. **What you would type instead**, and what each option in your command is for.
3. **One sentence for a report** stating what you can and cannot say about that image now.

### Success criteria

You have named at least one specific thing that is written, not just "it modifies it". You can
defend every option in your replacement command — an option you cannot explain is an option you
have copied.

---

## What this is training

Both exercises are the same skill in different clothes: **separating what a result says from what
you want it to say.** In (a) the temptation is to answer the question you know how to answer. In
(b) it is to trust a source because it is popular and well made.

The Forensic Imaging room is worth doing. Its Task 2 — an audit trail built from seven bash
settings plus session recording with `script` — is the best treatment of *logging the examiner*
in any room we reviewed. **A source can be worth using and still be wrong in one place.** Telling
which is which is the job.
