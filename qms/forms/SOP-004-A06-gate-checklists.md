<!-- SOP-004-A06 Gate checklists (appendix to SOP-004; revised with it) -->

# Gate checklists

Each gate has two lists. **Records** must exist before the gate review; CI checks them
against `gates.yaml`. **Questions** are answered in the review; the agent uses them to
prepare the review package (SOP-003) and asks them during the stage, so that they are
answered as the work happens rather than at the gate.

For a later iteration, answer each question for what the iteration changes.

## G0 Scope approved

**Records:** `plan.yaml` (goal, scope in and out, make/buy, roles, target dates), `roles.yaml`.

**Questions**
- [ ] What problem does the product solve, and for whom?
- [ ] What is in scope, and what is explicitly out?
- [ ] What is made in-house, and what is bought?
- [ ] Who approves, and who builds?
- [ ] For a new iteration: which ECRs and lessons learned does it address?

## G1 Requirements reviewed

**Records:** `requirements.yaml`, `risks.csv`.

**Questions**
- [ ] Is each requirement measurable, with a number or a clear pass or fail?
- [ ] Does each requirement have a verification method (test, inspection, analysis or review)?
- [ ] Are the operating environment, power, safety and applicable standards covered?
- [ ] What could go wrong in use, in the build or with a supplier? Does each serious risk
      have a planned control?
- [ ] Is any requirement unnecessary, and could it be removed?

## G2 Design freeze

**Records:** design review minutes and the build document with its appendices
(A01 BOM, A02 make files including PCB files, A03 inspection and test, A04 traveller), all
exported before the review. Software that only runs on the finished unit is not frozen at G2.

**Questions**
- [ ] Does every requirement have a design output that meets it, and a test or check that
      will show it?
- [ ] Is the control for every risk in the design?
- [ ] Does every part have a supplier, is it in stock, and can the chosen assembler build
      with it?
- [ ] Is anything new or unproven, and has it been prototyped or analyzed?
- [ ] Could the product be bought, built and tested from the build package alone?
- [ ] Has every independent review finding been accepted, or rejected with a reason?
- [ ] For a later iteration: what changed since the last release, does it affect units
      already built, and is each change a new revision or a new part (SOP-002)?

## G3 Verified

**Records:** `build.yaml`, the travellers and `test_results.csv` for each build (`trace.csv`
and `inspection.csv` only where kept, SOP-006); the released build document and its tag.

**Questions**
- [ ] Has every requirement verified by test been tested on every unit, or on the agreed
      sample?
- [ ] Was every failure traced to the design or to the unit, and resolved (SOP-004
      section 6, SOP-008)?
- [ ] Was the test equipment fit for use, with calibration in date?
- [ ] Where a unit is traced, does its trace record resolve to inspected parts?
- [ ] Did anything pass but behave unexpectedly, and is it recorded?
- [ ] Is every fix found while building in the build document, re-exported, and do the units
      to be released match it (or are the differences recorded)?
- [ ] Release: is the build document set to Released, and tagged `<PN>-rev<X>`?

## G4 Released

**Records:** `release.yaml` for every unit, NC records closed or dispositioned, lessons
learned, `scorecard.csv`.

**Questions**
- [ ] Is every unit released or dispositioned, and labelled?
- [ ] Are open NCs and review actions closed or carried forward?
- [ ] What went well, what went wrong, and where was the AI wrong?
- [ ] What should the next iteration change? Are those changes raised as ECRs?
- [ ] Where did the human time go, according to the scorecard?
