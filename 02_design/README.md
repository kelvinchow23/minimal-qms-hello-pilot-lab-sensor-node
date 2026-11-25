# Design

Design sources and history, in folders:
- `build_document/`: sources of the build document (instruction steps, pictures, BOM,
  inspection checks, CAD exports) and `build_document.py`, which generates it.
- `test_procedures/`: TP-nnn and AN-nnn sources, and the test tools.
- `software/`: software source.
- `reviews/DR-nnn/`: formal reviews.

CAD lives in Fusion (project Tech, folder `LSN- Lab Sensor Node`); the version each output came
from is recorded in the document's title block, the A02 README and the review minutes.

The build package `03_build_package/` holds only the generated, controlled outputs, flat:
`<PN>_rev<X>.pdf` and its appendices `_A01_` to `_A05_`, plus `parts.csv`.
