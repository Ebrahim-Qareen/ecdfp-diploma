---
room: EXT Analysis ("Discover the forensic basics of the EXT file system.")
url: https://tryhackme.com/room/extanalysis
difficulty: Medium
time: 60 min (room header)
tasks: 7 (Task 1 Introduction · Task 2 EXT File System Structure · Task 3 Forensic Artifacts in EXT · Task 4 Analyzing File System Timestamps · Task 5 Tools for EXT Forensics · Task 6 Practical · Task 7 Conclusion)
free-or-premium: Premium room (subscription required); room type = walkthrough ("Back to all walkthroughs"); header counters showed 3,555 (joined) and 80 (recommend)
extracted: 2026-09-10 (logged-in Chrome session; room rendered in full, no login wall)
completeness: ALL 7 tasks read in full — body text, code/terminal blocks and every question captured verbatim. Of the 15 content images, all 4 Task-2 figures were inspected pixel-by-pixel (hexdump and dumpe2fs transcribed), and 6 of the 11 Task-5 Autopsy screenshots were inspected (5.2, 5.6, 5.7, 5.9, 5.10, 5.11); the other 5 Autopsy wizard screens are described from their alt text only, as marked in §7. The lab VM was NOT started; anything that only exists inside the VM (e.g. the /mnt/ext_exercises contents, ext4_case.img size) is marked "not stated".
---

## 1. What the room teaches

The room is a short, structure-first introduction to EXT4 forensics on a live Linux VM. It opens (Task 2) with a history line — EXT was the "first file system specifically for Linux", "first introduced in April 1992", supported 2 GB file systems and "is also the first to incorporate the Virtual File System (VFS)" — then names the five shared building blocks of EXT2/3/4: superblocks, inodes, block groups/data blocks, directory structures, and bitmaps. Its mental model of a file write is stated once and reused throughout: create a file → an inode is allocated for metadata (permissions, ownership, timestamps) → content goes to one or more data blocks → the inode records pointers to those blocks → the file name is linked to the inode in the directory structure → superblock, bitmaps and related metadata are updated "to reflect the changes, ensuring consistency". Two diagrams carry the layout idea: (a) the volume is divided into equal-size blocks (1024/2048/4096) numbered 0..N and gathered into block groups, all groups equal-sized except the last; (b) a partition = boot sector + block group 0..N + unused sectors, and each block group = superblock, group descriptors, block bitmap, inode bitmap, inode table, data blocks.

The teaching method is "read the kernel struct, then find the same value three ways": the room prints the Linux `struct ext4_super_block` and `struct ext4_inode` definitions, has the student read the raw superblock with `dd | hexdump -C` (finding `s_log_block_size` at offset 0x18, value 2, little-endian, block size = 2^(10+2) = 4096), then confirms it with `dumpe2fs`, and finally inspects inodes with `debugfs` (`stat .`, `stat <11>`). Task 3 shows that changing permissions (`chmod 755`) updates `i_mode` and `ctime` but not `mtime/atime/crtime`, then performs a manual recovery of a deleted file by content carving: `strings -t d` to find a byte offset, divide by the block size to get a block number, `dd bs=4096 skip=N count=1` to extract the block. Task 4 covers the five EXT timestamps (atime, mtime, ctime, dtime, crtime — crtime "only available in EXT4"), demonstrates timestomping (a file whose atime/mtime say 2016 while ctime/crtime say 2025) and teaches `find -newerct` as the detection query, with the caveat that ctime "can only be changed to the time on the system" so an attacker could shift the system clock (link to an inversecos article on Linux anti-forensics).

Task 5 replays the same observations in Autopsy 4.21.0 (New Case → Disk Image or VM File → `ext4_case.img` → Data Sources tree → file listing with Modified/Change/Access/Created columns → Deleted Files view showing an orphan file), mentioning `debugfs` and `extundelete` as CLI alternatives. Task 6 is an unguided practical on a third mounted file system (`/mnt/ext_exercises`): find the timestomped file's real creation date and recover a deleted file containing a flag. Tools actually used: `lsblk`, `dd`, `hexdump`, `dumpe2fs`, `debugfs`, `ls`, `stat`, `chmod`, `strings`, `grep`, `echo $(( ))`, `cat`, `find`, Autopsy. Sleuth Kit CLI (`fsstat/fls/istat/icat/blkcat`), `xxd`, `ext4magic` and the journal tools are NOT used.

## 2. Structures and artifacts

Legend: "ROOM:" = stated by the room; "FIGURE:" = visible in one of the room's screenshots but not written in the text; "SUPPLIED:" = added by the extractor, not in the room. Offsets are given only where the room states or shows them.

### 2.1 Superblock (`struct ext4_super_block`)

- What it is — ROOM: "one of the most important structures within the EXT4 that defines some key options, for example, the block size"; "Superblocks contain metadata information about a file system, such as size and status."
- Where it lives — ROOM (by command, not by sentence): read with `sudo dd if=/dev/loop0 bs=1024 count=1 skip=1 | hexdump -C`, i.e. 1024 bytes starting at byte offset 1024 of the device. The room's struct listing (verbatim, including the kernel's hex row markers) is:

```
struct ext4_super_block {
/*00*/  __le32  s_inodes_count;         /* Inodes count */
        __le32  s_blocks_count_lo;      /* Blocks count */
        __le32  s_r_blocks_count_lo;    /* Reserved blocks count */
        __le32  s_free_blocks_count_lo; /* Free blocks count */
/*10*/  __le32  s_free_inodes_count;    /* Free inodes count */
        __le32  s_first_data_block;     /* First Data Block */
        __le32  s_log_block_size;       /* Block size */
        __le32  s_log_cluster_size;     /* Allocation cluster size */
/*20*/  __le32  s_blocks_per_group;     /* # Blocks per group */
        __le32  s_clusters_per_group;   /* # Clusters per group */
        __le32  s_inodes_per_group;     /* # Inodes per group */
        __le32  s_mtime;                /* Mount time */
/*30*/  __le32  s_wtime;                /* Write time */
        __le16  s_mnt_count;            /* Mount count */
        __le16  s_max_mnt_count;        /* Maximal mount count */
        __le16  s_magic;                /* Magic signature */
        __le16  s_state;                /* File system state */
        __le16  s_errors;               /* Behaviour when detecting errors */
        __le16  s_minor_rev_level;      /* minor revision level */
/*40*/  __le32  s_lastcheck;            /* time of last check */
        __le32  s_checkinterval;        /* max. time between checks */
        __le32  s_creator_os;           /* OS */
        __le32  s_rev_level;            /* Revision level */
/*50*/  __le16  s_def_resuid;           /* Default uid for reserved blocks */
        __le16  s_def_resgid;           /* Default gid for reserved blocks */

(...)
};
```

  The only offset the room states in prose: `s_log_block_size` "is located at the 7th position in the structure … Since each 32-bit integer takes up 4 bytes, the block size will be found at offset 0x18." The room also states the decode rule: values are little-endian ("02000000 will be 00000002") and block size = "2 ^ (10 + s_log_block_size)" → 2^(10+2) = 4096 bytes.

  Offsets derivable from the room's own row markers (/*00*/, /*10*/ … are hex byte offsets) and field widths — room states only 0x18 explicitly:

  | offset | field | width |
  |---|---|---|
  | 0x00 | s_inodes_count | le32 |
  | (T2 Q2 asks for this — withheld) | s_blocks_count_lo | le32 |
  | 0x08 | s_r_blocks_count_lo | le32 |
  | 0x0C | s_free_blocks_count_lo | le32 |
  | 0x10 | s_free_inodes_count | le32 |
  | 0x14 | s_first_data_block | le32 |
  | 0x18 | s_log_block_size (ROOM-stated) | le32 |
  | 0x1C | s_log_cluster_size | le32 |
  | 0x20 | s_blocks_per_group | le32 |
  | 0x24 | s_clusters_per_group | le32 |
  | 0x28 | s_inodes_per_group | le32 |
  | 0x2C | s_mtime | le32 |
  | 0x30 | s_wtime | le32 |
  | 0x34 | s_mnt_count | le16 |
  | 0x36 | s_max_mnt_count | le16 |
  | 0x38 | s_magic | le16 |
  | 0x3A | s_state | le16 |
  | 0x3C | s_errors | le16 |
  | 0x3E | s_minor_rev_level | le16 |
  | 0x40 | s_lastcheck | le32 |
  | 0x44 | s_checkinterval | le32 |
  | 0x48 | s_creator_os | le32 |
  | 0x4C | s_rev_level | le32 |
  | 0x50 | s_def_resuid | le16 |
  | 0x52 | s_def_resgid | le16 |

  Fields after 0x52 (first inode, inode size, feature flags, UUID, volume name, …) are elided by the room as "(...)": not stated.

- What it proves — ROOM: block size, block count, inode count, free blocks/inodes, inode size, where the FS was last mounted, when it was created (`dumpe2fs` output: "not only the block size but also block count, inodes, free inodes, and the inode size"; "a description, where the file system is mounted, the inodes and blocks available to write data, which ones are free, the size of each block, and when it was created"). FIGURE (dumpe2fs): Filesystem volume name `ext4_partition`; Last mounted on `/mnt/ext4_partition`; magic `0xEF53`; features line visible as `has_journal ext_attr resize_inode dir_index filetype needs_recovery extent 64bit flex_bg sparse_super larg` (cut off at the right edge of the screenshot) continuing on the next line with `ra_isize metadata_csum` — the cut-off middle part (SUPPLIED guess: large_file huge_file dir_nlink ext…) is not readable; Inode count 25600; Block count 25600; Reserved block count 1280; Free blocks 22952; Free inodes 25587; First block 0; Block size 4096; Blocks per group 32768; Inodes per group 25600; Inode blocks per group 1600; Flex block group size 16; Group descriptor size 64; Reserved GDT blocks 12; Filesystem created `Fri Nov 29 00:04:22 2024`; Last mount/write time `Tue Dec 10 00:07:08 2024`; Mount count 3; Maximum mount count -1; First inode 11; Inode size 256; Required/Desired extra isize 32; Journal inode 8; Default directory hash half_md4.
- What it does NOT prove — SUPPLIED: nothing about individual files; mount/write times are file-system-wide and are rewritten on every mount; `s_wtime`/`s_mtime` do not survive a re-mount, so they are weak timeline anchors; the volume label and "last mounted on" path are trivially editable (`tune2fs -L`, or by mounting elsewhere).
- How the room parses it — ROOM, verbatim: `sudo dd if=/dev/loop0 bs=1024 count=1 skip=1 | hexdump -C` (raw), `sudo dumpe2fs /dev/loop0` (human-readable). Cross-check offered by the room: the hexdump shows `02 00 00 00` boxed at 0x18; `dumpe2fs` shows `Block size: 4096`.
- Caveats — SUPPLIED: (1) the room never mentions backup superblocks; with `sparse_super` (set on this volume per the figure) copies live in block groups 0, 1 and powers of 3, 5, 7 — `dumpe2fs` lists them as "Backup superblock at …", and `mke2fs -n` / `e2fsck -b` use them; a wiped primary superblock is therefore not fatal. (2) Reading with `bs=1024 skip=1` works for any ext block size because the primary superblock is always at byte 1024; with 1 KiB blocks it is block 1, with 4 KiB blocks it sits inside block 0 (room does not say this). (3) `dumpe2fs` on a mounted, dirty volume shows `needs_recovery`, which the figure indeed shows — a hint the image was taken from a live mount, not a clean acquisition.

### 2.2 Block groups / group descriptor table

- What it is — ROOM: "EXT4 first divides the file system space into blocks of equal size (1024, 2048, 4096). Consequential blocks are grouped together, and each group must have the same number of blocks except for the last one, which will have the remaining blocks left. Blocks are also numbered from 0 to N." "Data is kept in blocks, which are gathered together as block groups."
- Where it lives — ROOM (figure only): the second Task 2 diagram places "Group Descriptors" immediately after "Super block" inside a block group, followed by Block Bitmap, Inode Bitmap, Inode Table, Data Blocks. Byte offsets: not stated. FIGURE (dumpe2fs): Group descriptor size 64; Reserved GDT blocks 12; Blocks per group 32768; Flex block group size 16.
- What it proves — SUPPLIED: where each group's bitmaps and inode table start, free counts per group, and (with `flex_bg`) that metadata for 16 groups is packed together — needed to translate an inode number to an on-disk location.
- What it does NOT prove — SUPPLIED: nothing about content or timeline.
- How the room parses it — the room does not parse the GDT; `dumpe2fs` (whose full output lists every group) is run but the figure is cut before the group listing.
- Caveats — SUPPLIED: with 4 KiB blocks and 32768 blocks/group a group spans 128 MiB; this 100 MiB volume therefore has a single block group (25600 blocks < 32768), which is why the room's "block number = offset / 4096" shortcut works without any group arithmetic.

### 2.3 Inodes and the inode table (`struct ext4_inode`)

- What it is — ROOM: "Inodes contain metadata for files, including ownership, permissions, and pointers to a data block." "Each file and directory in the EXT4 file system is assigned an inode number, which will be then linked to an ext4_inode struct that typically occupies 256 bytes and contains information such as i_mode (file type/permissions), i_uid (owner), i_size_lo (file size), i_blocks (allocated blocks), i_links_count (hard links), and i_block (data block pointers or extents)."
- Where it lives — ROOM (figure only): the "Inode Table" region of each block group. Per-field offsets: not stated (the inode struct is printed without row markers). Struct listing verbatim:

```
struct ext4_inode {
	__le16	i_mode;		/* File mode */
	__le16	i_uid;		/* Low 16 bits of Owner Uid */
	__le32	i_size_lo;	/* Size in bytes */
	__le32	i_atime;	/* Access time */
	__le32	i_ctime;	/* Inode Change time */
	__le32	i_mtime;	/* Modification time */
	__le32	i_dtime;	/* Deletion Time */
	__le16	i_gid;		/* Low 16 bits of Group Id */
	__le16	i_links_count;	/* Links count */
	__le32	i_blocks_lo;	/* Blocks count */
	__le32	i_flags;	/* File flags */
	union {
		struct {
			__le32  l_i_version;
		} linux1;
		struct {
			__u32  h_i_translator;
		} hurd1;
		struct {
			__u32  m_i_reserved1;
		} masix1;
	} osd1;				/* OS dependent 1 */
	__le32	i_block[EXT4_N_BLOCKS];/* Pointers to blocks */
	__le32	i_generation;	/* File version (for NFS) */
	__le32	i_file_acl_lo;	/* File ACL */
	__le32	i_size_high;
	__le32	i_obso_faddr;	/* Obsoleted fragment address */
	union {
		struct {
			__le16	l_i_blocks_high; /* were l_i_reserved1 */
			__le16	l_i_file_acl_high;
			__le16	l_i_uid_high;	/* these 2 fields */
			__le16	l_i_gid_high;	/* were reserved2[0] */
			__le16	l_i_checksum_lo;/* crc32c(uuid+inum+inode) LE */
			__le16	l_i_reserved;
		} linux2;
		struct {
			__le16	h_i_reserved1;	/* Obsoleted fragment number/size which are removed in ext4 */
			__u16	h_i_mode_high;
			__u16	h_i_uid_high;
			__u16	h_i_gid_high;
			__u32	h_i_author;
		} hurd2;
		struct {
			__le16	h_i_reserved1;	/* Obsoleted fragment number/size which are removed in ext4 */
			__le16	m_i_file_acl_high;
			__u32	m_i_reserved2[2];
		} masix2;
	} osd2;				/* OS dependent 2 */
	__le16	i_extra_isize;
	__le16	i_checksum_hi;	/* crc32c(uuid+inum+inode) BE */
	__le32  i_ctime_extra;  /* extra Change time      (nsec< 2 | epoch) */
	__le32  i_mtime_extra;  /* extra Modification time(nsec< 2 | epoch) */
	__le32  i_atime_extra;  /* extra Access time      (nsec< 2 | epoch) */
	__le32  i_crtime;       /* File Creation time */
	__le32  i_crtime_extra; /* extra FileCreationtime (nsec< 2 | epoch) */
	__le32  i_version_hi;	/* high 32 bits for 64-bit version */
	__le32	i_projid;	/* Project ID */
};
```

  (Note: the room's listing reads "nsec< 2" where the kernel source has "nsec << 2"; the "<<" was lost in rendering.) FIGURE/ROOM: `Inode size: 256`, `First inode: 11`, `Size of extra inode fields: 32`, root directory is inode 2 (`debugfs stat .` → "Inode: 2 Type: directory Mode: 0755 Flags: 0x80000 … Links: 3 Blockcount: 8 … EXTENTS: (0):15"). Flag 0x80000 is shown but not explained (SUPPLIED: it is EXT4_EXTENTS_FL — the inode uses an extent tree).
- What it proves — ROOM: type and permissions (`i_mode`), owner/group, size, link count, block count, generation, version, the four timestamps with sub-second parts, the inode checksum, and the extents (block ranges) holding the data. The chmod experiment proves that a metadata-only change bumps `ctime` and `Version` (0x…03 → 0x…04) and changes the inode checksum, while `atime/mtime/crtime` stay put.
- What it does NOT prove — SUPPLIED: the file name (names live in directory entries, not in the inode — the room says "we can gather the inode number … which can help us identify the file regardless of its name"); who made the change (uid is the owner, not the actor); nothing after deletion once the extent tree is zeroed.
- How the room parses it — ROOM, verbatim: `ls -al /mnt/ext4_partition`; `sudo stat test_file2.txt`; `sudo debugfs /dev/loop0` then `stat .` and `stat <11>` (angle brackets = inode number); `sudo chmod 755 /mnt/ext4_partition/test_file2.txt` then re-run `stat <11>`.
- Caveats — ROOM: none beyond the timestomping discussion. SUPPLIED: (1) the room's own screenshots are internally inconsistent (ls shows `test_file2.txt` as 0 bytes / `-rw-r--r--`, `stat` shows 9 bytes / 0755, the first `debugfs stat <11>` shows 0777 — they were captured at different times); teach students that live-VM artefacts drift. (2) `debugfs` also has `set_inode_field`, which can rewrite `crtime`/`ctime` directly on the block device — the very "unforgeable" fields the room relies on (this is the technique in the linked inversecos article). (3) `i_checksum` (metadata_csum) will mismatch after such raw edits unless the attacker also fixes it — a detection lever the room does not mention.

### 2.4 Block bitmap and inode bitmap

- What it is — ROOM: "Bitmaps track the status of the assignment of blocks and inodes." Diagram places "Block Bitmap" and "Inode Bitmap" after Group Descriptors and before the Inode Table.
- Where it lives — offsets: not stated.
- What it proves / does not prove — SUPPLIED: whether a block or inode is currently allocated; an unallocated block that still contains data is the basis of the room's recovery exercise (Autopsy's `$Unalloc (1)` entry is this space). It does not tell you which file the block belonged to.
- How the room parses it — not parsed directly; `dumpe2fs` reports the aggregate free counts (Free blocks 22952 / Free inodes 25587) that derive from the bitmaps.
- Caveats — SUPPLIED: bitmaps only say "free/in use"; never treat a "free" block as empty.

### 2.5 Directory entries

- What it is — ROOM: "File names are related to inodes through directory structures." "The file name is then linked to the inode within the directory structure." Nothing more; `ext4_dir_entry_2` is not shown. Offsets: not stated.
- What it proves — ROOM (implicit): the name-to-inode mapping (`ls -al` output; Autopsy listing shows `[current folder]`, `[parent folder]`, `lost+found`).
- What it does NOT prove — SUPPLIED: after deletion the name may remain as slack in the directory block (dentry unlinked by lengthening the previous record) — this is how `fls -d` / Autopsy show deleted names; the room's deleted file appears in Autopsy only as `OrphanFile-14` under `$OrphanFiles`, i.e. an inode with no surviving name.
- How the room parses it — `ls -al`, `debugfs stat .` (directory inode 2, `Links: 3`, size 4096, one extent at block 15), Autopsy Data Sources tree.
- Caveats — none stated.

### 2.6 Extents vs block pointers

- What it is — ROOM: `i_block[EXT4_N_BLOCKS]` "Pointers to blocks" / "data block pointers or extents"; `debugfs stat` prints `EXTENTS: (0):15` for the root directory and `(0):24577` for inode 11 (meaning logical block 0 → physical block N). The comparison table rows do not mention extents; the feature list in the figure shows `extent`.
- Where it lives — inside the inode's `i_block` area (60 bytes in the kernel; size not stated by the room).
- What it proves — ROOM (implicit): the exact physical block(s) of a file's data, which is what `dd bs=4096 skip=<block>` reads back.
- What it does NOT prove — SUPPLIED: once a file is deleted on ext4 the extent header/tree in the inode is zeroed, so the inode no longer points anywhere; this is why the room recovers by content search rather than by inode.
- How the room parses it — `debugfs` `stat <inode>` (EXTENTS section); manual: `strings -t d` offset ÷ 4096.
- Caveats — SUPPLIED: multi-extent (fragmented) files cannot be recovered with a single `dd … count=1`; the room's example is a 1-block file.

### 2.7 Journal (EXT3/EXT4)

- What it is — ROOM: "Some of the features that have been incorporated in the EXT3 and extended into EXT4 include journaling. This helps in the prevention of corruption by making a list of changes that are to be made on the disk recently. This is why they are both targets of a forensic investigation. As we will learn, journals of deleted files can have metadata, events, and data that can be processed or recovered." Comparison table: EXT2 "No", EXT3 "Yes (metadata, optional data)", EXT4 "Yes (with checksums for integrity)".
- Where it lives — FIGURE: `Journal inode: 8`; feature `has_journal`. Offsets: not stated.
- What it proves / does not — SUPPLIED: the journal can hold pre-deletion copies of inode-table blocks (old timestamps, old extent trees), which `ext4magic`/`extundelete` mine; in the default `data=ordered` mode it holds metadata only, so file content is usually not in the journal; it is circular and short-lived.
- How the room parses it — not parsed. No `debugfs logdump`, no `jls/jcat`, no `ext4magic`. (Despite "as we will learn", the room never returns to the journal.)
- Caveats — SUPPLIED: a mounted-dirty image shows `needs_recovery`; replaying the journal (mounting rw, or `e2fsck`) alters evidence — work on a read-only copy.

### 2.8 Deleted files and what deletion changes

- What it is — ROOM: "Deletion Time (dtime) For deleted files, EXT inodes can store the time the file was deleted." "The EXT4 file system works by writing on available blocks, so files that have not been overwritten can be recovered. … We can do that if we know the inode number or scanning them with tools." "Usually, recovery tools scan the system for patterns of bytes and inodes in order to recover files."
- Where it lives — `i_dtime` in the inode (offset not stated); data remains in now-free blocks. Autopsy view: `File Views > Deleted Files > File System (1)` and `$OrphanFiles (1)` showing `OrphanFile-14`, Size 0, File Name Allocation: Unallocated, Metadata Allocation: Unallocated, MIME `application/octet-stream`.
- What it proves — ROOM: that data survives deletion until overwritten; recovered block content in the demo: `AAAAAAAA / BBBBBBBB / ZZZZZZZZ / You find the content!`.
- What it does NOT prove — SUPPLIED: a carved block has no name, owner or timestamps attached; attribution needs a directory-slack name or a journal copy of the inode.
- How the room parses it — ROOM, verbatim: `sudo strings -t d /dev/loop0 | grep -i "AAAAAAAA"` → `100671488 AAAAAAAA`; `echo $((100671488 / 4096))` → `24578`; `sudo dd if=/dev/loop0 bs=4096 skip=24578 count=1 of=/tmp/recovered_file`; `cat /tmp/recovered_file`. The room calls 24578 "the offset within the clock group" (typo for block group; it is the physical block number).
- How deletion differs EXT2/EXT3/EXT4 — NOT STATED by the room. SUPPLIED: ext2 leaves the block pointers in the deleted inode (so inode-based undelete via `debugfs lsdel`/`icat` works); ext3 and ext4 zero the pointer/extent area (and set `i_dtime`, link count 0) on unlink, so recovery must rely on the journal (old inode copies) or on content carving — exactly the fallback the room teaches. ext4's `extent` flag stays set, which is one way tools recognise a wiped ext4 inode.
- Caveats — SUPPLIED: `strings -t d` reports the byte offset of the *string*, not the block start; the integer division only works because the string sits at the start of the block. If the string were mid-block the `dd` would still return the right block (division floors), but a file spanning blocks needs `count>1` and may not be contiguous.

### 2.9 Timestamps (incl. crtime on EXT4)

- What it is — ROOM, verbatim list: "Access Time (atime) Records the last time a file was read. / Modification Time (mtime) Indicates the last time the content of the file was modified. / Change Time (ctime) Tracks the last time the file's metadata (e.g., permissions) was modified. / Deletion Time (dtime) For deleted files, EXT inodes can store the time the file was deleted. / Birth Time (crtime) Represents the time the file was originally created (only available in EXT4)."
- Where it lives — inode fields `i_atime`, `i_ctime`, `i_mtime`, `i_dtime`, `i_crtime` plus `*_extra` fields (the struct comments say "(nsec< 2 | epoch)"); per-field offsets not stated. `debugfs` prints them as `ctime: 0x675789e1:914449a4 -- Tue Dec 10 00:22:57 2024` (hex seconds : hex extra word — decode not explained by the room). `stat` prints Access/Modify/Change/Birth with nanoseconds.
- What it proves — ROOM: normal file → all four equal (`2025-01-05 06:33:35.389419110`); timestomped file → Access/Modify `2016-01-01 12:00:00.000000000`, Change `2025-01-05 06:33:55.001578638`, Birth `2025-01-05 06:33:42.401109261`. "The access and modify time corresponds to the year 2016 … but the change and birth time are from 2025 … the file has been tampered with a 'fake' date." Detection: a `ctime`/`crtime` later than `mtime`/`atime`, round-number timestamps with zero nanoseconds, and `find -newerct` windows.
- What it does NOT prove — ROOM: "the time can only be changed to the time on the system, so an attacker could change the value by modifying the time on the system" (i.e. a shifted system clock defeats the ctime check). SUPPLIED: `debugfs set_inode_field` can rewrite crtime/ctime directly; `noatime`/`relatime` mount options make atime unreliable as "last read"; `cp -p`, `tar`, `rsync -a` legitimately preserve old mtimes, so "old mtime, new crtime" is not proof of malice on its own.
- How the room parses it — ROOM, verbatim: `ls -l`; `stat normal_file.txt`; `stat timestomped_file.txt`; `sudo find /mnt/ext4_time -newerct "2025-01-01" ! -newerct "2025-01-06" -ls` ("search for all files that have a change timestamp between January 1st and January 6th 2025"); Autopsy listing columns Modified/Change/Access/Created and the File Metadata tab.
- Caveats — ROOM: "not rely on commands like ls to analyze the files." Also note the room's definition "Timestomping is a technique that modifies the timestamps of a file (the modify, access, create, and change times)" while its own demo only manages to alter atime/mtime — worth teaching as the point.

### 2.10 Hard links, symbolic links, extended attributes

- Hard links — ROOM: only `i_links_count` "(hard links)" and the `Links:` line in `stat`/`debugfs` (root dir `Links: 3`, regular file `Links: 1`). No exercise.
- Symbolic links — not covered.
- Extended attributes / ACLs — ROOM: only `i_file_acl_lo` "File ACL" in the struct and `File ACL: 0` in debugfs output; FIGURE: feature `ext_attr`, default mount options `user_xattr acl`. No exercise. (SUPPLIED: xattrs can carry `security.selinux`, capabilities, and attacker-planted data; `getfattr -d` / `debugfs ea_list`.)

## 3. Tools and commands

| # | Task | Command (verbatim) | What it outputs (per the room) |
|---|---|---|---|
| 1 | T2 | `sudo lsblk` | Block devices: `loop0 7:0 0 100M 0 loop /mnt/ext4_partition`, loop1–3 snap mounts, `nvme0n1 259:0 0 40G 0 disk` / `nvme0n1p1 259:1 0 40G 0 part /` |
| 2 | T2 | `sudo dd if=/dev/loop0 bs=1024 count=1 skip=1 \| hexdump -C` | Raw primary superblock (1024 bytes from byte 1024); figure boxes `02 00 00 00` at 0x18 = `s_log_block_size` |
| 3 | T2 | `sudo dumpe2fs /dev/loop0` | Human-readable superblock (`dumpe2fs 1.47.0 (5-Feb-2023)`): volume name, last mounted on, UUID, magic 0xEF53, features, counts, block size 4096, inode size 256, created/mount/write times, journal inode 8, … |
| 4 | T2 | `sudo debugfs /dev/loop0` then `stat .` | Inode 2 (root dir) record: Type directory, Mode 0755, Flags 0x80000, Links 3, Blockcount 8, ctime/atime/mtime/crtime, extra fields 32, checksum, `EXTENTS: (0):15` |
| 5 | T3 | `ls -al /mnt/ext4_partition` | `test_dir`, `test_file.txt` (28 B), `test_file2.txt` (0 B) |
| 6 | T3 | `sudo stat test_file2.txt` (cwd `/mnt/ext4_partition`) | Size 9, Blocks 8, IO Block 4096, Device 7,0, Inode 11, Links 1, mode 0755, uid/gid root, Access/Modify/Change/Birth with ns |
| 7 | T3 | `sudo debugfs /dev/loop0` then `stat <11>` | `debugfs 1.47.0 (5-Feb-2023)`; inode 11 record: Type regular, Mode 0777, Generation 555018483, Version 0x…03, Size 9, Links 1, Blockcount 8, four timestamps, checksum 0x6e0c2268, `EXTENTS: (0):24577` |
| 8 | T3 | `sudo chmod 755 /mnt/ext4_partition/test_file2.txt` then `sudo debugfs /dev/loop0` / `stat <11>` | Mode now 0755, Version 0x…04, ctime updated (`Fri Feb 7 16:01:48 2025`), atime/mtime/crtime unchanged, checksum now 0x0d1497d0 |
| 9 | T3 | `sudo strings -t d /dev/loop0 \| grep -i "AAAAAAAA"` | `100671488 AAAAAAAA` (decimal byte offset of the string) |
| 10 | T3 | `echo $((100671488 / 4096))` | `24578` (block number) |
| 11 | T3 | `sudo dd if=/dev/loop0 bs=4096 skip=24578 count=1 of=/tmp/recovered_file` | `1+0 records in / 1+0 records out / 4096 bytes (4.1 kB, 4.0 KiB) copied` |
| 12 | T3 | `cat /tmp/recovered_file` | `AAAAAAAA` / `BBBBBBBB` / `ZZZZZZZZ` / `You find the content!` |
| 13 | T4 | `ls -l` (in `/mnt/ext4_time`) | `normal_file.txt` 22 B `Jan 5 06:33`; `timestomped_file.txt` 31 B `Jan 1 2016`; owner `analyst` |
| 14 | T4 | `stat normal_file.txt` | Inode 1024624, Device 259,1, all four timestamps `2025-01-05 06:33:35.389419110 +0000` |
| 15 | T4 | `stat timestomped_file.txt` | Inode 1024627; Access/Modify `2016-01-01 12:00:00.000000000`; Change `2025-01-05 06:33:55.001578638`; Birth `2025-01-05 06:33:42.401109261` |
| 16 | T4 | `sudo find /mnt/ext4_time -newerct "2025-01-01" ! -newerct "2025-01-06" -ls` | Lists inode, blocks, mode, links, owner, size, date, path for the dir (1024591) and both files — the timestomped file is listed despite its 2016 display date |
| 17 | T5 | `cd /home/ubuntu/autopsy/autopsy-4.21.0/bin` then `./autopsy --nosplash` (or desktop shortcut) | Launches Autopsy 4.21.0 GUI |
| 18 | T5 | (GUI) New Case → name `thm-case`, base dir `/home/ubuntu`, Single-User → Finish → "Generate new host name based on data source name" → Disk Image or VM File → `/home/ubuntu/ext4_case.img` → Next (default ingest) → OK on "Ingest Module Startup Failure" → Finish | Case tree `Data Sources > ext4_case.img_1 Host > ext4_case.img` |
| — | T5 | `extundelete` | Named only ("Linux command-line tools such as debugfs and extundelete"); no command shown |

Not used anywhere in the room: `fsstat`, `fls`, `istat`, `icat`, `blkcat`, `xxd`, `ext4magic`, `tune2fs`, `e2fsck`, `mount -o ro,loop`, hashing. Versions shown: e2fsprogs `1.47.0 (5-Feb-2023)` (debugfs/dumpe2fs), Autopsy `4.21.0`.

## 4. Evidence used

All evidence lives inside the THM lab VM (split-screen, "around 2 minutes to load"); there are NO downloadable task files.

| Evidence | Where | Size | Contents (as shown) | Downloadable |
|---|---|---|---|---|
| Loop-device EXT4 volume | `/dev/loop0` mounted at `/mnt/ext4_partition` | 100M (lsblk); 25600 × 4096-byte blocks; single block group | `test_dir/`, `test_file.txt` (28 B), `test_file2.txt` (inode 11, 9 B / 0 B depending on screenshot), a deleted file whose block 24578 holds `AAAAAAAA / BBBBBBBB / ZZZZZZZZ / You find the content!`; volume label `ext4_partition`, created `Fri Nov 29 00:04:22 2024` | No (VM only) |
| Timestamp exercise directory | `/mnt/ext4_time` (Device 259,1 = the root disk `nvme0n1p1`, i.e. NOT a separate image) | n/a | `normal_file.txt` (22 B, inode 1024624), `timestomped_file.txt` (31 B, inode 1024627), owner `analyst` (uid 1001) | No |
| Autopsy disk image | `/home/ubuntu/ext4_case.img` | not stated | Autopsy listing: `$OrphanFiles`, `$Unalloc`, `[current folder]`, `[parent folder]`, `lost+found` (16384 B), `normal_file.txt` (22 B), `timestomped_file.txt` (31 B); one deleted orphan `OrphanFile-14` (0 B). Note the image's timestomped dates read `2017-01-01 12:00:00 UTC` (not 2016 as in the live directory) — it is a different copy of the scenario | No |
| Practical file system | mounted at `/mnt/ext_exercises` | not stated | not shown; contains one timestomped file and one deleted file whose content starts with `FFFFFFFFFF` | No |
| Host file | `/etc/passwd` on the VM root FS | n/a | Used for T3/T4 questions (inode number, btime) | No |
| Tooling | `/home/ubuntu/autopsy/autopsy-4.21.0/bin/autopsy`, e2fsprogs 1.47.0 | | | |

## 5. Lab design worth reusing

1. **Warm-up: identify the volume** — `sudo lsblk` to find the loop device and its mount point; student learns to work on `/dev/loop0` (device) rather than the mount.
2. **Superblock three ways** — print the kernel struct; count fields to derive an offset (7th le32 → 0x18); `dd bs=1024 skip=1 | hexdump -C` and box the bytes; decode little-endian; apply 2^(10+n); confirm with `dumpe2fs`. Extendable: have students locate `s_magic` (0x38 → `53 ef`) and the UUID bytes and match them against `dumpe2fs`.
3. **Inode dissection** — `debugfs` `stat .` on inode 2, then `ls -al` → `stat <file>` → `debugfs stat <N>` on a regular file; compare fields with the struct.
4. **Cause-and-effect on timestamps** — `chmod 755` then re-`stat`: only `ctime` (and inode Version/checksum) move. Good pattern: "predict which timestamp changes, then verify".
5. **Manual undelete by carving** — known content string → `strings -t d | grep` → offset ÷ block size → `dd bs=4096 skip=N count=1` → `cat`. Reusable as a template for any small deleted file with a known marker; requires a single-block, contiguous file.
6. **Timestomping demo + detection** — a pair of files, one with `touch -d`-style 2016 atime/mtime; compare `ls -l` vs `stat`; explain why ctime/crtime lag; `find -newerct A ! -newerct B -ls` as the hunting query; link to the anti-forensics article for the system-clock caveat.
7. **Same case in Autopsy** — New Case wizard (Single-User, base dir), Disk Image data source, accept default ingest, dismiss Windows-only module failures (aLEAPP, iLEAPP, YARA), browse Data Sources, read Modified/Change/Access/Created columns, File Metadata tab for inode number, Deleted Files / $OrphanFiles for the orphan inode.
8. **Unguided practical** — new mount (`/mnt/ext_exercises`): (a) find the timestomped file and report its true creation (birth) time; (b) recover a deleted file by a known prefix (`FFFFFFFFFF`) and read the flag. Mirrors steps 5 and 6 exactly.
9. **Questions that force use of the VM** — inode number and btime of `/etc/passwd` (root FS), so students run `stat` on a real system file.

## 6. Question patterns

(Answers deliberately not recorded. None of the answer boxes carries a placeholder/format hint beyond what is in the question text.)

- Task 1: "Let's get started!" — no answer; shown as "Correct Answer" (click-to-complete).
- Task 2 Q1: "What is the member of the ext4_super_block struct that holds the offset value to the first data block?" — free text (struct member name).
- Task 2 Q2: "What is the offset where we can find the member s_blocks_count_lo in the ext4_super_block struct? (decimal format)" — number, decimal.
- Task 3 Q1: "What is the inode number for the file /etc/passwd in the VM?" — number.
- Task 4 Q1: "What is the btime for the file /etc/passwd?" — timestamp; format not stated.
- Task 5 Q1: "Select Data Sources > ext4_case.img_1 Host > ext4_case.img and select the file normal_file.txt. Analyze the data in the File Metadata tab on the bottom pane. What is the inode number of the file?" — number.
- Task 5 Q2: "What is the creation time of the file timestomped.txt? (Format: YYYY-MM-DD hh:mm:ss)" — timestamp in the stated format. (The file is actually named `timestomped_file.txt` in the image.)
- Task 6 Q1: "Identify the timestomped file in the mounted file system in /mnt/ext_exercises. What is the original creation date of the file? (Format: YYYY-MM-DD hh:mm:ss)" — timestamp in the stated format.
- Task 6 Q2: "What is the flag in the deleted file that starts with the characters "FFFFFFFFFF" in the mounted file system in /mnt/ext_exercises?" — flag string (format not stated).
- Task 7: "Click to finish your journey through the EXT file system fundamentals and complete the room." — no answer; click Check.

## 7. Figures the room uses

Task 1 has only UI icons (lab-machine card). Task 3, 4, 6, 7 have no images.

**Task 2**

- **Fig 2.1 — "A diagram of block groups containing blocks in the EXT4 file system going from 0 to N"** (1140×375). Dark navy background. Top row: four rounded pill labels "Block Group 0", "Block Group 1", "Block Group 2", "Block Group N". Below each, a rounded rectangle stacking "Block 0 / Block 1 / Block 2 / Block N" (white bold text). Bright-green right-pointing arrows connect the four columns. Details for redraw: the Block Group 2 column mistakenly reads "Block 1, Block 1, Block 2, Block N" (typo); the Block Group N column has only three rows ("Block 0, Block 1, Block 2") — shorter, to show the last group holding "the remaining blocks".
- **Fig 2.2 — "A descriptive diagram of the EXT4 file system struct"** (1140×330). A label "Partition" centred above a dashed green rounded box. Inside the box, one row of dark cells: "Boot Sector | Block Group 0 | .... | Block Group N | Unused Sectors". Two thin green lines fan down from the block-group row to a second, wider row of cells: "Super block | Group Descriptors | Block Bitmap | Inode Bitmap | Inode Table | Data Blocks". (Note: the Sleuth Kit / kernel layout; no reserved-GDT cell.)
- **Fig 2.3 — "An output of the command sudo dd if=/dev/loop0 bs=1024 count=1 skip=1 | hexdump -C highlighting the value 2"** (667×416). Black terminal, prompt `analyst@tryhackme:~$`. Rows 0x00–0x140 of the superblock; an orange box around `02 00 00 00` at 0x18. Transcription of the visible rows (verbatim from the figure):

```
00000000  00 64 00 00 00 64 00 00  00 05 00 00 a8 59 00 00  |.d...d.......Y..|
00000010  f3 63 00 00 00 00 00 00  02 00 00 00 02 00 00 00  |.c..............|
00000020  00 80 00 00 00 80 00 00  00 64 00 00 2c 86 57 67  |.........d..,.Wg|
00000030  2c 86 57 67 03 00 ff ff  53 ef 01 00 01 00 00 00  |,.Wg....S.......|
00000040  06 05 49 67 00 00 00 00  00 00 00 00 01 00 00 00  |..Ig............|
00000050  00 00 00 00 0b 00 00 00  00 01 00 00 3c 00 00 00  |............<...|
00000060  c6 02 00 00 6b 04 00 00  ee ca 17 a6 fd 6a 42 88  |....k........jB.|
00000070  88 a1 db 14 04 37 ef 3f  65 78 74 34 5f 70 61 72  |.....7.?ext4_par|
00000080  74 69 74 69 6f 6e 00 00  2f 6d 6e 74 2f 65 78 74  |tition../mnt/ext|
00000090  34 5f 70 61 72 74 69 74  69 6f 6e 00 00 00 00 00  |4_partition.....|
000000a0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
000000c0  00 00 00 00 00 00 00 00  00 00 00 00 00 0c 00 00  |................|
000000d0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
000000e0  08 00 00 00 00 00 00 00  00 00 00 00 06 a7 bb b6  |................|
000000f0  03 5a 45 5b a2 dc f1 5f  5f 2e f8 78 01 01 40 00  |.ZE[..__..x..@.|
00000100  0c 00 00 00 00 00 00 00  06 05 49 67 0a f3 03 00  |..........Ig....|
00000110  04 00 00 00 00 00 00 00  00 00 00 00 0a 00 00 00  |................|
00000120  14 00 00 00 0a 00 00 00  0f 00 00 00 1f 00 00 00  |................|
00000130  19 00 00 00 e7 03 00 00  6f 06 00 00 00 00 00 00  |........o.......|
00000140  00 00 00 00 00 00 00 00  00 00 00 00 00 40 00 00  |.............@..|
```

  Useful for an SVG redraw: annotate 0x00 `00 64 00 00` = 25600 inodes, 0x04 = 25600 blocks, 0x18 `02` = log block size, 0x38 `53 ef` = magic 0xEF53, 0x68–0x77 = UUID `eeca17a6-fd6a-4288-88a1-db140437ef3f` (matches the dumpe2fs figure), 0x78 = volume name `ext4_partition`, 0x88 = last-mounted path `/mnt/ext4_partition`. (These annotations are SUPPLIED cross-checks; the room only annotates 0x18.)
- **Fig 2.4 — "Displaying the output of the command sudo dumpe2fs /dev/loop0, showing and highlighting stats"** (1055×897). Black terminal, `dumpe2fs 1.47.0 (5-Feb-2023)`. Orange boxes around: `Last mounted on: /mnt/ext4_partition`, `Inode count: 25600` + `Block count: 25600`, `Free blocks: 22952` + `Free inodes: 25587`, `Block size: 4096`, `Filesystem created: Fri Nov 29 00:04:22 2024`. Full visible key/values are listed in §2.1 and §8.

**Task 5 (Autopsy 4.21.0 screenshots, all light-grey Java Swing UI)**

- Fig 5.1 "The Welcome screen from Autopsy highlighting the new case button" (1157×707) — alt text only (not inspected in detail): Autopsy welcome dialog, New Case button boxed.
- Fig 5.2 "The New Case screen from Autopsy" (1143×708) — inspected: "New Case Information" wizard, Steps: 1 Case Information, 2 Optional Information; fields Case Name `thm-case`, Base Directory `/home/ubuntu` (both boxed in orange), Case Type Single-User (Multi-User greyed), "Case data will be stored in the following directory: /home/ubuntu/thm-case"; buttons < Back, Next >, Finish, Cancel, Help.
- Fig 5.3 "The New Case screen from Autopsy highlighting the finish button" (1154×697) — alt text only: second wizard step with Finish boxed.
- Fig 5.4 "The Select Host screen from Autopsy highlighting the 'Generate new host name based on data source name' option." (955×652) — alt text only: Add Data Source wizard, Select Host step, that radio option boxed.
- Fig 5.5 "The Add Data Source from Autopsy highlighting the Disk Image or VM button" (1148×698) — alt text only: Select Data Source Type step, "Disk Image or VM File" boxed.
- Fig 5.6 "The Add Data Source from Autopsy highlighting the ext4_case.img file" (881×545) — inspected: wizard steps "1. Select Host, 2. Select Data Source Type, 3. Select Data Source, 4. Configure Ingest, 5. Add Data Source"; an "Open" file chooser over it, Look in `ubuntu`, entries autopsy, Desktop, Documents, Downloads, Music, Pictures, Public, snap, Templates, thm-case, Videos and the file `ext4_case.img` (boxed); Files of Type "All Supported Types"; Open / Cancel.
- Fig 5.7 "A warning message highlighting the ok button" (438×220) — inspected: dialog titled "Ingest Module Startup Failure": "Unable to start up one or more ingest modules, ingest cancelled. Please disable the failed modules or fix the errors before restarting ingest. Errors: Android Analyzer (aLEAPP): aLeapp module requires windows. iOS Analyzer (iLEAPP): iLeapp module requires windows. YARA Analyzer: The YARA ingest module is only available on 64bit Windows."
- Fig 5.8 "The main Autopsy screen highlighting the left panel and the file to examine on the right" (1155×708) — alt text only (same layout as Fig 5.9).
- Fig 5.9 "The main Autopsy screen highlighting the left panel with the case, source file and at the right, showing the artifacts" (1149×704) — inspected: toolbar (Add Data Source, Images/Videos, Communications, Geolocation, Timeline, Discovery, Keyword Lists, Keyword Search); Tree: Data Sources > ext4_case.img_1 Host > ext4_case.img > `$OrphanFiles (1)`, `$Unalloc (1)`, `lost+found (2)`; File Views (File Types, Deleted Files, File Size); Data Artifacts; Analysis Results; OS Accounts; Tags; Score; Reports. Listing `/img_ext4_case.img`, "7 Results", columns Name | S | C | O | Modified Time | Change Time | Access Time | Created Time; rows `$OrphanFiles`, `$Unalloc`, `[current folder]`, `[parent folder]`, `lost+found`, `normal_file.txt`, `timestomped_file.txt` (both boxed). Bottom pane "Data Content" tabs: Hex, Text, Application, File Metadata, OS Account, Data Artifacts, Analysis Results, Context, Annotations, Other Occurrences.
- Fig 5.10 "The Autopsy shows the timestamps for the file normal_file.txt" (896×230) — inspected: crop of the listing with a Size column; `normal_file.txt` row selected; `timestomped_file.txt` Modified and Access cells (`2017-01-01 12:00:00 UTC`) boxed in orange while Change/Created show 2025-01-06.
- Fig 5.11 "The Autopsy shows the deleted file" (1140×700) — inspected: Tree with `Deleted Files > File System (1)` boxed; listing "1 Result": `OrphanFile-14` (red-x icon), all four times `2025-01-06 03:35:2x UTC`, Size 0, Flags(Dir) Unallocated; bottom pane on File Metadata tab: Name `/img_ext4_case.img/$OrphanFiles/OrphanFile-14`, Type File System, MIME `application/octet-stream`, Size 0, File Name Allocation Unallocated, Metadata Allocation Unallocated.

## 8. Key facts worth quoting

- History (ROOM): EXT first introduced April 1992; supported 2 GB file systems; "first to incorporate the Virtual File System (VFS)"; lineage EXT → EXT2 → EXT3 → EXT4.
- Comparison table (ROOM, verbatim): Maximum File Size EXT2 2 TiB / EXT3 2 TiB / EXT4 16 TiB; Maximum Volume Size 32 TiB / 32 TiB / 1 EiB; Journaling No / Yes (metadata, optional data) / Yes (with checksums for integrity); Backward Compatibility N/A / Can mount EXT2 / Can mount EXT2 & EXT3. (SUPPLIED caveat: ext2/3 limits depend on block size — 2 TiB files and 32 TiB volumes are the 8 KiB-block maxima; with 4 KiB blocks it is 2 TiB / 16 TiB.)
- Block sizes (ROOM): 1024, 2048, 4096; block size = 2^(10 + s_log_block_size); demo volume: s_log_block_size = 2 → 4096.
- Superblock location (ROOM by command): byte 1024, length 1024 (`dd bs=1024 count=1 skip=1`). `s_log_block_size` at 0x18. Little-endian.
- Magic number: `0xEF53` — FIGURE only (dumpe2fs "Filesystem magic number: 0xEF53"; hexdump bytes `53 ef` at 0x38). Not written in the room's prose.
- Demo volume numbers (FIGURE): 25600 inodes, 25600 blocks, 1280 reserved, 22952 free blocks, 25587 free inodes, first block 0, block size 4096, blocks per group 32768, inodes per group 25600, inode blocks per group 1600, flex_bg size 16, group descriptor size 64, reserved GDT blocks 12, inode size 256, first inode 11, required/desired extra isize 32, journal inode 8, directory hash half_md4, revision 1 (dynamic), state clean, errors Continue, OS Linux, mount count 3, max mount count -1, check interval 0, lifetime writes 6629 kB.
- Inode facts (ROOM): `ext4_inode` "typically occupies 256 bytes"; root directory = inode 2; first user inode = 11 (FIGURE); "Size of extra inode fields: 32"; flag 0x80000 on both inodes shown.
- Timestamps EXT4 has (ROOM): atime, mtime, ctime, dtime, crtime — crtime "only available in EXT4"; `stat` shows it as "Birth"; extra 32-bit fields hold nanoseconds and epoch bits ("nsec< 2 | epoch").
- What changes on `chmod` (ROOM demo): `i_mode`, `ctime`, inode Version (+1), inode checksum; NOT atime/mtime/crtime.
- Timestomping fingerprint (ROOM demo): atime/mtime `2016-01-01 12:00:00.000000000` vs ctime `2025-01-05 06:33:55.001578638` / crtime `2025-01-05 06:33:42.401109261`; detection `find <dir> -newerct "<from>" ! -newerct "<to>" -ls`; caveat: ctime can only be set to the current system time, so clock manipulation is the bypass.
- Recovery arithmetic (ROOM): string offset 100671488 ÷ 4096 = block 24578; `dd bs=4096 skip=24578 count=1`; recovered 4096 bytes.
- Deletion differences EXT2/3/4: not stated by the room (see §2.8 SUPPLIED).
- Backup superblock locations: not stated by the room (see §2.1 SUPPLIED).
- Versions in the room: e2fsprogs 1.47.0 (5-Feb-2023); Autopsy 4.21.0 at `/home/ubuntu/autopsy/autopsy-4.21.0/bin`; Autopsy modules that fail on Linux: aLEAPP, iLEAPP, YARA.
- External references: Autopsy https://www.autopsy.com/ ; inversecos "Detecting Linux Anti-Forensics" https://www.inversecos.com/2022/08/detecting-linux-anti-forensics.html ; prerequisite rooms: Linux File System Analysis (https://tryhackme.com/r/room/linuxfilesystemanalysis), MBR and GPT Analysis (https://tryhackme.com/room/mbrandgptanalysis), Autopsy (https://tryhackme.com/r/room/btautopsye0).
- Errata / currency notes (for the course author): the "Autopsy documentation here" link is broken (its href is a sentence of text, not a URL); Task 5 Q2 says `timestomped.txt` but the file is `timestomped_file.txt`; Task 3 says "offset within the clock group" (block group); Task 4's prompt shows `~/mnt/ext4_time` while the path is `/mnt/ext4_time`; the `find` output truncates to `timestomped_file.tx`; Fig 2.1 repeats "Block 1" in the third column; the "(...)" in the superblock listing and the "nsec< 2" comment are rendering losses; `extundelete` is recommended by name although it is unmaintained (last release 2013) and unreliable on extent-based ext4 — `ext4magic` or Sleuth Kit + journal parsing would be the current choice; Autopsy 4.21.0 and e2fsprogs 1.47.0 are 2023 releases (Autopsy 4.22.x and e2fsprogs 1.47.2+ are current) — nothing in the room's on-disk facts is version-sensitive.
