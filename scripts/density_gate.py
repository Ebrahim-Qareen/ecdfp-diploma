#!/usr/bin/env python3
"""D61 visual-density gate + D78 bilingual checks.
Usage: density_gate.py docs/page-NN/index.html

D78: the Arabic layer is EXCLUDED from every word count. It restates; it does not
add concepts, so counting it would fail a page for a feature we required. Two
checks replace what that exclusion gives up (both below): every teaching block
carries its Arabic, and no Arabic block runs far longer than its English.
"""
import re,sys
f=sys.argv[1] if len(sys.argv)>1 else "docs/page-01/index.html"
h=open(f,encoding="utf-8").read()
body=re.sub(r"(?s)<script.*?</script>|<style.*?</style>","",h)

AR=re.compile(r'(?s)<span class="ar">.*?</span>')
def strip_ar(x):
    """Remove the Arabic layer. Nested tags inside .ar are shallow (b/i/code), so a
       non-greedy match to the first </span> would stop early -- balance instead."""
    out=[];i=0
    while True:
        m=re.search(r'<(?:span|p|div) class="ar">',x[i:])
        if not m: out.append(x[i:]); break
        st=i+m.start(); out.append(x[i:st]); j=st+len(m.group(0)); depth=1
        while depth and j<len(x):
            nx=re.search(r'<span\b|</span>',x[j:])
            if not nx: j=len(x); break
            j+=nx.end(); depth += 1 if nx.group(0)!='</span>' else -1
        i=j
    return "".join(out)

# An <svg> is a PICTURE. Its <text> labels are parts of a drawing, not prose --
# count them and every well-labelled diagram reads as a wall of text, which
# pushes the author toward worse diagrams. The gate must not fight D94.
SVG=re.compile(r'(?s)<svg\b.*?</svg>')
SIMOPEN=re.compile(r'<div class="(?:wu|simscreen)\b[^"]*"[^>]*>')
def strip_sim(x):
    """Drop .wu / .simscreen subtrees. A SIMSCREEN is a recreated Windows screen
       (D95): its Explorer rows, menu items and terminal output are PIXELS, not
       prose. Counting them makes a lab screen look like a wall of text and asks
       for an Arabic line under a dialog's own body copy.

       Balanced scan, not regex peeling. Peeling a div tree with a regex loses
       its footing the moment the markup is not perfectly matched, and it took
       two whole <section>s with it -- silently, since the only symptom was a
       structural count that had nothing to do with SIMSCREENs."""
    out=[];i=0
    while True:
        m=SIMOPEN.search(x,i)
        if not m: out.append(x[i:]); break
        out.append(x[i:m.start()]); j=m.end(); depth=1
        while depth and j<len(x):
            nx=re.compile(r'<div\b|</div>').search(x,j)
            if not nx: j=len(x); break
            j=nx.end(); depth += 1 if nx.group(0)!='</div>' else -1
        i=j
    return "".join(out)

def collapse_reveal(x):
    """A .cmp figure (D94 parallel-rows + spotlight) REVEALS one row at a time.
       Summing its rows measures a wall the student never sees; what is on
       screen at once is the heaviest single row. Same principle as strip_sim:
       count what is displayed, not what exists in the file."""
    def one(m):
        rows=re.findall(r'(?s)<div class="cmp-row">.*?(?=<div class="cmp-row">|$)',m.group(1))
        if not rows: return m.group(0)
        wc=lambda r: len(re.sub(r"\s+"," ",re.sub(r"(?s)<[^>]+>"," ",r)).split())
        return '<div class="cmp-rows">'+max(rows,key=wc)+'</div>'
    x=re.sub(r'(?s)<div class="cmp-rows">(.*?)</div>\s*(?=<div class="cmp-cap">|</figure>)',one,x)
    def cap(m):
        its=re.findall(r'(?s)<i>.*?</i>',m.group(1))
        if not its: return m.group(0)
        wc=lambda r: len(re.sub(r"\s+"," ",re.sub(r"(?s)<[^>]+>"," ",r)).split())
        return '<div class="cmp-cap">'+max(its,key=wc)+'</div>'
    return re.sub(r'(?s)<div class="cmp-cap">(.*?)</div>',cap,x)

body_en=SVG.sub('', collapse_reveal(strip_sim(strip_ar(body))))
secs=re.split(r'(?s)(?=<section class="page")',body_en)[1:]
# RAW sections: anything structural or visual is counted on the real document.
# A SIMSCREEN is stripped from the PROSE view only -- strip it from the visual
# scan too and the one screen that is nothing but a picture reports "no visual".
secs_raw=re.split(r'(?s)(?=<section class="page")',body)[1:]
RAW={ (re.search(r'id="(p\d+)"',x) or [None,"?"])[1]: x for x in secs_raw }
secs_full=re.split(r'(?s)(?=<section class="page")',SVG.sub('',strip_sim(body)))[1:]
# A "visual" is anything that is not a wall of prose. The list is the components
# the course actually ships (D94 patterns + D95 SIMSCREEN + D27 boxes), not the
# session-era list -- a topic page carries different furniture than a session did.
VIZ=(r'<svg|<table|<pre|class="gui|class="artifact|class="q mcq'
     r'|class="split|class="steps|class="chips|class="cheat|key-takeaway'
     r'|class="simscreen|class="wu\b|class="cmp\b|class="cmp-row'
     r'|class="finding|class="interpretation|class="limitation'
     r'|class="note|class="eg\b|class="warn|class="snaptree|wu-term')
rows=[];fails=[]
for s in secs:
    pid=re.search(r'id="(p\d+)"',s); pid=pid.group(1) if pid else "?"
    txt=re.sub(r"(?s)<[^>]+>"," ",s); w=len(re.sub(r"\s+"," ",txt).split())
    raw=RAW.get(pid,s)
    # D119: a part divider is a full-screen title card. It IS the visual; asking
    # it for a figure would mean putting a diagram on a signpost.
    viz=1 if 'class="page divider"' in raw else len(re.findall(VIZ,raw))
    # A "wall of prose" is 4+ paragraphs that are SIBLINGS at the top of the
    # screen. Nested containers must come out first: `<p[ >].*?</p>` is happy to
    # jump over a <div class="finding"> and report three encoded boxes as a wall.
    flat=s
    for _ in range(6):
        flat2=re.sub(r'(?s)<div\b[^>]*>((?:(?!<div\b|</div>).)*)</div>','',flat)
        if flat2==flat: break
        flat=flat2
    runs=re.findall(r"(?:<p[ >][^<]*(?:<(?!/?p\b)[^>]*>[^<]*)*</p>\s*){4,}",flat,re.S)
    rows.append((pid,w,viz,len(runs)))
tot=sum(r[1] for r in rows); n=len(rows); avg=tot//n; worst=max(r[1] for r in rows)
noviz=[r[0] for r in rows if r[2]==0]; pruns=[r[0] for r in rows if r[3]>0]
print("%-34s %s" % ("D61 GATE", f))
print("-"*72)
def chk(label,val,limit,ok):
    print("  %-38s %-12s limit %-10s %s" % (label,val,limit,"PASS" if ok else "FAIL"))
    if not ok: fails.append(label)
chk("total visible words",tot,"<= 4000",tot<=4000)
chk("average words / page",avg,"<= 180",avg<=180)
chk("worst single page",worst,"<= 250",worst<=250)
chk("pages with NO visual",len(noviz) or "0","0",not noviz)
chk("pages with 4+ consecutive <p>",len(pruns) or "0","0",not pruns)
if noviz: print("      -> %s" % ", ".join(noviz))
if pruns: print("      -> %s" % ", ".join(pruns))
print()
print("  concept ownership (D58: taught on ONE page, only used elsewhere)")
print("  [advisory on a single file -- ownership is a CROSS-PAGE property, and a")
print("   topic page legitimately USES words another topic owns. Run the course-")
print("   wide check in Part 9 once more than one page exists.]")
for c in ["hash","chain of custody","interpretation","write block","finding"]:
    per=[]
    for s in secs:
        pid=re.search(r'id="(p\d+)"',s).group(1)
        tx=re.sub(r"\s+"," ",re.sub(r"(?s)<[^>]+>"," ",s)).lower()
        if tx.count(c): per.append((pid,tx.count(c)))
    if not per: continue
    owner=max(per,key=lambda x:x[1])
    others=[p for p in per if p[0]!=owner[0] and p[1]>3]
    ok=not others
    print("    %-18s owner %-4s x%-2d   %d other pages   %s%s"
          % (c,owner[0],owner[1],len(per)-1,"PASS" if ok else "FAIL",
             "" if ok else "  -> re-explained on "+", ".join("%s x%d"%o for o in others)))
    # advisory only -- see the note above
    # if not ok: fails.append("ownership:"+c)
print()
print("  structure")
# D119: dividers are class="page divider", and a part row in the sidebar carries a class
pages=len(re.findall(r'<section class="page[ "]',body))
nav=len(re.findall(r'<li[^>]*><a href="#p\d+"',body))
for lbl,cond in [("pages == sidebar entries","%d/%d"%(pages,nav)),]:
    print("    %-22s %s   %s" % (lbl,cond,"PASS" if pages==nav else "FAIL"))
if pages!=nav: fails.append("sidebar")
svg=len(re.findall(r"<svg",body)); ttl=len(re.findall(r"<title id=",body))
print("    %-22s %d svg / %d <title>   %s" % ("every svg titled",svg,ttl,"PASS" if svg==ttl else "FAIL"))
if svg!=ttl: fails.append("svg-title")
mcq=len(re.findall(r'class="q mcq"',body)); fb=len(re.findall(r'class="feedback"',body))
cor=len(re.findall(r'data-correct',body))
print("    %-22s %d mcq / %d feedback / %d correct   %s" % ("mcq contract",mcq,fb,cor,"PASS" if mcq==fb==cor else "FAIL"))
if not(mcq==fb==cor): fails.append("mcq")
# D101: the unit is a TOPIC page, not a session. The break and the print button
# belong to the session (the instructor calls the break; the cheat sheet is
# printed once), so a page is not required to carry them. taskList still is --
# every page sets homework.
tl=len(re.findall(r'id="taskList"',body))
print("    %-22s taskList=%d   %s" % ("required components",tl,"PASS" if tl==1 else "FAIL"))
if tl!=1: fails.append("components")

print()
print("  bilingual layer (D78 -- these replace the excluded word count)")

ARB=re.compile(r'(?s)<(?:span|p|div) class="ar">(.*?)</(?:span|p|div)>')
def words(x): return len(re.sub(r"\s+"," ",re.sub(r"(?s)<[^>]+>"," ",x)).split())

# 1. every teaching block carries its Arabic.
#    A teaching block is a <p>, <li>, <h2>, <h3> or box body inside a .page that
#    carries real prose -- 4+ English words. Short labels and chips are not blocks.
missing=[];total_ar=0
for sec in secs_full:
    pid=re.search(r'id="(p\d+)"',sec); pid=pid.group(1) if pid else "?"
    total_ar+=len(ARB.findall(sec))
    for m in re.finditer(r'(?s)<(p|li|h2|h3)\b[^>]*>(.*?)</\1>',sec):
        blk=m.group(2)
        if 'class="ar"' in blk: continue
        if re.match(r'(?s)\s*<(?:a|button)\b[^>]*>.*</(?:a|button)>\s*$',blk): continue  # a control
        if 'eCDFP Diploma' in blk or 'class="foot' in m.group(0): continue  # page footer
        if 'divider-meta' in m.group(0): continue   # "5 screens - about 20 min": metadata, not teaching
        if words(strip_ar(blk))>=4:
            missing.append(pid+" <"+m.group(1)+"> "+re.sub(r"(?s)<[^>]+>","",blk).strip()[:44])
chk("Arabic blocks present",total_ar,">= 1",total_ar>0)
chk("teaching blocks with no Arabic",len(missing) or "0","0",not missing)
for x in missing[:6]: print("      -> %s" % x)

# 2. D104 relaxed rule 4: the Arabic is ABOUT the same length as its English --
#    an explanation may need a clause a translation would not. Flag only runaway
#    blocks, over 2.2x, which are the ones that started summarising the section.
runaway=[]
for sec in secs_full:
    pid=re.search(r'id="(p\d+)"',sec); pid=pid.group(1) if pid else "?"
    for m in re.finditer(r'(?s)<(p|li|td|h2|h3)\b[^>]*>(.*?)</\1>',sec):
        blk=m.group(2); ar=ARB.search(blk)
        if not ar: continue
        en=words(strip_ar(blk)); a=words(ar.group(1))
        if en>=4 and a>en*2.2:
            runaway.append("%s %d ar vs %d en :: %s" % (pid,a,en,re.sub(r"(?s)<[^>]+>","",ar.group(1)).strip()[:34]))
chk("Arabic runaway (> 2.2x English)",len(runaway) or "0","0",not runaway)
for x in runaway[:6]: print("      -> %s" % x)

# 3. D104: professional written Arabic. Heavy Egyptian colloquial belongs in
#    instructor_script_ar.md, not in student material.
# Whole words only. "\u064a\u0628\u0642\u0649" is dropped: "\u0641\u064a\u0628\u0642\u0649 \u0641\u0631\u062f\u064a\u0627\u064b" is correct MSA for "remains
# individual", and flagging it trains the writer to avoid good Arabic. The
# "-\u0648\u0634" negation suffix (\u0645\u0637\u0644\u0628\u0648\u0634, \u0645\u0641\u064a\u0634) has no MSA reading, so it stays.
COLLOQ=["\u0627\u0644\u0644\u064a","\u0645\u0634","\u0639\u0634\u0627\u0646","\u062f\u0644\u0648\u0642\u062a\u064a","\u062f\u0644\u0648\u0642\u062a","\u0643\u062f\u0627","\u0643\u062f\u0647",
        "\u0628\u062a\u0627\u0639","\u0639\u0627\u0648\u0632","\u0627\u0632\u0627\u064a","\u0625\u0632\u0627\u064a","\u062a\u0628\u0635","\u0623\u0647\u0648","\u062f\u0647","\u062f\u064a"]
NEGSUF=re.compile(r'\b\w+\u0648\u0634\b')
hits=[]
for sec in secs_full:
    pid=re.search(r'id="(p\d+)"',sec); pid=pid.group(1) if pid else "?"
    for ar in ARB.findall(sec):
        t=re.sub(r"(?s)<[^>]+>","",ar)
        toks=set(re.findall(r'[\u0600-\u06ff]+',t))
        for c in COLLOQ:
            if c in toks: hits.append("%s '%s' :: %s" % (pid,c,t.strip()[:38]))
        for m2 in NEGSUF.findall(t): hits.append("%s '%s' (-\u0648\u0634) :: %s" % (pid,m2,t.strip()[:38]))
chk("colloquial in student Arabic",len(hits) or "0","0",not hits)
for x in hits[:6]: print("      -> %s" % x)

# 4. D122: a technical term is written in ENGLISH inside the Arabic line.
#    D76 rule 2 said so from the start and was broken ~460 times, most of it in
#    the SIMSCREEN and Dgm caption strings -- which live in <script>, not in a
#    <span class="ar">, so the earlier sweep never saw them. This check reads
#    the WHOLE FILE for that reason: every Arabic string ships to the student,
#    wherever it is authored.
BANNED = {
 u"\u0627\u0644\u0628\u0635\u0645\u0629":"hash / signature", u"\u0628\u0635\u0645\u0629":"hash / signature",
 u"\u0627\u0644\u0628\u0635\u0645\u0627\u062a":"hashes / signatures", u"\u0628\u0635\u0645\u0627\u062a":"hashes / signatures",
 u"\u0627\u0644\u0628\u0627\u064a\u062a\u0627\u062a":"bytes", u"\u0628\u0627\u064a\u062a\u0627\u062a":"bytes", u"\u0628\u0627\u064a\u062a":"byte",
 u"\u0628\u062a\u0627\u062a":"bits", u"\u0627\u0644\u0628\u062a\u0627\u062a":"bits",
 u"\u0627\u0644\u062a\u0631\u0648\u064a\u0633\u0629":"header", u"\u062a\u0631\u0648\u064a\u0633\u0629":"header",
 u"\u0627\u0644\u0648\u0642\u0627\u0626\u0639":"findings", u"\u0627\u0644\u0627\u0633\u062a\u0646\u062a\u0627\u062c":"interpretation",
 u"\u0627\u0644\u062d\u0631\u0632":"exhibit", u"\u0627\u0644\u0623\u062b\u0631":"artifact", u"\u0627\u0644\u0622\u062b\u0627\u0631":"artifacts",
 u"\u0627\u0644\u0628\u064a\u0627\u0646\u0627\u062a \u0627\u0644\u0648\u0635\u0641\u064a\u0629":"metadata",
 u"\u0633\u0644\u0633\u0644\u0629 \u0627\u0644\u062d\u064a\u0627\u0632\u0629":"chain of custody",
 u"\u0645\u0627\u0646\u0639 \u0627\u0644\u0643\u062a\u0627\u0628\u0629":"write blocker",
 u"\u0627\u0644\u0645\u0646\u0637\u0642\u0629 \u0627\u0644\u0645\u062d\u0645\u064a\u0629":"HPA",
 u"\u0628\u064a\u0627\u0646 \u0627\u0644\u0628\u0635\u0645\u0627\u062a":"manifest",
 u"\u0627\u0644\u062d\u0627\u0648\u064a\u0629":"container", u"\u0627\u0644\u0639\u0646\u0627\u0642\u064a\u062f":"clusters",
 u"\u0627\u0644\u0645\u062c\u0645\u0648\u0639\u0627\u062a":"clusters", u"\u0627\u0644\u0647\u064a\u0643\u0633":"hex",
 u"\u0627\u0644\u0646\u0632\u0627\u0647\u0629":"integrity", u"\u0627\u0644\u0647\u0648\u064a\u0629":"identity",
 u"\u0627\u0644\u0627\u0633\u062a\u062d\u0648\u0627\u0630":"acquisition", u"\u0627\u0644\u0648\u0633\u064a\u0637":"media",
 u"\u0644\u0642\u0637\u0629":"snapshot", u"\u0627\u0644\u0644\u0642\u0637\u0629":"snapshot",
}
# D132 -- two classes, because one rule could not serve both.
#
# The first version anchored on '(?<![arabic letter])TERM' and listed the bare
# and 'AL-' forms by hand. Arabic glues its particles to the front of a word --
# LI+AL contracts to LIL -- so 'lil-tarwisa' had a letter immediately before the
# stem and walked past a gate that had already been run on the page. Eight pages
# were clean by that gate and were not.
#
# Allowing prefixes on everything then over-corrected: 'athar' is the translation
# we ban for 'artifact' AND the ordinary word for 'effect', so 'its effect is
# long' was reported as a terminology break. A banned word that is also a normal
# Arabic word is only a violation in its definite, technical form.
#
# STEMMED  -- never anything but the technical term. Prefixes and suffixes match.
# LITERAL  -- an ordinary Arabic word too. Only the exact listed form matches.
STEMMED = {u'\u0628\u0635\u0645\u0629', u'\u0628\u0635\u0645\u0627\u062a',
           u'\u0628\u0627\u064a\u062a', u'\u0628\u0627\u064a\u062a\u0627\u062a',
           u'\u0628\u062a\u0627\u062a', u'\u062a\u0631\u0648\u064a\u0633\u0629',
           u'\u0627\u0644\u0647\u064a\u0643\u0633'}
PRE = u'(?:[\u0648\u0641]?(?:\u0644\u0644|\u0628\u0627\u0644|\u0643\u0627\u0644|\u0627\u0644|\u0628|\u0643|\u0644)?)'
SUF = u'(?:\u0627\u062a|\u0627\u0646|\u064a\u0646|\u0647\u0627|\u0647\u0645|\u0647)?'
AR  = u'[\u0621-\u064a]'
bad=[]; seen=set()
for term,eng in BANNED.items():
    stem = term[2:] if term.startswith(u'\u0627\u0644') else term
    if stem in STEMMED or term in STEMMED:
        # a stem ending in TA MARBUTA turns it into TA before a suffix:
        # basma -> basmatuha. Matching the listed form only would miss it,
        # which is what the mutation test caught on the first attempt.
        if stem.endswith(u'\u0629'):
            body = re.escape(stem[:-1]) + (u'(?:\u0629|\u0627\u062a|\u062a'
                    u'(?:\u0647\u0645\u0627|\u0647\u0627|\u0647\u0645|\u0647|\u0627\u0646|\u064a\u0646)?)')
        else:
            body = re.escape(stem) + SUF
        pat = u'(?<!'+AR+u')'+PRE+body+u'(?!'+AR+u')'
    else:
        pat = u'(?<!'+AR+u')[\u0648\u0641]?'+re.escape(term)+u'(?!'+AR+u')'
    for m3 in re.finditer(pat, h):
        line=h.count("\n",0,m3.start())+1
        if (line,m3.start()) in seen: continue
        seen.add((line,m3.start()))
        bad.append(u"line %d '%s' -> use %s" % (line,m3.group(0),eng))
chk("translated technical terms (D76 r2)",len(bad) or "0","0",not bad)
for x in bad[:6]: print(u"      -> %s" % x)

# 4b. D133: an Arabic suffix glued to a Latin word, or the reverse. Both are
#     always defects and neither is a "banned term": "partition" + the dual
#     ending, and the substring-replace corruption D122 warned about
#     (thubit -> thu-bit) are the same shape. The house style always puts a
#     space between the two scripts, so any join is a break.
glued = []
for m5 in re.finditer(u'[A-Za-z]{2,}[\u0621-\u064a]{1,}|[\u0621-\u064a]{2,}[A-Za-z]{2,}', h):
    line = h.count("\n", 0, m5.start()) + 1
    glued.append(u"line %d '%s'" % (line, m5.group(0)))
chk("Latin and Arabic glued together (D133)", len(glued) or "0", "0", not glued)
for x in glued[:6]: print(u"      -> %s" % x)


# 6. D126: the Arabic must name the SAME technical term as its English.
#    The D122 sweep mapped one Arabic word to one English term, but the word
#    meant TWO things -- signature (magic bytes) and hash -- so ten blocks on
#    P03 said "hash" under an English line about signatures. Neither side is
#    illegal alone, which is why the D122 check cannot see it: the PAIR is
#    what is wrong.
#    NOT a regex over nested HTML. `re.finditer` scans forward from the end of
#    each match, so an outer <div> wrapping a table swallows every row inside
#    it and the rows are never examined -- the first version of this check
#    passed a deliberately broken page. Instead: walk each .ar span and read
#    the English immediately BEFORE it, which is the D108 relationship anyway.
PAIRS = [("signature", "hash"), ("hash", "signature"),
         ("metadata", "header"), ("header", "metadata"),
         ("cluster", "sector"), ("sector", "cluster")]
mismatch = []
for m4 in re.finditer(r'(?s)<span class="ar">(.*?)</span>', h):
    ar_t = re.sub(r"<[^>]+>", " ", m4.group(1)).lower()
    lead = h[max(0, m4.start() - 700):m4.start()]
    lead = lead.rsplit("</span>", 1)[-1] if "class=\"ar\"" in lead else lead
    lead = re.split(r'<(?:tr|li|p|h2|div)\b', lead)[-1]
    en_t = re.sub(r"<[^>]+>", " ", lead).lower()
    for want, wrong in PAIRS:
        if want in en_t and wrong not in en_t and wrong in ar_t and want not in ar_t:
            mismatch.append("EN '%s' vs AR '%s' :: %s" %
                            (want, wrong, re.sub(r"\s+", " ", en_t).strip()[-46:]))
chk("EN/AR term disagreement (D126)", len(mismatch) or "0", "0", not mismatch)
for x in mismatch[:6]: print("      -> %s" % x)

# 5. D119: a divider screen is announced in the sidebar and nowhere else.
dv=re.findall(r'<section class="page divider"',h)
ip=re.findall(r'<li class="is-part"',h)
chk("part dividers == is-part entries","%d/%d"%(len(dv),len(ip)),"equal",len(dv)==len(ip))

print("-"*72)
print("RESULT: %s" % ("ALL PASS" if not fails else "FAIL -> "+", ".join(fails)))
sys.exit(1 if fails else 0)
