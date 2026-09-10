# P02 · Quiz — Evidence integrity

Topic `T03`. Ten questions. Every question maps to a numbered objective.
Answer key and justifications: `quiz_answer_key.md`.

**Objectives**
1. State precisely what a matching hash proves.
2. Identify what a matching hash does not prove.
3. Read a hash mismatch without over-claiming.
4. Explain what a chain of custody carries that a hash cannot.
5. Explain how the use of a write blocker is evidenced.
6. Distinguish a tool's self-verification from an independent check.

---

**Q1 · obj 1.** A disk image verifies against the SHA-256 recorded during acquisition. Which
statement is exactly true, with nothing added?

- a) The evidence has not been tampered with.
- b) The image is an authentic copy of the suspect's drive.
- c) The image is byte-identical to what the tool read from the source at acquisition time.
- d) The acquisition was complete.

---

**Q2 · obj 2.** A drive has a host protected area. The imaging tool's interface never reports it,
so it is never read. The image verifies against the source hash. What is true?

- a) The hashes will mismatch, revealing the HPA.
- b) The hashes match perfectly, and the copy is incomplete.
- c) The hash covers the HPA regardless of whether it was read.
- d) HPAs cannot exist on drives that are being imaged.

---

**Q3 · obj 3.** `sha256sum -c` reports `FAILED` on one file in a set of four. Which is the only
statement you can put in the **Findings** section?

- a) The file was tampered with after the manifest was created.
- b) The file's computed digest does not match the digest recorded in the manifest.
- c) The manifest is corrupt.
- d) The file was modified by an unauthorised user.

---

**Q4 · obj 3.** You re-hash a 2 TB SSD exhibit that has been powered on twice since acquisition,
and it no longer matches. Which explanation can you rule **out** on this evidence alone?

- a) Deliberate alteration.
- b) A failing sector.
- c) The drive's own garbage collection after TRIM.
- d) None of them — the hash mismatch does not distinguish between these.

---

**Q5 · obj 6.** FTK Imager's log says `MD5 checksum: … : verified`. What was compared?

- a) The source drive against the finished image.
- b) The digest computed while writing the image against the digest computed while reading it back.
- c) The image against the value on the chain-of-custody form.
- d) The image against a manufacturer-published baseline.

---

**Q6 · obj 5.** Two examiners produce images of the same drive. One used a hardware write blocker;
one did not. Comparing only the two image files, which is true?

- a) The blocked image contains a flag recording the blocker.
- b) The unblocked image will be larger.
- c) The two images are byte-identical, and neither records how it was made.
- d) The unblocked image will fail verification.

---

**Q7 · obj 5.** Which of these is *proof* that a write blocker was in the path during a specific
acquisition?

- a) The blocker is listed in the lab's equipment inventory.
- b) The examiner remembers using it.
- c) The blocker's log, a photograph of the connected rig with serials legible, the custody-form
     line naming make/model/serial, and contemporaneous notes.
- d) The image verified successfully.

---

**Q8 · obj 4.** An organisation's incident wiper ran three hours before seizure. The chain of
custody afterwards is flawless. What does the chain of custody establish?

- a) That the data on the exhibit is genuine and unaltered.
- b) That the exhibit was handled continuously from seizure onward — and nothing about the state of
     the data before seizure.
- c) That the wiper's effects can be reversed.
- d) That the exhibit is admissible.

---

**Q9 · obj 2.** An attacker has write access to both the evidence server holding an image and the
file holding its hash. What is the value of that hash?

- a) It still proves integrity, because the hash is one-way.
- b) It proves integrity only if SHA-256 is used rather than MD5.
- c) None — anyone who can alter the image can recompute and replace the hash.
- d) It proves integrity as long as the image is larger than the hash file.

---

**Q10 · obj 1, 2.** A room verifies an image's MD5, confirms the match, and on the next page runs
`sudo mount -o loop image.img /mnt/x`. What is the state of the verification?

- a) Unaffected — mounting is a read operation.
- b) Unaffected, because the hash was computed before mounting.
- c) Invalidated — a read-write mount writes superblock and access-time data into the image.
- d) Invalidated, but only if files are opened.

---

> **Q3 and Q10 are the same idea at two depths.** Q3 asks you to state a mismatch without
> over-claiming. Q10 asks you to notice that a *match* has quietly stopped being true. Getting Q3
> right and Q10 wrong means the rule was memorised and the reasoning was not.
