#!/bin/bash
# EVS-15 -- the live-session disk set (Tier 1, built in our own lab; fictional Meridian Retail Group data).
# Four raw images: mbr_lab.001, gpt_lab.001, corrupt_lab.001, ctf_disk.001 (+ ctf_disk_FIXED_reference.001, instructor only).
#
#   usage:  sudo scripts/make_evs15.sh <out dir OUTSIDE the repo> <path to an EVS-10 build>
#   needs:  sfdisk sgdisk mkfs.vfat mtools(mcopy mmd mdel) mkntfs ntfs-3g exiftool python3
#   secrets: the three challenge flags are NOT in this file. They are read from
#            $EVS15_SECRETS (default instructor/evs15_secrets.env, which is never committed):
#              FLAG1=... FLAG2=... FLAG3=... RB_SID=S-1-5-21-... CTF_DELETED=<name of the deleted root file>
#
# mkntfs draws a random volume serial, so the NTFS images are not byte-reproducible (same caveat as
# EVS-11); record numbers, offsets and sector positions are, and those are what the pages cite.
set -e
OUT=${1:?out dir}; EVS10=${2:?EVS-10 dir}; OUT=$(readlink -f "$OUT"); EVS10=$(readlink -f "$EVS10")
REPO=$(cd "$(dirname "$0")/.." && pwd)
SECRETS=${EVS15_SECRETS:-$REPO/instructor/evs15_secrets.env}
[ -f "$SECRETS" ] || { echo "missing $SECRETS (FLAG1 FLAG2 FLAG3 RB_SID CTF_DELETED)"; exit 2; }
. "$SECRETS"; : "${FLAG1:?}" "${FLAG2:?}" "${FLAG3:?}" "${RB_SID:?}" "${CTF_DELETED:?}"
WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT
cd "$WORK"; mkdir -p "$OUT"
ts="2026-08-25 09:14:02"   # course attack window (D19/D57)

content() {  # fictional content tree in $1
  local d=$1; rm -rf $d; mkdir -p $d/Invoices $d/photos $d/HR $d/Finance
  printf 'Meridian Retail Group - shared drive\nOwner: l.bennett\nDo not copy customer data to removable media. Policy MRG-SEC-004.\n' > $d/readme.txt
  printf 'INVOICE AP-2026-0812\nVendor: Nile Office Supplies\nAmount: 4,250.00 EGP\nStatus: PAID 2026-08-12\n' > $d/Invoices/inv_2026_0812.txt
  printf 'id,name,department,site\nMRG-1001,L. Bennett,Finance,Cairo-Floor3\nMRG-1002,R. Osei,IT,Cairo-Floor2\nMRG-1003,S. Farouk,Sales,Alexandria\n' > $d/HR/staff_list.csv
  printf 'Q3 2026 summary (internal)\nRevenue 12.4M EGP, +6%% QoQ. Customer export scheduled for audit on 2026-08-26.\n' > $d/Finance/q3_summary.txt
  cp $EVS10/office_floor3.jpg $d/photos/office_floor3.jpg
  cp $EVS10/team_photo.jpg   $d/photos/team_photo.jpg
  printf 'Copy customer_export to USB before the audit. Delete this note after.\n' > $d/secret_plan.txt
  find $d -exec touch -d "$ts" {} +
}

fill_fat() {  # $1 image  $2 offset-bytes  $3 srcdir
  local spec="$1@@$2" src=$3
  for dir in Invoices photos HR Finance; do mmd -i "$spec" ::/$dir; done
  ( cd $src && for f in readme.txt secret_plan.txt Invoices/* photos/* HR/* Finance/*; do mcopy -i "$spec" -m "$f" ::/$f; done )
  mdel -i "$spec" ::/secret_plan.txt          # deleted on FAT -> first byte of the directory entry becomes 0xE5
}

fill_ntfs() { # $1 standalone-ntfs-file $2 (unused) $3 srcdir  [$4 = ctf]
  local img=$1 src=$3 m=$WORK/mnt_$$; mkdir -p $m
  ntfs-3g -o streams_interface=windows $img $m
  if [ "$4" = "ctf" ]; then
    cp $src/readme.txt $m/readme.txt
    printf 'Not that simple. You have to try a little bit harder.\nHere:\n%s\n' "$(printf '%s' "$FLAG1" | od -An -tx1 | tr -d '\n' | sed 's/^ //')" > $m/Flag1.txt
    printf 'Flag 2 is where deleted things go.\nFlag 3 is where no partition goes.\n' > $m/Flag2.txt
    cp $EVS10/office_floor3.jpg $m/Photo.jpg
    exiftool -q -overwrite_original -UserComment="$FLAG2" -ImageDescription='Office floor 3 (recycled)' $m/Photo.jpg
    sid="$RB_SID"; mkdir -p "$m/\$RECYCLE.BIN/$sid"
    mv $m/Photo.jpg "$m/\$RECYCLE.BIN/$sid/\$RGPMI4F.jpg"
    python3 - "$m/\$RECYCLE.BIN/$sid/\$IGPMI4F.jpg" <<'PY'
import sys,struct,datetime
p=sys.argv[1]; path=r"C:\Users\l.bennett\Pictures\Photo.jpg"
ft=int((datetime.datetime(2026,8,25,10,42,0)-datetime.datetime(1601,1,1)).total_seconds()*10**7)
open(p,'wb').write(struct.pack('<QQQI',2,78130,ft,len(path)+1)+(path+'\0').encode('utf-16-le'))
PY
    printf 'Model - Mey.mp3 placeholder (not a real recording)\n' > "$m/Model - Mey.mp3"
    cp $EVS10/receipt_scan_clean.png $m/receipt_scan.png
    printf 'MRG-INTERNAL draft. The export archive is customer_export.7z. Delete me.\n' > "$m/$CTF_DELETED"; sync; rm "$m/$CTF_DELETED"
  else
    cp -r $src/. $m/
    for i in $(seq -w 1 12); do cp $src/photos/office_floor3.jpg $m/photos/site_$i.jpg; done   # enough entries to force an $INDEX_ALLOCATION ($I30 file)
    sync
    rm $m/photos/team_photo.jpg            # deleted on NTFS -> FTK Imager shows it with a red X
    rm $m/photos/site_07.jpg               # second deleted name, stays in $I30 slack
    # an Alternate Data Stream on readme.txt (NTFS feature; FTK Imager shows it as readme.txt:policy_note.txt)
    printf 'MRG-INTERNAL: the customer_export archive was staged under HR\\ before the audit. Do not mention in the shared readme.\n' > "$m/readme.txt:policy_note.txt"
  fi
  find $m -mindepth 1 -not -name '\$*' -exec touch -d "$ts" {} + 2>/dev/null || true
  sync; umount $m; rmdir $m
}

content $WORK/src

# ---------- A: mbr_lab.001  (128 MiB · MBR · P1 FAT32 48 MiB · P2 NTFS 78 MiB · 1 MiB unpartitioned tail)
A=$OUT/mbr_lab.001; dd if=/dev/zero of=$A bs=1M count=128 status=none
sfdisk -q $A <<'EOF'
label: dos
label-id: 0x4d524731
unit: sectors
start=2048,   size=98304,  type=c
start=100352, size=159744, type=7
EOF
mkfs.vfat -F 32 -n USB_DATA --offset 2048 $A 49152 >/dev/null 2>&1
fill_fat $A $((2048*512)) $WORK/src
dd if=/dev/zero of=ntfs_a.img bs=512 count=159744 status=none
mkntfs -F -Q -L MRG-DATA -s 512 -c 4096 -p 100352 -S 63 -H 255 ntfs_a.img >/dev/null 2>&1
fill_ntfs ntfs_a.img 0 $WORK/src
dd if=ntfs_a.img of=$A bs=512 seek=100352 conv=notrunc status=none; rm ntfs_a.img
# something in the unpartitioned tail, so "unpartitioned != empty"
printf 'MRG-INTERNAL: old backup fragment. staged archive is customer_export.7z\n' | dd of=$A bs=512 seek=260600 conv=notrunc status=none

# ---------- B: gpt_lab.001  (128 MiB · GPT · P1 FAT32 32 MiB · P2 NTFS rest)
B=$OUT/gpt_lab.001; dd if=/dev/zero of=$B bs=1M count=128 status=none
sgdisk -o $B >/dev/null
sgdisk -n 1:2048:67583 -t 1:0700 -c 1:"USB_DATA" -u 1:6E2D2A5B-1F2A-4C7E-9B3E-0A1B2C3D4E01 $B >/dev/null
sgdisk -n 2:67584:0    -t 2:0700 -c 2:"MRG-DATA" -u 2:6E2D2A5B-1F2A-4C7E-9B3E-0A1B2C3D4E02 $B >/dev/null
sgdisk -U 4D524731-4750-5400-8000-000000000001 $B >/dev/null
P2START=$(sgdisk -i 2 $B | awk '/First sector/{print $3}'); P2END=$(sgdisk -i 2 $B | awk '/Last sector/{print $3}'); P2N=$((P2END-P2START+1))
mkfs.vfat -F 32 -n USB_DATA --offset 2048 $B 32768 >/dev/null 2>&1
fill_fat $B $((2048*512)) $WORK/src
dd if=/dev/zero of=ntfs_b.img bs=512 count=$P2N status=none
mkntfs -F -Q -L MRG-DATA -s 512 -c 4096 -p $P2START -S 63 -H 255 ntfs_b.img >/dev/null 2>&1
fill_ntfs ntfs_b.img 0 $WORK/src
dd if=ntfs_b.img of=$B bs=512 seek=$P2START conv=notrunc status=none; rm ntfs_b.img
echo "GPT P2: start=$P2START end=$P2END sectors=$P2N" > $OUT/_gpt_geometry.txt

# ---------- C: corrupt_lab.001  = A with the 64-byte partition table zeroed (signature 55AA kept)
C=$OUT/corrupt_lab.001; cp $A $C
dd if=/dev/zero of=$C bs=1 seek=446 count=64 conv=notrunc status=none

# ---------- D: ctf_disk.001 (150 MiB · MBR · one NTFS partition of 99 MiB · tail unpartitioned) — then table zeroed
D=$OUT/ctf_disk.001; dd if=/dev/zero of=$D bs=1M count=150 status=none
sfdisk -q $D <<'EOF'
label: dos
label-id: 0x43544631
unit: sectors
start=2048, size=202752, type=7
EOF
dd if=/dev/zero of=ntfs_d.img bs=512 count=202752 status=none
mkntfs -F -Q -L "New Volume" -s 512 -c 4096 -p 2048 -S 63 -H 255 ntfs_d.img >/dev/null 2>&1
fill_ntfs ntfs_d.img 0 $WORK/src ctf
dd if=ntfs_d.img of=$D bs=512 seek=2048 conv=notrunc status=none; rm ntfs_d.img
# Flag 3 in the unpartitioned tail (sector 300000 of 307200)
printf '\n\n== MRG backup fragment ==\n%s\n\n' "$FLAG3" | dd of=$D bs=512 seek=300000 conv=notrunc status=none
cp $D $OUT/ctf_disk_FIXED_reference.001          # instructor-only reference with an intact table
dd if=/dev/zero of=$D bs=1 seek=446 count=64 conv=notrunc status=none   # the challenge ships corrupted

cd $OUT && sha256sum *.001 > SHA256SUMS.txt && md5sum *.001 > MD5SUMS.txt && ls -la
