# P01 · Report stage

**Which of the twelve sections this page fills, and what a good entry into each looks like**
(`D85` rule 3). The canonical template is `design/report_template.md`; the student copy is
`docs/report/`.

**This page opens the report.** Nothing is filled before it, and three sections are started here.

---

## `T01` fills §1 and §3

### §1 · Case identification

Complete, not partial. It is the only section with no judgement in it, so there is no excuse for a
gap.

| Field | A good entry |
|---|---|
| Case ID | `FL-2026-014` — the lab job number, not a description |
| Requesting party | the role and organisation, not a person's first name |
| Examiner name and role | `<name>, Forensic Analyst` |
| Report version | `0.1` — and it increments every time the report is handed in |
| Date issued (UTC) | `2026-09-15` — one date format for the whole report, chosen now |
| Classification / handling | who may read this, and what happens to it afterwards |

> **The trap:** students leave *Report version* blank because the report is not finished. It is never
> finished; it is versioned. `0.1` today, `0.2` after `P02`.

### §3 · Authorisation & scope

Three questions the examination must answer, and **at least one thing that is out of scope.**

**A good entry:**

> **Questions.** (1) Was data copied from `FIN-WKS-07` to a removable device between 24 and 26
> August 2026? (2) If so, which device, and what was copied? (3) Which account was in use at the
> time?
>
> **Out of scope.** The Kali host at `<address>` was part of the incident but was not made available
> for examination. No conclusion in this report rests on it. Instructed by `<requesting party>`.

**A weak entry** — and the one most students write first:

> *"Investigate the incident on FIN-WKS-07."*

That is a task, not a scope. It has no questions, no boundary, and nothing that can later be shown
to have been respected.

> **Why the out-of-scope line matters this early:** the Kali host is genuinely not examined in this
> course (`D87`), and a report that never says so reads as a report that did not notice. Stating a
> limitation on day one is the habit; §10 is where it compounds.

---

## `T02` opens §8 and §9, and marks §2 · §9 · §11 as written last

`T02` teaches the **shape** of §8 and §9 rather than filling them — there is no evidence yet. What
it produces is the student's first written triple, which lives in the homework, not the report.

**What is recorded in the report itself:**

- a note at §2, §9 and §11: **written last** (`D85`)
- §8 and §9 headings created, empty, with the format line under each so the student writes into a
  shape rather than a blank page:

> §8 — `F-nn` — `<artifact>` at `<exact path>`, `<UTC timestamp>`: `<one observable fact>`
>
> §9 — `I-nn` — `<claim>` is assessed with `<confidence>` confidence, resting on `F-xx`.
> Considered and not excluded: `<alternative>`, because `<reason>`.

---

## What the guided lab adds to §6

The lab produces one real line, and it is written **during** the lab, not afterwards:

> **Tools.** `<tool>` `<version>` — SHA-256 checked against the lab baseline manifest
> (`TOOLS.sha256`, generated at the `CLEAN-TOOLS` snapshot), `<YYYY-MM-DD hh:mm>` UTC.
> Examination platform `FOR-WS01`, snapshot `CLEAN-TOOLS`.

> **The wording is graded.** *"Verified against the vendor"* is stronger and false — nobody in this
> lab checked a vendor signature. Writing what you actually did, in the weaker words that are true,
> is criterion 2 in practice.

---

## Section state after `P01`

| # | Section | After this page |
|--:|---|---|
| 1 | Case identification | **complete** |
| 2 | Executive summary | marked *written last* |
| 3 | Authorisation & scope | **complete** |
| 4 | Chain of custody | empty — `T03` |
| 5 | Evidence inventory | empty — `T03` |
| 6 | Tools and method | **one row**, from the lab |
| 7 | Acquisition details | empty — `T06` |
| 8 | Findings | heading + format line |
| 9 | Interpretation | heading + format line, marked *written last* |
| 10 | Limitations | empty — the first real line arrives in `T03` |
| 11 | Conclusions | marked *written last* |
| 12 | Appendices | empty |

**Three of twelve complete or started, on a page with no evidence.** That is the argument for
`D85`: the report is not a thing you begin when the analysis ends.
