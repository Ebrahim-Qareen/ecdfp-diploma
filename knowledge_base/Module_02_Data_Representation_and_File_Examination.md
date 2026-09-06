# Module 02 — Data Representation & File Examination

| | |
|---|---|
| **INE source** | unit 3 — *Data Representation & Files Examination* (247 pp) |
| **Feeds sessions** | `S3` |
| **Source text** | [`_source_text/INE_Unit_03_Data_Representation_Files_Examination.md`](_source_text/INE_Unit_03_Data_Representation_Files_Examination.md) |
| **Instructor delivery** | [`instructor/Session_02_Data_Representation_and_File_Examination.md`](instructor/Session_02_Data_Representation_and_File_Examination.md) |

> Condensed reference, our words, from INE's eCDFP courseware. Not published.
> Page cites `[U3 p128–148]` point into the source-text file, which is OCR — check any exact
> string on the source page before putting it in front of students.

## 0 · What this module is for

After this module a student can open an unknown file in a hex editor, read its first and last
bytes, and say what format it actually is — regardless of what the file is called. They can pull
the metadata out of a JPEG, an OOXML document, a PDF and a PE, and — the part that matters — say
precisely what each field proves and what it only suggests. It sits after acquisition (S1–S2 gave
us a verified image, EVI-SRC01) and before file systems (S3 onward explains why the bytes are
where they are); it is the first session where students touch evidence content rather than
evidence containers. It is also the session that seeds the carry-through case (D19): the lure
document and the payload dropped from it are both examined here, at the byte level, before any
system artefact is read.

## 1 · Core concepts

### Bit, byte, and the units above them
- **Definition** — a bit is one binary digit (0 or 1); a byte is eight bits and is the smallest
  unit an operating system normally addresses in a file.
- **Why it exists** — a computer is an electrical machine with no fingers; it reliably detects
  two states, current present (1) and current absent (0), so everything it stores or sends is
  encoded base 2 `[U3 p7–8]`.
- **Where it shows up** — every offset, length and size field in this course: hex editor offsets,
  PE `SizeOfRawData`, PCAP frame lengths, disk sector counts.
- **Example** — INE's Wireshark frame reads "102 bytes on wire (816 bits)": 102 × 8 = 816
  `[U3 p30]`. INE uses 1 KB = 1024 bytes, 1 GB = 1024 MB throughout `[U3 p9–10]`.
- **Kilobit vs kilobyte** — pronounced alike, different by a factor of eight. Bytes measure stored
  files; bits measure link speed `[U3 p10]`. A student who reports a "600 Kb file" has said
  something different from what they meant.
- **In the case (D19)** — the exfiltration volume in S6 is a byte count off the USB device; the
  beacon interval and throughput in S5 are bit-rate figures. Do not mix them in one table.
`[U3 p7–10]`

### Binary, hexadecimal and the nibble
- **Definition** — hex is base 16 (0–9, A–F). One hex digit encodes exactly four bits, so two hex
  digits are one byte `[U3 p24–26]`.
- **Why it exists** — nobody can read 64 raw bits reliably. Hex compresses binary 4:1 with no
  ambiguity and maps to byte boundaries, which binary-as-text and decimal do not.
- **Where it shows up** — every hex editor pane, every file signature, every PE field value, every
  offset you will ever cite in a report.
- **Example** — `1011 1111 1000` splits into three nibbles and converts group by group `[U3 p25]`;
  converting back is the same table read the other way `[U3 p26]`. INE walks decimal→binary by
  repeated subtraction of powers of two (100 → `1100100`) `[U3 p11–18]` and binary→decimal by
  summing the powers with a 1 above them `[U3 p19–23]`.
- **In the case (D19)** — the header bytes that unmask the renamed staging archive are quoted in
  hex in the report; get students used to writing `FF D8 FF E1`, not `255 216 255 225`.
`[U3 p24–26]`

### Endianness ⚠ not covered by INE unit 3
- **Definition** — the order in which a multi-byte value is stored: little-endian puts the least
  significant byte first, big-endian the most significant.
- **Why it exists** — hardware designers made different choices; x86 and therefore Windows and
  NTFS are little-endian, while many network protocol fields are big-endian ("network byte order").
- **Where it shows up** — the moment a student reads a *value* rather than a *pattern*: PE
  `TimeDateStamp`, section sizes, MFT record fields, FILETIME timestamps.
- **Example** — the bytes `00 10 00 00` in a PEview field are the value `0x00001000`, not
  `0x00100000`. Signatures such as `FF D8` are byte *patterns* and are read left to right — this
  is the distinction students trip over.
- **Why it is here anyway** — the course needs it to read anything in §2's PE tables; unit 3 never
  defines it. Logged as a gap in §7.

### Character encoding — ASCII and what comes after it
- **Definition** — an encoding maps numeric codes to characters; ASCII assigns a code to each
  letter, digit and symbol `[U3 p27]`.
- **Why it exists** — text has to survive as numbers; without an agreed table, bytes are not text.
- **Where it shows up** — the right-hand pane of every hex editor and packet dissector. Bytes with
  no printable ASCII equivalent are rendered as `.` — that dot is a substitution by the tool, not
  a byte in the file `[U3 p31]`.
- **Example** — INE's Wireshark screenshot shows the same payload twice, hex on the left and ASCII
  on the right `[U3 p29–31]`.
- **Caution** — unit 3 stops at ASCII. Windows artefacts are overwhelmingly UTF-16LE, which is why
  a default `strings` run misses half the interesting text in a Windows binary. See §7.
`[U3 p27–32]`

### File extension vs file signature — the central lesson
- **Definition** — the extension is a naming convention the shell uses to pick a handler; the
  signature (magic number) is a byte pattern inside the file that declares its real format.
- **Why it exists** — Windows identifies file type by extension and hands the file to a registered
  reader `[U3 p34]`; Unix-like systems read the magic number instead `[U3 p37, p66]`. Two different
  answers to the same question, and only one of them lives inside the file.
- **Where it shows up** — offset 0 of the file, and in the Linux magic database at
  `/usr/share/file/magic` `[U3 p68]`.
- **Example** — rename a JPEG to `.PDF` and Adobe Reader fails, because the reader cannot parse the
  bytes it was handed `[U3 p35]`. Renaming is a two-second operation `[U3 p36]`, so a keyword search
  for `*.jpg` will not find every JPEG on a disk — which is the whole reason signature analysis
  exists. INE opens the unit with the same point: a PNG can carry a ZIP, a JPEG can wear `.DOC`
  `[U3 p4]`.
- **In the case (D19)** — the collection archive staged before the USB copy carries a
  non-archive extension. Signature analysis is how it surfaces; §4 covers what that does and does
  not establish.
`[U3 p33–38, p65–70]`

### File structure — header, body, trailer
- **Definition** — a file is not a bag of bytes; it is a defined arrangement of components, and the
  arrangement is a property of the *format*, not of the operating system `[U3 p39–40]`.
- **Why it exists** — a reader application has to know where to find the name, the size, the
  content and the error-check data without scanning the whole file `[U3 p41, p66]`.
- **Where it shows up** — a header at the start `[U3 p58]`, a trailer at the end, and often extra
  structural sections in between — INE names the PDF cross-reference table as an example
  `[U3 p61]` (the OCR renders it "KREF"; the correct string is `xref`, confirmed at `[U3 p169]`).
- **Example** — a `.txt` file has no header at all: open one in a hex editor and there is nothing
  but the ASCII content `[U3 p59, p63]`. That is a real result, not a failed examination.
- **Note** — the reader checks the header before opening, which is why a damaged PDF is rejected
  the instant Adobe Reader touches it `[U3 p60]`.
`[U3 p39–41, p57–64]`

### Metadata and its four types
- **Definition** — data that describes other data `[U3 p43]`.
- **Why it exists** — the OS and applications need to open, index, recognise and process files
  without reading their contents `[U3 p45]`.
- **Where it shows up** — INE's three starting places when examining a file: MFT records, the file
  header, and the magic number `[U3 p47]`. It may sit inside the file or in a different file
  entirely, as binary or as text `[U3 p46]`.
- **The four types** — *system* (written by the OS/file system) `[U3 p73]`, *substantive*
  (a record of modifications to a document) `[U3 p71–72]`, *embedded* (written into the file by the
  creating application) `[U3 p95]`, and *external* (kept separately by document-management software
  about the files it manages) `[U3 p72, p91–94]`.
- **Example** — the envelope analogy: sender, recipient and postmark are not part of the letter,
  but they describe it `[U3 p43–44]`.
- **In the case (D19)** — the lure document's embedded properties and the payload's PE metadata are
  both examined in S3; both feed the timeline built in S6.
`[U3 p42–48, p71–98]`

### MAC and Entry Modified
- **Definition** — Modified, Accessed, Created, plus NTFS's fourth value, Entry Modified `[U3 p77]`.
- **Why it exists** — the file system has to track when the content changed, when it was last read
  and when the record itself changed, for its own housekeeping; investigators borrow it.
- **Where it shows up** — MFT attributes; a subset is exposed on the file's General and Details
  property tabs `[U3 p86]`.
- **Example** — Created is when *this* file object came into being, not when the data was authored;
  copy a 2015 file to another disk and the copy's creation date is the date of the copy
  `[U3 p79–80]` (⚠ the OCR sentence mixes 2015 and 2017 — the years are inconsistent, the principle
  is not). Accessed is the most volatile: any touch updates it `[U3 p81]`. Modified changes only on
  content change — altering another attribute does not move it `[U3 p82–83]`, though copying a file
  into a folder can move the *folder's* modified time `[U3 p84]`. Entry Modified says an attribute
  changed but never which one `[U3 p85]`.
- **Discipline** — INE is explicit that the examiner must not alter MAC/EM while examining
  `[U3 p78]`, and that metadata alone will not build a timeline — logs, network traffic and
  application data are needed too `[U3 p90]`.
`[U3 p73–94]`

### What a rename actually changes ⚠ not explained by INE unit 3
- **Definition** — renaming a file rewrites a name string in the directory index and the file's
  `$FILE_NAME` attribute. It does not read, move or rewrite the clusters holding the content.
- **Why it matters** — this is the mechanism behind the whole signature-analysis lesson: the header
  survives a rename because the header is content, and the extension is not.
- **Where it shows up** — the header bytes sit in the file's first data cluster; the name sits in
  the MFT record and the parent directory index.
- **Example** — `photo.jpg` → `report.docx` leaves `FF D8 FF E1` untouched at offset 0.
- **Note** — unit 3 asserts the outcome (`[U3 p36]`) but never explains the mechanism; clusters,
  slack and directory entries belong to the disks and file-systems module. Logged as a gap in §7.

### Data hiding locations
- **Definition** — places a file's content can sit that ordinary browsing does not show.
- **Why it exists** — an experienced suspect will not leave material where a directory listing
  finds it; INE frames it as a cat-and-mouse game with no complete list `[U3 p108–109]`.
- **Where it shows up** — unit 3 covers three: document metadata `[U3 p116–117]`, the Windows
  registry `[U3 p110–114]`, and NTFS alternate data streams `[U3 p118–122]`. It names
  steganography and covert channels in network protocols and explicitly defers them `[U3 p123]`.
- **Example** — a value named plausibly, planted deep in the registry tree, reads as configuration
  to an untrained eye `[U3 p114]`.
- **In the case (D19)** — treat ADS and metadata stashing as hypotheses to test on EVI-SRC01, not
  as facts; both produce famous false positives (see §2).
`[U3 p107–126]`

### Static vs dynamic analysis
- **Definition** — static analysis examines an executable without running it; dynamic analysis runs
  it under observation `[U3 p214–215]`.
- **Why it exists** — running an unknown binary changes the machine and can destroy or fabricate
  evidence; static work is repeatable and safe.
- **Where it shows up** — basic static is header, imports, sections, resources and strings;
  advanced static is disassembly. Basic dynamic is detonation in a VM with monitoring; advanced
  dynamic is a debugger, step by step `[U3 p214–215]`.
- **Scope** — eCDFP teaches basic static analysis only and leaves the rest to malware analysis and
  reverse engineering `[U3 p216]`. Do not let a keen student turn S3 into a malware course.
`[U3 p211–216]`

## 2 · Artifacts

### File header / magic number (file signature)
| | |
|---|---|
| **What it is** | The byte pattern at the start of a file that declares its real format, independent of the file's name. |
| **Where it lives** | Offset `0x00`, typically the first 2–8 bytes. Linux keeps its pattern database at `/usr/share/file/magic` `[U3 p68]`. INE gives JPEG as `FF D8`, usually followed by `FF E0` (JFIF) or `FF E1` (EXIF) `[U3 p143]`; PDF as `%PDF-1.x` between comment markers `[U3 p155]`. The DOCX slide is truncated in the OCR — it reads only "A DOCX file starts with" `[U3 p133]`; the value is the ZIP local-file-header `50 4B 03 04` ⚠ verify against source page. |
| **What it proves** | What format the bytes are actually in, and therefore which parser will read them — and, where it disagrees with the extension, that name and content do not match. |
| **What it does NOT prove** | It does not prove intent, authorship or timing. A mismatch does not identify who renamed the file, when, or whether a human did it at all — downloads, exports and buggy applications all produce wrong extensions, and an extension can also be *absent* rather than wrong. It does not prove the file is complete or valid: a correct header sits happily in front of a truncated or corrupt body. It does not uniquely identify a format either, because whole families share one container — every OOXML document, JAR, APK and ODF file starts `50 4B 03 04`, so "PK" narrows the answer to "some ZIP" and nothing more. And because the header is only a handful of editable bytes, a matching signature does not prove the content is what the signature claims. |
| **How to parse it** | Open at offset 0 in HxD or Hex Workshop `[U3 p62]`; on Linux `file suspect.doc` `[U3 p67]`; TrID for a ranked signature-database match (not an INE tool — see §7). Compare against a signature reference table before quoting a value. |
| **Anti-forensics / false positive** | Headers are trivially editable in any hex editor — INE says so twice about metadata fields generally `[U3 p150, p175]`. A wiped header makes a real document look like garbage; a grafted header makes garbage look like a JPEG. Text files have no header at all `[U3 p59]`, so "no signature found" is a legitimate result and not evidence of tampering. |
`[U3 p33–38, p57–70, p133, p143, p155]`

### File trailer (footer) and data past the end
| | |
|---|---|
| **What it is** | The terminating byte pattern that marks a file's logical end. Most formats have both a header and a trailer `[U3 p61]`. |
| **Where it lives** | End of file. JPEG ends `FF D9` `[U3 p149]`. PDF ends with the trailer dictionary then `%%EOF` `[U3 p171–172]` (the OCR renders it `%EOF` ⚠ verify against source page). INE notes the DOCX tail region carries the `docProps/app.xml` name string `[U3 p134]` (OCR: "app.xnll"). |
| **What it proves** | Where the reader stops parsing. With the header it gives the two boundaries a carving tool needs to cut a file out of raw sectors. |
| **What it does NOT prove** | It does not prove the file ends there on disk. Bytes after the trailer are ignored by the reader but remain present — which is exactly INE's opening example of a PNG carrying a hidden ZIP `[U3 p4]`. It does not prove the file is complete: a carved fragment often has a good header, no footer at all, and a body containing another file's clusters, and it will still open in some viewers. Nor does a missing trailer prove tampering — truncation from a failed copy, a full disk or an interrupted download looks identical to deliberate cutting. |
| **How to parse it** | Jump to end of file in the hex editor; `xxd suspect.jpg \| tail`; compare the byte length of the file against the offset of the trailer to expose appended data. |
| **Anti-forensics / false positive** | Appended archives and polyglot files; a padded file whose extra bytes are harmless slack from the producing application. Absence of a footer is common in legitimate carved output and must not be reported as concealment. |
`[U3 p4, p61, p134, p149, p171–172]`

### MFT record and its attributes
| | |
|---|---|
| **What it is** | The NTFS per-file metadata record. Every file has one or more `[U3 p49]`. |
| **Where it lives** | The `$MFT` system file on the NTFS volume; not visible through Windows Explorer, so a file-system examination tool is required `[U3 p52]`. INE's attribute list: `$STANDARD_INFORMATION` (access mode, timestamps, link count), `$ATTRIBUTE_LIST`, `$FILE_NAME`, `$DATA`, `$OBJECT_ID`, `$REPARSE_POINT`, `$INDEX_ROOT`, `$INDEX_ALLOCATION`, `$BITMAP`, `$VOLUME_INFORMATION`, `$VOLUME_NAME`, and a security descriptor attribute `[U3 p50]` (the OCR garbles the last name ⚠ verify against source page). |
| **What it proves** | That a file with that name, size, timestamp set and cluster allocation existed on that volume — including files that have since been deleted or moved `[U3 p51]`. The record is also the anchor for timeline construction `[U3 p76]`. |
| **What it does NOT prove** | It does not give you content. INE states it directly: system metadata will not help you retrieve the file's data `[U3 p76]`. A surviving record for a deleted file proves the *metadata* survived, not that the clusters still hold the original bytes — they may already be reallocated to something else. It does not prove who created or last touched the file: NTFS records a security descriptor, not an audit trail of actions. And because a single file can carry more than one `$DATA` and more than one `$FILE_NAME`, a record does not prove there is exactly one name or one stream of content. |
| **How to parse it** | Directory Snoop for low-level NTFS and FAT32 examination, including MFT records `[U3 p53–54]`; DiskExplorer for NTFS from Runtime Software `[U3 p55–56]`; The Sleuth Kit `istat` / `fls` for bulk collection `[U3 p89]` (TSK commands are ours — INE names the framework only). |
| **Anti-forensics / false positive** | `$STANDARD_INFORMATION` timestamps are the easiest values on a Windows system to falsify. Hard links and multiple `$FILE_NAME` entries make one object look like several. MFT internals belong to the file-systems module — do not over-teach them here. |
`[U3 p47–56, p76, p89]`

### MAC and Entry Modified timestamps
| | |
|---|---|
| **What it is** | The four time values an investigator cares about: Modified, Accessed, Created, plus Entry Modified on NTFS `[U3 p77]`. |
| **Where it lives** | MFT attributes on NTFS; a subset is surfaced under the file's General tab, with more format-specific fields under Details `[U3 p86]`. |
| **What it proves** | When this file object was created on this volume, when its content last changed, when it was last accessed, and — for EM — when the MFT entry itself was last altered `[U3 p78, p85]`. |
| **What it does NOT prove** | Created does not prove when the data was authored; INE's own example is a file copied to a second disk, where the copy's creation date is the date of the copy, not of the original `[U3 p79–80]`. Accessed does not prove a human opened the file — antivirus scans, search indexers, backup agents and the act of copying all update it `[U3 p81]`, and on modern Windows last-access updating is frequently disabled outright, so an old access time may mean nothing happened *or* that nothing is being recorded. Entry Modified proves an attribute changed but never says which `[U3 p85]`. None of the four prove which user account did anything, and none of them prove the machine's clock was correct. |
| **How to parse it** | Explorer properties for a quick look `[U3 p86]`; Directory Snoop's file filter to list only files whose attributes fall inside a time window `[U3 p87–88]`; TSK `fls -m` piped to `mactime` for a body-file timeline. |
| **Anti-forensics / false positive** | Timestomping. Clock skew, time-zone and DST errors. INE's standing warning that the examiner must not alter MAC/EM during examination `[U3 p78]` — work on the image, never the original. Metadata alone is never a timeline; it needs logs, traffic and application data `[U3 p90]`. |
`[U3 p77–90]`

### Embedded EXIF metadata in a JPEG
| | |
|---|---|
| **What it is** | Metadata the creating application or camera driver writes inside the image file `[U3 p95–96]`. |
| **Where it lives** | In the JPEG's leading application segment, after `FF D8 FF E1` for EXIF (or `FF E0` for JFIF) `[U3 p143, p147]`. INE's samples show a handset make and model with the capture date `[U3 p148]`, and in another file a Photoshop signature marking the editor that produced it `[U3 p145]`. |
| **What it proves** | Exactly what the writing software recorded: make, model, capture date and camera settings, sometimes GPS coordinates, sometimes an editing application's signature. |
| **What it does NOT prove** | It does not prove the named device took the picture, and it certainly does not prove who was holding it — a device model is not a person. It does not prove the timestamp is right, because a camera clock is user-set and routinely wrong or in the wrong time zone. It does not prove the values are original: INE says plainly that these fields are editable with any hex editor `[U3 p150]`. Absence proves as little as presence — social platforms and messengers strip EXIF on upload, so a bare image is not evidence of scrubbing. A Photoshop signature proves the file passed through an editor, not that the image content was faked. |
| **How to parse it** | `exiftool -a -u -G1 image.jpg` (ExifTool appears only in INE's reference list `[U3 p247]`); Ghiro for automated image analysis `[U3 p151]`; a hex editor for the raw segment `[U3 p150]`. |
| **Anti-forensics / false positive** | Metadata scrubbers; deliberate EXIF forgery; a re-save in any editor rewrites or drops fields. EXIF is also itself a hiding place — INE flags data thieves stashing stolen content in metadata fields for later retrieval `[U3 p97]`. |
`[U3 p95–98, p141–153]`

### OOXML document properties (docProps/core.xml and app.xml)
| | |
|---|---|
| **What it is** | The XML metadata parts inside the ZIP container that is a modern `.docx` / `.xlsx` / `.pptx` `[U3 p130, p132]`. |
| **Where it lives** | `docProps/core.xml` — title, subject, creator, keywords, description, lastModifiedBy, revision, `dcterms:created`, `dcterms:modified` `[U3 p136]`. `docProps/app.xml` — Template, Pages, Words, Characters, Lines, Paragraphs, Application, AppVersion, Company, DocSecurity, TotalTime `[U3 p137]`. Open the container in WinZip or WinRAR to see them `[U3 p132]`. |
| **What it proves** | The account names, timestamps, authoring application and version, revision count and content statistics that Office wrote at save time. |
| **What it does NOT prove** | It does not identify a human being. `creator` and `lastModifiedBy` are strings taken from an Office installation's profile — unauthenticated, frequently a shared, default or deliberately blank name, and stored in a plain text file inside a ZIP that anyone can edit and re-zip in under a minute. Matching that string to a suspect is an inference and must be written as one. A revision count of 2 does not prove the document was barely touched, `TotalTime` of `00:00:00` does not prove nobody edited it, and a `Company` value does not prove the document originated at that organisation — it is inherited from the template. |
| **How to parse it** | `unzip -o suspect.docx -d out/` then read `out/docProps/core.xml` and `out/docProps/app.xml`; WinRAR/WinZip for a GUI look `[U3 p132]`; ExifTool reads OOXML properties directly. |
| **Anti-forensics / false positive** | Edit the XML, re-zip, done. Office's own "Inspect Document / Remove Personal Information" strips these fields legitimately, so blank properties are as likely to be corporate policy as concealment. |
`[U3 p126–137]`

### OLE binary document structure (DOC/XLS/PPT) and macros
| | |
|---|---|
| **What it is** | The pre-2007 Microsoft Office binary format. Each of doc, ppt and xls had its own structure, and the structures changed between Office versions; the family is commonly called OLE `[U3 p127]`. |
| **Where it lives** | Streams inside a single binary file: a Mainstream holding the document's main data, headed by the File Information Block (FIB) which carries pointers to other elements; a summary section; and a table stream holding the objects the FIB points at `[U3 p128–129]`. |
| **What it proves** | That the file is a compound-document container, and — from the FIB and stream pointers — which components exist, including embedded objects and macro storage. |
| **What it does NOT prove** | The presence of a macro proves code is present. It does not prove the macro ran, that macros were enabled on the victim host, that the user clicked Enable Content, or that the code is hostile — legitimate business documents carry macros every day. Equally, the absence of a macro does not prove the document was harmless: INE gives the second delivery path explicitly, a specially crafted file that exploits a vulnerability in an Office product with no macro involved `[U3 p138]`. And an OLE structure does not prove the file is old — a `.doc` extension can front RTF or even OOXML and Word will still open it. |
| **How to parse it** | INE teaches hex-level structure only, and pairs an OOXML and a binary document in the lab `[U3 p131]`. Current document triage uses `oleid`, `olevba` and `oledump.py` — none of them appear in unit 3, see §7. |
| **Anti-forensics / false positive** | Obfuscated and auto-executing macro entry points; password-protected VBA projects; the same lure shipped in three container formats so that one signature-based rule misses it. INE claims OOXML is *less* susceptible to exploitation than the old binary formats `[U3 p131]` — that claim needs qualification, see §7. |
`[U3 p126–131, p138]`

### PDF object and stream structure, and the action keywords
| | |
|---|---|
| **What it is** | A PDF is a header, a body of numbered objects, a cross-reference table and a trailer `[U3 p155–172]`. |
| **Where it lives** | Header: `%PDF-1.4` in INE's example, wrapped in comment markers, with non-printable bytes that tell the reader to expect binary `[U3 p155]`. Body: objects between `obj` and `endobj`, identified by object number and generation number, referencing each other `[U3 p156–157]`; streams between `stream` and `endstream` hold large data and are usually compressed `[U3 p159–162]`. Cross-reference table starts with the literal `xref`; each entry is a 10-byte offset, a generation number and an `f`/`n` in-use flag `[U3 p168–170]`. Trailer begins with `trailer`, holds `/Size`, `/Root`, `/Info` and `startxref` inside `<< >>`, and ends `%%EOF` `[U3 p171–172]`; `/Author` and creation date follow the Author tag `[U3 p173–174]`. |
| **What it proves** | What the document is built from, and what it is configured to do when opened. INE's keyword list: `/JavaScript`, `/JS`, `/RichMedia` mean embedded script `[U3 p164]`; `/Action`, `/OpenAction`, `/Named`, `/Launch`, `/AcroForm` mean something is set to execute on open `[U3 p165]`; `/URI` means a remote address is referenced `[U3 p167]`; `/Encrypt` means encrypted content `[U3 p167]`. |
| **What it does NOT prove** | None of those keywords proves malice. `/OpenAction` and `/JavaScript` are everywhere in ordinary forms, portfolios and print scripts; finding one tells you the file has earned decompression and reading, not that it is a dropper. A `/URI` proves an address is written in the file, not that anything ever contacted it — that requires network or host evidence. `/Launch` proves an action object exists, not that the reader would honour it, since modern readers block or prompt on most of these. And a *clean* keyword scan proves little, because streams are compressed `[U3 p161]`: grep across raw bytes will miss what is inside them. |
| **How to parse it** | Hex editor plus stream decompression — INE defers decompression to the lab `[U3 p162]`. Acrobat Reader's Document Properties reads the author fields directly `[U3 p176]`. Current practice: `pdfid.py` for a keyword census then `pdf-parser.py` to pull and decompress objects — neither is in unit 3, see §7. Never open a suspect PDF in a reader on the examination host. |
| **Anti-forensics / false positive** | INE notes the author and date fields are editable with any hex editor `[U3 p175]`. Incremental updates leave several xref sections and trailers, so the last-listed author is not necessarily the only one. Object streams and nested compression hide keywords from naive scanning. |
`[U3 p154–178]`

### PE headers (IMAGE_FILE_HEADER and IMAGE_OPTIONAL_HEADER)
| | |
|---|---|
| **What it is** | The metadata block a compiler prepends to Windows executable code `[U3 p181–182]`. Note that PE means `.exe` *and* `.dll` — a DLL is a PE that simply cannot be launched by double-click `[U3 p189]`. |
| **Where it lives** | After the legacy `IMAGE_DOS_HEADER` and MS-DOS stub, both vestigial `[U3 p220]`. `IMAGE_FILE_HEADER`: Machine (architecture it was compiled for), NumberOfSections, TimeDateStamp, Size of Optional Header, Characteristics `[U3 p221–223]`. `IMAGE_OPTIONAL_HEADER`: Magic, linker version, Size of Code, Address of Entry Point, Base of Code, Image Base, Section and File Alignment, Subsystem (GUI or command line), Number of Data Directories `[U3 p225–226]`. |
| **What it proves** | The declared architecture, section count, entry point, image base and subsystem, and the compile timestamp *as recorded in the file*. |
| **What it does NOT prove** | The TimeDateStamp does not prove when the binary was built. INE makes the point twice: some compilers write a fixed constant regardless of build date `[U3 p201]`, and malware authors deliberately falsify the field to obstruct analysts `[U3 p202, p224]` — so a strange date means the field is untrustworthy, not that the date is interesting. The header does not prove the file ever executed on this host, that it is the file that executed, or who wrote it. A GUI subsystem value does not prove a user saw a window; it is a request to the loader, nothing more. |
| **How to parse it** | PEview, which lays out the headers and sections field by field `[U3 p220–227]`. |
| **Anti-forensics / false positive** | Timestomped TimeDateStamp; copied or forged linker metadata; a DOS stub message replaced to mislead; NumberOfSections inflated by a packer. INE's own use of a fixed-1997 example is itself questionable — see §7. |
`[U3 p179–187, p201–204, p220–226]`

### PE imports and exports
| | |
|---|---|
| **What it is** | The record of which functions the binary borrows from other DLLs (imports) and which it publishes for others (exports) `[U3 p188, p192–195]`. |
| **Where it lives** | Normally in `.rdata`; when a compiler splits them, imports land in `.idata` and exports in `.edata` `[U3 p208]`. |
| **What it proves** | Capability. Which Windows APIs the code is wired to reach, grouped by the DLL that supplies them. INE's worked example: an offline game that imports `WSOCK32.DLL`, which provides socket creation and management, is doing something it has no business doing `[U3 p200]`. |
| **What it does NOT prove** | An import proves a function is resolvable at load time — not that the code path is ever reached. Compilers and runtime libraries pull in imports the author never calls, so an import list is a menu, not a receipt. It proves capability, never intent, and never that the capability was exercised on this machine. Conversely a short or empty import table does not prove the file is harmless: it usually means the sample resolves APIs at runtime or is packed, and INE says exactly that — very little or no output from these tools points at packing `[U3 p245]`. |
| **How to parse it** | Dependency Walker lists the imported DLLs and, per DLL, the functions called; clicking a function opens an MSDN search `[U3 p196–199]`. PEview's import directory shows the same data (Dependency Walker is abandonware — see §7). |
| **Anti-forensics / false positive** | Runtime API resolution via `LoadLibrary`/`GetProcAddress`, API hashing, and packers that rebuild the import table only in memory. Remember that a DLL's code can be run without any importer at all, through `rundll32` with a DLL name and a function name `[U3 p194]` — so "it is only a DLL" is not a defence. |
`[U3 p188–200, p208]`

### PE sections and the packing signal
| | |
|---|---|
| **What it is** | The named segments the PE body is divided into, each holding a different kind of code or data `[U3 p206]`. |
| **Where it lives** | `.text` holds the executable code the CPU runs, and is the primary target for reverse engineering `[U3 p207]`; `.rdata` holds import/export information and read-only data `[U3 p208]`; `.data`; `.rsrc` holds icons, strings, menus and other resources `[U3 p209]`; `.reloc`; some x64 builds add `.pdata` for exception handling `[U3 p210]`. Each `IMAGE_SECTION_HEADER` records the section's Virtual Size (space needed once loaded into memory) and the size of raw data (space taken on disk) `[U3 p227–228]`. |
| **What it proves** | The layout the loader will construct, and a measurable disk-versus-memory discrepancy for each section. Normally the two sizes are equal or close `[U3 p228]`. |
| **What it does NOT prove** | A large gap between virtual size and raw size suggests packing `[U3 p229]` — it does not prove the file is malicious, because commercial software is packed routinely for size and licence protection. Unusual section names prove a non-default toolchain, not hostility. In the other direction, a tidy section table does not prove the sample is unpacked: loaders that decrypt into freshly allocated memory leave the on-disk section headers looking perfectly ordinary. And section layout says nothing at all about whether the binary ever ran. |
| **How to parse it** | PEview, comparing Virtual Size against Size of Raw Data per section `[U3 p227–229]`. |
| **Anti-forensics / false positive** | Packers and protectors; high-entropy blobs parked in `.rsrc` or `.data`; a section flagged executable that should be read-only. Note that INE teaches the size heuristic but gives no entropy measure — see §7. |
`[U3 p203, p206–210, p227–229]`

### PE resources (.rsrc) and VersionInfo
| | |
|---|---|
| **What it is** | The non-code assets a binary carries: icons, menus, dialogs, string tables, manifest and the version block `[U3 p205, p230–242]`. |
| **Where it lives** | The `.rsrc` section, browsable as a tree — Icon, Menu, Dialog, String Table, Accelerators, Icon Group, Manifest, Version Info `[U3 p232–238]`. VersionInfo holds CompanyName, FileDescription, InternalName, LegalCopyright, OriginalFilename, ProductName and ProductVersion `[U3 p242]`. |
| **What it proves** | What the file claims about itself, and what a user would have seen: the icon in Explorer, the window title, the description on the Details tab. |
| **What it does NOT prove** | Provenance. Every one of those strings is editable in Resource Hacker in under a minute, and INE demonstrates precisely that — changing the values and showing the new text appear under the executable's Details tab `[U3 p243–244]`, and changing the dialog layout and string table so the running application looks different `[U3 p237, p239]`. `CompanyName: Microsoft Corporation` is therefore a claim made by the file, not a fact about the file; a copied icon plus a borrowed OriginalFilename is the cheapest disguise in malware. Only a valid code signature turns a claim into evidence, and unit 3 does not cover code signing at all. |
| **How to parse it** | Resource Hacker rather than PEview, which is a poor fit for `.rsrc` `[U3 p230–231]`; Explorer's Details tab for the user's-eye view `[U3 p243]`. |
| **Anti-forensics / false positive** | Resource editing and icon spoofing; a payload stored as a fake resource; legitimate localisation work also rewrites resources heavily, which is what Resource Hacker was built for `[U3 p231]`. |
`[U3 p205, p209, p230–244]`

### Strings in a binary
| | |
|---|---|
| **What it is** | The printable character runs recovered from a file's raw bytes `[U3 p238, p240]`. |
| **Where it lives** | Anywhere — `.rdata`, `.data`, `.rsrc`, or inside a packed blob. INE also applies the technique to documents, listing `strings` as a way to dump text out of a file's metadata `[U3 p117]`. |
| **What it proves** | The literal text the file carries. INE's list of what is worth finding: function names being called, and more importantly hard-coded passwords, domain names and IP addresses `[U3 p241]`. |
| **What it does NOT prove** | A string proves the text is present in the file — nothing more. A domain in `.rdata` does not prove the sample resolved it, connected to it, or that the domain belongs to the attacker; libraries, certificates, compiler debug paths and dead code all contribute strings, and attackers plant decoys deliberately. `This program cannot be run in DOS mode` appears in effectively every PE `[U3 p240]` and proves only that it is a PE. Nor does an empty result mean a clean file: no strings, no imports and no exports together point at a packer `[U3 p245]`. |
| **How to parse it** | `strings -n 6 sample.exe`; add `-e l` for UTF-16LE, which is where most Windows text actually lives (⚠ INE does not mention wide strings — see §7). INE notes `strings` ships with Kali `[U3 p238]`; on Windows use the Sysinternals build. |
| **Anti-forensics / false positive** | Encrypted or encoded configuration; stack-constructed strings; string obfuscation; and planted strings pointing at an innocent third party. |
`[U3 p117, p238–241, p245]`

### Alternate Data Streams (ADS)
| | |
|---|---|
| **What it is** | An additional named `$DATA` attribute attached to an NTFS file — content that is not the file's default content `[U3 p118–119]`. |
| **Where it lives** | NTFS only `[U3 p118]`. Addressed with the colon syntax, `file.txt:hidden.txt`, and created or read from the command line and Notepad `[U3 p120]`. INE's demo leaves the host file showing 0 KB in Explorer while the stream holds text `[U3 p121]`. NTFS introduced the feature for Macintosh file-system compatibility `[U3 p119]`. |
| **What it proves** | That named non-default data is attached to a file, and that the size and listing Explorer shows do not account for it. |
| **What it does NOT prove** | It does not prove a person hid anything. Windows itself writes a `Zone.Identifier` stream onto every file arriving through a browser or mail client, which makes "this file has an ADS" one of the most common false positives in the whole module (⚠ Zone.Identifier is not mentioned by INE — course addition, see §7). It does not prove the stream was ever opened or executed, and it does not identify who wrote it: a stream carries no owner and no timestamps of its own, only the host file's. A large stream on a small file proves storage, not exfiltration. |
| **How to parse it** | Sysinternals `streams.exe`, or ADS Detector `[U3 p122]`; `dir /R` on a live host; TSK against the acquired image, which is the only method that does not touch the evidence. |
| **Anti-forensics / false positive** | ADS does not survive a copy to a file system that lacks it — INE offers moving the file to FAT32 as a way to neutralise ADS-based exfiltration `[U3 p122]`. That is an IT remediation step; applied to evidence it destroys the artifact (see §7). Email and HTTP transfer strip streams too, so their absence on a copy says nothing about the original. |
`[U3 p118–122]`

### Registry key or value used as a hiding place
| | |
|---|---|
| **What it is** | The Windows registry as a store of arbitrary data — a tree of keys, each holding values, each value holding data `[U3 p110, p112]`. |
| **Where it lives** | INE's named example of what runs at startup is `HKLM\software\microsoft\windows\currentversion\run` `[U3 p111]`. Its data-hiding demonstration is an ordinary key holding a value whose data is plain text `[U3 p114]`. Registry is a Windows-only concept; Linux keeps configuration as files under `/etc` `[U3 p115]`. |
| **What it proves** | That a value of that name with that data exists under that key — and, for a Run key, that the system is configured to launch what the data names at logon. |
| **What it does NOT prove** | A Run entry proves configuration, not execution: it does not prove the named program ever ran, ran successfully, still exists at that path, or was reached at all — execution evidence lives in other artefacts (Prefetch, Amcache, event logs) covered in the Windows forensics module. It does not prove who created the value; the registry records a LastWrite time per *key*, not per value, and no per-value owner. Data parked in a value proves storage, not that anyone retrieved it. And a legitimate-looking Run entry is often exactly that — vendors fill these keys by the dozen. |
| **How to parse it** | Regedit on a live system `[U3 p112–113]`; offline hive parsing belongs to the Windows forensics module. Registry values are also reachable with the Windows search tool, which searches content and metadata `[U3 p117]`. |
| **Anti-forensics / false positive** | A well-named value deep in the tree passes for configuration to an inexperienced eye `[U3 p114]`. Value names containing null characters can hide entries from Regedit's own display. Do not build the module's registry teaching here — this is a hiding location, not a registry lesson. |
`[U3 p110–115]`

### Temporary files
| | |
|---|---|
| **What it is** | Files an application or the OS creates intending to delete them again shortly `[U3 p100]`. |
| **Where it lives** | Application-specific paths — INE gives editor autosave/recovery files `[U3 p100]`, browser cache objects from recently visited pages `[U3 p102]`, and the OS's own paging of unused process data out of RAM to disk, which it calls swapping `[U3 p101]`. There is no complete list; read the vendor documentation for whatever application you meet `[U3 p103]`. |
| **What it proves** | That content existed on this machine at some point. Their forensic value is that they can hold metadata, an earlier revision of a document, or an unencrypted copy of something that was later protected `[U3 p105]`. |
| **What it does NOT prove** | A temp file does not prove the final document said the same thing — it is a working copy captured at an arbitrary moment, and may be partial, stale, or from a different editing session entirely. Its timestamps record the application's write, not a human action, so it does not prove when a user did anything. It does not prove the user knew a copy was left behind, and the fact that it survived usually proves only that something crashed `[U3 p104]`, not that anyone chose to keep it. |
| **How to parse it** | Treat it as any other file — signature check, hex editor, ExifTool, unzip. Deleted temp files remain recoverable while their clusters are unallocated and unoverwritten, which is why deleted-file recovery belongs in the evidence hunt `[U3 p106]`. |
| **Anti-forensics / false positive** | Normal cleanup on graceful exit removes them; secure-delete tools target temp paths explicitly. A temp file carved from unallocated space arrives with no reliable file-system metadata at all, so its "when" and "where" are unknown by default. |
`[U3 p99–106]`

## 3 · Tools

| Tool | What it is for | Command / entry point | Output | Caveat |
|---|---|---|---|---|
| HxD | Free hex editor — read bytes, headers, trailers, offsets | Open file, go to offset 0 | Hex pane plus ASCII pane | Not an INE tool; it is what the delivery deck uses. Confirm read-only mode before opening evidence |
| WinHex | Commercial hex and disk editor | GUI | Hex, disk, interpreter panes | Forensic features sit behind the higher licence tier |
| Hex Workshop | INE's chosen hex editor for header work | GUI | Hex plus ASCII | Dated commercial product `[U3 p62–63]` |
| `file` (Linux) | Identify a file by magic number, not extension | `file suspect.doc` | One-line type description | Reads the magic database at `/usr/share/file/magic` `[U3 p67–68]`; it sniffs patterns and can be fooled by a grafted header |
| TrID | Signature-database identification with confidence ranking | `trid suspect.bin` | Ranked format list with percentages | Not in INE — course addition (§7). Percentages are likelihoods, never proof |
| ExifTool | Read embedded metadata in almost any format | `exiftool -a -u -G1 image.jpg` | Grouped tag and value listing | INE lists it in references only `[U3 p247]`. It can also *write* metadata — never run write operations against evidence |
| Ghiro | Automated image forensics, EXIF and GPS | Web interface | Report with EXIF, hashes, GPS | INE's demo tool `[U3 p151]`; project is effectively dormant |
| Directory Snoop | Low-level NTFS and FAT32 examination, MFT records, attribute filter | GUI, File menu for the filter | MFT record view, cluster chain, filtered file list | `[U3 p53–54, p88]`; dated commercial shareware |
| DiskExplorer for NTFS | NTFS attribute examination | GUI | Sector and attribute view | Runtime Software `[U3 p55]` |
| The Sleuth Kit | Bulk metadata collection across a whole file system | `fls`, `istat`, `mactime` | Body file, timeline, per-file metadata | INE names the framework as the time-saving option `[U3 p89]` but gives no commands — these are ours |
| WinZip / WinRAR / `unzip` | Open the OOXML container | `unzip -o suspect.docx -d out/` | `word/`, `docProps/`, `_rels/` tree | `[U3 p132]`; work on a copy, never the evidence file |
| Regedit | View and edit registry keys and values | `regedit` | Live registry tree | `[U3 p112]`; live-system tool. Offline hive parsing belongs to the Windows forensics module |
| Streams.exe (Sysinternals) | List alternate data streams | `streams -s C:\path` | Stream names and sizes | `[U3 p122]` |
| ADS Detector | Scan files for alternate data streams | GUI | Stream listing | `[U3 p122]` |
| `strings` | Pull printable text out of a binary or document | `strings -n 6 sample.exe` | Candidate URLs, paths, function names | `[U3 p117, p238–241]`. INE notes the Kali build; use Sysinternals `strings` on Windows. Add `-e l` for UTF-16 |
| PEview | Browse PE headers and section headers | GUI, tree on the left | Field-by-field header values | `[U3 p220–229]`; still usable, unmaintained |
| Dependency Walker | List imported DLLs and the functions called from each | GUI | Import and export tree, MSDN lookup | `[U3 p196–199]`; abandoned since 2006 and misreports API-set DLLs on modern Windows (§7) |
| Resource Hacker | Browse the `.rsrc` section — icons, menus, dialogs, strings, VersionInfo | GUI | Resource tree with editable values | `[U3 p230–239]`; it edits as readily as it reads — keep read-only discipline |
| VirusTotal | Multi-engine scan and reputation check | Web upload, or search by hash | Detection ratio and engine names | `[U3 p217–219]`. INE's own caveat: evasion is not hard, so experts do not rely on the verdict `[U3 p219]`. Uploading evidence publishes it — search by hash instead |
| Adobe Acrobat Reader | Read PDF document properties | File → Properties `[U3 p176]` | Author, dates, producer | Opening a suspect PDF in a reader is executing it. Use only on a sacrificial VM |
| OpenKM | Example document management system | Web interface | DMS metadata store | `[U3 p91]`; read the product's documentation before collecting from any DMS `[U3 p94]` |

## 4 · Findings vs interpretation — worked from this module

> **FINDING** — `Q3_forecast.docx` on EVI-SRC01 begins with the bytes `FF D8 FF E1` at offset 0
> and ends `FF D9`. Those are JPEG boundary markers `[U3 p143, p149]`; the file does not begin
> `50 4B 03 04` as an OOXML document must.
> **INTERPRETATION** — the file is a JPEG image carrying a document extension, most plausibly
> renamed to make it uninteresting to a directory listing or a keyword sweep.
> **CANNOT PROVE** — that a person renamed it, that the same person put it there, when the rename
> happened, or that the motive was concealment. Extensions are also set wrongly by downloads,
> exports and broken applications. It does not prove the image content is relevant, and it does
> not prove the file is even the whole image — a valid header and footer can bracket a body
> stitched from another file's clusters.

> **FINDING** — `docProps/core.xml` inside the lure document names a creator account and a
> `dcterms:created` value roughly three days before the incident `[U3 p136]`.
> **INTERPRETATION** — the document was most likely produced on an Office installation whose
> profile carried that account name, shortly before it was delivered — consistent with a
> purpose-built lure rather than a recycled corporate file.
> **CANNOT PROVE** — that the named account belongs to any particular person; the field is an
> unauthenticated string in a text file inside a ZIP, editable and re-zippable in a minute. It
> does not prove the document was authored on the victim network, and the timestamp proves what
> some machine's clock said, not what time it was.

> **FINDING** — the dropped executable's `TimeDateStamp` reads a date two years before the
> intrusion; its `.text` section reports a virtual size several times the size of its raw data;
> `strings` returns almost nothing and the import table lists a handful of functions
> `[U3 p223, p229, p245]`.
> **INTERPRETATION** — the sample is packed, and the compile timestamp is not usable as a build
> date; the small import table is a consequence of packing, not of a simple program.
> **CANNOT PROVE** — that the file is malicious, since commercial software is packed too. It does
> not prove the binary ran on this host, does not prove who built it, and — because the timestamp
> is falsifiable and some compilers write a constant `[U3 p201–202]` — does not even prove the
> file is old. It cannot support any statement about the attacker's identity.

> **FINDING** — a file in the user profile has an alternate data stream attached; the host file's
> size in Explorer is unchanged `[U3 p121]`.
> **INTERPRETATION** — worth examining: named non-default data is attached to a file where a
> listing will not show it.
> **CANNOT PROVE** — that anyone hid anything. Windows attaches a `Zone.Identifier` stream to
> every downloaded file automatically, which is the single most likely explanation before the
> stream is read. Even a stream with real content does not prove who wrote it — streams carry no
> owner and no timestamps of their own — nor that it was ever read back.

> **FINDING** — the sample's `.rsrc` VersionInfo block reads `CompanyName: Microsoft Corporation`
> and `OriginalFilename: CALC.EXE`, and the file carries the Windows calculator icon
> `[U3 p242–244]`.
> **INTERPRETATION** — the binary is dressed to pass as a Microsoft system utility; combined with
> its location outside `%SystemRoot%`, that is a masquerade indicator.
> **CANNOT PROVE** — that Microsoft produced it, or that it did not. INE demonstrates rewriting
> exactly these fields with Resource Hacker and shows the forged values appearing on the Details
> tab `[U3 p243–244]`, so the strings are a claim by the file about itself. Only a validated code
> signature settles origin, and that is outside unit 3.

## 5 · Exam-relevant points

- 1 bit = one binary digit; 1 byte = 8 bits; INE uses 1 KB = 1024 bytes and 1 GB = 1024 MB.
  Bytes measure stored files, bits measure connection speed `[U3 p9–10]`.
- One hex digit = 4 bits; two hex digits = one byte `[U3 p25]`.
- In a hex/ASCII dual pane, a `.` in the ASCII column means the byte has no printable ASCII
  equivalent — it is the tool's substitution, not data `[U3 p31]`.
- Windows identifies file type by extension; Linux and Unix use the file signature / magic number
  `[U3 p34, p37, p66]`. Magic database: `/usr/share/file/magic` `[U3 p68]`. Command: `file`.
- Renaming a file does not change its contents, so extension-based searching misses renamed files
  `[U3 p36]`.
- Some files have no header at all — `.txt` is the stock example `[U3 p59, p63]`.
- Most formats have a header *and* a trailer; PDFs add a cross-reference (`xref`) section
  `[U3 p61, p169]`.
- Three starting places for metadata: MFT records, file header, magic number `[U3 p47]`.
- Metadata types: system, substantive, embedded, external `[U3 p71–72]`.
- MAC = Modified, Accessed, Created; NTFS adds Entry Modified, which records when the MFT entry
  last changed and not which attribute changed `[U3 p77, p85]`.
- Copying a file gives the copy a new Created date `[U3 p79–80]`. Accessed is the most volatile
  attribute `[U3 p81]`. Modified moves only on content change `[U3 p82–83]`.
- Metadata alone is not a timeline — logs, network traffic and application data are required
  `[U3 p90]`.
- ADS is NTFS-only, was introduced for Macintosh compatibility, does not change the visible file
  size, is addressed with `file:stream`, and is destroyed by a copy to FAT32 `[U3 p118–122]`.
- JPEG: starts `FF D8`, commonly `FF D8 FF E0` (JFIF) or `FF D8 FF E1` (EXIF), ends `FF D9`; `FF`
  is the section delimiter `[U3 p143, p147, p149]`. JFIF, TIFF and EXIF are different formats that
  share JPEG compression `[U3 p142]`. Extensions include jpg, jpeg, jpe, jfif `[U3 p141]`.
- DOCX is a compressed container of XML and binary parts; metadata lives in `docProps/core.xml`
  (author, last editor, created, modified) and `docProps/app.xml` (words, characters, lines,
  application) `[U3 p132, p135–137]`.
- DOC and the other pre-2007 formats are OLE binary files; the main stream's header is the File
  Information Block `[U3 p127–129]`.
- PDF structure: header with version, body of objects (`obj`/`endobj`) and streams
  (`stream`/`endstream`), `xref` table, trailer with `/Size`, `/Root`, `/Info`, `startxref`,
  ending `%%EOF` `[U3 p155–172]`. Keywords to hunt: `/JavaScript`, `/JS`, `/RichMedia`, `/Action`,
  `/OpenAction`, `/Named`, `/Launch`, `/AcroForm`, `/URI`, `/Encrypt` `[U3 p163–167]`.
- PE files include `.dll` as well as `.exe`; a DLL cannot be launched by double-click but runs via
  `rundll32` with a DLL and function name `[U3 p189, p194]`.
- PE sections: `.text` (code), `.rdata` (import/export and read-only data), `.data`, `.rsrc`
  (resources), `.reloc`; split imports/exports go to `.idata`/`.edata`; x64 may add `.pdata`
  `[U3 p206–210]`.
- Virtual size much larger than raw size, especially for `.text`, suggests packing `[U3 p229]`;
  so does an absence of strings, imports and exports `[U3 p245]`.
- The PE `TimeDateStamp` is the compile time as recorded, is falsified by malware authors, and is
  a fixed constant from some compilers `[U3 p201–202, p223–224]`.
- Static analysis = not running it (basic: header/strings; advanced: disassembly). Dynamic =
  running it (basic: VM with monitoring; advanced: debugger). eCDFP covers basic static only
  `[U3 p214–216]`.
- Temp files persist mainly because of crashes, and may hold earlier or unencrypted versions
  `[U3 p104–105]`.

## 6 · Teaching notes

- **Lead with the failure, not the tool.** Open the session by renaming a JPEG to `.docx` on the
  projector, double-clicking it and letting Word refuse. Then open it in HxD and read `FF D8`.
  The lesson lands in ninety seconds and every later point hangs off it.
- **The mistake to pre-empt, every cohort:** a header/extension mismatch is treated as proof of
  guilty intent. Force the wording. "The signature does not match the extension" is a finding;
  "the user hid this file" is an interpretation that needs corroboration — and §4's first triple
  is the model answer. Mark it in the rubric.
- **Second most common mistake:** treating the header as truth because it is "inside the file".
  Demonstrate the reverse in the same hex editor — change two bytes, watch the icon change, change
  them back. Students who have seen a signature forged stop over-claiming from one.
- **Third:** reading offsets as decimal, or reading a multi-byte value left to right. Endianness is
  not in the INE unit; teach it in five minutes before the PE section or the PEview screenshots
  will not make sense.
- **Twelve-file identification exercise.** Give the set as the lab, not the lecture: identify each
  by header, state the true type, state what the mismatch does and does not establish. Require the
  "does not establish" column — an answer sheet that only names the format scores half. Include at
  least one file with a corrupted header (real type unrecoverable from bytes 0–3) and one text file
  with no header at all, so "no signature" is a result they have practised reporting.
- **Live demo, in this order:** hex editor at offset 0 and at EOF, `file` on the same sample,
  `unzip` a `.docx` and read `core.xml`, `exiftool` on a photo, `strings` on the case payload,
  PEview on its headers and sections. Six tools, one file each, twenty minutes.
- **Leave to homework:** PDF stream decompression, the resource-editing walkthrough, and the
  conversion drills in `[U3 p11–26]` — the arithmetic is a self-study exercise, not lecture time.
- **Handling discipline, said out loud each time:** every examination happens on a copy; hash
  before and after; never "repair" a header on the original. INE's own advice to move a file to
  FAT32 to strip ADS `[U3 p122]` is an IT remediation step — on evidence it is destruction, and
  saying so makes the point about tool intent versus examiner intent better than any slide.
- **Do not let S3 drift into malware analysis.** INE draws the line explicitly `[U3 p216]`; draw it
  in the room too. Basic static only: what the file claims, what it can reach, whether it is packed.
- **Case tie-in.** Use the D19 lure document and the payload it drops as the worked examples all
  session — same two files in the demo, the lab and the report exercise. Students should finish
  able to write two paragraphs that a lawyer could not dismantle.

## 7 · Gaps, cautions and disagreements

**Topics the course needs that unit 3 does not cover (gap rows)**

1. **Endianness.** Never defined anywhere in the unit, yet every PEview field value in
   `[U3 p221–228]` is a little-endian integer. Needed before the PE material.
2. **Unicode, UTF-8 and UTF-16.** The unit stops at ASCII `[U3 p27–28]`. Windows artefacts are
   largely UTF-16LE, which is why a default `strings` run misses most of the interesting text.
3. **Clusters, slack space and what a rename actually touches.** The unit asserts that renaming
   does not change content `[U3 p36]` but never explains why. Belongs to the disks/file-systems
   module; S3 needs one slide of it borrowed.
4. **File carving as a procedure.** Header-plus-footer carving, and tools for it (PhotoRec,
   foremost, scalpel, Autopsy's carving), appear nowhere in unit 3, though the unit teaches every
   ingredient. The delivery deck covers it; the courseware does not.
5. **Signature reference tables and database tools.** The unit promises to "examine some famous
   file headers" `[U3 p62]` but the pages that would carry the table produced no OCR text (see the
   OCR caution below), so there is no signature list in the source. TrID and a maintained
   signature reference (the Gary Kessler file-signature table is what the delivery deck uses) are
   course additions.
6. **Modern document triage tooling.** No `oleid`, `olevba`, `oledump.py`, `pdfid.py` or
   `pdf-parser.py` anywhere. Unit 3 teaches manual hex reading and defers stream decompression to
   an unspecified lab `[U3 p162]`.
7. **Macro and VBA analysis.** Macros get one sentence `[U3 p138]`. No extraction, no
   deobfuscation, no auto-execute entry points — and this is the delivery mechanism in the
   carry-through case, so the gap is load-bearing.
8. **Hash-based identification.** MD5/SHA-256 as a complement to signature identification, and
   known-file filtering against a reference set, are not in this unit (hashing is introduced in the
   acquisition unit). Worth one cross-reference so students do not think signature analysis is the
   only way to identify a file.
9. **Steganography.** Named and explicitly deferred by INE `[U3 p123]`. The delivery lab covers it;
   the courseware does not.
10. **Authenticode / code signing.** Absent. Without it, §2's PE VersionInfo box has no positive
    counterpart — students learn the claim is forgeable but not what would make it evidence.
11. **`Zone.Identifier` and mark-of-the-web.** Not mentioned, despite being the commonest ADS on
    any real Windows system and therefore the commonest false positive for the ADS artifact. Also
    the cleanest available evidence that a file arrived by download.
12. **Entropy as a packing measure.** INE teaches only the virtual-size-versus-raw-size heuristic
    `[U3 p229]`. Entropy is the standard modern indicator and is one line of tooling.
13. **Substantive metadata.** The type is named `[U3 p71–72]` but the contents table jumps from
    `3.4.2.1` System Metadata to `3.4.2.3` Embedded Metadata — section `3.4.2.2` does not exist in
    the courseware. The gap is in the source itself, not the OCR.
14. **NTFS journalling sources** (`$LogFile`, `$UsnJrnl`, `$I30`) as metadata evidence — not here;
    flag as file-systems module material so students do not think the MFT is the whole story.

**Dated or superseded**

- **Hex Workshop** `[U3 p62–63]` — use HxD (free) or WinHex; the delivery deck already uses HxD.
- **Dependency Walker** `[U3 p196–199]` — last released 2006 and unmaintained; on Windows 7 and
  later it misreports API-set (`api-ms-win-*`) DLLs as missing dependencies, which will confuse
  students badly. Use PE-bear, CFF Explorer, pestudio, or the modern "Dependencies" rewrite.
- **Directory Snoop and DiskExplorer for NTFS** `[U3 p53–56]` — dated commercial shareware; TSK,
  Autopsy or FTK Imager cover the same ground and are what students will meet.
- **Ghiro** `[U3 p151]` — effectively dormant; ExifTool covers the same requirement.
- **Screenshots** are Windows XP era (the `calc.exe` walkthrough, `[U3 p231–239]`) and the sample
  document properties are dated 2017 `[U3 p86]`. Say so before showing them.
- **Last-access timestamps.** INE describes Accessed as the most frequently changing attribute
  `[U3 p81]`. On modern Windows, NTFS last-access updates are throttled or disabled by default, so
  the attribute is far less informative than the courseware implies. Teach INE's model, add the
  current behaviour.
- **VirusTotal** `[U3 p217–218]` — the workflow shown is uploading the sample. Uploading evidence
  makes it available to third parties; search by hash first, and treat upload as a documented
  decision, not a default.

**Disagreements with INE — recorded, not silently resolved**

- **Delphi timestamp.** INE says some Delphi compilers "always add 1997 as the date of creation"
  `[U3 p201]`. The widely documented fixed Delphi PE timestamp is 19 June 1992
  (`0x2A425E19`). INE's *point* — that some compilers emit a constant, so a fixed-looking
  timestamp is not a build date — is correct and is what the exam will test. The specific year is
  doubtful; do not put "1997" on a slide as a fact.
- **OOXML being safer.** INE states that open XML formats are "less susceptible to exploitation by
  attackers than the older binary files" `[U3 p131]`. As a parsing statement that is defensible;
  as a security statement it does not survive contact with reality — `.docm` macros, remote
  template injection, relationship and external-object abuse and embedded OLE objects all live in
  OOXML. Teach INE's claim as INE's claim and add the qualification.
- **PDF xref subsection header.** INE's text reads that the first line "indicates the number of
  entries in the table (7 in this case) and the 1 indicates that the objects starts from object
  number 1" `[U3 p170]`. The PDF specification's order is *first object number* then *count*, and
  the sample entry shown (`0000000000 65535 f`) is the free entry for object 0. The OCR may have
  scrambled the sentence — ⚠ verify against source page before teaching the field order.
- **"A renamed JPEG will not open on Windows"** `[U3 p35]`. True of Adobe Reader being handed a
  JPEG. Not true generally: Windows Photos, browsers and many viewers sniff content and will open
  it regardless of extension. The forensic point is unaffected.

**OCR and source cautions**

- Eleven pages produced no extractable text: 3, 42, 57, 65, 99, 107, 146, 154, 158, 160, 212. Most
  are section-divider slides, but **p57 is the opening page of the File Headers section and p65 the
  opening page of the Magic Number section**, and pp154/158/160 sit inside PDF Analysis — so any
  signature table or definition on those pages is simply not in the source text.
- `[U3 p133]` "A DOCX file starts with" is truncated — the signature value did not OCR.
  ⚠ verify against source page before quoting `50 4B 03 04`.
- OCR spelling to correct on sight: "MET records" `[U3 p47]` and "MIT record" `[U3 p49]` are MFT;
  "KREF" `[U3 p61]` is `xref`; "app.xnll" `[U3 p134]` is `app.xml`; "FF EO" `[U3 p143]` is `FF E0`;
  "%EOF" `[U3 p172]` is `%%EOF`; "cashing" `[U3 p102]` is caching; ".rsre" `[U3 p209]` is `.rsrc`.
  The `$SECURITY_DESCRIPTOR` row of the MFT attribute table `[U3 p50]` is unreadable.
- `[U3 p79–80]` the copy example gives an original created in 2015 and a copy created in 2017
  within the same sentence; the years do not line up. The principle stands.
- **Personal data:** the sample OOXML properties `[U3 p136]` and the PDF author example
  `[U3 p174]` contain short account-name strings from INE's own lab, and the delivery deck contains
  a screenshot with a real local user path. None are reproduced here; use `<account-name>` and
  `C:\Users\<user>\...` in all teaching material.
- **Out of scope, named once and skipped:** Linux and macOS file-system forensics, and mobile
  device forensics. Unit 3 touches Linux only as a *tool platform* (`file`, the magic database,
  `strings` on Kali, ELF as a contrast to PE) — that stays in scope; Linux-as-evidence does not.

## 8 · Section index → source pages

| INE § | Section | Pages | Covered in |
|---|---|---|---|
| `3.1` | INTRODUCTION | 2–6 | §0; the PNG-hiding-a-ZIP framing is used in §1 (extension vs signature) and §2 (file trailer) |
| `3.2.1` | BITS, BYTES AND MORE | 7–9 | §1 Bit, byte and the units above them; §5 |
| `3.2.2` | KILOBIT VS KILOBYTE | 10–10 | §1 Bit, byte and the units above them; §5 |
| `3.2.3` | FROM DECIMAL TO BINARY | 11–23 | §1 Binary, hexadecimal and the nibble — worked arithmetic not reproduced (self-study drill, §6) |
| `3.2.4` | HEXADECIMAL | 24–24 | §1 Binary, hexadecimal and the nibble; §5 |
| `3.2.5` | FROM BINARY TO HEX | 25–25 | §1 Binary, hexadecimal and the nibble — conversion table not reproduced (self-study drill) |
| `3.2.6` | FROM HEX TO BINARY | 26–26 | §1 Binary, hexadecimal and the nibble — conversion table not reproduced (self-study drill) |
| `3.2.7` | ASCII | 27–28 | §1 Character encoding; §7 gap 2 |
| `3.2.8` | VIEW DATA IN PRACTICE | 29–32 | §1 Character encoding (hex/ASCII dual pane); §5 |
| `3.3.1` | File Identification | 33–38 | §1 Extension vs signature; §2 File header / magic number; §4 triple 1 |
| `3.3.2` | File Structure | 39–41 | §1 File structure — header, body, trailer |
| `3.4` | Metadata | 42–46 | §1 Metadata and its four types |
| `3.4.1` | Metadata Locations | 47–48 | §1 Metadata and its four types; §2 MFT record |
| `3.4.1.1` | MFT Attributes | 49–56 | §2 MFT record and its attributes; §3 (Directory Snoop, DiskExplorer) |
| `3.4.1.2` | File Headers | 57–64 | §1 File structure; §2 File header / magic number — note pp57 and 65 produced no OCR text (§7) |
| `3.4.1.3` | Magic Number | 65–70 | §1 Extension vs signature; §2 File header / magic number; §3 (`file`) |
| `3.4.2` | Metadata Types | 71–72 | §1 Metadata and its four types; §7 gap 13 (substantive metadata has no section) |
| `3.4.2.1` | System Metadata | 73–94 | §1 MAC and Entry Modified; §2 MAC and Entry Modified timestamps; §2 MFT record |
| `3.4.2.3` | Embedded Metadata | 95–98 | §2 Embedded EXIF metadata; §2 OOXML document properties |
| `3.5` | Temporary Files | 99–106 | §2 Temporary files |
| `3.6` | Data Hiding Locations | 107–126 | §1 Data hiding locations; §2 Alternate Data Streams; §2 Registry key or value used as a hiding place |
| `3.7.1` | DOCX Analysis | 127–140 | §2 OOXML document properties; §2 OLE binary document structure; §4 triple 2 |
| `3.7.2` | JPEG Analysis | 141–153 | §2 Embedded EXIF metadata; §2 File header; §2 File trailer; §4 triple 1 |
| `3.7.3` | PDF Analysis - Malicious obj | 154–178 | §2 PDF object and stream structure |
| `3.7.4` | EXE Analysis | 179–247 | §1 Static vs dynamic analysis; §2 PE headers; §2 PE imports and exports; §2 PE sections; §2 PE resources; §2 Strings in a binary; §4 triples 3 and 5 |
