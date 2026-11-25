---
id: DR-003
gate: G2
ecrs: [ECR-001, ECR-002]
prepared_by: design-agent
prepared_on: 2026-11-24
---

# DR-003 review package: G2 design freeze

Review copy (commentable): see the link in `minutes.md`. Drafted in one pass from the design
conversation (kc: research/hobby rigour, speedrun).

## Scope
| Item | Rev | Source |
|---|---|---|
| LSN-A-0001 Lab sensor node | A | Fusion: Tech/General/minimal-qms/LSN- Lab Sensor Node/LSN-A-0001 |
| LSN-0001 Base, LSN-0002 Lid | A | Fusion, same folder (PETG) |
| OTS parts ECM-0001..0004, ECW-0001, ECP-0001, ECX-0001, HWN-0006 | - | minimal-qms-ots-library PR #10 |
| Software lsn-node | v0.1.1 draft | Not frozen at G2 (kc, 2026-11-25: "i dont want software to be frozen here"). Working draft in `02_design/software/lsn-node/`; checked by TP-001..004 at G3 |
| Document LSN-A-0001 rev A: assembly instruction with appendices A01 BOM (ordering info), A02 make files, A03 inspection and test (TP-001..004, AN-001), A04 build traveller | A | `03_build_package/` |

## Outputs to open before approving (all in `03_build_package/`, flat)
| Output | File | From |
|---|---|---|
| Main document: assembly instruction | `LSN-A-0001_revA.pdf` | steps.json, Fusion renders |
| A01 BOM for ordering | `LSN-A-0001_revA_A01_bom.csv` | read from Fusion LSN-A-0001 v29 (BOM check: quantities match) |
| A02 make files | `LSN-A-0001_revA_A02_make-files.zip` | STLs from LSN-0001 Base v7, LSN-0002 Lid v6 |
| A03 inspection and test | `LSN-A-0001_revA_A03_inspection-test.pdf` | inspection, in-process and final checks, TP-001..004, AN-001 in full |
| A04 build traveller | `LSN-A-0001_revA_A04_traveller.pdf` | |

No PCB, so no Gerbers. After approval the Fusion milestones go on exactly these versions; if a
design has changed since, it is re-exported and brought back first.

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
   agreement), TP-003 (restart), TP-004 (72 h), AN-001 (operating environment), inspection
   checks for every Class A part.

## Gate checklist (SOP-004-A06, G2)
| Question | Answer |
|---|---|
| Every requirement has a design output and a test or check? | Yes: REQ-001..004, 009, 011..013 by TP-001..004; REQ-005, 014 by inspection checks; REQ-007 by one caliper check on the first unit; REQ-006 by AN-001; REQ-008 (no soldering step in the instruction), REQ-010 and REQ-015 (software README) by this review |
| Control for every risk in the design? | Yes: RISK-001 partition and Pi-bay vents; -003 overlay file system; -006 config on the unit; -010 time_synced flag; -011 onboarding confirmed by kc; -013 sensor-bay vents; -014 README statement |
| Parts released, with a supplier, in stock, assemblable? | Mouser parts in stock; Pi, supply and card from kc's inventory; screws from McMaster (HWB-0036) |
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

## Buildability check in CAD (agent, 2026-11-25, Fusion LSN-A-0001 v28)
Full results in `02_design/build_document/README.md`. Order, tool access, closing and
the BOM check pass. Findings:
- **G2-F6** The SD slot is 14 mm inside the end wall. (Agent: fixed in the instruction; the card
  goes in at step 2, before the Pi is mounted.)
- **G2-F7** The Pi's ports clear the inside of the front wall by 0.4 mm; a slightly thick print
  may jam. Suggest moving the Pi 0.5 mm toward the partition (`pi_cy` -16 to -15.5 mm).
  kc, 2026-11-25 in this session: "f7 yes move it". Applied: LSN-0001 v7, LSN-A-0001 v29; clearance now 0.9 mm.
- **G2-F8** The 100 mm cable from the BME280 to the SGP40 spans about 26 mm, leaving about 70 mm
  loose in the sensor bay. Suggest a 50 mm Qwiic cable for that run (new OTS PN).
  kc, 2026-11-25 in this session: "no lets use two 100mm i'd rather have shorter bom". Rejected: two 100 mm cables kept; the spare is coiled below the rim (step 5 note).

## Open items
- Screw: HWB-0036 (McMaster 92492A702, black nylon), added 2026-11-24.
- Closed 2026-11-25: AN-001 ratings checked against the manufacturers' documents (Pi -20 to 70 °C; SGP40 -10 to 50 °C, compensation limit just exceeded at 35 °C/80 %RH, accepted; supply temperature not published, accepted). Radio IDs corrected to FCC 2ABCB-RPIZ2, IC 20953-RPIZ2.
- Fusion (2026-11-25): LSN-0001 v6, LSN-0002 v6 and LSN-A-0001 v28 saved; tree grouped into
  Custom parts and OTS parts (Electronics, Fasteners, BOM only). Pi (ECM-0004) and screw
  (HWB-0036) Part Number properties still to be set by hand; the BOM check reads their PNs from
  the file names. An unexplained 0.2 mm³ base/Pi PCB overlap in the interference check.
- After approval: release parts (lifecycle), Fusion milestones, STEP/STL exports (fusion-cad
  Releasing).
