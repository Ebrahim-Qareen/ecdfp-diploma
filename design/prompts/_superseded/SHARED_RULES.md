# SHARED RULES — read this before either session prompt

You are building the HTML teaching page for one session of the **eCDFP digital forensics diploma**
at ITGate Academy. The page is projected in a 4-hour classroom and re-opened by students later.

## 0 · Read these files before writing a single line

| File | Why |
|---|---|
| `design/design_system.md` | **the contract.** Colours, type, components, diagram rules |
| `docs/assets/css/ecdfp.css` | the only stylesheet. Never fork it, never inline CSS |
| `docs/assets/base_template.html` | the skeleton every page starts from |
| `design/topic_map.md` | the topic rows and their minutes. **Scope comes from here only** |
| `design/session_blueprint.md` §3 | the ten delivery rules |
| `docs/session-01/index.html` | a page that already passes both gates — match its markup exactly |

## 1 · The one component that carries the course

Three boxes, and **the border style is the lesson**, not the colour:

| Class | Border | Chip | Means |
|---|---|---|---|
| `.finding` | **solid** | FINDING | what the artifact literally says — artifact named, exact path |
| `.interpretation` | **dashed** | INTERPRETATION | what you reason from findings |
| `.limitation` | **dotted** | CANNOT PROVE | what this evidence cannot show, however read |

Colour alone fails a colour-blind student, a bad projector and a greyscale printout. Never nest
them. Never reuse them for emphasis. Also available: `.caveat` `.lab-box` `.key-takeaway`
`.attacker-view` `.detection-view` `.coc`.

## 2 · Density — the page is a teaching surface, NOT a textbook

**A gate enforces this. Run it before you report done:**
`python3 scripts/density_gate.py docs/session-NN/index.html`

| Check | Limit |
|---|--:|
| average visible words per page | **≤ 180** |
| worst single page | **≤ 250** |
| total visible words | ≤ 4,000 |
| teaching pages with no visual | **0** |
| runs of 4+ consecutive `<p>` | **0** |
| a concept re-explained on a non-owner page | **0** |

**Where the prose goes instead.** Long explanation belongs in
`packages/session-NN/student_guide.md` — the student reads that alone, after class. The page gets
**a visual plus a caption**. If you can delete the diagram and lose nothing, the page is not built.

The previous build of this course failed exactly here: 11,111 words, 462 per page, "hash" written
86 times while "magic bytes" — a 22-minute hands-on block — appeared once. Do not repeat it.

## 3 · Animation — allowed, but only one way (`D51`)

Diagrams **should** animate when the animation shows **a mechanism changing over time**. That is
the one thing a static picture cannot do. Animate: a write being dropped by a blocker, volatile
data draining, a digest scrambling, a header surviving a rename, bytes being overwritten.

**The hard constraints — breaking any of these fails the gate:**

- **Hand-authored inline SVG + SMIL only.** No GIF, no video, no JavaScript, no diagram library.
- **No autoplay. No loop.** Nothing may move while the instructor is talking over the page.
- Every animation sits behind an explicit control: `begin="<controlId>.click"`, and the control is
  `<g class="svg-play" role="button" tabindex="0">` with a visible ▶ Play / Replay label.
- ⚠️ **SMIL cannot interpolate a CSS `var()`.** Animating `fill` to `var(--accent-red)` renders
  **white**. Cross-fade a second shape with `opacity` instead — that keeps the design tokens.
- Everything stays inside the `viewBox`. Arrows never cross label text. `stroke-width` ≥ 1.5,
  text ≥ 12 units. Every `<svg>` gets `role="img"` and a `<title>` as its **first child**.
- Wrap every figure: `<figure class="svg-wrap" role="group" aria-label="SN-FN">…<figcaption>`

## 4 · Every theory block gets a practical within the same block

**Non-negotiable, and it is the point of the rebuild.** No block is theory alone. Each one ends in
one of: a `.gui` panel showing a **real command and its real output**, a 3–5 step micro-task the
student runs at the keyboard, or a "read this and tell me what it proves" artifact.

Order inside a block **never inverts**:
> concept → where it lives → read it manually → read it with a tool → how an attacker abuses it →
> apply it to the case

**Manual before tool, always — and say why**: structure is what lets you adjudicate when two tools
disagree.

## 5 · Type and layout — already decided, do not re-invent (`D53`)

`h1` 3.1 rem · `h2` with a cyan left rule · `--content-max` 1320 px · `--sidebar-w` 240 px ·
kicker rendered as a state pill (use it for `SN-NN · N min`) · `mark` = amber highlight ·
inline `<code>` on a cyan tint · tables as rules, not boxes.

**`.split`** = content beside a narrow sticky visual, collapses under 900 px.
**`.gui`** = a labelled mock window (`.gui-bar` > `.gui-dots` + `.gui-title`, then `.gui-body`
with `.l` lines classed `.p` prompt `.ok` `.no` `.d` dim, then `.gui-cap`). `.gui-row` swaps the
mono body for a two-column field list.

⚠️ **`.gui-title` truncates (`D62`)** — put the identifying part of a filename **first**, the tail
is what gets cut.

**`.gui` is an illustration of real output, never a fake screenshot.** It must never be dressed up
as a capture of a real product.

**No webfonts.** System stacks only — the lab is offline.

**Never invent** a colour, font, spacing value or layout pattern. If the page needs something the
system lacks, that is a `design_system.md` change first, logged in `DECISIONS.md`.

## 6 · Page shape — Tier A, exactly 22 pages

```
1 Cover · 2 How this session works · 3 Objectives · 4 Case hook
5-7 Theory A/B/C · 8 Instructor demo · 9 Lab setup · 10 Guided hands-on · 11 Knowledge check 1
12 BREAK (data-timer="15") · 13-14 Theory D/E · 15 Independent practice
16 Investigation · 17 Knowledge check 2 · 18 Check 2 / summary · 19 Cheat sheet + Print
20 Takeaways · 21 Homework + rubric · 22 Additional practice + references
```

Required on every page set: the break page · **all questions multiple choice** (`D52`) using
`.q.mcq > .opts > li[data-correct][data-why]` + a `.feedback` div · a cheat sheet with
`data-action="print"` · `#taskList` homework + the task-creator modal · prev/next nav + `kbd-hint`
· sidebar entries matching the page count exactly.

## 7 · Question rules (`D60`)

- One question, **one artifact, one answer**; the sequence reads as a narrative.
- **State the answer format** every time — timestamp mask, timezone, units, sector size.
- A stem says **what to find, never why it happened**.
- **Exactly one "cannot be determined" question per session.** This is ours — zero of the 33
  TryHackMe rooms we studied ask one, and it is the cheapest way to teach the limits of evidence.
- Every `li` needs `data-why` — the wrong answers teach as much as the right one.
- Never make an answer a credential or anyone's personal data.

## 8 · The report thread — do not drop it

The fixed report template is taught in **S1** and written in **every** session's closing 15
minutes. Same rubric, four criteria × 25 marks, all six sessions, never changed:
**Integrity · Method · Findings (each tied to a named artifact) · Separation**.

## 9 · Verify before you report done — both gates, and say the numbers

```
python3 scripts/density_gate.py docs/session-NN/index.html      # must print ALL PASS
node testing/render_gate.js docs/session-NN/index.html          # 1400/1100/900/700/480, zero findings
```
Playwright is not installed on the device — run the render gate where it is available.
**Report the actual numbers.** "Looks good" is not a result.

## 10 · Do not

- Do not write a paragraph where a diagram would carry it.
- Do not re-explain something an earlier session owns — name it in one clause and move on.
- Do not introduce a tool the course has not taught by this session (`design/tools_by_session.md`).
- Do not put instructor stage directions ("ask the room", "expect them to struggle") on the page
  or in any student-facing file.
- Do not expand scope. If you need a topic that is not in `topic_map.md`, stop and say so.
- Do not regenerate a whole page for one change — edit the affected `<section>` only.
