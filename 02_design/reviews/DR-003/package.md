---
id: DR-003
gate: G2
ecrs: [ECR-001, ECR-002]
prepared_by: design-agent
prepared_on: 2026-11-24
updated_on: 2026-11-26
---

# DR-003 review package: G2 design freeze

Review copy (commentable): see the link in `minutes.md`. Drafted in one pass from the design
conversation (kc: research/hobby rigour, speedrun). Involvement level: balanced (G2 on its own;
G3 and G4 together after the first build). minimalQMS revision 3c041ac, which includes the
approved-for-build lifecycle of minimal-qms PR #44 (kc, 2026-11-26: "i like this please update
the repos accordingly"; merged 2026-11-26 on kc's instruction).

## What G2 approves
LSN-A-0001 rev A **approved for build**, not released: parts may be ordered and the first units
printed, built and tested. Fixes found while building go in by PR and keep rev A; each
traveller records the git commit and CAD version it was built from. Rev A is released (tagged
`LSN-A-0001-revA`) at G3 + G4, once a unit built from it passes TP-001..004.

Approval question: *Approve DR-003, G2 design freeze: LSN-A-0001 rev A approved for build (not
released), as in the build package on `design/parts-bom` (CAD LSN-A-0001 v31), with the
decisions and findings in this review?*

## Scope
| Item | Rev | Source |
|---|---|---|
| LSN-A-0001 Lab Sensor Node | A | Fusion: Tech/General/minimal-qms/LSN- Lab Sensor Node/LSN-A-0001 |
| LSN-0001 Base, LSN-0002 Lid | A | Fusion, same folder (PETG) |
| OTS parts ECM-0001..0004, ECW-0001, ECP-0001, ECX-0001, HWN-0006 | - | minimal-qms-ots-library (PR #10 merged; PR #17 open: SD card and SHIM to class B, BOM tools) |
| Software lsn-node | v0.1.1 draft | Not frozen at G2 (kc, 2026-11-25: "i dont want software to be frozen here"). Working draft in `02_design/software/lsn-node/`; checked by TP-001..004 at G3 |
| Document LSN-A-0001 rev A: assembly instructions with appendices A01 BOM (ordering info), A02 make files, A03 test, A04 build traveller | A | `03_build_package/` (draft dated 2026-11-26; released names add `_YYMMDD`) |

## Outputs to open before approving (all in `03_build_package/`, flat)
| Output | File | From |
|---|---|---|
| Main document: assembly instruction | `LSN-A-0001_assembly_instructions_rev_A.pdf` | steps.json, Fusion renders |
| A01 BOM for ordering | `LSN-A-0001-A01_bom_rev_A.csv` | read from Fusion LSN-A-0001 v31 (BOM check: quantities match) |
| A02 make files | `LSN-A-0001-A02_make_files_rev_A.zip` | STLs and `.f3d` backups from LSN-0001 Base v7, LSN-0002 Lid v6; assembly STEP from LSN-A-0001 v31 |
| A03 test | `LSN-A-0001-A03_test_rev_A.pdf` | no incoming inspection (reason stated); in-process and final checks; TP-001..004 with briefs and in full; AN-001 |
| A04 build traveller, one per unit | `LSN-A-0001-A04_traveller_rev_A.pdf` (+ `.csv` to fill) | step checks, final checks, first-unit checks, tests; pass/fail, comments, NC; notes and photos |
| Suppliers | `purchasing/suppliers.csv` | Mouser, DigiKey, McMaster-Carr, PiShop approved; class B parts from any supplier: SHIM and inserts exact part; SD card, screws and cables any matching part (A01 Purchasing column) |

After approval the Fusion milestones (`<PN> rev A`, "G2 approved for build") go on exactly these
versions (LSN-A-0001 v31, LSN-0001 v7, LSN-0002 v6); if a design has changed since, it is
re-exported and brought back first.

## Incoming inspection and traceability (2026-11-25)
kc, in this session: "incoming inspection should only done for critical components ... all this
is just nonsense for this build as long as we have parts purhcased from approved suppliers", and
on per-unit purchase tracing: "yes optional". So LSN has no incoming inspection (all parts are
off the shelf from approved suppliers or printed in house), no A05 record, and no per-unit trace
to purchase lines; parts with the same PN are pooled. REQ-005 is now checked on the first unit
(UL/CSA mark, A04) and REQ-014 by document review (FCC grant, ISED certificate).

## Change groups
1. **Parts and BOM:** Pi Zero 2 W, BME280, SGP40 (ECR-002), Qwiic SHIM and cables, PiShop
   supply, SanDisk card, 8 M2 heat-set inserts (HWN-0006) and 8 M2 x 5 nylon pan-head screws
   (HWB-0036): 4 for the Pi, and 2 per sensor board on diagonal holes (kc, 2026-11-25: "2 will
   be good enough"). All 12 bosses stay in the print, so a sensor can take more screws later.
   Every BOM line is read from the Fusion assembly; cables, SD card and supply are ghost designs.
2. **Housing:** 95 x 68 x 26 mm base and snap-fit lid; Pi and sensor bays split by a partition with
   a small cable notch at the end wall; vents over both bays; boards on bosses with M2 inserts;
   assembly fully held by joints.
3. **Software (draft, not frozen at G2):** v0.1.1, one Python script and a systemd service; sends
   JSON over HTTP every 5 s. Not part of this approval; checked by TP-001..004 at G3.
4. **Verification:** TP-001 (readings, rate, reporting, timestamps), TP-002 (response and unit
   agreement), TP-003 (restart), TP-004 (72 h), AN-001 (operating environment), first-unit
   checks (REQ-005 UL/CSA mark, REQ-007 size). No incoming inspection (above).

## Gate checklist (SOP-004-A06, G2)
| Question | Answer |
|---|---|
| Every requirement has a design output and a test or check? | Yes: REQ-001..004, 009, 011..013 by TP-001..004; REQ-005 (UL/CSA mark) and REQ-007 (caliper) by first-unit checks on the traveller; REQ-014 by document review (FCC 2ABCB-RPIZ2, IC 20953-RPIZ2); REQ-006 by AN-001; REQ-008 (no soldering step in the instruction), REQ-010 and REQ-015 (software README) by this review |
| Control for every risk in the design? | Yes: RISK-001 partition and Pi-bay vents; -003 overlay file system; -006 config on the unit; -010 time_synced flag; -011 onboarding confirmed by kc; -013 sensor-bay vents; -014 README statement |
| Every part has a supplier, is in stock, and can be assembled? | Mouser parts in stock; Pi, supply and card from kc's inventory; screws from McMaster (HWB-0036) |
| New or unproven? | Software not yet run on hardware; snap fit needs a test print |
| Buildable from the package alone? | Yes |
| Independent findings dispositioned? | See below |

## Independent findings (fresh Claude Code subagent, Claude Opus 5.5, 2026-11-24)
- **G2-F1** `interval_s = 10` against a 10 s gap limit will fail TP-001/TP-004 on network
  jitter. Suggest `interval_s = 5`.
- **G2-F2** Screws not in the BOM.
- **G2-F3** Screw length vs insert hole depth not checked. (Agent: holes are 5 mm deep,
  `insert_depth`; M2 x 5 engages 3.4 mm, the full 2.5 mm insert plus 0.9 mm below it.)
- **G2-F4** BME280 holes unconfirmed. (Agent: from SparkFun's Eagle board file, H1/H2/H4.)
- **G2-F5** A-004 (network onboarding) not closed. (Agent: kc confirmed on 2026-11-24: university
  Wi-Fi, then Tailscale to the server.)
- Code: stale VOC value sent after an SGP40 read failure; set `voc = None` on failure.
  G2-F1 and this fix applied 2026-11-25 in the software draft (v0.1.1): interval 5 s, `voc = None` on failure.
- **Decisions (2026-11-26):** G2-F2 to G2-F5 and the code finding accepted as answered above
  (kc, in this session: "yea accept all they seemed fine i just didnt approve"). G2-F1 was
  applied in the software draft; kc's decision on it is not yet recorded.

## Buildability check in CAD (agent, 2026-11-25, Fusion LSN-A-0001 v28)
Full results in `02_design/build_document/README.md`. Order, tool access, closing and
the BOM check pass. Findings:
- **G2-F6** The SD slot is 14 mm inside the end wall. (Agent: fixed in the instruction; the card
  goes in at step 2, before the Pi is mounted.) Accepted 2026-11-26 (kc: "yea accept all").
- **G2-F7** The Pi's ports clear the inside of the front wall by 0.4 mm; a slightly thick print
  may jam. Suggest moving the Pi 0.5 mm toward the partition (`pi_cy` -16 to -15.5 mm).
  kc, 2026-11-25 in this session: "f7 yes move it". Applied: LSN-0001 v7, LSN-A-0001 v29; clearance now 0.9 mm.
- **G2-F8** The 100 mm cable from the BME280 to the SGP40 spans about 26 mm, leaving about 70 mm
  loose in the sensor bay. Suggest a 50 mm Qwiic cable for that run (new OTS PN).
  kc, 2026-11-25 in this session: "no lets use two 100mm i'd rather have shorter bom". Rejected: two 100 mm cables kept; the spare is coiled below the rim (step 5 note).

## Independent review of the current package (fresh Claude Code subagent, Claude Opus 5.5, 2026-11-26)
Read-only review of the build package at commit d4a84c2 (CAD LSN-A-0001 v31). Checked and consistent:
A01 quantities against the STEP, STL sizes, export versions, boss and insert counts. Decisions pending
(kc); recommendation first.
- **G2R-1** (fix before build) Preparation says software README steps 1 to 3; steps 4 to 7 (install,
  config, service) are never called for, so the step 7 check cannot pass. Rec: preparation calls for
  README steps 1 to 7, overlay (step 8) last before TP-001.
- **G2R-2** (fix before build) Network onboarding (enterprise Wi-Fi, Tailscale) is "following lab IT's
  instructions", not in the package, and the tools list has no way to set it up headless. Rec: write
  down the method and its tools; needs kc's input.
- **G2R-3** (fix before build) `receiver.py` appends to one file and `check_run.py` has no time
  window, so readings from first boot (before time sync) and the TP-003 outages fail TP-001 and
  TP-004. Rec: a fresh receiver file per test, started after the unit is time-synced.
- **G2R-4** (fix before build) No test shows the BME280 is not heated by the Pi (RISK-001). Rec: add to
  TP-002 a warm-up check, first minute after power-up vs after 1 h, limit 2 °C.
- **G2R-5** (fix before build) REQ-015 / RISK-014 ("monitoring only, not a safety alarm") has no output
  in the build package. Rec: a line on the instruction cover and on the step 7 label.
- **G2R-6** (minor) B6 supply described as 5.1 V 2.5 A; the PiShop link reads 5.25 V 2.4 A. Rec: correct
  from the product page.
- **G2R-7** (minor, unsure) BME280 board holes may be about 3.3 mm, against an M2 pan head of about 4 mm.
  Rec: check the board file; accept and recheck on the test print.
- **G2R-8** (minor) REQ-002 says a 1 h run; TP-001 runs 15 min with at least 85 readings (about 180
  expected at 5 s). Rec: REQ-002 also verified by TP-004; TP-001 count at least 170.
- **G2R-9** (minor) A01 is per unit; the package does not say how many units to order for, and the
  Pi, supply and card come from inventory. Rec: confirm inventory for 2 units; order the rest for 2.

## Open items
- Screw: HWB-0036 (McMaster 92492A702, black nylon), added 2026-11-24.
- Closed 2026-11-25: AN-001 ratings checked against the manufacturers' documents (Pi -20 to 70 °C; SGP40 -10 to 50 °C, compensation limit just exceeded at 35 °C/80 %RH, accepted; supply temperature not published, accepted). Radio IDs corrected to FCC 2ABCB-RPIZ2, IC 20953-RPIZ2.
- Closed 2026-11-26: Part Number properties set (LSN-A-0001 v30, Part Numbers only, no geometry
  change; HWB-0036 v3, ECM-0002 v3, ECM-0004 v4). Fusion refuses exactly `ECM-0004` on the
  uploaded Pi model, so its property reads `ECM-0004 Raspberry Pi Zero 2 W`. Assembly STEP
  re-exported from v31, every part named by PN; the v29 STEP had left out the hidden lid, so v31 is saved with the lid shown (fusion-cad rev D: nothing hidden when saved).
- Closed 2026-11-26: the unexplained 0.2 mm³ base/Pi PCB overlap in the interference check is
  accepted (kc, in this session: "overlap is fine"); recheck on the test print.
- After approval: status "Approved for build", Fusion milestones on the versions above, merge
  to `main` (no tag); order, print, build B001.
- At G3 + G4: fixes from the builds in, re-exported; status Released with the date (file names
  gain `_YYMMDD`); milestones "G3 released"; tag `LSN-A-0001-revA` with a GitHub Release
  (fusion-cad Releasing; SOP-002 section 5).
