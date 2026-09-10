# P01 · Quiz

Ten questions. **Stems are bilingual; the options stay in English** (`D76`) — those are the words
the exam uses.

---

**Q1.** What is the last part of the digital-forensics mandate, and the part the rest of this course exists to serve?
<span class="ar">إيه آخر جزء في مهمة التحليل الجنائي الرقمي، و الجزء اللي باقي الكورس موجود عشانه؟</span>

- A. Recover the deleted data
- B. Identify the attacker
- C. **Interpret the evidence so it survives challenge**
- D. Restore the system to service

*Objective 1*

---

**Q2.** *Repeatable* and *reproducible* are not the same thing. Which pair is correct?
<span class="ar">الاتنين مش نفس الحاجة. أنهي زوج صح؟</span>

- A. Repeatable = different lab, same result · Reproducible = same lab, same result
- B. **Repeatable = same lab and tools, same result · Reproducible = different lab or tools, same result**
- C. Repeatable = the same analyst can redo it · Reproducible = the tool produces the same hash
- D. They are synonyms in a forensic context

*Objective 2*

---

**Q3.** Of INE's three admissibility tests, which one is the examiner's responsibility?
<span class="ar">من اختبارات القبول التلاتة، أنهي واحد مسؤولية المحلل؟</span>

- A. Relevance
- B. Competence
- C. **Authenticity, inside Reliability**
- D. All three

*Objective 3*

---

**Q4.** A statement reads: *"The user `l.bennett` copied the database to a USB device."* Why can this not appear in §8 Findings?
<span class="ar">جملة بتقول: "المستخدم l.bennett نسخ قاعدة البيانات على USB." ليه دي ما تنفعش في قسم ٨؟</span>

- A. It has no timestamp
- B. It does not name the artifact
- C. **It names a person as the actor — artifacts record accounts, not people**
- D. It uses the past tense

*Objective 4*

---

**Q5.** Which single word, if a sentence needs it, proves the sentence is not a finding?
<span class="ar">أنهي كلمة، لو الجملة محتاجاها، بتثبت إنها مش finding؟</span>

- A. *when*
- B. **because**
- C. *approximately*
- D. *apparently*

*Objective 4*

---

**Q6.** The `CLEAN-TOOLS` snapshot must be taken at which moment?
<span class="ar">سناب شوت `CLEAN-TOOLS` بيتاخد إمتى بالظبط؟</span>

- A. Before the tools are installed
- B. **After the tools are installed and hash-verified, and before any case data touches the machine**
- C. At the end of each case
- D. Immediately after the first acquisition

*Objective 5*

---

**Q7.** You compute a tool's SHA-256 and it matches the vendor's published value. What does that prove?
<span class="ar">حسبت الـ SHA-256 لأداة و طابق اللي الشركة نشرته. ده بيثبت إيه؟</span>

- A. The tool is free of vulnerabilities
- B. The tool will not alter evidence
- C. **The binary you hold is byte-identical to the one the vendor published**
- D. The vendor is trustworthy

*Objective 5 · this pattern returns in `T03`*

---

**Q8.** An interpretation is complete only when it does three things. Which is **not** one of them?
<span class="ar">الـ interpretation بتبقى كاملة لما تعمل تلات حاجات. أنهي واحدة **مش** منهم؟</span>

- A. Cites the finding numbers it rests on
- B. States a confidence level
- C. Names an alternative explanation
- D. **States that the conclusion is certain**

*Objective 6*

---

**Q9.** Why is §2 Executive summary written last?
<span class="ar">ليه قسم ٢ بيتكتب آخر حاجة؟</span>

- A. Because it is the shortest section
- B. Because the reader reads it first
- C. **Because a summary written first becomes a conclusion you then look for evidence to support**
- D. Because the rubric does not grade it

*Objective 7*

---

**Q10 · scenario.** A disk image verifies perfectly against its acquisition hash. The examiner cannot say who handed them the drive, or when. Which statement is true?
<span class="ar">صورة قرص طابقت هاش الاستحواذ بالظبط. المحلل مش قادر يقول مين سلّمهاله ولا إمتى. أنهي جملة صح؟</span>

- A. The evidence is authentic because the hash matched
- B. **The hash proves the image matches what was acquired; it says nothing about where the drive came from — authenticity is broken and it is the examiner's failure**
- C. The evidence is inadmissible for relevance
- D. This is the lawyer's failure, not the examiner's

*Objective 3 · **this is the page's "what it cannot prove" question***
