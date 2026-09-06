# Kali — the Linux acquisition host (D56; replaces the planned FOR-LNX01)

The instructor's existing Kali VM is the Linux acquisition + timeline machine. Set up 2026-09-06.

## Install
```
sudo apt update
sudo apt install -y plaso dc3dd sleuthkit foremost bulk-extractor tcpdump
```

## Command names & versions (verified 2026-09-06) — for S6 version binding (M6/L7)
- **plaso 20260119** — on Kali the tools are **prefixed**: `plaso-log2timeline`, `plaso-psort`,
  `plaso-pinfo`, `plaso-image_export` (NOT `log2timeline.py`). S6 super-timeline commands must use these.
- **dc3dd 7.3.1** · **Sleuth Kit 4.14.0** (`tsk_recover`, `mmls`, `fls`, `istat`) · **foremost 1.5.7** ·
  **bulk_extractor 2.1.1** · **tcpdump 4.99.6**.

## Gotchas hit (and fixed)
- **Network AV block:** a proxy/AV blocked hacktool `.deb`s over plain HTTP (`499 forbidden by antivirus`).
  Fix — switch APT to HTTPS: `sudo sed -i 's|http://http.kali.org|https://http.kali.org|g' /etc/apt/sources.list /etc/apt/sources.list.d/*.sources`.
- **python3-aardwolf vs python 3.14:** a broken Kali-rolling dependency blocked apt; resolved by the `+b2`
  rebuild once fetched over HTTPS. Unrelated to plaso.
