
# Abstract {-}

Precision mapping techniques coupled with high resolution image acquisition of
the mouse brain permit the study of the spatial organization of gene activity
and their mutual interaction for a comprehensive view of salient
structural/functional relationships. Such research is facilitated by
standardized anatomical coordinate systems, such as the well-known Allen Common
Coordinate Framework (AllenCCFv3), and the ability to spatially map to such
standardized spaces.   The Advanced Normalization Tools Ecosystem (ANTsX) is a
comprehensive open-source software toolkit for generalized quantitative imaging,
which includes template building and mapping functionality, with applicability
to multiple organ systems, modalities, and animal species. Herein, we illustrate
the utility of ANTsX for generating precision spatial mappings of the mouse
brain.  \textcolor{red}{First, we provide ANTsX-based protocols for mapping
MERFISH, fMOST, and lightsheet datasets to AllenCCFv3 accounting for common
artefacts and other confounds.}  Novel ANTsX contributions include recently
developed ANTsX functionality for generating a velocity flow-based mapping
spanning the spatiotemporal domain of a longitudinal trajectory which we apply
to the Developmental Common Coordinate Framework (DevCCF).  Additionally, we
present an automated structural morphological pipeline for determining
volumetric and cortical thickness measurements analogous to the well-utilized
ANTsX pipeline for human neuroanatomical structural morphology.  This latter
development also illustrates a more general open-source ANTsX framework for
determining tailored brain parcellations using the AllenCCFv3 and DevCCF
templates.

\clearpage