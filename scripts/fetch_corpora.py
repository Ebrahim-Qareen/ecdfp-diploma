#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fetch_corpora.py -- EVS-12, EVS-13, EVS-14: the Tier 2 Windows artifact sets.

Tier 2 means PUBLISHED corpora, linked and credited, never rehosted (D22, R9).
This script fetches each source repository at a PINNED commit, copies the
exact files the pages use into <out>/EVS-NN/, and refuses to finish unless
every byte matches the SHA-256 recorded here. Nothing is invented, nothing is
edited, and the repo carries this manifest -- not the files.

  EVS-12  registry hives          P10   Eric Zimmerman, Registry (MIT)
  EVS-13  user-activity artifacts P11   Eric Zimmerman, Prefetch / Lnk / JumpList /
                                        RBCmd / AppCompatCacheParser (MIT)
  EVS-14  Windows event logs      P12   Samir Bousseaden, EVTX-ATTACK-SAMPLES (GPL-3.0)

Usage: python3 fetch_corpora.py --out <a path OUTSIDE the repo>
Requires: git with HTTPS access to github.com.
"""
import argparse, hashlib, os, shutil, subprocess, sys

REPOS = {
  'ez-registry':          ('https://github.com/EricZimmerman/Registry.git',              '1b0b3c414569debb5ffcc629de28e3ff27145a42'),
  'Prefetch':             ('https://github.com/EricZimmerman/Prefetch.git',              '27d87a095fe0bd4b07726aec867e1c0f1aef08f9'),
  'Lnk':                  ('https://github.com/EricZimmerman/Lnk.git',                   '918bea4a9c8d99b02aae2b1a5d1512aff0c07de2'),
  'JumpList':             ('https://github.com/EricZimmerman/JumpList.git',              'e87bacd4869cbe0633c16ad11d3d26c9f39d0a2b'),
  'RBCmd':                ('https://github.com/EricZimmerman/RBCmd.git',                 '756498f9b5e94327abe5398b19435b7142f7265c'),
  'AppCompatCacheParser': ('https://github.com/EricZimmerman/AppCompatCacheParser.git',  '0cf059f40c2f7b31acdccb142461945402217398'),
  'EVTX-ATTACK-SAMPLES':  ('https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES.git',     '4ceed2f4706daf601c212a8f91c113dd85349a2c'),
}

# (set, repo, path inside the repo, sha256, name in the set)
FILES = [
 ('EVS-12','ez-registry','Registry.Test/Hives/SYSTEM',     'ec01a4ec205c5354a4ad1d5d088f45e2331ffb13773dcc7008e6ea6f2175466f','SYSTEM'),
 ('EVS-12','ez-registry','Registry.Test/Hives/SOFTWARE',   '658c4323cc2c4e33e09ef3e5251651300ff1a49937e136242565cc5c49fd5e96','SOFTWARE'),
 ('EVS-12','ez-registry','Registry.Test/Hives/SAM',        '8aea3c9217bfe1ecc39df535c25a02d5dfb76d0427298898a370a086c10f72aa','SAM'),
 ('EVS-12','ez-registry','Registry.Test/Hives/SECURITY',   '4a427cfa5a9de9075b38a71717bbe9f303ed3cd458015cc4d39a58f47589a567','SECURITY'),
 ('EVS-12','ez-registry','Registry.Test/Hives/NTUSER.DAT', '8d5fdee75d69b878a0bf602f7a15f0410c5622b9c8c84a5c2f346d44a8cdb759','NTUSER.DAT'),

 ('EVS-13','ez-registry','Registry.Test/Hives/UsrClass 1.dat',           '6dbfecef68d01ddaedaec98b9142e3c17ae9d4a6ec98456680f0c9a74a054a07','UsrClass.dat'),
 ('EVS-13','ez-registry','Registry.Test/Hives/UsrClassDeletedBags.dat',  '8a649ddeff18e1d4b2f913794ab006c7d2d4e8c702bf32a545e3484324cf9abc','UsrClassDeletedBags.dat'),
 ('EVS-13','Prefetch','Prefetch.Test/TestFiles/Win10/CMD.EXE-D269B812.pf',    '0ef6ce683365dac64191608b47a74665ddec28eaae530ce2622900130c404077','CMD.EXE-D269B812.pf'),
 ('EVS-13','Prefetch','Prefetch.Test/TestFiles/Win10/CHROME.EXE-B3BA7868.pf', '52543b5a85b9ee1936e048dc7f7fab6ffaa18834f5db68ee87926e38e84b8e13','CHROME.EXE-B3BA7868.pf'),
 ('EVS-13','Prefetch','Prefetch.Test/TestFiles/Win10/CALC.EXE-3FBEF7FD.pf',   'e1d11876560511788c58e957d302a4a953e8cd8e8d7c0290796393058c164319','CALC.EXE-3FBEF7FD.pf'),
 ('EVS-13','Lnk','Lnk.Test/TestFiles/Win10/!!__Files from SOME COMPUTER_Files Copied.txt.lnk.test',
                                                                              '744a78dc8ea8ca49edf45e2a8536447918663fbc718469a9b938f05c9be6bc3c','Files Copied.txt.lnk'),
 ('EVS-13','JumpList','JumpList.Test/TestFiles/Win10/f01b4d95cf55d32a.automaticDestinations-ms',
                                                                              'a724713d2ff51d32e3f028c57ab906339f882de0c93dc9903f0f8b241c53fd56','f01b4d95cf55d32a.automaticDestinations-ms'),
 ('EVS-13','RBCmd','RecycleBin.Test/TestFiles/Win10 - DEFCON 2018 Desktop/$I2JRX90','d2966f4c3de5968bffb5cdaacf75857cd34357f00c86def6fdcff67fe31d9af8','$I2JRX90'),
 ('EVS-13','RBCmd','RecycleBin.Test/TestFiles/Win10 - DEFCON 2018 Desktop/$IFATB0K','6a49ebf257e3bf193eeeb021c1bfda524594b50e71615d71711f6f588a891420','$IFATB0K'),
 ('EVS-13','AppCompatCacheParser','AppCompatCacheParserTest/TestFiles/Win10.bin','6f175c17506bd1ae94683b791b2151a6b8266196d33db2ad4971c09287c632fa','AppCompatCache-Win10.bin'),

 ('EVS-14','EVTX-ATTACK-SAMPLES','Defense Evasion/DE_1102_security_log_cleared.evtx',                     'a0615707b547a2ac254688fd725c3c590f62440fc9b7947c2843dd40498a39e8','DE_1102_security_log_cleared.evtx'),
 ('EVS-14','EVTX-ATTACK-SAMPLES','Defense Evasion/DE_104_system_log_cleared.evtx',                       '5579cdca073ee4864ea82d656aa2d25400b5c1e85b8e688db5d85f6dc558c2af','DE_104_system_log_cleared.evtx'),
 ('EVS-14','EVTX-ATTACK-SAMPLES','Credential Access/CA_4624_4625_LogonType2_LogonProc_chrome.evtx',      '75f199b68d473172705bf874720b01820317fdd7aa4843545c98720dd6de197f','CA_4624_4625_LogonType2.evtx'),
 ('EVS-14','EVTX-ATTACK-SAMPLES','Lateral Movement/LM_4624_mimikatz_sekurlsa_pth_source_machine.evtx',   'bbfd87cacdd56a9135de1838666937cd6c74daba47b366bba0c11f95ce97f461','LM_4624_pth_source.evtx'),
 ('EVS-14','EVTX-ATTACK-SAMPLES','Persistence/evasion_persis_hidden_run_keyvalue_sysmon_13.evtx',        'b8df8232d917fed223e2bf9abebb249489f84c6204c40b72dab6a74157d6f8bd','persist_run_key_sysmon_13.evtx'),
 ('EVS-14','EVTX-ATTACK-SAMPLES','Persistence/Network_Service_Guest_added_to_admins_4732.evtx',         '9619b9d9d7bb8a277080167ff639fd9162e3d88d61d674cf1606beadce17ea5a','guest_added_to_admins_4732.evtx'),
]


def sh(*a, cwd=None):
    r = subprocess.run(a, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if r.returncode:
        sys.stdout.write(r.stdout.decode('utf-8', 'replace'))
        raise SystemExit('failed: ' + ' '.join(a))


def fetch(out, name, url, sha):
    d = os.path.join(out, '_src', name)
    if os.path.isdir(os.path.join(d, '.git')):
        head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=d, stdout=subprocess.PIPE).stdout.decode().strip()
        if head == sha:
            return d
        shutil.rmtree(d)
    os.makedirs(d)
    sh('git', 'init', '-q', cwd=d)
    sh('git', 'remote', 'add', 'origin', url, cwd=d)
    sh('git', 'fetch', '-q', '--depth', '1', 'origin', sha, cwd=d)   # by commit, so upstream cannot move it
    sh('git', 'checkout', '-q', 'FETCH_HEAD', cwd=d)
    return d


def main(out):
    os.makedirs(out, exist_ok=True)
    src = {}
    for name, (url, sha) in REPOS.items():
        print('fetching %-22s @ %s' % (name, sha[:12]))
        src[name] = fetch(out, name, url, sha)
    manifests = {}
    bad = 0
    for evs, repo, rel, want, dst in FILES:
        p = os.path.join(src[repo], rel)
        b = open(p, 'rb').read()
        got = hashlib.sha256(b).hexdigest()
        tgt = os.path.join(out, evs)
        os.makedirs(tgt, exist_ok=True)
        open(os.path.join(tgt, dst), 'wb').write(b)
        ok = got == want
        bad += not ok
        print('  %-7s %-42s %9d B  %s' % (evs, dst, len(b), 'OK' if ok else 'HASH MISMATCH -- upstream changed'))
        manifests.setdefault(evs, []).append('%s  %s' % (got, dst))
    for evs, lines in manifests.items():
        open(os.path.join(out, evs, evs + '.sha256'), 'w').write('\n'.join(lines) + '\n')
    if bad:
        raise SystemExit('%d file(s) differ from the pinned manifest -- do not use them' % bad)
    print('\nall %d files match the pinned manifest' % len(FILES))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    main(ap.parse_args().out)
