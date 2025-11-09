# Introduction

Over the past decade, there have been significant advancements in mesoscopic
single-cell analysis of the mouse brain. It is now possible to track single
neurons [@Keller:2015aa], observe whole-brain developmental changes at cellular
resolution [@La-Manno:2021aa], associate brain regions with genetic composition
[@Wen:2022aa], and locally characterize neural connectivity [@Oh:2014aa]. These
scientific achievements have been propelled by high-resolution profiling and
imaging techniques that enable submicron, multimodal, 3D
characterizations of whole mouse brains. Among these are micro-optical
sectioning tomography [@Gong:2013aa;@Li:2010aa], tissue clearing methods
[@Keller:2015aa;@Ueda:2020aa], spatial transcriptomics
[@Stahl:2016aa;@Burgess:2019aa], and single-cell genomic profiling
[@hardwick:2022aa], each offering expanded specificity and resolution for
cell-level brain analysis.

Recent efforts by the NIH BRAIN Initiative have mobilized large-scale
international collaborations to create a comprehensive reference database of
mouse brain structure and function. The BRAIN Initiative Cell Census Network
has aggregated over 40 multimodal datasets from more than 30 research
groups [@hawrylycz:2023aa], many of which are registered to standardized
anatomical coordinate systems to support integrated analysis. Among the most
widely used of these frameworks is the Allen Mouse Brain Common Coordinate
Framework (CCFv3) [@Wang:2020aa]. Other CCFs include modality-specific
references [@perens:2021aa;@ma:2005aa;@qu:2022aa] and developmental atlases
[@Kronman:2024aa;@chuang:2011aa] that track structural change across time.

<!-- ## Mouse brain mapping challenges -->

Robust mapping of cell type data into CCFs is essential for integrative analysis
of morphology, connectivity, and molecular identity. However, each modality
poses unique challenges. For example, differences in tissue processing, imaging
protocols, and anatomical completeness often introduce artifacts such as
distortion, tearing, holes, and signal dropout
[@dries:2021aa;@ricci:2022aa;@agarwal:2016aa;@agarwal:2017aa;@tward:2019aa;@cahill:2012aa].
Intensity differences and partial representations of anatomy can further
complicate alignment. Also, while alternative strategies for mapping single-cell
spatial transcriptomic data exist (e.g., gene expression–based models such as
Tangram [@Biancalani:2021aa]) this work focuses on image-based anatomical
alignment to common coordinate frameworks using spatially resolved reference
images.  Given this diversity specialized strategies are often needed to address
the unique, modality-specific challenges.  

Existing mapping solutions fall into three broad categories. The first includes
integrated processing platforms that provide users with mapped datasets (e.g.,
Allen Brain Cell Atlas [@sunkin:2012], Brain Architecture Portal [@kim:2017aa],
OpenBrainMap [@Furth:2018aa], and Image and Multi-Morphology Pipeline
[@li:2022aa]). These offer convenience and high-quality curated data, but
limited generalizability and customization. The second category involves highly
specialized pipelines tailored to specific modalities such as histology
[@puchades:2019aa;@eastwood:2019aa;@Ni:2020aa], magnetic resonance imaging (MRI)
[@Pallast:2019aa;@Celestine:2020aa;@Ioanas:2021aa], microCT
[@aggarwal:2009aa;@chandrashekhar:2021aa], light sheet fluorescence microscopy
(LSFM) [@Jin:2022aa;@Negwer:2022aa], flourescence micro-optical sectioning
tomography (fMOST) [@qu:2022aa;@lin:2023aa], and spatial transcriptomics,
including multiplexed error-robust fluorescence in situ hybridization (MERFISH)
[@zhang:2021aa;@shi:2023aa;@zhang:2023aa]. While effective, these solutions
often require extensive engineering effort to adapt to new datasets or
modalities.  Finally, general-purpose toolkits such as elastix [@Klein:2010aa],
Slicer3D [@fedorov:2012aa], and the Advanced Normalization Tools Ecosystem
(ANTsX) [@Tustison:2021aa] have all been applied to mouse brain mapping
scenarios. These toolkits support modular workflows that can be flexibly
composed from reusable components, offering a powerful alternative to rigid,
modality-specific solutions. However, their use often requires familiarity with
pipeline modules, parameter tuning, and tool-specific conventions which can
limit adoption.

Building on this third category, we describe a set of modular, ANTsX-based
pipelines specifically tailored for mapping diverse mouse brain data into
standardized anatomical frameworks. These include two new pipelines: a velocity
field–based interpolation model that enables continuous transformations across
developmental timepoints of the DevCCF, and a template-based deep learning
pipeline for whole brain segmentation (i.e., brain extraction) and structural
anatomical regional labeling of the brain (i.e., brain parcellation) requiring
minimal annotated data. In addition, we include two modular pipelines for
aligning MERFISH and fMOST datasets to the Allen CCFv3. While the MERFISH
dataset was previously published as part of earlier BICCN efforts [@Yao:2023aa],
the full image processing and registration workflow had not been described in
detail until now. The fMOST workflow, by contrast, was developed internally to
support high-resolution morphology mapping and has not been previously published
in any form. Both pipelines were built using ANTsX tools, adapted for
collaborative use with the Allen Institute, and are now released as fully
reproducible, open-source workflows to support reuse and extension by the
community.  To facilitate broader adoption, we also provide general guidance for
customizing these strategies across imaging modalities and data types.  We first
introduce key components of the ANTsX toolkit, which provide a basis for all of
the mapping workflows described here, and then detail the specific contributions
made in each pipeline.
