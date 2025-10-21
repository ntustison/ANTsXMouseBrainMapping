
# Abstract {-}

Large-scale efforts by the BRAIN Initiative Cell Census Network (BICCN) are
generating a comprehensive reference atlas of cell types in the mouse brain. A
key challenge in this effort is mapping diverse datasets, acquired with varied
imaging, tissue processing, and profiling methods, into shared coordinate
frameworks. Here, we present mouse brain mapping pipelines developed using the
Advanced Normalization Tools Ecosystem (ANTsX) to align MERFISH spatial
transcriptomics and high-resolution fMOST morphology data to the Allen Common
Coordinate Framework (CCFv3), and developmental MRI and LSFM data to the
Developmental CCF (DevCCF). Simultaneously, we introduce two novel methods: 1) a
velocity field–based approach for continuous interpolation across developmental
timepoints, and 2) a deep learning framework for automated brain parcellation
using minimally annotated and publicly available data. All workflows are
open-source and reproducible. We also provide general guidance for selecting
appropriate strategies across modalities, enabling researchers to adapt these
tools to new data.

\clearpage