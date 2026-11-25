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
| Software lsn-node | v0.1.0 | `03_build_package/software/lsn-node/` |
| TP-001..004, AN-001, assembly instruction, inspection checks | A | `03_build_package/` |

## Change groups
1. **Parts and BOM:** Pi Zero 2 W, BME280, SGP40 (ECR-002), Qwiic SHIM and cables, PiShop
   supply, SanDisk card, 12 M2 heat-set inserts; M2 x 5 nylon pan-head screws (HWB-0036).
2. **Housing:** 95 x 68 x 26 mm base and snap-fit lid; Pi and sensor bays split by a partition with
   a small cable notch at the end wall; vents over both bays; boards on bosses with M2 inserts;
   assembly fully held by joints.
3. **Software v0.1.0:** one Python script and a systemd service; sends JSON over HTTP every
   `interval_s`.
4. **Verification:** TP-001 (readings, rate, reporting, timestamps), TP-002 (response and unit
   agreement), TP-003 (restart), TP-004 (72 h), AN-001 (operating environment), inspection
   checks for every Class A part.

## Gate checklist (SOP-004-A06, G2)
| Question | Answer |
|---|---|
| Every requirement has a design output and a test or check? | Yes: REQ-001..004, 009, 011..013 by TP-001..004; REQ-005, 007, 008, 014 by inspection checks; REQ-006 by AN-001; REQ-010, 015 by this review (software README) |
| Control for every risk in the design? | Yes: RISK-001 partition and Pi-bay vents; -003 overlay file system; -006 config on the unit; -010 time_synced flag; -011 onboarding confirmed by kc; -013 sensor-bay vents; -014 README statement |
| Parts released, with a supplier, in stock, assemblable? | Mouser parts in stock; Pi, supply and card from kc's inventory; screws pending PN |
| New or unproven? | Software not yet run on hardware; snap fit needs a test print |
| Buildable from the package alone? | Yes once the screw PN is added |
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

## Open items
- Screw: HWB-0036 (McMaster 92492A702, black nylon), added 2026-11-24.
- Datasheet values marked "to confirm" in AN-001 and the radio IDs in the inspection checks.
- Fusion: confirm LSN-0001 v6 (M2 inserts, parameters trimmed) and LSN-0002 v6 saved; display
  names of OTS components; OTS/custom grouping.
- After approval: release parts (lifecycle), Fusion milestones, STEP/STL exports (fusion-cad
  Releasing).
