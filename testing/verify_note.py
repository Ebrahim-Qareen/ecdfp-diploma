# eCDFP note verification checker (D39). Run from Resources/THM:
#   python3 ../../testing/verify_note.py <note>.md '{"finding":"exact phrase that must appear"}'
# Controls, re-run on any change to CRED: 7/7 leak shapes caught, 0 false positives across all notes.
# NEVER run a copy from /tmp - see D39.
# extra-dict assertions must be copied VERBATIM from the note, INCLUDING markdown emphasis.
# Three false-positive modes seen so far, all in the assertion string and not the note:
#   1. phrase split across a line wrap  -> fixed by the flat/whitespace normalisation below
#   2. case mismatch ('neither' vs 'Neither')            -> room 23, 2026-08-29
#   3. markdown emphasis inside the phrase ('**potentially** contain') -> room 25, 2026-08-29
#   4. blockquote '> ' marker on a wrapped line   -> room 29, 2026-08-29 (now normalised away)
# Always grep the note before changing it in response to a MISSING result.
import re, sys, json
p = sys.argv[1]
extra = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
t = open(p, encoding='utf-8').read()
# `flat` powers the extra-dict assertions only; CRED patterns still run on raw `t`.
# Strip blockquote/continuation markers first, so an assertion spanning a wrapped
# blockquote line matches (FP mode 4, found in room 29).
flat = re.sub(r'\n\s*>\s?', '\n', t)
flat = re.sub(r'\s+', ' ', flat)
fails = []
blocks = re.findall(r'^### 2\.\d+ (.+)$', t, re.M)
boxes = {k: len(re.findall(re.escape(v), t)) for k, v in {
 'is':'- **What it is**','where':'- **Where it lives**','proves':'- **What it proves**',
 'NOT':'- **What it does NOT prove**','parse':'- **How to parse it**',
 'caveat':'- **Anti-forensics / false-positive caveat**'}.items()}
if len(set(boxes.values())) != 1 or list(boxes.values())[0] != len(blocks):
    fails.append("6-box mismatch")
secs = [s for s in range(1,10) if re.search(r'^## %d\. ' % s, t, re.M)]
if len(secs) != 9: fails.append("sections: %s" % secs)
CRED = [
    (r'(?im)^\s*\|?\s*(username|user)\b[^\n]{1,60}\n\s*\|?\s*(password|passwd)\b\s*\S',
     'user/password pair'),
    (r'(?im)^\s*\|?\s*(password|passwd|pwd)\s*[:|=]\s*\S', 'labelled password'),
    (r'(?im)^\s*\|?\s*(password|passwd|pwd)\s+(?=\S*[\d!@#$%^&*_-])(\S{4,})\s*\|?\s*$',
     'space-separated password'),
    (r'(?i)\b(api[_-]?key|secret[_-]?key|access[_-]?token)\s*[:=]\s*\S', 'api key/token'),
    (r'Bearer\s+[A-Za-z0-9._-]{10,}', 'bearer token'),
    (r'(?i)\bkeyMaterial\b\s*[:=>]', 'WLAN pre-shared key'),
    (r'-----BEGIN [A-Z ]*PRIVATE KEY-----', 'private key'),
]
for pat, label in CRED:
    m = re.search(pat, t)
    if m: fails.append("CREDENTIAL LEAK (%s): %r" % (label, m.group(0).strip()[:40]))
for k, v in extra.items():
    if re.sub(r'\s+',' ',v) not in flat: fails.append("MISSING: %s (%r)" % (k, v))
print("ARTIFACTS:", len(blocks)); print("6-BOX:", boxes); print("SECTIONS:", secs)
print("BYTES:", len(t.encode()))
print("=== RESULT ===", "PASS - zero findings" if not fails else "FAIL:\n  " + "\n  ".join(fails))
