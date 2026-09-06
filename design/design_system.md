# design_system.md — eCDFP Diploma

**The visual contract.** Every session page obeys this file. `ecdfp-session-html` enforces it and
may never invent a colour, a font, a spacing value or a layout pattern that is not defined here.

Owned by eCDFP: `docs/assets/css/ecdfp.css` is **ours** (D6). The tokens below are inherited from
the eCIR system so the two sites read as siblings, but the file is a **copy, not a share** — eCDFP
may diverge without breaking eCIR.

**One stylesheet. Never forked per session. Never inlined.**

---

## 1 — Colour tokens

### 1.1 Inherited from eCIR — do not change

```css
--bg-primary:    #0a0e14;   /* page ground */
--bg-secondary:  #10161f;   /* sidebar, header, footer */
--bg-card:       #151c27;   /* cards, callouts, code blocks */
--border:        #232c3a;
--text-primary:  #e6edf3;
--text-secondary:#8b98a9;
--accent-cyan:   #00d9ff;   /* primary accent, links, headings */
--accent-green:  #00ff9d;   /* defender / detection / verified */
--accent-red:    #ff4d5e;   /* attacker / critical / integrity failure */
--accent-amber:  #ffb454;   /* warning / caution / anti-forensics caveat */
```

Students arrive from eCIR carrying these meanings. Do not repurpose them. Green already means
"detection / safe" and red already means "attacker" — a finding must never be green and an
interpretation must never be amber, or the page says the opposite of what it means.

### 1.2 The eCDFP pair — FINDING vs INTERPRETATION

**This is the course in two colours.** D7 makes the distinction the thing eCDFP exists to teach;
D20 criterion 4 grades it; this section makes it visible on every page.

```css
--finding:          #7aa2f7;                  /* FACT — what the artifact says */
--finding-bg:       rgba(122,162,247,0.08);
--interpretation:   #c792ea;                  /* INFERENCE — what it means */
--interpretation-bg:rgba(199,146,234,0.08);
--limitation:       #8b98a9;                  /* what this evidence CANNOT show */
--limitation-bg:    rgba(139,152,169,0.06);
```

**Colour is never the only signal.** Three redundant encodings carry the distinction, so it
survives colour blindness, a bad projector, and a greyscale printout:

| | FINDING | INTERPRETATION | LIMITATION |
|---|---|---|---|
| Hue | blue `#7aa2f7` | violet `#c792ea` | muted grey `#8b98a9` |
| **Left border** | **solid** 3px | **dashed** 3px | **dotted** 3px |
| Chip label | `FINDING` | `INTERPRETATION` | `CANNOT PROVE` |
| Body type | regular | *italic* | regular, `--text-secondary` |

> **Why solid vs dashed.** The border style *is* the lesson: a solid line is something you
> observed, a dashed line is something you reasoned to. A student who cannot distinguish blue from
> violet still reads the page correctly, and the metaphor does the teaching. Never ship one of
> these boxes without its border style — the colour alone is not the component.

### 1.3 Usage rules

- A `.finding` box contains **only** what an artifact literally says, with the artifact named and
  its exact path given. No verbs of inference: no "suggests", "indicates", "was likely".
- An `.interpretation` box contains the reasoning, and must reference at least one finding.
- Never nest one inside the other. Never use either for decoration or emphasis.
- Every investigation page carries at least one `.limitation`. Part 8 requires that at least one
  case question has the correct answer *"this artifact cannot prove that."*

---

## 2 — Typography

```css
--font-body: 'Inter', 'Segoe UI', system-ui, sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', ui-monospace, monospace;
```

Fonts are **system-stack only** — no webfont is fetched. The lab is offline (Part 6) and a page
that waits on `fonts.googleapis.com` renders unstyled in a classroom with no internet.

**Revised 2026-08-30 (`D53`) — the scale below is current; the previous one is kept in the row for
comparison.**

| Element | Size | Weight |
|---|---|---|
| Page title `h1` | `clamp(2rem, 1.4rem + 2.4vw, 3.1rem)` · was `…2.1rem` | 700 |
| Section `h2` | `clamp(1.35rem, 1.1rem + 1vw, 1.9rem)` · was `…1.45rem` · **cyan left rule, 4px** | 650 |
| Sub `h3` | `1.22rem` · was `1.05rem` | 650 |
| Body | `clamp(.94rem, .9rem + .18vw, 1rem)` · line-height 1.65 | 400 |
| Mono / code | `.88em` | 400 |
| Chip / kicker | `.7rem`, uppercase, letter-spacing `.08em` | 600 |

Keep text density low — these pages are projected and talked over, not read silently.
Short paragraphs, bullets, and a code block for every command or artifact path.

---

## 3 — Page model

### 3.1 Anatomy

```
header        ITGate mark · session number and title · progress "3 / 6"
page-layout   ├─ sidebar   numbered page list (the only nav index)
              └─ main      exactly one .page visible at a time
footer        prev / next · kbd-hint · page counter
```

One document per session: `docs/session-NN/index.html`, `<body data-session="sNN">`.
Every page is a `<section class="page" id="pN">`. `session.js` shows one and hides the rest.

### 3.2 The two official shapes

**Tier A — concept session (~22 pages).** S1, S2, S3, S6.

```
1 Cover · 2 How this session works · 3 Objectives · 4 Case hook
5-7 Theory A/B/C · 8 Instructor demo · 9 Lab setup · 10 Guided hands-on · 11 Knowledge check 1
12 BREAK (data-timer="15") · 13-14 Theory D/E · 15 Independent practice
16 Investigation / case file · 17 Knowledge check 2 · 18 Summary + cheat sheet · 19 Takeaways
20 Homework + report · 21 Additional practice · 22 References
```

**Tier B — catalogue session (chapters of 8-15 micro-pages).** S4, S5.
Many artifacts, each small and uniform, **every one on the 6-box template (R10)**. The closing
blocked hour (D15) is the **last chapter run as one continuous investigation**, not more
micro-pages.

**Both shapes must carry:** the break page · mixed `.q.mcq` + `<details>` reveal questions · a
cheat sheet with a Print button · `#taskList` homework + the task-creator modal · prev/next nav
and `kbd-hint` · and a recap that maps to the previous session's takeaways.

### 3.3 Session rhythm (D15/D23)

130 min integrated · 60 min blocked investigation · 15 min hash-verify and chain-of-custody
close · 15 min break = **220**. The break page is page 12 in Tier A and closes the third chapter
in Tier B.

---

## 4 — Components

| Class | Border | Meaning |
|---|---|---|
| `.finding` | solid `--finding` | fact stated by an artifact |
| `.interpretation` | dashed `--interpretation` | reasoning from findings |
| `.limitation` | dotted `--limitation` | what the evidence cannot show |
| `.attacker-view` | solid `--accent-red` | how an attacker abuses this |
| `.detection-view` | solid `--accent-green` | what the analyst looks for |
| `.lab-box` | solid `--accent-cyan` | hands-on pointer |
| `.key-takeaway` | solid `--accent-amber` | summary point |
| `.caveat` | solid `--accent-amber` | **required** anti-forensics / false-positive caveat (R10) |
| `.coc` | solid `--accent-green` | chain-of-custody line — who · what · when · from where · hash · where stored |

### 4.1 The 6-box artifact template (R10)

`.artifact` renders exactly six labelled cells, in this order, every time:

```
what it is · where it lives (exact path) · what it proves
what it does NOT prove · how to parse it (tool + command) · one anti-forensics caveat
```

A `.artifact` with fewer than six cells is a defect, not a shorthand. `ecdfp-session-html`
must refuse to emit one.

### 4.2 Questions

- `.q.mcq` — radio options, one `[data-correct]`, immediate feedback, no score kept.
  Contract: `.q.mcq > .opts > li[data-correct][data-why]` containing `input[type=radio]`, plus a
  `.feedback` div. `quiz.js` reads exactly that.
- `<details class="q reveal">` — free-recall, answer hidden behind the summary.

> ⚠️ **Superseded by `D52` (2026-08-30): every knowledge check and quiz question is multiple
> choice.** The mixed-format rule below is kept for the record, not applied.
> ~~Every knowledge-check page mixes both. Never one type alone.~~
>
> **What the change costs, stated so it is not forgotten:** MCQ tests *recognition*; free recall
> tests *production*. Writing a clean finding is a producing skill, so it now has to be produced in
> `student_activity.md` and in the graded report — nowhere else in the session does a student write
> one unprompted.

### 4.3 Interactive diagram panels

`[data-node]` in an SVG or a flow list toggles the `[data-detail]` whose value matches.
**Exactly one `data-detail` per `data-node`.** The Part 9 gate asserts the pairing and fails on
a duplicate or an orphan.

---

### 4.4 `.split` — content beside a small visual (`D53`)

```
.split  →  [ content, 1fr ] [ visual, 330px, sticky ]
```

Collapses to one column under 900 px, and the sticky is released with it. Both children get
`min-width: 0` so a wide table inside the left column scrolls in its own wrapper.

### 4.5 `.gui` — a labelled mock window, never a screenshot (`D53`)

```
.gui > .gui-bar  ( .gui-dots + .gui-title )
     > .gui-body ( .l lines, classed .p prompt · .ok · .no · .d dim )
.gui-cap         the caption underneath
```

`.gui-row` swaps the mono body for a two-column field list — a form rather than a terminal.

**The rule that makes this safe:** a `.gui` renders a command and its **real** output as styled
text, and its caption says so. It is an illustration, and it must never be dressed up as a capture
of a real product. Anything that would be mistaken for a screenshot of a real interface is a
screenshot, and screenshots are taken on `FOR-WS01` (Part 7) or not used.

**Why it earns its place:** it weighs nothing, it is sharp on a projector, it reads correctly in the
dark theme, and it exists before the screenshots do — `S1-06` shows the real `sha256sum -c` output
(3 `OK`, 1 `FAILED`) with no capture in the repo at all.

---

## 5 — Diagram rules

- Hand-authored **inline SVG** only. No image files for diagrams, no diagram libraries.
- Everything inside the `viewBox` — no element or text may extend past it.
- **Arrows never cross label text.** Route around, or move the label.
- `stroke-width` ≥ 1.5 at the rendered size; text ≥ 12 units in viewBox space.
- Colours come from the tokens only, via `fill="var(--...)"`.
- Every diagram gets `role="img"` and a `<title>` as its first child.
- **Animation is allowed only under `D51`:** it must show a mechanism over time, and it must sit
  behind an explicit play/replay control — SMIL `begin="<id>.click"`, no autoplay, no loop, no
  JavaScript, no GIF. Give the control `class="svg-play" role="button" tabindex="0"`.
  ⚠️ SMIL cannot interpolate a CSS `var()`; cross-fade a second shape rather than animating `fill`.
- Wrap in `.svg-wrap` so a wide diagram scrolls inside its own container instead of widening
  the page.

---

## 6 — Load-bearing CSS — do not delete

```css
.page-layout > * { min-width: 0; }
```

Without it, one wide nested table forces the whole page wider than the viewport instead of
scrolling inside its own wrapper. This has already cost the project once. It is asserted by the
Part 9 gate at all five widths.

Everything that can be wide gets its own scroll container, never the document:
`.table-wrap`, `.svg-wrap`, `pre` — all `overflow-x: auto`.

```css
html, body { overflow-x: hidden; }   /* the backstop, not the fix */
```

---

## 7 — Responsive

| Width | Layout |
|---|---|
| ≥ 1100 px | sidebar **240 px** + main, content max **1320 px** (`D53`; was 260 / 1000) |
| 900–1099 px | sidebar 210 px + main |
| < 900 px | sidebar collapses above main, horizontal scroll strip |
| < 640 px | single column, footer nav stacks, chips wrap |

Gate widths: **1400 / 1100 / 900 / 700 / 480** for session pages, and **1920 / 1400 / 1100 / 900 /
700 / 480** for hub pages. 1920 is not optional on the hub: the container cap is 1680, so any rule
that cancels it is invisible at every narrower width — which is how it reached the browser twice.

---

## 8 — Rules for `ecdfp-session-html`

1. Start from `docs/assets/base_template.html`. Never author a page from scratch.
2. Never invent a colour, font, spacing value or layout pattern.
3. Never inline CSS or JS. Never fork the stylesheet per session.
4. Edit the affected `<section>` only — never regenerate a whole page for one change.
5. Look only, never content. Content comes from the approved outline and the package.
6. No light mode. Dark theme only.
7. Animations only on section entrance. Nothing decorative, nothing looping.
8. Every command, path and artifact name goes in `<code>` or `<pre><code>`.
9. Student-facing pages carry **zero** instructor stage directions (Part 11, Part 9 scan).

---

## 9 — The platform layer (D45 · D46)

The public site has **two layers on one stylesheet**. Section 14 of `ecdfp.css` is the hub layer;
everything above it is the session layer. A hub page never uses `.page-layout`, `.sidebar` or
`.page`, and **loads no JavaScript at all**.

### 9.1 Page anatomy — identical on every hub page

```
topbar     ITGate mark · course sub-label · Sessions Roadmap Lab Evidence Resources About
band       eyebrow · two-line h1 with one accent span · lede · stat row
main       .wrap .section (+ .hub-main on reading pages - full width, prose capped)
footer     one line + the reference line
```

This is the CEH and eCIR skeleton, region for region (D46). Do not invent a new region.

### 9.2 The pages

| Path | What it is |
|---|---|
| `index.html` | the home: hero, the legend, six session cards + the review card, tile hubs, about |
| `roadmap.html` | `topic_map.md` published — anchored `#s1`…`#s6`, plus domain balance and the D25 edges |
| `session-NN/brief.html` | the session syllabus (D48). `session-NN/index.html` is the Phase 4 teaching page |
| `lab/index.html` | topology, the three VMs, host requirements, `#before`, `#snapshots` |
| `cases/index.html` | the six investigations and the carry-through incident |
| `resources/evidence.html` | policy · the pre-class hash ritual · `EVS-*` · sourcing tiers · chain of custody |
| `resources/report.html` | the D20 rubric, criterion 4 worked, the template |
| `resources/references.html` | INE module map · exam domains · corpora · tool notes |

Unbuilt hubs (`cheatsheets/`, `review/`, `resources/labs.html`, `resources/glossary.html`,
`lab/setup.html`) appear as **non-link `<span class="tile">`**, dashed and dimmed (D30).

### 9.3 Components the hub layer adds

`.wrap` `.topbar` `.hb` `.topnav` `.band` `.eyebrow` `.stats/.stat` `.sec-desc` `.grid` `.card`
`.snum` `.chips` `.tag` `.status` `.hands-track/.hands-fill/.hands-label` `.tiles` `.tile`
`.note` `.hub-main` `.anchor-row` `.s-block` `.meta-row` `.site-footer`.

- **Card colour is state only** (D47): `.card.live` gets the cyan rule, everything else the border grey.
- **`.hands-*` is a meter, not a chart**: one cyan fill on a neutral track, and it is **always**
  directly labelled with the raw minutes as well as the percentage. Never two coloured segments.
- **`.note`** is the hub-only state banner (“the teaching pages publish in Phase 4”). It is grey by
  design — it is not a caveat, not a finding, and never appears on a session page.
- The finding/interpretation/limitation components are allowed on **four hub pages only** (D45), and
  always as the real component: chip label, border style, no nesting.

### 9.4 Rules

1. Never upper-case the course name. `text-transform: uppercase` anywhere near “eCDFP” turns it into
   “ECDFP” — the lower-case `e` is the brand.
2. `.section` and `.section-sm` set **`padding-block` only**. A `padding` shorthand there silently
   kills `.wrap`'s horizontal padding and the text lands on the screen edge at 480 px.
3. Every hub table lives in `.table-wrap` and carries `min-width: 600px`, so it scrolls in its own
   container instead of squeezing an ID column into four lines.
4. **One container, every region.** `--hub-max` (1680 px) on `.wrap` is the only width in the hub
   layer, and **nothing else may set `max-width`** - not `.hub-main`, not a section. Prose alone is
   capped, at `96ch`. Why it is a rule and not a preference: `.hub-main { max-width: none }` sits
   later in the file than `.wrap`, so it silently cancelled the container - the hero stayed inset at
   145 px while the table below it ran from 33 px to the window edge, and the page read as broken.
   Tables, card grids and diagrams fill the container; the reading column never has 500 px of dead
   space either side.
5. **Hub diagrams are full-width responsive SVG.** No `width`/`height` attributes; keep
   `preserveAspectRatio="xMidYMid meet"`; the CSS gives them `width: 100%` and
   `min-width: 780px` inside `.svg-wrap`, so they scale *up* with the page and scroll on a phone
   instead of shrinking their labels. Draw the `viewBox` wide - 1500-1600 units - and size text in
   viewBox units accordingly (15-23, not 11-13). A seven-step flow is **one row**, not two: the
   two-row version needed a wrap connector, and a connector that has to travel back across the whole
   diagram is a sign the layout is wrong.
6. Grids use `auto-fit`, never `auto-fill` - `auto-fill` leaves dead tracks when a section has fewer
   tiles than the row can hold. Tile minimum is 236 px so six tiles land in one row at full width;
   card minimum is 350 px, which gives four session cards across.
7. **Tables are rules, not a grid of boxes.** `.table-wrap` is a rounded, bordered panel; the table
   inside uses `border-collapse: separate`, no vertical borders, a hairline under each row, a mono
   uppercase header on `--bg-secondary`, and a row hover.
   **Column widths are declared per table, never inferred.** The table is `table-layout: fixed` and
   every table emits a `<colgroup>` whose widths its generator supplies. A blanket CSS rule cannot
   know which column carries the prose: `td:last-child { width: 1% }` reads correctly on a
   three-column table and crushes a two-column one, which is exactly how the report rubric shipped
   with its whole right-hand column squeezed into a ribbon.
8. **Diagrams sit in the same panel treatment** - `.svg-wrap` gets the border, radius and padding, so
   a figure reads as a deliberate object rather than loose artwork on the page background.
9. Depth is one shared token, `--lift` (an inset top highlight plus a soft drop shadow), used by
   cards, tiles, stat blocks, tables and figure panels. Hover raises 3 px and turns the border cyan.
   Nothing else glows, pulses or animates.
5. Never link to a page that does not exist (D30), and never claim a session is published.

