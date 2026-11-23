---
id: DR-001
gate: G0                 # G0 is passed by approval (SOP-004 §6), not a formal review; see Q1
ecrs: []                 # iteration 1: no ECRs or lessons learned carried in
prepared_by: design-agent
prepared_on: 2026-11-23
---

# DR-001 review package: G0 scope approved

## Review copy
kc reviews this package as a commentable Claude Docs document, "LSN G0 scope review
(DR-001)", https://claude.ai/artifact/WwepEcjmhVSdb5uHai2ykD (private to kc unless shared).
This file stays the record in the repo; decisions made in the doc are copied into
`minutes.md`.

## How to review this (for kc)
1. Read **What you are approving** below: it is the whole scope on one page. Open
   `00_planning/plan.yaml` and `roles.yaml` beside it if you want the exact text.
2. Check the **Findings** table. Each row is a possible problem found by a second AI
   session or by the design agent. You already decided the ones marked *kc*. The ones marked
   *proposed* were filled in by the agent at your request; change any you disagree with.
3. Answer the approval question at the end with your own yes or no.

The minutes (`minutes.md`) record your decisions. Nothing is approved until you answer.

## What you are approving
**Goal.** A minimal hardware unit that can be deployed in self-driving labs, used as a
hardware pilot to run design iterations through minimalQMS. Each iteration should produce a
working unit and a list of QMS fixes. When the two conflict, the product comes first.

**In scope**
- Design, build and test a minimal sensing hardware unit deployable in a self-driving lab
- Iterate it through minimalQMS (G0 to G4, then further iterations)

**Out of scope:** not yet stated. Decide at the review whether to list anything (e.g.
production volumes, certification) or leave it empty.

**Make or buy (coarse)**
| Item | Decision |
|---|---|
| Electronics | buy (off-the-shelf boards; parts chosen in the design stage) |
| Integration | make |
| Software | make |
| Enclosure, if needed | make |

**Roles.** kc approves everything, is quality lead, and builds. The internal auditor is not
named yet (to be named before QMS-rev A). AI agents write and review, never approve.

**Target dates.** G0 2026-11-23, G1 2026-11-27 (planned back to back with G0),
G2 2026-12-04, G3 2026-12-11, G4 2026-12-18.

**Not decided at G0 on purpose.** What it senses, how often, how it reports, power, unit
count, enclosure and parts. These came up in the session and are kept as notes for G1 in
`worklog.md`; they become requirements right after G0.

## Gate checklist (SOP-004-A06, G0)
| Question | Answer | Evidence |
|---|---|---|
| What problem does the product solve, and for whom? | A minimal unit deployable in self-driving labs; also the hardware pilot for minimalQMS; product first | `plan.yaml` goal |
| What is in scope, and what is explicitly out? | In: above. Out: to decide at the review | `plan.yaml` scope |
| What is made in-house, and what is bought? | Above | `plan.yaml` make_buy |
| Who approves, and who builds? | kc approves; kc builds | `roles.yaml` |
| For a new iteration: which ECRs and lessons learned? | N/A, iteration 1 | `plan.yaml` iteration |

## Findings
F = from the independent review (a fresh Claude Code subagent session, Claude Opus 5.5,
with no memory of the work, 2026-11-23). Q = from the design agent. Each is input only.

*kc* = kc's decision in the session of 2026-11-23. *proposed* = filled in by the agent
because kc asked it to ("fill in a lot of these unimportant ones for me and let me figure
it out later"); kc to confirm or change at the review.

### About this product
| # | Finding | Disposition | Result |
|---|---|---|---|
| F1 | Naming the Pi Zero 2 W, Qwiic and micro-USB picks parts before G1 | accept (*kc*) | Preference moved to `worklog.md` G1 notes; later scope rewrite removed all part detail |
| F2 | Reporting destination open, but the goal depends on it | accept (*kc*) | Superseded: reporting is now a G1 note, not G0 scope |
| F3 | Ranged values ("5 to 10 s", "2 to 3 units") aren't measurable | accept (*kc*) | Superseded: the ranges are now G1 notes |
| F4 | "Not selected at G0" reads as deferred | accept (*kc*) | Superseded: the out-of-scope list is now empty, kc to decide |
| F5 | Product and pilot goals mixed, no priority | accept (*kc*) | Product first; goal rewritten to kc's restated scope |
| F6 | Power supply and cabling make/buy open | accept (*kc*) | Superseded: "buy" kept as a G1 note; G0 make/buy is coarse |
| F7 | README problem statement was agent-written | accept (*proposed*) | Invented phrase removed |
| F8 | Broken reference in `roles.yaml`; blank worklog | accept (*proposed*) | Both fixed |
| F9 | No internal auditor; same model for design and review | accept (*kc*) | Same-model review accepted for the pilot; auditor before QMS-rev A |
| F10 | Iteration ECR question unanswered | accept (*proposed*) | "N/A, iteration 1" |
| F11 | No GitHub username in `roles.yaml` | accept (*kc*) | `kelvinchow23` added (*proposed* value, kc to confirm) |

### About minimalQMS itself
These don't change this product. Proposed for all: accept, and raise in the minimal-qms
repo after G0 (not done yet).

| # | Finding | Disposition |
|---|---|---|
| F12 / Q3 | Roles template has no builder role; one was added here | accept (*proposed*) |
| F13 / Q4 | Plan template has no field for open items; `scope.open` was added here | accept (*proposed*) |
| F14 / Q5 | Procedures say CI blocks gates, but the template has no CI; no checks could run (YAML parse only, passed) | accept (*proposed*) |
| F15 | SOP-004 says the gate checklists aren't copied, but they are in `forms/` | accept (*proposed*) |
| F16 | Pilot runs under unreleased (draft) procedures at a commit, not a tag | accept (*proposed*) |
| Q1 | No defined place for a G0 record (G0 is approval-only); `02_design/reviews/DR-001/` used | accept (*proposed*) |
| Q2 | Three commit prefixes conflict: `[PN]`/`[DOC]`, `[LSN]`, `[QMS]` | accept (*proposed*) |
| Q6 | "Approve after a break, ideally next day" vs a same-day G0 target | accept (*proposed*) |
| Q7 | Procedures don't say whether a human-stated platform at G0 is allowed (see F1) | accept (*proposed*) |
| Q8 | No defined place to archive the G0 approval transcript | accept (*proposed*) |
| Q9 | Unclear whether independent review is needed when the agent authors and kc approves | accept (*proposed*) |
| Q10 | Scope (G0) and requirements (G1) are split too finely for a small product: specs such as the reading interval and unit count get pushed to G1 when it is natural to decide them with the scope. Consider letting simple products pass G0 and G1 together in one review. For this project, kc plans to pass G0 and G1 back to back in one sitting, as SOP-004 §6 allows. | accept (*kc*, 2026-11-23) |
| Q11 | The agent pulled design detail (sensors, power, unit count, a specific board) into G0 by asking requirements questions. The G0 checklist questions don't say how deep G0 should go. The SOP or checklist should say G0 stays at purpose, users, boundaries, coarse make/buy and roles. | accept (*proposed*) |
| Q12 | kc prefers reviewing in a commentable document (Claude Docs) over this markdown file. SOP-003 §4 and §6 expect `package.md` in the repo and say nothing about an external review copy, where comments live, or how they become part of the record. | accept (*proposed*) |

## Open items
- Out of scope: decide at the review.
- Internal auditor (before QMS-rev A).
- Confirm GitHub username `kelvinchow23`.
- kc's hands-on time for 2026-11-23 (for `worklog.md`).

## Approval question
> "Approve G0 for LSN: the goal, scope, coarse make/buy, roles and target dates in
> `00_planning/plan.yaml` and `roles.yaml` as committed on branch `docs/g0-scope` (commit
> named in the minutes), with the findings dispositioned as in DR-001?"
