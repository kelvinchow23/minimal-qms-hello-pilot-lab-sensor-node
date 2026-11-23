# AGENTS.md

Instructions for any AI agent (Claude Code, Codex, Cowork, …) working in this repo.
`CLAUDE.md` just imports this file.

## What this repo is

**Lab sensor node** (project code `LSN`): Pilot lab sensor node, used to run minimalQMS end to end before QMS-rev A.

This product is developed under [minimalQMS](https://github.com/kelvinchow23/minimal-qms),
revision `f4d60f4` (recorded in `00_planning/plan.yaml` and `.copier-answers.yml`).
- The procedures (SOPs) are in the minimal-qms repo, `sops/`. Shared names, IDs and the
  layout of this repo are defined in its `docs/INTERFACES.md`.
- Every form and template is copied into `forms/` here. Create records from those copies;
  do not edit `forms/` (it is replaced by `copier update`).
- Off-the-shelf parts, project codes and purchasing tools are in
  [minimal-qms-ots-library](https://github.com/kelvinchow23/minimal-qms-ots-library).

The human does not need to read the SOPs. Your job is to follow them on the human's behalf:
ask the right questions at the right time, keep the records, and bring decisions to the
human for approval.

## How to work with the human

1. **Know the current gate.** Read `00_planning/plan.yaml`: the first gate without an
   `actual` date is the current one. Work on that gate's stage only (rule 9).
2. **Ask the gate's questions as the work makes them relevant** (`forms/SOP-004-A06-gate-checklists.md`),
   in plain language, without naming the SOP. Record the answers in the stage's records.
3. **Check in after each work session** in `worklog.md`: what changed and who changed it,
   what is next, what is blocked, and the session's time (see Time tracking).
4. **At a gate,** prepare the review package (`forms/SOP-003-A01-review-package.md`), walk the
   human through it, and ask one yes-or-no question that names exactly what is approved.
   Record the answer in the minutes (`forms/SOP-003-A02-review-minutes.md`) and the actual
   date in `plan.yaml`.
5. **At G0 approval,** register `LSN` in the OTS library's `projects.csv`
   (a PR in that repo).

## Hard rules

1. **Never commit to `main`.** Always use a branch and a PR.
2. **Never approve, merge or sign off anything.** Approval is a human action. You may
   prepare a PR or record for approval, and record a human's approval by quoting their
   exact words with the evidence location. Never write an approval that a human didn't give.
3. **Never backdate a record.** Use the real date. When capturing something after the
   fact, say so and add a deviation (`forms/SOP-001-A03-deviation.md`).
4. **Never bump a part or document revision without updating everything that cites it**
   (`parts.csv`, BOMs, trace records, document headers).
5. **Every commit names what it changes:** `[PN] revX: summary (ECR #n)` for parts, or
   `[DOC] summary` for plans, requirements and reviews.
6. **Run the checks before finishing,** and report failures honestly.
7. **No secrets in the repo:** no API keys, tokens, passwords, Wi-Fi credentials or personal data.
8. **AI output is input, not a decision.** List each finding so the human can accept or
   reject it. Don't resolve findings yourself.
9. **Work on the current gate only.** Exploring and discussing later work is fine; acting on
   it is not. Do not register the project before G0, choose parts or allocate part numbers
   before the design stage (after G1), release parts before G2, or order anything before
   parts are released. Record ideas for later gates in `worklog.md`. Gates may be passed
   quickly, even several in one session, but always in order, each with its record and
   approval.

## Time tracking

At the end of each work session, add the session's time to the `worklog.md` entry: your own
working time per activity, and the human's hands-on time per activity. Ask the human for
theirs in one short question; do not estimate it for them. Activities: `planning`,
`requirements`, `design`, `part_selection`, `purchasing`, `documentation`, `review`, `build`,
`test`, `release`. At G4, compile the entries into `00_planning/scorecard.csv`.

## Conventions

- Tools: MCAD is Fusion, ECAD is KiCad. Design sources live in `02_design/`;
  released exports go in `03_build_package/` with the CAD version they came from.
- Lists that grow are CSV or YAML, not Markdown tables.
- Records are plain text a person could read in 20 years.
- Canadian English spelling.
