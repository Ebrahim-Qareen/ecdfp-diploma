#!/usr/bin/env python3
"""stamp_assets.py -- cache-bust every local CSS/JS reference under docs/.

Rewrites  href="../assets/css/x.css"  ->  href="../assets/css/x.css?v=<sha256[:8]>"
(and src= for js), using the referenced file's current content hash, so a
changed asset always gets a new URL and a browser can never pair new HTML with
a stale cached stylesheet or script (GitHub Pages caches assets for 10 min).
Idempotent: an existing ?v=... is replaced, not appended. Run before publish:

    python3 scripts/stamp_assets.py            # stamp docs/**/*.html
    python3 scripts/stamp_assets.py --check    # exit 1 if any stamp is stale
"""
import hashlib, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs')
PAT = re.compile(r'(?P<attr>\b(?:href|src))="(?P<path>[^"?#]*assets/(?:css|js)/[^"?#]+)(?:\?v=[0-9a-f]+)?"')

def sha8(p):
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()[:8]

def main():
    check = '--check' in sys.argv
    changed = stamped = missing = stale = 0
    for dp, _, fns in os.walk(ROOT):
        for fn in fns:
            if not fn.endswith('.html'):
                continue
            hp = os.path.join(dp, fn)
            src = open(hp, encoding='utf-8').read()
            def sub(m):
                nonlocal stamped, missing, stale
                rel = m.group('path')
                target = os.path.normpath(os.path.join(dp, rel))
                if not os.path.isfile(target):
                    missing += 1
                    print(f'  warn: {os.path.relpath(hp, ROOT)} -> {rel} (file not found, left as is)')
                    return m.group(0)
                new = f'{m.group("attr")}="{rel}?v={sha8(target)}"'
                stamped += 1
                if new != m.group(0):
                    stale += 1
                return new
            out = PAT.sub(sub, src)
            if out != src:
                changed += 1
                if not check:
                    open(hp, 'w', encoding='utf-8').write(out)
    mode = 'CHECK' if check else 'STAMP'
    print(f'{mode}: {stamped} asset references, {changed} page(s) {"stale" if check else "updated"}, {missing} unresolved')
    if check and stale:
        sys.exit(1)

if __name__ == '__main__':
    main()
