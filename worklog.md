# Work log

Check-ins and notable working decisions (SOP-003 §7). Newest at the top. Not approvals.

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
  merges; there is no remote yet). LSN not registered in the OTS library: waiting for kc to ask.
- **Next:** G1 requirements and risks from the G1 notes above.
- **Time:** agent 1.25 h (0.5 h planning, 0.75 h review); human hands-on 0.5 h on planning
  and review (kc: "it was like half an hour"; not split by activity).

## YYYY-MM-DD: <who> (human / agent)
- **Changed:** <what, by whom>
- **Next:**
- **Blocked / unsure:**
- **For the next review:**
- **Time:** agent <h> on <activity>; human hands-on <h> on <activity>
