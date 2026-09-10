# P04 · Report stage

Two sections advance on this page.

## Section 6 — Tools and method (`T06`, 4 min)

| Field | Where it comes from |
|---|---|
| Tool name and version | the pre-arrival note, confirmed against the binary |
| Commands executed, in order | `Processing_Details.txt`, pasted |
| Start and end time | same file, first and last line |
| Destination media | your serial number, from the pre-arrival note |
| **Known effects on the source** | **you write this — nobody generates it for you** |

**The last row is the one that separates a professional report.** State, before anyone asks, that
the collection created a USBSTOR entry, a prefetch record and a driver load. Volunteering it makes
it *method*. Being caught with it makes it *contamination*.

## Section 4 — Evidence received (`T07`, 4 min)

A memory capture breaks the usual shape of Section 4: **you created the exhibit, and its source no
longer exists in that state.** Three fields carry that:

1. **Acquisition hash, and when it was taken** — SHA-256 on the examiner drive **before power-down**,
   because afterwards there is nothing left to compare against.
2. **Verification is one-way** — state plainly that the source cannot be re-read. A reader who
   assumes a re-image was possible will assume you chose not to take one.
3. **Machine state on arrival** — powered on, session locked, network cable in. This is what
   justifies every ordering decision that follows.

Then repeat the **known effects on the source** line here, against the exhibit itself: this capture
required loading a kernel driver, and the collector's own process is inside the image.

> An examiner who is in the evidence says so in the section that describes the evidence.

## Sections that stay empty

`Section 2` executive summary and `Section 12` conclusions — as always, written last (`P01`).
`Section 9` interpretation gets nothing from this page yet: a memory image with no timeline supports
no interpretation on its own.
