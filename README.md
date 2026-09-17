<p align="center"><img src="assets/readme/banner.svg" alt="eCDFP Diploma — ITGate Academy" width="100%"></p>

<p align="center">
  <img src="https://skillicons.dev/icons?i=windows,linux,kali,powershell,py,html,css,js,md&perline=9" alt="Stack">
</p>
<p align="center">
  <img src="https://img.shields.io/badge/FTK_Imager-acquisition-374151?style=for-the-badge" alt="FTK Imager">
  <img src="https://img.shields.io/badge/Autopsy-file_systems-00D9FF?style=for-the-badge&logoColor=black" alt="Autopsy">
  <img src="https://img.shields.io/badge/EZ_Tools-registry_·_MFT-C792EA?style=for-the-badge&logoColor=black" alt="EZ Tools">
  <img src="https://img.shields.io/badge/Volatility_3-memory-00FF9D?style=for-the-badge&logoColor=black" alt="Volatility">
  <img src="https://img.shields.io/badge/evidence_bytes_in_repo-none-FF4D5E?style=for-the-badge" alt="No evidence">
  <a href="https://ebrahim-qareen.github.io/ecdfp-diploma/"><img src="https://img.shields.io/badge/live%20site-open-00D9FF?style=for-the-badge&logo=githubpages&logoColor=black" alt="Live site"></a>
</p>

Practical **Windows digital forensics** for the INE eCDFP exam. Six 4-hour sessions, one incident carried through all of them. Fourth course in the ITGate path.

**Live site →** https://ebrahim-qareen.github.io/ecdfp-diploma/

## Course arc

<p align="center"><img src="assets/readme/course-arc.svg" alt="Course arc" width="100%"></p>

## Lab and evidence flow

<p align="center"><img src="assets/readme/lab-evidence-flow.svg" alt="Lab and evidence flow" width="100%"></p>

> **Finding** — what the evidence says. **Interpretation** — what you conclude. **Cannot prove** — say it.
> Colour-coded on every page, graded on every report.

**No evidence bytes are in this repository.** Manifests, hashes and logs are published; images, dumps, hives and captures are distributed offline. Every push runs a credential, PII and evidence-bytes scan.

## Layout

```
docs/            # site: dashboard + 14 topic pages
design/          # coverage matrix, topic map, design system
knowledge_base/  # one file per INE module
packages/        # instructor documents (never served)
labs/ scripts/ tools/ testing/   # setup guide, generators, scans, render gate
```

```bash
python3 -m http.server --directory docs 8000
```

© ITGate Academy · INE eCDFP referenced, not republished.
**Ebrahim Mohamed** — Lead Cybersecurity Instructor · SOC Analyst · [LinkedIn](https://linkedin.com/in/EbrahimMohamed)
