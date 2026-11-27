# Work log

Check-ins and notable working decisions (SOP-003 §7). Newest at the top. Not approvals.

## 2026-11-27: design-agent (agent, Claude Code / Claude Opus 5.5), with kc
- **Changed:** G2-F1 accepted (kc: "yes accpet it"); G2R-5 monitoring-only statement on the
  cover and label. One findings register, `02_design/reviews/findings.csv` (kc: "where do i
  find this?"); QMS finding statuses updated; Q32. **G2 approved** (kc, 2026-11-27 16:27 EST:
  "i have made my comments and approve."), recorded in DR-003 minutes and plan.yaml; build
  document status "Approved for build". Order files for 2 units drafted with the OTS library's
  requisition.py (PR #17 code): Mouser 4 lines, DigiKey 1, McMaster-Carr 1; Pi, supply and SD
  card from kc's inventory.
- **Next:** kc marks the Fusion milestones (LSN-A-0001 v31, LSN-0001 v7, LSN-0002 v6, each
  `<PN> rev A`, "G2 approved for build"); kc merges PR #8 and OTS library PR #17; the purchase
  reqs (Mouser, DigiKey, McMaster) through the organization's process; print; build B001.
- **Blocked / unsure:** the Fusion MCP returned no script output this session, so the agent
  could not check for a milestone API. The OTS parts are still `draft` in the library; the
  purchasing skill asks for `released` (kc's active/obsolete question is open).
- **Time:** agent about 0.75 h (review 0.25, documentation 0.25, purchasing 0.25); human: not yet given.

## 2026-11-26 (evening): design-agent (agent, Claude Code / Claude Opus 5.5), with kc
- **Changed:** fresh independent review of the package (G2R-1 to G2R-9) recorded in DR-003 with
  kc's decisions. ECR-003 (issue #9; kc: "i would do a hardware bring up test as whats needed to
  check hardware. software should be its own thing"): TP-002 is now the hardware bring-up
  (sensors found, readings, warm-up rise at most 2 °C, response, unit agreement) with
  `tools/bringup.py`; AN-002 shows hardware capability from datasheets (BME280 rev 1.24, SGP40
  v1.2, Pi Zero 2 W brief); REQ-002, 004, 009, 011, 012 and TP-001, 003, 004 move to the
  software item; build package preparation and step 7 no longer need the software. QMS finding
  Q31 (software as its own item).
- **Next:** kc decides G2R-5 (monitoring-only statement) and G2-F1 (5 s interval); then the G2
  question.
- **Blocked / unsure:** OTS lifecycle states (library PR #17), transcripts, deviations before
  QMS-rev A: waiting on kc.
- **Time:** agent about 1 h (review 0.5, documentation 0.5); human: not yet given.

## 2026-11-26 (later): design-agent (agent, Claude Code / Claude Opus 5.5), with kc
- **Changed:** minimal-qms PRs #44 (approved for build at G2, released at G3) and playbook #6
  (nothing hidden when saved) merged on kc's instruction ("merge and run copier"); LSN updated
  to minimalQMS 3c041ac. Assembly saved as v31 with the lid shown; STEP re-exported. DR-003: G2
  approves rev A for build; overlap accepted (kc: "overlap is fine"); G2-F2 to F6 and the code
  finding accepted (kc: "yea accept all"). An independent compliance review of LSN against
  minimalQMS and the playbook found requirements.yaml broken (REQ-005 quotes) and REQ-007/008
  and RISK-005/008 still pointing at IC-nnn: fixed. Also fixed: BOM source column names
  (internal_pn, manufacturer_pn), A03 incoming wording, DR-003 checklist, build-document README,
  calipers and weather-station reference in equipment.csv.
- **Next:** a fresh independent review of the current package before the G2 question (kc: "its
  always good to do an independent review before a gate to catch the small mixups").
- **Blocked / unsure:** kc to decide on OTS lifecycle states (library PR #17 open), deviations
  before QMS-rev A, and archived review transcripts.
- **Time:** agent about 1.5 h (documentation 0.5, review 0.5, design 0.5); human: not yet given.

## 2026-11-26: design-agent (agent, Claude Code / Claude Opus 5.5), with kc
Written 2026-11-26 after the fact, from git history and the session, covering the work of
2026-11-24 evening to 2026-11-26 since the last entry. No deviation: kc treats minimalQMS as
pre-rev A for this pilot.
- **Changed (design):** M2 x 5 nylon screws (HWB-0036) into M2 inserts; 2 screws per sensor,
  4 for the Pi (kc: "yea lets do two per sensor. pi can stay 4"); ghost designs for cables,
  SD card and supply, so the whole BOM is read from Fusion. CAD buildability check (order,
  insertion path, tool access, cables, lid, BOM): G2-F6 SD card in at step 2 (applied),
  G2-F7 Pi bay 0.5 mm toward the partition (kc: "f7 yes move it"; base v7, assembly v29),
  G2-F8 rejected (kc: "no lets use two 100mm i'd rather have shorter bom"). Part Number
  properties set (assembly v30, no geometry change); v31 saved with the lid shown, because
  the hidden lid had been left out of the v29 STEP (new fusion-cad rule: nothing hidden when
  saved); assembly STEP re-exported from v31.
- **Changed (verification):** AN-001 ratings checked against manufacturer documents; radio IDs
  corrected; REQ-006 source corrected (ranges were agent proposals); REQ-005 and REQ-007
  first-unit checks, REQ-014 document review. No incoming inspection (kc: critical parts
  only); purchase trace optional; software v0.1.1 stays a draft, not frozen at G2 (kc).
- **Changed (build package):** one controlled document, LSN-A-0001 rev A: assembly
  instructions (cover, 7 picture steps with callouts A/B/H/W) and appendices A01 BOM, A02 make
  files (STL, `.f3d`, STEP), A03 test, A04 traveller (serial, build number, P/F, comments, NC,
  notes and photos). Flat `03_build_package/`; sources in `02_design/build_document/`;
  `parts.csv` dropped (state from git). Draft dated 2026-11-26.
- **Changed (process):** involvement level balanced (kc). minimalQMS PRs #42 and #43 and
  playbook PRs #3, #4, #5 (+ private #5) merged on kc's instruction ("merge all rules and run
  copier"); LSN updated to minimalQMS f0ba1f4 by copier. QMS findings Q20, Q22-Q30 proposed.
- **Next:** kc answers the G2 question (DR-003); then release, milestones, order, print, build.
- **Blocked / unsure:** kc's question on revisions during the first builds (does rev A wait
  until a unit works?) changes what G2 releases; answer before the G2 question.
- **For the next review:** 0.2 mm³ base/Pi PCB overlap; snap fit and Pi-port clearance on
  the test print.
- **Time:** agent about 8.5 h estimated from session activity (design 1.5, documentation 4.5,
  review 1.5, planning 1); human hands-on about 2 h (kc: "like 2 hours hands on but i swear
  most of that time was cleaning up minimalqms"), not split by activity; the share spent on
  the LSN design itself is unknown.

## 2026-11-24 (design): design-agent (agent, Claude Code / Claude Opus 5.5), with kc
- **Changed:** ECR-001 (light) and ECR-002 (VOC, replaces light) raised, approved by kc and
  merged. Parts chosen on Mouser and from kc's inventory; ECM-0001..0004, ECW-0001, ECP-0001,
  ECX-0001 allocated (ots-library PR #10); LSN-A-0001, LSN-0002 Base, LSN-0003 Lid allocated.
  Housing first built with direct modelling (no history), then rebuilt to the playbook
  fusion-cad rev B after kc asked whether the agent followed kc's Fusion practices. Fusion:
  Tech/General/minimal-qms/LSN- Lab Sensor Node (assembly + parts), OTS parts subfolder holds
  ECM-0002 (Adafruit STEP, MIT), ECM-0004 (modelled from the Raspberry Pi mechanical drawing),
  ECM-0001 (outline and 3 holes from SparkFun Eagle file). SD opening moved to the +x wall to
  match the Pi drawing. Interference check: none.
- **Confirmed from supplier data:** SGP40 holes 2.5 mm at 20.32 x 12.7 mm; BME280 holes 3.302 mm,
  only 3 (H1, H2, H4) at 20.32 mm; Pi holes 58 x 23 mm, power port 54 mm from the left edge.
- **Unconfirmed:** Pi connector heights and sizes; SD slot y; BME280 connector sizes; SHIM not
  modelled (no mounting; sits on the header).
- **Open:** SGP40 2.5 mm holes are tight for M2.5 screws; one BME280 boss unused; lid is
  friction fit (no screws); lid copies base parameters; fillets not done; STEP model library
  approach (kc's question) proposed but not started.
- **Then:** kc uploaded a GrabCAD Pi Zero 2 W model; it replaces the drawing-based ECM-0004
  (old file renamed SUPERSEDED, not deleted). It has no GPIO header, so a 2x20 header (black
  plastic, gold pins) was added. It showed the agent had misread the Pi drawing: the SD slot is
  at the mini-HDMI end (-x), so the base SD opening was moved back to the -x wall and centred on
  the real slot; USB and SD heights now come from the model. ECM-0003 Qwiic SHIM modelled from
  SparkFun's Eagle file, on GPIO pins 1-6. Colours: Pi green (GrabCAD), SparkFun boards red,
  Adafruit SGP40 from its STEP. Interference check: no contact with the housing; the SHIM's
  staggered holes grip the pins by design.
- **Then:** at kc's request the front wall now exposes the mini-HDMI and both micro-USB ports
  (one shared opening for the two USB ports; separate ones would leave a 0.4 mm web). kc asked
  about Pi ventilation: agent estimated about 1 W and a 10-20 C internal rise (not measured), so
  no overheating risk, but heat pooling near the sensors (RISK-001). kc approved ("Yes, add
  both"): 5 lid vents over the Pi bay (chimney with the low port openings), and TP-004 (72 h run)
  will log the Pi CPU temperature (vcgencmd measure_temp) with the readings.
- **Then:** kc: "there needs more room between the qwiic sensors. i cant connect a cable between
  the two now". Housing lengthened 75 -> 95 mm (still within REQ-007's 100 mm); BME280 moved to
  x -20 and SGP40 to x +28 (about 23 mm between connectors, about 13 mm beside the BME280 for the
  SHIM cable); vents spread. Found and fixed an agent error: the base Outline sketch had no
  centring constraint (an earlier fix had rolled back unnoticed), so the first 95 mm edit grew
  the box to one side. Now fully constrained and symmetric.
- **Then:** kc: the cutout "can move all the way to the end ... can be minimized". Cable notch
  now flush against the -x end wall, 6 mm wide x 8 mm deep (cable clears the 4 mm lid lip).
- **Then:** kc chose snap detents for the lid ("Snap detents") over screws: 4 half-round bumps
  (r 0.5 mm, 10 mm long) on the lid lip's front and back faces click into 4 grooves (r 0.6 mm,
  11 mm) in the base walls, 2 mm below the rim. Interference while closing = snap_bump_r -
  lip_clearance = 0.3 mm; needs a test print to tune. fusion-cad says printed parts fasten with
  screws into inserts; agent reads a snap detent as not fastening hardware. kc to confirm at G2.
- **Then:** assembly reworked to fusion-cad hard rules (kc: no Move/Position; nothing
  draggable): base grounded, every part on joints to real geometry, imported boards rigidly
  grouped in their designs and in the assembly, timeline ordered insert-then-joint, sketches
  hidden. Agent error found: base and lid edits since their v4 had gone into duplicate open
  copies and never saved. Replayed onto fresh copies: Fusion now LSN-0002 v5, LSN-0003 v5,
  LSN-A-0001 v18; all parts in place. Unexplained 0.2 mm3 base/Pi PCB overlap remains.
- **Then:** G2 package drafted in one pass (kc: research/hobby rigour, speedrun): software
  v0.1.0, TP-001..004, AN-001 (print in PETG), assembly instruction, inspection checks; screws
  HWB-0036 (McMaster 92492A702, black nylon M2 x 6, kc's choice). DR-003 review doc pre-filled.
- **Then:** kc renamed the Fusion parts to LSN-0001 Base and LSN-0002 Lid (separate number
  sequences for parts and assemblies, finding Q20); repo records renamed to match (nothing was
  released). Fusion rebuilt and confirmed saved: LSN-0001 v6 and LSN-0002 v6 (M2 inserts,
  parameters trimmed to 15 and 8, fillets), assembly tree split into Custom parts and OTS parts.
  Agent lesson: part copies opened through the assembly cannot be saved; open parts directly.
- **Next:** software, test procedures TP-001..004, assembly instructions, inspection checks,
  then the G2 review (DR-003).
- **Time:** agent about 2.5 h on design and part selection; human hands-on: not asked yet.

## 2026-11-24: design-agent (agent, Claude Code / Claude Opus 5.5), with kc
- **Changed:** G1 started on branch `docs/g1-requirements`. kc answered: "Every 10 s,
  2 units", "Any, design decides" (reporting), "Typical breakout" accuracy, "Sits on a bench".
  Drafted `requirements.yaml` (REQ-001 to REQ-010; REQ-009 and REQ-010 agent-proposed) and
  `risks.csv` (RISK-001 to RISK-008, agent-proposed); plan.yaml scope adds 2 units. Independent
  review: G1-F1 to G1-F12. Review package DR-002 and commentable review doc
  (https://claude.ai/artifact/MpbBYcgDyLTVhmGL3apR5x).
- **Then:** kc asked for an open conversation at gate start (saved as a preference; finding
  Q14), then a read-back of what is known. Requirements redrafted from that talk (see DR-002
  package). kc: "please drop labsense, it is unrelated" (the earlier G0 note naming it is
  superseded).
- **Next:** kc decides six items and the twelve findings in the doc; agent updates the records;
  G1 approval question.
- **Blocked / unsure:** nothing; waiting on kc's review.
- **Then:** kc filled in the review doc; agent applied the decisions (d4f73b1) and recorded
  DR-002 minutes. kc asked whether the Pi Zero 2 W radio is certified (agent: believed FCC
  2ABCB-RPIZ2W and ISED 20953-RPIZ2W, from memory; confirm in design; 2.4 GHz only).
- **G1 approved:** kc, 2026-11-24 10:01 EST: "i have reviewed and made my comments, which have
  been updated. approve and continue". Recorded in DR-002 minutes and plan.yaml.
- **Next:** design stage (G2 target 2026-11-26). A-004: kc confirms device onboarding with lab IT.
- **Time:** agent 1.5 h on requirements and review; human hands-on: not asked yet.

## 2026-11-23: design-agent (agent, Claude Code / Claude Opus 5.5), with kc
- **Changed:** G0 scope records drafted from kc's answers: `00_planning/plan.yaml` (goal,
  scope, make/buy, gate target dates), `roles.yaml` (builder, agent tools), `README.md`
  "Why it exists". Review package and draft minutes in `02_design/reviews/DR-001/`.
  Independent review by a fresh subagent session: findings F1–F16; agent QMS findings Q1–Q9.
- **Next:** kc dispositions the findings and answers the G0 approval question. After
  approval: record it in DR-001 minutes and `plan.yaml`, then register `LSN` in the OTS
  library (only if kc asks). Then G1 requirements.
- **Blocked / unsure:** reporting destination and protocol; power supply and cabling
  make/buy; internal auditor not named.
- **Ideas for later gates:** kc prefers a Raspberry Pi Zero 2 W (easy Wi-Fi) with Qwiic
  sensor boards; the existing LabSense stack (`../sensor_prefect_server`, MQTT to
  TimescaleDB) is a possible reporting destination; `../sen55-enviro-sensor` is prior work
  on the same board.
- **For the next review:** findings F1–F16, Q1–Q9 in DR-001.
- **Later the same session:** kc decided F1–F6, F9, F11 and asked the agent to fill in the
  rest ("fill in a lot of these unimportant ones for me and let me figure it out later");
  those are marked *proposed* in DR-001. plan.yaml revised to match (scope states needs, not
  parts; power supply and cabling bought; product goal first). kc wants the formal G0 review
  held later with the package in front of them.
- **Then:** at kc's request, the goal now states both purposes (product, and a simple unit
  iterated to fix minimalQMS); finding Q10 added (G0/G1 split too fine for a small product).
  kc plans to pass G0 and G1 back to back in one sitting.
- **Then:** kc restated the scope: "the scope is just a minimal hardware unit that is
  deployable to self driving labs and can be used as a hardware pilot project to do design
  iterations through this qms". The agent had pulled design detail into G0 by asking
  requirements questions (finding Q11). plan.yaml rewritten to that minimal scope with
  coarse make/buy, as in the draft kc accepted ("Yes, back to back"). The detail moves to
  the G1 notes below; nothing in it is decided.
- **Notes for G1 (from kc's answers on 2026-11-23, not yet requirements):**
  - Senses air temperature, relative humidity and barometric pressure. Light, CO2,
    particulates, VOC and NOx were not selected.
  - Reads every 5 to 10 seconds; firmware detail mattered less to kc than the hardware
    being able to do this.
  - Reports readings over Wi-Fi; destination and protocol undecided (LabSense over MQTT is
    one option).
  - Wall-powered over USB; battery not wanted.
  - Very simple 3D-printed enclosure to keep everything together.
  - 2 to 3 units.
  - No custom PCB: off-the-shelf boards.
  - Part preference for the design stage: Raspberry Pi Zero 2 W with Qwiic sensor boards.
  - Power supply and cables: buy.
  - Self-driving labs as the deployment target is new in kc's restated scope; what that
    means for the unit (mounting, interfaces, environment) is a G1 question.
- **Then:** G0 review moved to a commentable doc (https://claude.ai/artifact/WwepEcjmhVSdb5uHai2ykD;
  finding Q12). kc commented: "i plan to run through this in a week for the first
  iteration. want to get through a second iteration before christmas break". Target dates
  for G1 to G4 moved to 2026-11-24, 11-26, 11-28 and 11-30 (agent's proposed spread).
- **Then:** kc reviewed the doc; decisions recorded in DR-001 minutes (commit 4a40a32).
  kc on dates: "target dates seem ok but may not be feasible". kc wants to place a parts
  purchase this week and will write purchasing work instructions meanwhile, outside this
  repo. Note: under AGENTS.md rule 9, ordering waits until parts are released at G2
  (target 2026-11-26); ordering earlier needs a deviation.
- **G0 approved:** kc answered the approval question "yes  i approve g0  for lsn" at
  2026-11-23 01:40 EST; recorded in DR-001 minutes and plan.yaml. Branch not merged (a human
  merges; there is no remote yet). At kc's request ("Yes, register LSN"), LSN registration
  opened as https://github.com/kelvinchow23/minimal-qms-ots-library/pull/9 (not merged).
- **Next:** G1 requirements and risks from the G1 notes above.
- **Time:** agent 1.25 h (0.5 h planning, 0.75 h review); human hands-on 0.5 h on planning
  and review (kc: "it was like half an hour"; not split by activity).

## YYYY-MM-DD: <who> (human / agent)
- **Changed:** <what, by whom>
- **Next:**
- **Blocked / unsure:**
- **For the next review:**
- **Time:** agent <h> on <activity>; human hands-on <h> on <activity>
