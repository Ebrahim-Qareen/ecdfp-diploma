#!/usr/bin/env python3
"""D80 ordering gate — verifies design/topic_map.md as WRITTEN.

A failing order does not ship. Run before any page is built.
Usage:  python3 scripts/order_gate.py [design/topic_map.md]
"""
import re, sys

F = sys.argv[1] if len(sys.argv) > 1 else 'design/topic_map.md'
t = open(F, encoding='utf-8').read()

# ---- where each evidence set becomes available (D91: evidence is a prerequisite) ----
EVS_READY = {          # EVS id -> the first topic at which it exists
    # Tier 3, synthesized before the course starts — available from day one
    'EVS-01': 'T01', 'EVS-05': 'T01', 'EVS-07': 'T01', 'EVS-08': 'T01', 'EVS-10': 'T01',
    # Tier 3 synthesized / Tier 2 published corpora, built in the build phase -- available from day one
    'EVS-11': 'T01',   # synthesized FAT/NTFS/carving volumes (make_evs11.py)
    'EVS-12': 'T01',   # published registry corpus (Zimmerman), fetched at a pinned commit
    'EVS-13': 'T01',   # published parser-test corpus (Zimmerman), fetched at a pinned commit
    'EVS-14': 'T01',   # published EVTX-ATTACK-SAMPLES (GPL-3.0), fetched at a pinned commit
    # Tier 1, produced by the lab acquisition run
    'EVS-03': 'T07',   # memory capture, taken in the memory-forensics topic
    'EVS-02': 'T09',   # the disk image, made in the imaging guided lab
    'EVS-04': 'T09',   # the suspect USB image
    'EVS-09': 'T09',   # triage collection
    'EVS-06': 'T09',   # the malicious document, extracted from EVS-02
}
EXAM = {'F': 33, 'T': 27, 'P': 20, 'S': 20}
TOL, RITUAL = 2.0, 90     # D74 tolerance ; six 15-min integrity closes (Preservation)

sec  = t[t.find('## The map'):t.find('## The pages')]
rows = [l for l in sec.split('\n') if l.startswith('| **`T')]

topics, order = {}, []
for l in rows:
    c   = [x.strip() for x in l.split('|')[1:-1]]
    tid = re.search(r'`(T\d\d)`', c[0]).group(1)
    topics[tid] = dict(
        name = c[1], page = c[2].strip('`'), mins = int(c[3]),
        doms = re.findall(r'`([FTPS])`', c[4]),
        pre  = re.findall(r'`(T\d\d)`', c[5]),
        evs  = re.findall(r'`(EVS-\d\d)`', c[6]))
    order.append(tid)
pos = {t_: i for i, t_ in enumerate(order)}

fails, warns = [], []
def chk(label, ok, detail=''):
    print("  %-44s %s%s" % (label, 'PASS' if ok else 'FAIL', ('   -> ' + detail) if detail and not ok else ''))
    if not ok: fails.append(label)

print("D80 ORDERING GATE   %s\n" + "-" * 74 if False else "D80 ORDERING GATE   %s" % F)
print("-" * 74)

# 1 structure
nums = [int(x[1:]) for x in order]
chk("topic ids sequential, no gaps", nums == list(range(1, len(nums) + 1)),
    str([n for n in range(1, (max(nums) if nums else 0) + 1) if n not in nums]))
chk("no duplicate ids", len(set(order)) == len(order))

# 2 prerequisites exist
missing = [(a, p) for a in order for p in topics[a]['pre'] if p not in topics]
chk("every prerequisite exists", not missing, str(missing))

# 3 nothing before its prerequisite
early = [(a, p) for a in order for p in topics[a]['pre'] if p in pos and pos[p] >= pos[a]]
chk("no topic precedes a prerequisite", not early, str(early))

# 4 no cycles
seen, stack, cyc = set(), set(), []
def visit(n):
    if n in stack: cyc.append(n); return
    if n in seen: return
    seen.add(n); stack.add(n)
    for p in topics[n]['pre']:
        if p in topics: visit(p)
    stack.discard(n)
for n in order: visit(n)
chk("no cycles", not cyc, str(cyc))

# 5 reachability — every topic is either a root or depends on something earlier
orphan = [a for a in order[1:] if not topics[a]['pre'] and not any(a in topics[b]['pre'] for b in order)]
chk("no unreachable topic", not orphan, str(orphan))

# 6 evidence is a prerequisite too (D91)
bad_ev = []
for a in order:
    for e in topics[a]['evs']:
        r = EVS_READY.get(e)
        if r is None: bad_ev.append('%s needs %s (acquisition point undeclared)' % (a, e))
        elif pos.get(r, 99) > pos[a]: bad_ev.append('%s needs %s, acquired later in %s' % (a, e, r))
chk("evidence available before the topic that uses it", not bad_ev, ' | '.join(bad_ev))

# 7 budget
tot = sum(topics[a]['mins'] for a in order)
chk("topic minutes total 1140", tot == 1140, str(tot))

# 8 domain reconciliation (D24 as amended by D74)
# per-topic minute split, read from the detail sections — a topic spans domains
LONG = {'Fundamentals': 'F', 'Tools & Techniques': 'T', 'Preservation': 'P', 'Storage': 'S'}
agg = {}
for m in re.finditer(r'domain ([^·\n]+?) · prereq', t):
    for part in m.group(1).split(','):
        mm = re.match(r'\s*(.+?)\s+(\d+) min\s*$', part)
        if mm and mm.group(1).strip() in LONG:
            k = LONG[mm.group(1).strip()]
            agg[k] = agg.get(k, 0) + int(mm.group(2))
agg['P'] = agg.get('P', 0) + RITUAL
grand = tot + RITUAL
worst = max(abs(agg.get(k, 0) / grand * 100 - v) for k, v in EXAM.items())
chk("domain deviation <= %.1f pp (worst %.1f)" % (TOL, worst), worst <= TOL)

# --- informational ---
pp = {}
for a in order: pp[topics[a]['page']] = pp.get(topics[a]['page'], 0) + topics[a]['mins']
print("-" * 74)
print("  %d topics · %d pages · %d min · pages %d-%d (avg %d)"
      % (len(order), len(pp), tot, min(pp.values()), max(pp.values()), sum(pp.values()) / len(pp)))
for k in 'FTPS':
    print("    %s  %4d min  %5.1f %%  (exam %d %%)" % (k, agg.get(k, 0), agg.get(k, 0) / grand * 100, EXAM[k]))
print("-" * 74)
print("  VERDICT:", "PASS — the map may ship" if not fails else "FAIL — %d check(s): %s" % (len(fails), ', '.join(fails)))
sys.exit(0 if not fails else 1)
