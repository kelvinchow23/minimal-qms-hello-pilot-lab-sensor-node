# Design

Design sources and history:
- `build_document/`: sources of each assembly's build document (instruction steps, pictures,
  `bom.csv`, `inspection_checks.csv`, CAD exports) and `build_document.py`, which generates it.
- `test_procedures/`: test procedure and analysis sources, and test tools.
- `software/`: software and firmware source.
- `reviews/DR-nnn/`: formal reviews.

CAD lives in Fusion (project Tech, folder `LSN- Lab Sensor Node`); the version each output came
from is recorded in the document's title block, the A02 README and the review minutes.

The build documents generated from these go in `03_build_package/`, flat (SOP-004 section 9).
