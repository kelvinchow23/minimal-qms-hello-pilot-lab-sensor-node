---
id: DR-001
gate: G0                 # G0 is passed by approval (SOP-004 §6), not a formal review; see Q1
ecrs: []                 # iteration 1: no ECRs or lessons learned carried in
prepared_by: design-agent
prepared_on: 2026-11-23
---

# DR-001 review package: G0 scope approved

## Scope
| Item | From | To | Source |
|---|---|---|---|
| `00_planning/plan.yaml` | template | G0 draft | branch `docs/g0-scope` |
| `roles.yaml` | template | G0 draft | branch `docs/g0-scope` |
| `README.md` "Why it exists" | empty | G0 draft | branch `docs/g0-scope` |

No parts, part numbers or CAD versions: the design stage starts after G1.

## Agenda
1. Goal and scope (in, out, open)
2. Make/buy
3. Roles
4. Target dates

## Change group 1: goal and scope
- **What changed and why:** goal and scope written from kc's answers in the agent session
  of 2026-11-23. Senses temperature, humidity and barometric pressure every 5 to 10 s;
  reports over Wi-Fi; wall-powered through micro-USB; very simple 3D-printed enclosure;
  2 to 3 units. Out: light, CO2, particulates/VOC/NOx, custom PCB, battery, USB-C input.
  Open: where the readings are reported to, and over which protocol.
- **Who made it:** agent directed by human (kc's answers; agent's wording).
- **Where to look:** `00_planning/plan.yaml` (goal, scope), `README.md`.
- **Requirements and risks affected:** none yet (G1).
- **Verification done or planned:** independent agent review (below).

## Change group 2: make/buy
- **What changed and why:** buy the controller (kc's stated intent: Raspberry Pi Zero 2 W,
  for easy Wi-Fi) and Qwiic sensor boards; make the enclosure (printed in-house), the
  software, and the assembly and test. Power supply and cabling are open (not asked).
- **Who made it:** agent directed by human.
- **Where to look:** `00_planning/plan.yaml` (`make_buy`).

## Change group 3: roles
- **What changed and why:** kc holds every approver role and quality lead, and builds the
  units (`builder`, added; see Q3). Internal auditor left unnamed at kc's choice. Agent
  tools set: design-agent and review-agent are both Claude Code with Claude Opus 5.5.
- **Who made it:** agent directed by human.
- **Where to look:** `roles.yaml`.

## Change group 4: target dates
- **What changed and why:** kc chose about one week per gate: G0 2026-11-23, G1 2026-11-27,
  G2 2026-12-04, G3 2026-12-11, G4 2026-12-18.
- **Where to look:** `00_planning/plan.yaml` (`gates`).

## Gate checklist (SOP-004-A06, G0)
| Question | Answer | Evidence |
|---|---|---|
| What problem does the product solve, and for whom? | Room-condition monitoring for lab staff; also the minimalQMS pilot ("Both") | `plan.yaml` goal |
| What is in scope, and what is explicitly out? | See group 1; reporting destination open | `plan.yaml` scope |
| What is made in-house, and what is bought? | See group 2; power supply and cabling open | `plan.yaml` make_buy |
| Who approves, and who builds? | kc approves; kc builds | `roles.yaml` |
| For a new iteration: which ECRs and lessons learned? | N/A, iteration 1 | `plan.yaml` iteration |

## Independent findings
From a fresh agent session with no memory of the work (Claude Code subagent, Claude Opus
5.5, 2026-11-23). Input only: each needs kc's accept or reject. The agent already fixed two
of its own errors that F7 and F8 point at: an invented phrase in the README was removed, and
the dangling reference in `roles.yaml` now points here. The worklog entry is added in this
change.

Product records:
- **F1** Rule 9: naming the Raspberry Pi Zero 2 W, Qwiic and micro-USB fixes design choices
  before G1. Suggest stating needs (single-board computer with Wi-Fi, I2C sensors, USB wall
  power) and keeping the Pi preference in `worklog.md` for the design stage.
- **F2** Reporting destination is open but central to the goal; G1 can't write interface,
  network or security requirements without it. Answer before approval, or carry it over by
  name in the approval question.
- **F3** Ranged or vague values ("5 to 10 s", "2 to 3 units", "very simple", "quickly")
  will block measurable requirements. Fix numbers, or state that G1 sets them.
- **F4** "Not selected at G0" reads as deferred. Say "out for iteration 1".
- **F5** Product goal and pilot goal are mixed with no priority. Split them and say which
  wins in a conflict.
- **F6** `decision: open` in make/buy is not a template value, and G0 asks for make/buy
  decided. Decide or explicitly defer.
- **F7** README problem statement may be agent-written. (Agent: it was; reworded to kc's
  answers only.)
- **F8** `roles.yaml` cited a non-existent "G0 findings"; `worklog.md` was blank. (Agent: fixed.)
- **F9** No internal auditor named; design-agent and review-agent use the same model, which
  weakens independence. Set a target date for the auditor; accept or reject same-model review.
- **F10** The iteration ECR question was unanswered. (Agent: answered "N/A, iteration 1" above.)
- **F11** `people` entry lacks the template's `github` field, needed for PR approval evidence.

QMS templates and SOPs (for the minimal-qms repo):
- **F12** Roles template has no builder/assembler role, though G0 asks "who builds" and G2
  cites "the chosen assembler". (Same as Q3.)
- **F13** Plan template has no field for open items, problem and users, or iteration ECRs.
  (Same as Q4.)
- **F14** SOP-004 §3 and `gates.yaml` say CI blocks gates, but the template ships no
  `.github/workflows`; and a file-exists check would pass a blank template. (Same as Q5.)
- **F15** SOP-004 appendix table says A06 is "not copied", but `forms/SOP-004-A06-gate-checklists.md`
  exists in the product repo.
- **F16** `qms_rev` is a commit and the SOPs are draft: the pilot runs under unreleased
  procedures. Record as a note or deviation.

## QMS findings from the design-agent
- **Q1** G0 passes by approval alone (SOP-004 §6), but `AGENTS.md` step 4 asks for a review
  package and minutes "at a gate", and the A01/A02 `gate` field lists only G1 to G4. Where a
  G0 record lives is undefined; this package uses `02_design/reviews/DR-001/`.
- **Q2** Commit prefix: `AGENTS.md` rule 5 allows `[PN]` and `[DOC]`; this session was asked
  for `[LSN] G0:`; the template's first commit used `[QMS]`. One convention is needed.
- **Q3** No builder role in SOP-001-A04; `builder` was added to answer the G0 question.
- **Q4** No place for open items in SOP-004-A01; `scope.open` and `decision: open` were added.
- **Q5** `AGENTS.md` rule 6 "run the checks": the repo has no CI and no remote, so no checks
  could run. Only a YAML parse of the two records was done (passed).
- **Q6** SOP-001 §8 says approval should follow a break, ideally the next day, but the G0
  target date kc chose is today. SOP-004 §6 allows quick gates; the two pull different ways.
- **Q7** Rule 9 vs a human naming a platform at G0 (see F1): the SOPs don't say whether a
  human-stated constraint at G0 is allowed or belongs in G1 requirements.
- **Q8** Approval evidence for G0 is "a reply quoted from an archived transcript", but
  SOP-003 §6 archives transcripts only for formal reviews. No place is defined for the G0
  transcript.
- **Q9** SOP-003 §4 requires the independent review be a fresh session; SOP-001 §8 wants it
  for author = approver. Here the author is the agent and the approver is kc; the SOPs don't
  say whether the independent review is still required. It was done anyway.

## Open items
- Reporting destination and protocol (F2).
- Make/buy for the power supply and cabling (F6).
- Internal auditor (F9).
- Human hands-on time for this session (for `worklog.md`).
