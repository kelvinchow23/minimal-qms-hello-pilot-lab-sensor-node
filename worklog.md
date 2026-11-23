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
- **Time:** agent 0.75 h (0.5 h planning, 0.25 h review); human hands-on: asked, not yet given.

## YYYY-MM-DD: <who> (human / agent)
- **Changed:** <what, by whom>
- **Next:**
- **Blocked / unsure:**
- **For the next review:**
- **Time:** agent <h> on <activity>; human hands-on <h> on <activity>
