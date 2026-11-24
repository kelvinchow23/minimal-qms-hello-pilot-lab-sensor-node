---
id: DR-002
gate: G1
ecrs: []
prepared_by: design-agent
prepared_on: 2026-11-24
---

# DR-002 review package: G1 requirements reviewed

Review copy (commentable): "LSN G1 requirements review (DR-002)",
https://claude.ai/artifact/MpbBYcgDyLTVhmGL3apR5x. This file is the record in the repo;
decisions made in the doc are copied into `minutes.md`.

## Scope
| Item | From | To |
|---|---|---|
| `01_requirements/requirements.yaml` | empty | REQ-001 to REQ-010 |
| `01_requirements/risks.csv` | empty | RISK-001 to RISK-008 |
| `00_planning/plan.yaml` scope | G0 | adds "Build and test 2 units in iteration 1" |

## Change groups
1. **Requirements from kc's answers** (REQ-001 to REQ-008): agent directed by human. Sources:
   G1 notes in `worklog.md` (2026-11-23) and kc's answers on 2026-11-24 (every 10 s, 2 units,
   any Wi-Fi method chosen in design, typical breakout accuracy, sits on a bench).
2. **Agent-proposed requirements** (REQ-009 restart on its own, REQ-010 no credentials in the
   repo): agent.
3. **Risks** (RISK-001 to RISK-008): agent.
4. **Scope change:** 2 units added to plan.yaml: agent directed by human.

## Gate checklist (SOP-004-A06, G1)
| Question | Answer |
|---|---|
| Each requirement measurable? | Yes: a number or a pass/fail in each |
| Each has a verification method? | Yes |
| Environment, power, safety, standards covered? | REQ-006, REQ-005, RISK-008; no formal standards apply (challenged by G1-F1) |
| What could go wrong; serious risks controlled? | Eight risks, each with a control |
| Any requirement unnecessary? | kc to decide; REQ-008 to REQ-010 are candidates (G1-F7) |

## Independent findings
Fresh Claude Code subagent session (Claude Opus 5.5), 2026-11-24. Input only.
- **G1-F1** Safety/standards: REQ-005 should require a CSA or UL listed supply; add radio
  certification (ISED/FCC), or state "no applicable standards" with the reason.
- **G1-F2** REQ-005 has no voltage or current (e.g. 5 V, 1 A or less).
- **G1-F3** REQ-003 "room conditions" undefined: state assembled, warm-up, band, and a
  reference at least 2× better than the limit.
- **G1-F4** REQ-004 timestamps have no accuracy (e.g. ±2 s of network time); add a
  no-network-time risk.
- **G1-F5** REQ-006 leaves out humidity (non-condensing range) and lab air; add a risk for
  sensor drift from solvent vapours.
- **G1-F6** Missing risk: lab network blocks unregistered devices or needs enterprise login;
  confirm network rules before G2.
- **G1-F7** REQ-008 repeats make/buy; REQ-010 is a repo rule. Move or accept as constraints.
- **G1-F8** REQ-009 needs a pass count (e.g. 20 power cuts).
- **G1-F9** RISK-008 severity 3 is low for burn or fire; consider 4.
- **G1-F10** Some `verified_by` entries aren't IDs; use e.g. IC-001, DR-003.
- **G1-F11** 2 units changes the G0 scope; approve explicitly; say requirements apply to each unit.
- **G1-F12** minimalQMS templates: A03 has no field for standards or accepted/proposed status,
  no ID scheme for inspections/reviews; A04 doesn't define "serious" or residual risk.

## QMS findings from the design-agent
- **Q14** `AGENTS.md` step 2 says "ask the gate's questions"; the agent opened G0 and G1
  with preset multiple-choice questions. kc: "giving me just preset questions to answer right
  out of the gate is restrictive". Suggest: at each gate start, open with a free-form
  conversation (G0: what are we trying to do; G1: rough requirements in the user's words),
  then specific questions; make this a per-user preference so users who want to skip it can.

## Open items
- kc's decisions on the four items and twelve findings.
