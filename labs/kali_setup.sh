#!/usr/bin/env bash
# kali_setup.sh — Kali (FOR-LNX01 role): install the Linux acquisition + timeline tools.
# Run as root (sudo). Idempotent.  Ref: labs/kali_setup.md
set -e

# 1. Switch APT to HTTPS — dodges a network antivirus that blocks hacktool .debs over plain HTTP (err 499)
sed -i 's|http://http.kali.org|https://http.kali.org|g' /etc/apt/sources.list /etc/apt/sources.list.d/*.sources 2>/dev/null || true
apt update

# 2. Tools (plaso = super-timelines/S6; dc3dd = imaging; the rest usually already on Kali)
apt install -y --fix-missing plaso dc3dd sleuthkit foremost bulk-extractor tcpdump

# 3. Verify — NOTE plaso tools are PREFIXED on Kali (plaso-log2timeline, not log2timeline.py)
echo "--- versions ---"
plaso-log2timeline --version
dc3dd --version | head -1
which tsk_recover foremost bulk_extractor tcpdump
