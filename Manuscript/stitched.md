---
title:
author: 
address:
output:
  pdf_document:
    fig_caption: true
    latex_engine: pdflatex
    keep_tex: yes
    number_sections: true
    toc: true
  word_document:
    fig_caption: true
bibliography:
  - references.bib
  - references2.bib
csl: nature.csl
longtable: true
urlcolor: blue
header-includes:
  - \usepackage{longtable}
  - \usepackage{graphicx}
  - \usepackage{booktabs}
  - \usepackage{textcomp}
  - \usepackage{xcolor}
  - \usepackage{colortbl}
  - \usepackage{geometry}
  - \usepackage{subcaption}
  - \usepackage{lineno}
  - \usepackage{makecell}
  - \usepackage{pdflscape}
  - \definecolor{listcomment}{rgb}{0.0,0.5,0.0}
  - \definecolor{listkeyword}{rgb}{0.0,0.0,0.5}
  - \definecolor{listnumbers}{gray}{0.65}
  - \definecolor{listlightgray}{gray}{0.955}
  - \definecolor{listwhite}{gray}{1.0}
geometry: margin=1.0in
fontsize: 12pt
linestretch: 1.5
mainfont: Georgia
---

\linenumbers
\pagenumbering{gobble}

\setstretch{1}

\begin{centering}

$ $

\vspace{6cm}

\LARGE

{\bf Modular strategies for spatial mapping of multi-modal mouse brain data}

\vspace{1.0 cm}

\normalsize

Nicholas J. Tustison$^{1}$,
Min Chen$^{2}$,
Fae N. Kronman$^{3}$,
Jeffrey T. Duda$^{2}$,
Clare Gamlin$^{4}$,
Mia G. Tustison,
Michael Kunst$^{4}$,
Rachel Dalley$^{4}$,
Staci Sorenson$^{4}$,
Quanxin Wang$^{4}$,
Lydia Ng$^{4}$,
Yongsoo Kim$^{3}$, and
James C. Gee$^{2}$

\small

$^{1}$Department of Radiology and Medical Imaging, University of Virginia, Charlottesville, VA \\
$^{2}$Department of Radiology, University of Pennsylvania, Philadelphia, PA \\
$^{3}$Department of Neural and Behavioral Sciences, Penn State University, Hershey, PA \\
$^{4}$Allen Institute for Brain Science, Seattle, WA \\

\end{centering}

\vspace{3.5 cm}

\noindent\rule{4cm}{0.4pt}

\scriptsize
Corresponding authors: \

Nicholas J. Tustison, DSc \
Department of Radiology and Medical Imaging \
University of Virginia \
ntustison@virginia.edu \

James C. Gee, PhD \
Department of Radiology \
University of Pennsylvania \
gee@upenn.edu 

\normalsize

\newpage

\setstretch{1.5}

# Abstract {-}

Large-scale efforts by the BRAIN Initiative Cell Census Network (BICCN) are
generating a comprehensive reference atlas of cell types in the mouse brain. A
key challenge in this effort is mapping diverse datasets—acquired with varied
imaging, tissue processing, and profiling methods—into shared coordinate
frameworks. Here, we present modular mapping pipelines developed using the
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


\clearpage# Introduction

Over the past decade, there have been significant advancements in mesoscopic
single-cell analysis of the mouse brain. It is now possible to track single
neurons [@Keller:2015aa], observe whole-brain developmental changes at cellular
resolution [@La-Manno:2021aa], associate brain regions with genetic composition
[@Wen:2022aa], and locally characterize neural connectivity [@Oh:2014aa]. These
scientific achievements have been propelled by high-resolution profiling and
imaging techniques that enable submicron, multimodal, three-dimensional
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

## Mouse brain mapping challenges

Robust mapping of cell type data into CCFs is essential for integrative analysis
of morphology, connectivity, and molecular identity. However, each modality
poses unique challenges. For example, differences in tissue processing, imaging
protocols, and anatomical completeness often introduce artifacts such as
distortion, tearing, holes, and signal dropout
[@dries:2021aa;@ricci:2022aa;@agarwal:2016aa;@agarwal:2017aa;@tward:2019aa;@cahill:2012aa].
Intensity differences and partial representations of anatomy can further complicate
alignment. Given this diversity specialized strategies are often needed to address
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
scenarios (e.g., [@Rolfe:2023aa]). These toolkits support modular workflows that
can be flexibly composed from reusable components, offering a powerful
alternative to rigid, modality-specific solutions. However, their use often
requires familiarity with pipeline modules, parameter tuning, and tool-specific
conventions which can limit adoption.

Building on this third category, we describe a set of modular, ANTsX-based
pipelines specifically tailored for mapping diverse mouse brain data into
standardized anatomical frameworks. These include two new pipelines: a velocity
field–based interpolation model that potentially enables biologically plausible
transformations across developmental timepoints, and a template-based deep
learning pipeline for brain extraction and parcellation requiring minimal
annotated data. In addition, we include two modular pipelines for aligning
multiplexed error-robust fluorescence in situ hybridization (MERFISH) and fMOST
datasets to the Allen CCFv3. These workflows were adapted and tailored using
ANTsX tools to support collaborative efforts within the BICCN and are now made
openly available in a reproducible format. To facilitate broader adoption, we
also provide general guidance for customizing these strategies across imaging
modalities and data types.  We first introduce key components of the ANTsX
toolkit, which provide a basis for all of the mapping workflows described here,
and then detail the specific contributions made in each pipeline.


## The Advanced Normalization Tools Ecosystem (ANTsX)

The Advanced Normalization Tools Ecosystem (ANTsX) has been used in a number of
applications for mapping mouse brain data as part of core processing steps in
various workflows
[@pagani:2016aa;@Anderson:2019aa;@Ni:2020aa;@allan:2019aa;@Yao:2023aa],
particularly its pairwise, intensity-based image registration capabilities
[@Avants:2008aa] and bias field correction [@Tustison:2010ac]. Historically,
ANTsX development is based on foundational approaches to image mapping
[@Bajcsy:1982aa;@Bajcsy:1989aa;@Gee:1993aa], especially in the human brain, with
key contributions such as the Symmetric Normalization (SyN) algorithm
[@Avants:2008aa]. It has been independently evaluated in diverse imaging domains
including multi-site brain MRI [@Klein:2009aa], pulmonary CT [@Murphy:2011aa],
and multi-modal brain tumor registration [@Baheti:2021aa].

Beyond registration, ANTsX provides functionality for template generation
[@Avants:2010aa], intensity-based segmentation [@Avants:2011uf], preprocessing
[@Manjon:2010aa;@Tustison:2010ac], and deep learning [@Tustison:2021aa]. It has
demonstrated strong performance in consensus labeling [@Wang:2013ab], brain
tumor segmentation [@Tustison:2014aa], and cardiac motion estimation
[@Tustison:2015ab]. Built on the Insight Toolkit (ITK) [@McCormick:2014aa],
ANTsX benefits from open-source contributions while supporting continued
algorithm evaluation and innovation.  In the context of mouse brain data, ANTsX
provides a robust platform for developing modular pipelines to map diverse
imaging modalities into CCFs. This paper highlights its use across distinct
BICCN projects such as spatial transcriptomic data from MERFISH, structural data
from fMOST, and multimodal developmental data from LSFM and MRI. We describe
both shared infrastructure and targeted strategies adapted to the specific
challenges of each modality.

## Novel ANTsX-based open-source contributions

We introduce two novel contributions to ANTsX developed as part of collabortive
efforts in creating the Developmental Common Coordinate Framework (DevCCF)
[@Kronman:2024aa]. First, we present an open-source velocity field–based
interpolation framework for continuous mapping across the sampled embryonic and
postnatal stages of the DevCCF atlas [@Kronman:2024aa]. This functionality
enables biologically plausible interpolation between timepoints via a
time-parameterized diffeomorphic velocity model [@Beg:2005aa], inspired by
previous work [@Tustison:2013ac]. Second, we present a deep learning pipeline
for structural parcellation of the mouse brain from multimodal MRI data. This
includes two novel components: 1) a template-derived brain extraction model
using augmented data from two ANTsX-derived template datasets
[@Hsu2021;@Reshetnikov2021], and 2) a template-derived parcellation model
trained on DevCCF P56 labelings mapped from the AllenCCFv3. This pipeline
demonstrates how ANTsX tools and public resources can be leveraged to build
robust anatomical segmentation pipelines with minimal annotated data. We
independently evaluate this framework using a longitudinal external dataset
[@Rahman:2023aa], demonstrating generalizability across specimens and imaging
protocols. All components are openly available through the R and Python ANTsX
packages, with general-purpose functionality documented in a reproducible,
cross-platform tutorial (https://tinyurl.com/antsxtutorial). Code specific to
this manuscript, including scripts to reproduce the novel contributions 
and all associated evaluations, is provided in a dedicated repository
(https://github.com/ntustison/ANTsXMouseBrainMapping). Additional tools for
mapping spatial transcriptomic (MERFISH) and structural (fMOST) data to the
AllenCCFv3 are separately available 
at (https://github.com/dontminchenit/CCFAlignmentToolkit).


\clearpage
\newpage

# Results

\begin{figure*}
\centering
\begin{subfigure}[t]{0.49\textwidth}
\centering
\includegraphics[width=0.99\textwidth]{Figures/merfishPipeline.pdf}
\caption{}
\end{subfigure} 
\begin{subfigure}[t]{0.49\textwidth}
\centering
\includegraphics[width=0.99\textwidth]{Figures/fmostPipeline.pdf}
\caption{}
\end{subfigure}
\caption{Diagram of the two ANTsX-based pipelines for mapping (a) MERFISH
          and (b)fMOST data into the space of AllenCCFv3.  Each generates
         the requisite transforms, $\mathcal{T}$, to map individual images
         to the CCF.}
\label{fig:allenpipelines}
\end{figure*}


## AllenCCFv3 brain image mapping

<!--
\newcommand{\ROT}[1]{\rotatebox{60}{\parbox{1.875cm}{\scriptsize #1}}}
\newcommand{\STAB}[1]{#1}

\begin{table}[!h]
  \centering
  \begin{tabular}{l|p{1.cm}p{1.cm}p{1.cm}p{1.cm}p{1.cm}p{1.cm}p{1.cm}p{1.cm}}
    & \STAB{\ROT{Background}}
    & \STAB{\ROT{Whole brain}}
    & \STAB{\ROT{Fimbria}}
    & \STAB{\ROT{Habenular commissure}}
    & \STAB{\ROT{Posterior choroid plexus}}
    & \STAB{\ROT{Anterior choroid plexus}}
    & \STAB{\ROT{Optic chiasm}}
    & \STAB{\ROT{Caudate putamen}}
    \\
    \hline
    {\footnotesize Dice} & {\footnotesize \bf 0.99} 
                         & {\footnotesize \bf 0.99} 
                         & {\footnotesize \bf 0.91} 
                         & {\footnotesize 0.63} 
                         & {\footnotesize \bf 0.93} 
                         & {\footnotesize \bf 0.96} 
                         & {\footnotesize 0.77} 
                         & {\footnotesize \bf 0.97}
  \end{tabular}
  \caption{Dice overlap of landmark labels between corresponding structures 
           in the fMOST average atlas and AllenCCFv3.} 
  \label{table:allenresults}
\end{table}
-->

### Mapping multiplexed error-robust fluorescence in situ hybridization (MERFISH) data

__Overview.__ The ANTsX framework was used to develop a pipeline for mapping
multiplexed error-robust fluorescence in situ hybridization (MERFISH) spatial
transcriptomic mouse data onto the AllenCCFv3 (see Figure
\ref{fig:allenpipelines}(a)). This pipeline, used recently in creating a
high-resolution transcriptomic atlas of the mouse brain [@Yao:2023aa], performs
mappings by first generating anatomical labels from tissue related gene
expressions in the MERFISH data, and then spatially matching these labels to
corresponding anatomical tissue parcellations in the AllenCCFv3. The pipeline
consists of MERFISH data specific preprocessing which includes section
reconstruction, mapping corresponding anatomical labels between AllenCCFv3 and
the spatial transcriptomic maps of the MERFISH data, and matching MERFISH
sections to the atlas space. Following preprocessing, two main alignment steps
were performed: 1) 3-D global affine mapping and section matching of the
AllenCCFv3 into the MERFISH data and 2) 2-D global and deformable mapping between
each MERFISH section and matched AllenCCFv3 section. Mappings learned via each
step in the pipeline are preserved and concatenated to provide point-to-point
correspondence between the original MERFISH data and AllenCCFv3, thus allowing
individual gene expressions to be transferred into the AllenCCFv3. 

__Data.__ MERFISH mouse brain data was acquired using a previously detailed procedure
[@Yao:2023aa]. Briefly, a brain of C57BL/6 mouse was dissected according to
standard procedures and placed into an optimal cutting temperature (OCT)
compound (Sakura FineTek 4583) in which it was stored at -80$^\circ$C. The fresh frozen
brain was sectioned at $10 \mu m$ on Leica 3050 S cryostats at intervals of 
$200 \mu m$ to evenly cover the brain. A set of 500 genes were imaged that had been
carefully chosen to distinguish the ${\sim}5200$ clusters of our existing RNAseq
taxonomy. For staining the tissue with MERFISH probes, a modified version of
instructions provided by the manufacturer was used [@Yao:2023aa]. Raw MERSCOPE
data were decoded using Vizgen software (v231).  Cells were segmented based on
DAPI and PolyT staining using Cellpose [@Liu:2023aa;@Stringer:2021aa].
Segmentation was performed on a median z-plane (fourth out of seven) and cell
borders were propagated to z-planes above and below. To assign cluster identity
to each cell in the MERFISH dataset, we mapped the MERFISH cells to the
scRNA-seq reference taxonomy. 

__Evaluation.__ Alignment of the MERFISH data into the AllenCCFv3 was
qualitatively assessed by an expert anatomist at each iteration of the
registration using known correspondence of gene markers and their associations
with the AllenCCFv3. As previously reported [@Yao:2023aa], further assessment of
the alignment showed that, of the 554 terminal regions (gray matter only) in the
AllenCCFv3, only seven small subregions were missed from the MERFISH dataset:
frontal pole, layer 1 (FRP1), FRP2/3, FRP5; accessory olfactory bulb, glomerular
layer (AOBgl); accessory olfactory bulb, granular layer (AOBgr); accessory
olfactory bulb, mitral layer (AOBmi); and accessory supraoptic group (ASO).


### Mapping fluorescence micro-optical sectioning tomography (fMOST) data

__Overview.__  We developed a pipeline for mapping fluorescence micro-optical
sectioning tomography (fMOST) mouse brain images into the AllenCCFv3 (see Figure
\ref{fig:allenpipelines}(b)). The pipeline is adapted from previously developed
frameworks for human brain mapping[@Avants:2010aa], and uses a modality specific
(fMOST) average atlas to assist in the image registration and mapping. This
approach has been well validated in human studies
[@jia:2011aa;@tang:2009aa;@dewey:2017aa], and successfully used in other mouse
data [@perens:2023aa;@Wang:2020aa;@qu:2022aa]. Briefly, we construct an
intensity- and shape-based average fMOST atlas using 30 fMOST images to serve as
an intermediate registration target for mapping fMOST images from individual
specimens into the AllenCCFv3. Preprocessing steps include downsampling to match
the $25 \mu m$ isotropic AllenCCFv3, acquisition-based stripe artifact removal,
and inhomogeneity correction [@Tustison:2010ac]. Preprocessing also includes a
single annotation-driven registration to establish a canonical mapping between
the fMOST atlas and the AllenCCFv3. This step allows us to align expert
determined landmarks to accurately map structures with large morphological
differences between the modalities, which are difficult to address using
standard approaches. Once this canonical mapping is established, standard
intensity-based registration is used to align each new fMOST image to the fMOST
specific atlas. This mapping is concatenated with the canonical fMOST
atlas-to-AllenCCFv3 mapping to further map each individual brain into the latter
without the need to generate additional landmarks. Transformations learned
through this mapping can be applied to single neuron reconstructions from the
fMOST images to evaluate neuronal distributions across different specimens into
the AllenCCFv3 for the purpose of cell census analyses.

__Data.__ The high-throughput and high-resolution fluorescence micro-optical
sectioning tomography (fMOST) [@Gong:2016aa;@Wang:2021aa] platform was used to
image 55 mouse brains containing gene-defined neuron populations, with sparse
transgenic expression [@Rotolo:2008aa;@Peng:2021aa]. In short, the fMOST imaging
platform results in 3-D images with voxel sizes of $0.35 \times 0.35 \times 1.0
\mu m^3$ and is a two-channel imaging system where the green channel displays
the green fluorescent protein (GFP) labeled neuron morphology and the red
channel is used to visualize the counterstained propidium iodide
cytoarchitecture. The spatial normalizations described in this work were
performed using the red channel, which offered higher tissue contrast for
alignment, although other approaches are possible including multi-channel
registration.

__Evaluation.__  Evaluation of the canonical fMOST atlas to Allen CCFv3 mapping
was performed via quantitative comparison at each step of the registration and
qualitative assessment of structural correspondence after alignment by an expert
anatomist. Dice values were generated for the following structures: whole brain,
0.99; fimbria, 0.91; habenular commissure, 0.63; posterior choroid plexus, 0.93;
anterior choroid plexus,  0.96; optic chiasm, 0.77; caudate putamen, 0.97.
Similar qualitative assessment was performed for each fMOST specimen including
the corresponding neuron reconstruction data.
<!--
## Template building

Template building using ANTsX tools was first described in the context of
hippocampal studies [@Avants:2010aa].  Multi-modal and symmetrical variants were
subsequently described as part of a proposed brain tumor segmentation approach
based on random forests [@Tustison:2015vl].  Template building
capabilities are available in both ANTsPy (``ants.build_template(...)``) and
ANTsR (``buildTemplate(...)``) as well as part of 
the core ANTs package (e.g., ``antsMultivariateTemplateConstruction.sh``).

### Data preparation

Multi-modal symmetric template construction is performed separately for each
developmental stage. Prior to optimization, preprocessing can include several
steps not all of which are required but are dependent on the data and the
particular requirements of the study.  For MRI scans, inhomogeneity correction
is often necessary and can be performed using the ANTsPy function
``ants.n4_bias_field_correction(...)`` which is a wrapper for the N4 algorithm
[@Tustison:2010ac].  Denoising is another preprocessing step that can
potentially improve template quality results.  The ANTsPy function
``ants.denoise_image(...)`` is an implementation of a well-known denoising
algorithm [@Manjon:2010aa].  For a typical image, both of these steps takes
approximately on the order of a couple minutes.  In ANTsX, due to legacy code
issues, only bias correction is wrapped with template building so one need not
perform this step prior to optimization.  In addition,
brain extraction has demonstrated improved performance in the context of human
brain normalization [@Klein:2010ab] and is similarly used in mouse brain
registration to maximize alignment.  Various approaches within ANTs are possible
including a template-based approach ``antsBrainExtraction.sh`` or using deep
learning ``antspynet.mouse_brain_extraction(...)``.  Additionally, it is
important to ensure a standardized orientation, similar to the Dicom standard
for human brain imaging.  A study requirement of template bilateral symmetry is
also an important consideration prior to template generation.  This can 
be performed by either flipping all the input images contralaterally such that
all input specimens are represented twice or one can generate an initial 
asymmetric template, flipping it contralaterally, and using the two asymmetric 
templates in a subsequent template generation call to create a single symmetric 
template.  For multi-modal templates, all the images for a single specimen need
to be mutually aligned in the same image space prior to optimization.  After 
selecting the target image space for a particular specimen (e.g., T2-weighted MRI),
this can be performed with a rigid transform registration call using 
``ants.registration(...)``.  It should be noted that for most applications, the 
general heuristic of $\approx 10$ randomly sampled specimens is sufficient for
a satisfactory template.

In the case of the DevCCF, bias correction was employed in generating the
multiple stage templates using the shell script
``antsMultivariateConstruction.sh``.  Brain extraction was applied to the
postnatal images.  Template symmetrization employed the original and
contralateral versions of all specimen images.

### Optimization {-}

Template generation is initialized with either a user-provided image or a
bootstrapped initialization template constructed from the input data.  If the
latter is selected, the voxelwise averaged image for each modality is
constructed followed by a linear registration of each specimen to this template
initialization which refines the estimate.  The former option is often used
where computational considerations are important.  For example, this initial
template can be generated using low resolution input data or only a subset of
the input cohort.  This higher quality initial estimate can then be further
refined using the entire data set at full resolution.  

Following template initialization, each specimen is registered to the current
template estimate, which can be performed in parallel.  After the current round
of registrations is complete, a voxelwise average of each modality is performed
with optional Laplacian sharpening followed by a "shape update" step. This shape
update step is used to warp the current estimate of the template so that its
shape is closer to the mean shape of the input data.  Implementation-wise this
is done by averaging each displacement field that points from the template to
the affinely warped specimen.  This average displacement field is then used to
deform the voxelwise-averaged template.  Shape and intensity template
convergence typically occurs in four deformable iterations.

-->

<!--
############################################
############################################
############################################
############################################
-->

## Continuously mapping the DevCCF developmental trajectory with a velocity flow model

\begin{figure}
\centering
\includegraphics[width=0.99\textwidth]{Figures/lowerLeftPanel.pdf}
\caption{The spatial transformation between any two time points within the
continuous DevCCF longitudinal developmental trajectory is available through the
use of ANTsX functionality for generating a velocity flow model.}
\label{fig:devccfvelocity}
\end{figure} 

The DevCCF is an openly accessible resource for the mouse brain research
community [@Kronman:2023aa].  It consists of multi-modal MRI and LSFM symmetric
ANTsX-generated templates [@Avants:2010aa] sampling the mouse brain
developmental trajectory, specifically the embryonic (E) and postnatal (P) days
E11.5, E13.5, E15.5, E18.5 P4, P14, and P56.  Each template space includes
structural labels defined by a developmental ontology. Its utility is also
enhanced by a coordinated construction with AllenCCFv3. Although this work
represents a significant contribution, the gaps between time points potentially
limit its applicability which could be addressed through the development of the
ability to map not only between time points but also within and across
time points.

To continuously generate transformations between the different stages of the
DevCCF atlases, we developed a general velocity flow model approach which we
apply to DevCCF-derived data.  We also introduce this functionality into both
the ANTsR and ANTsPy packages (for the latter, see
``ants.fit_time_varying_transform_to_point_sets(...)``) for potential
application to this and other analagous scenarios (e.g., modeling the cardiac
and respiratory cycles).  ANTsX, being built on top of ITK, uses an ITK image
data structure for the 4-D velocity field where each voxel contains the $x$,
$y$, $z$ components of the field at that point. 

<!-- Both ANTsX platforms include a complete suite of functions
for determining dense correspondence from sparse landmarks based on a variety of
transformation models ranging from standard linear models (i.e., rigid, affine)
to deformable diffeomorphic models (e.g., symmetric normalization
[@Avants:2008aa]).  The latter set includes transformation models for both the
pairwise scenario and for multiple sets, as in the case of the DevCCF.
 -->

### Data

\begin{figure}[!htb]
\centering
\includegraphics[width=0.75\textwidth]{Figures/SimplifiedAnnotations.pdf}
\caption{Annotated regions representing common labels across developmental stages which
are illustrated for both P4 and P14.}
\label{fig:simplifiedannotations}
\end{figure}

Labeled annotations are available as part of the original DevCCF and reside in
the space of each developmental template which range in resolution from $31.5-50
\mu$m.  Across all atlases, the total number of labeled regions exceeds 
2500.  From these labels, a common set of 26 labels (13 per hemisphere) across
all atlases were used for optimization and evaluation.  These simplified regions
include: terminal hypothalamus, subpallium, pallium, peduncular hypothalamus,
prosomere, prosomere, prosomere, midbrain, prepontine hindbrain, pontine
hindbrain, pontomedullary hindbrain, medullary hindbrain, and tracts (see Figure
\ref{fig:simplifiedannotations}).

Prior to velocity field optimization, all data were rigidly transformed to 
DevCCF P56 using the centroids of the common label sets. In order to
determine the landmark correspondence across DevCCF stages, the multi-metric
capabilities of ``ants.registration(...)`` were used. Instead of performing
intensity-based pairwise registration directly on these multi-label images, each
label was used to construct a separate fixed and moving image pair resulting in
a multi-metric registration optimization scenario involving 24 binary image
pairs (each label weighted equally) for optimizing diffeomorphic correspondence
between neighboring time point atlases using the mean squares metric and the
symmetric normalization transform [@Avants:2008aa].

To generate the set of common point sets across all seven developmental atlases,
the label boundaries and whole regions were sampled in the P56 atlas and then
propagated to each atlas using the transformations derived from the pairwise
registrations.  We selected a sampling rate of 10\% for the contour points and
1\% for the regional points for a total number of points being per atlas being
$173303$ ($N_{contour} = 98151$ and $N_{region}=75152$). Regional boundary
points were weighted twice as those of non-boundary points during optimization.  

### Velocity field optimization

\begin{figure}[!htb]
\centering
\includegraphics[width=0.99\textwidth]{Figures/convergence.pdf}
\caption{Convergence of the optimization of the velocity field for describing
the transformation through the developmental stages from E11.5 through P56.
Integration points in diagram on the right are color-coordinated with the center
plot and placed in relation to the logarithmically situated temporal placement
of the individual DevCCF atlases.}
\label{fig:convergence}
\end{figure}

The velocity field was optimized using the input composed of the seven
corresponding point sets and their associated weight values, the selected number
of integration points for the velocity field ($N=11$), and the parameters
defining the geometry of the spatial dimensions of the velocity field.  Thus,
the optimized velocity field described here is of size $[256, 182, 360]$ ($50
\mu$m isotropic) $\times 11$ integration points for a total compressed size of a
little over 2 GB.  This choice represented weighing the trade-off between
tractability, portability, and accuracy.  However,  all data and code to
reproduce the results described are available in the dedicated GitHub 
repository.

The normalized time point scalar value for each atlas/point-set in the temporal
domains $[0, 1]$ was also defined. Given the increasingly larger gaps in the
postnatal time point sampling, we made two adjustments.  Based on known mouse
brain development, we used 28 days for the P56 data.  We then computed the log
transform of the adjusted set of time points prior to normalization between 0
and 1 (see the right side of Figure \ref{fig:convergence}).  This log transform,
as part of the temporal normalization, significantly improves the temporal spacing
of data. 

The maximum number of iterations was set to 200 with each iteration taking
approximately six minutes on a 2020 iMac (processor, 3.6 GHz 10-Core Intel Core
i9; memory, 64 GB 2667 MHz DDR4) At each iteration we looped over the 11
integration points. At each integration point, the velocity field estimate was
updated by warping the two immediately adjacent point sets to the integration
time point and determining the regularized displacement field between the two
warped point sets.  As with any gradient-based descent algorithm, this field was
multiplied by a small step size ($\delta = 0.2$) before adding to the current
velocity field.  Convergence is determined by the average displacement error
over each of the integration points. As can be seen in the left panel of Figure
\ref{fig:convergence}, convergence occurred around 125 iterations when the
average displacement error over all integration points is minimized. The median
displacement error at each of the integration points also trends towards zero
but at different rates. 

<!-- 
\begin{figure}[!htb]
\centering
\includegraphics[width=0.75\textwidth]{Figures/warpedP56Volumes.pdf}
\caption{After the velocity field is generated, we can use it to warp
the simplified labels of the P56 atlas continuously over the interval
$[0, 1]$ and plot the volumes of the atlas regions.  Note how they 
compare with the volumes of the same regions in the other atlases.}
\label{fig:warpedP56}
\end{figure} 
-->

<!-- 
After optimization, we use the velocity field to warp
the P56 set of labels to each of the other atlas time points to compare the
volumes of the different simplified annotated regions.  This is shown in Figure
\ref{fig:warpedP56}. 
-->


### The velocity flow transformation model

\begin{figure}[!htb]
\centering
\includegraphics[width=0.8\textwidth]{Figures/CrossWarp.pdf}
\caption{Mid-sagittal visualization of the effects of the transformation model in
warping every developmental stage to the time point of every other developmental
stage.  The original images are located along the diagonal.  Columns correspond
to the warped original image whereas the rows represent the reference space to which
each image is warped.}
\label{fig:crosswarp}
\end{figure}

\begin{figure}[!htb]
\centering
\includegraphics[width=0.8\textwidth]{Figures/pseudo_template.pdf}
\caption{Illustration of the use of the velocity flow model for creating virtual templates
at continuous time points not represented in one of the existing DevCCF time points.
For example, FA templates at time point P10.3 and P20 can be generated by warping the 
existing temporally adjacent developmental templates to the target time point and using 
those images in the ANTsX template building process.}
\label{fig:virtual}
\end{figure}

Once optimized, the resulting velocity field can be used to generate the
deformable transform between any two continuous points within the time interval
bounded by E11.5 and P56.  As a demonstration, in Figure \ref{fig:crosswarp}, we
transform each atlas to the space of every other atlas using the DevCCF
transform model. Additionally, one can use this transformation model to
construct virtual templates in the temporal gaps of the DevCCF.  Given an
arbitrarily chosen time point within the normalized time point interval, the
existing adjacent DevCCF atlases on either chronological side can be warped to
the desired time point. A subsequent call to one of the ANTsX template building
functions then permits the construction of the template at that time point. In
Figure \ref{fig:virtual}, we illustrate the use of the DevCCF velocity flow
model for generating two such virtual templates for two arbitrary time points.
Note that both of these usage examples can be found in the GitHub repository
previously given.


## Automated structural parcellations of the mouse brain

<!-- One of the most well-utilized pipelines in the ANTsX toolkit is the generation
of cortical thickness maps in the human brain from T1-weighted MRI.  Starting
with the novel Diffeomorphic Registration-based Cortical Thickness (DiReCT)
algorithm [@Das:2009uv], a complete algorithmic workflow was developed for both
cross-sectional [@Tustison:2014ab] and longitudinal [@Tustison:2019aa]
T1-weighted MR image data.  This contribution was later refactored using deep
learning [@Tustison:2021aa] leveraging the earlier results [@Tustison:2014ab] 
for training data.   -->


\begin{figure}
\centering
\includegraphics[width=0.95\textwidth]{Figures/mousePipeline.pdf}
\caption{The mouse brain cortical parcellation pipeline integrating two deep
learning components for brain extraction and brain parcellation prior to
estimating cortical labels. Both deep learning networks rely heavily on
aggressive data augmentation on templates built from open data and provide an
outline for further refinement and creating alternative parcellations for
tailored research objectives.  Possible applications include
voxelwise cortical thickness measurements.}
\label{fig:mouseKK}
\end{figure}

Brain parcellation strategies for the mouse brain are pivotal for understanding
the complex organization and function of murine nervous system [@Chon:2019aa].
By dividing the brain into distinct regions based on anatomical, physiological,
or functional characteristics, researchers can investigate specific areas in
isolation and identify their roles in various behaviors and processes. For
example, such parcellation schemes can help elucidate the spatial distribution
of gene expression patterns [@Tasic:2016aa] as well as identify functional
regions involved in specific cognitive tasks [@Bergmann:2020aa]. 

Although deep learning techniques have been used to develop useful parcellation
tools for human brain research (e.g., SynthSeg [@Billot:2023aa], ANTsXNet
[@Tustison:2021aa]), analogous development for the mouse brain is limited.  In
addition, mouse data is often characterized by unique imaging issues such as
extreme anisotropic sampling which are often in sharp contrast to the high
resolution template-based resources available within the community, e.g.,
AllenCCFv3 and DevCCF. We demonstrate how one can use the ANTsX tools to develop
a complete mouse brain structural morphology pipeline as illustrated in Figure
\ref{fig:mouseKK} and detailed below. 

### Few-shot mouse brain extraction network

In order to create a generalized mouse brain extraction network, we built
whole-head templates from two publicly available datasets.  The Center for
Animal MRI (CAMRI) dataset [@Hsu2021] from the University of North Carolina at
Chapel Hill consists of 16 T2-w MRI volumes of voxel resolution $0.16
\times 0.16 \times 0.16 mm^3$.  The second high-resolution dataset
[@Reshetnikov2021] comprises 88 specimens each with three spatially aligned
canonical views with in-plane resolution of $0.08 \times 0.08 mm^2$ with a slice
thickness of $0.5 mm$.  These three orthogonal views were used to reconstruct a
single high-resolution volume per subject using a B-spline fitting algorithm
available in ANTsX [@Tustison:2006aa].  

From these two datasets, two ANTsX templates [@Avants:2010aa] were generated.
Bias field simulation, intensity histogram warping, noise simulation, random
translation and warping, and random anisotropic resampling in the three
canonical directions were used for data augmentation in training an initial T2-w
brain extraction network.  This network was posted and the corresponding
functionality was immediately made available within ANTsXNet, similar to our
previous contributions to the community.  

User interest led to a GitHub inquiry regarding possible study-specific
improvements (https://github.com/ANTsX/ANTsPyNet/issues/133).  This interaction
led to the offering of a user-made third template and extracted brian mask
generated from T2-w ex-vivo data with isotropic spacing of 0.08 mm in each voxel
dimension.  This third template, in conjunction with the other two, were used
with the same aggressive data augmentation to refine the network weights which
were subsequently posted and made available through ANTsPyNet using the function
``antspynet.mouse_brain_extraction(...)``.

### Single-shot mouse brain parcellation network

AllenCCFv3 and its hierarchical ontological labeling, along with the DevCCF,
provides the necessary data for developing a tailored structural parcellation
network for multi-modal imaging.  The ``allensdk`` Python library permits the
creation of any gross parcellation based on the AllenCCFv3 ontology.  Specifically, 
using ``allensdk`` we coalesced the labels to the following six major
structures:  cerebral cortex, cerebral nuclei, brain stem, cerebellum, main
olfactory bulb, and hippocampal formation.  This labeling was mapped to the P56
component of the DevCCF for use with the T2-w template component. 

The T2-w P56 DevCCF and labelings, in conjunction with the data augmentation
described previously for brain extraction, were used to train the proposed brain
parcellation network.  This is available in ANTsXNet (e.g. in ANTsPyNet using
``antspynet.mouse_brain_parcellation(...)``). Note that other brain parcellation
networks have also been trained using alternative regions and parcellation
schemes and are available in the same ANTsXNet functionality.  One usage note
is that the data augmentation used to train the network permits a learned 
interpolation in 0.08 mm isotropic space.  Since the training data is isotropic 
and data augmentation includes downsampling in the canonical directions, each of 
the two networks learns mouse brain-specific interpolation such that one can 
perform prediction on thick-sliced images, as, for example, in these evaluation 
data, and return isotropic probability and thickness maps (a choice available to 
the user).  This permits robust cortical thickness estimation even in the case 
of anisotropic data (see ``antspynet.mouse_cortical_thickness(...)``).

### Evaluation

\begin{figure}
\centering
  \includegraphics[width=0.75\textwidth]{Figures/diceWholeBrain.png}
\caption{Evaluation of the ANTsX mouse brain extraction on an
independent, publicly available dataset consisting of 12 specimens $\times$ 7
time points = 84 total images.  Dice overlap comparisons with the
user-generated brain masks provide good agreement with the automated results
from the brain extraction network.}
\label{fig:evaluation}
\end{figure}

\begin{figure}
\centering
\begin{subfigure}{0.25\textwidth}
  \centering
  \includegraphics[width=\linewidth]{Figures/AllenCCFv3_parcellation_slice91.png}
  \caption{}
  \label{fig:subp_a}
\end{subfigure}
\begin{subfigure}{0.25\textwidth}
  \centering
  \includegraphics[width=\linewidth]{Figures/NR5_M_Day0_slice53.png}
  \caption{}
  \label{fig:subp_b}
\end{subfigure} \\
\begin{subfigure}{.75\textwidth}
  \centering
  \includegraphics[width=\linewidth]{Figures/diceAllenCCFv3.png}
  \caption{}
  \label{fig:subc}
\end{subfigure}
\caption{Evaluation of the ANTsX mouse brain parcellation on the same dataset.
(a) T2-w DevCCF P56 with the described parcellation consisting of the cerebral
cortex, nuclei, brain stem, cerebellum, main olfactory bulb, and hippocampal
formation. (b) Sample subject (NR5 Day 0) with the proposed deep learning-based
segmentation. (c) Dice overlap for comparing the regional alignments between
registration using intensity information only and using intensity with the given
parcellation scheme.}
\label{fig:evaluationParcellation}
\end{figure}

For evaluation, we used an additional publicly available dataset
[@Rahman:2023aa] that is completely independent from the data used in training
the brain extraction and parcellation networks.  Data includes 12 specimens each
imaged at seven time points (Day 0, Day 3, Week 1, Week 4, Week 8, Week 20) with
in-house-generated brain masks for a total of 84 images.  Spacing is anistropic
with an in-plane resolution of $0.1 \times 0.1 mm^2$ and a slice thickness of
$0.5 mm$.  

Figure \ref{fig:evaluation} summarizes the whole brain overlap between the
provided segmentations for all 84 images and the results of applying the
proposed network.   Also, since mapping to the AllenCCFv3 atlas is crucial for
many mouse studies, we demonstrate the utility of the second network by
leveraging the labeled regions to perform anatomically-explicit alignment using
ANTsX multi-component registration instead of intensity-only registration. For
these data, the whole brain extraction demonstrates excellent performance across
the large age range.  And although the intensity-only image registration
provides adequate alignment, intensity with the regional parcellations
significantly improves those measures.

<!-- Although the utility of the proposed brain parcellation framework is highly
dependent on the specific application, we demonstrate the utility through the
generation of cortical thickness maps [@Das:2009uv] which leverages both brain
parcellation and the capabilities of mouse brain-based isotropic interpolation
for anisotropic data.  Cortical thickness has demonstrated utility in both human
(e.g., [@Tustison:2014ab;@Tustison:2019aa]) and non-human data (e.g., canines
[@Grewal:2020aa], dolphins [@Avelino-de-Souza:2024aa], non-human primates
[@Demirci:2023aa]) including the mouse brain
[@Lerch:2008aa;@Lee:2011aa;@Zoller:2018aa;@zhang:2021aa]. -->


<!-- 
\begin{figure}
\centering
\begin{subfigure}{0.5\textwidth}
  \centering
  \includegraphics[width=\linewidth]{Figures/diceWholeBrain.png}
  \caption{}
  \label{fig:suba}
\end{subfigure}\\
\begin{subfigure}{0.5\textwidth}
  \centering
  \includegraphics[width=\linewidth]{Figures/corticoPlot.png}
  \caption{}
  \label{fig:subb}
\end{subfigure}%
\begin{subfigure}{.5\textwidth}
  \centering
  \includegraphics[width=\linewidth]{Figures/kkPlot.png}
  \caption{}
  \label{fig:subc}
\end{subfigure}
\caption{Evaluation of the ANTsX mouse brain extraction and parcellation on an
independent, publicly available dataset consisting of 12 specimens $\times$ 7
time points = 84 total images.  (a) Dice overlap comparisons with the
user-generated brain masks provide good agreement with the automated results
from the brain extraction network. (b) Cortical volume measurements show similar
average quantities over growth and development between the original anisotropic
data and interpolated isotropic data.  (c) The volumetric comparative results
contrast with the cortical thickness measurements which illustrate estimation in
anisotropic space severely underestimates the actual values in comparison with
the isotropic prediction.}
\label{fig:evaluation}
\end{figure} 
-->


\clearpage
\newpage


# Discussion

The diverse mouse brain cell type profiles gathered through BICCN and associated
efforts provide a rich multi-modal resource to the research community. However,
despite significant progress, optimal leveraging of these valuable resources
remains an ongoing challenge. A central component to data integration is
accurately mapping novel cell type data into common coordinate frameworks (CCFs)
for subsequent processing and analysis. To meet these needs, tools for mapping
mouse brain data must be both broadly accessible and capable of addressing
challenges unique to each modality. In this work, we described modular
ANTsX-based pipelines developed to support three distinct BICCN efforts
encompassing spatial transcriptomic, morphological, and developmental data. We
demonstrated how a flexible image analysis toolkit like ANTsX can be tailored to
address specific modality-driven constraints by leveraging reusable, validated
components.

The MERFISH mapping pipeline illustrates how ANTsX tools can be adapted to
accommodate high-resolution spatial transcriptomic data. While the general
mapping strategy is applicable to other sectioned histological data, the
pipeline includes specific adjustments for known anatomical and imaging
artifacts present in MERFISH datasets. As such, this example demonstrates how
general-purpose tools can be customized to meet the requirements of highly
specialized data types.

The fMOST mapping pipeline was developed with the intention of broader applicability.
Built primarily from existing ANTsX preprocessing and registration modules, this
pipeline introduces an fMOST-specific intermediate atlas to facilitate
consistent mappings to the AllenCCFv3. The use of a canonical fMOST atlas
reduces the need for repeated manual alignment across new datasets, and the
resulting transformations can be directly applied to associated single-neuron
reconstructions. This supports integrative morphological analysis across
specimens using a common coordinate system.

For developmental data, we introduced a velocity field–based model for
continuous interpolation between discrete DevCCF timepoints. Although the DevCCF
substantially expands coverage of developmental stages relative to prior
atlases, temporal gaps remain. The velocity model enables spatio-temporal
transformations within the full developmental interval and supports the
generation of virtual templates at unsampled ages. This functionality is built
using ANTsX components for velocity field optimization and integration, and
offers a novel mechanism for interpolating across the non-linear developmental
trajectory of the mouse brain. Such interpolation has potential utility for both
anatomical harmonization and longitudinal analyses.

We also introduced a template-based deep learning pipeline for mouse brain
extraction and parcellation using aggressive data augmentation. This approach is
designed to reduce the reliance on large annotated training datasets, which
remain limited in the mouse imaging domain. Evaluation on independent data
demonstrates promising generalization, though further refinement will be
necessary. As with our human-based ANTsX pipelines, failure cases can be
manually corrected and recycled into future training cycles. Community
contributions are welcomed and encouraged, providing a pathway for continuous
improvement and adaptation to new datasets.

The ANTsX ecosystem offers a powerful foundation for constructing scalable,
reproducible pipelines for mouse brain data analysis. Its modular design and
multi-platform support enable researchers to develop customized workflows
without extensive new software development. The widespread use of ANTsX
components across the neuroimaging community attests to its utility and
reliability. As a continuation of the BICCN program, ANTsX is well positioned to
support the goals of the BRAIN Initiative Cell Atlas Network (BICAN) and future
efforts to extend these mapping strategies to the human brain.

\clearpage \newpage

# Methods  

The following methods are all available as part of the ANTsX ecosystem with
analogous elements existing in both ANTsR (ANTs in R) and ANTsPy (ANTs in
Python), underpinned by a shared ANTs/ITK C++ core. Most development for the
work described was performed using ANTsPy. For equivalent functionality in
ANTsR, we refer the reader to the comprehensive ANTsX tutorial:
[https://tinyurl.com/antsxtutorial](https://tinyurl.com/antsxtutorial).

## General ANTsX utilities

Although focused on distinct data types, the three pipelines presented in this
work share common components that address general challenges in mapping mouse
brain data. These include correcting image intensity artifacts, denoising,
spatial registration, template generation, and visualization. Table
\ref{table:methods} provides a concise summary of the relevant ANTsX
functionality.

\input{antsx_functionality_table}

**Preprocessing: bias field correction and denoising.** Standard preprocessing
steps in mouse brain imaging include correcting for spatial intensity
inhomogeneities and reducing image noise, both of which can impact registration
accuracy and downstream analysis. ANTsX provides implementations of widely used
methods for these tasks. The N4 bias field correction algorithm
[@Tustison:2010ac], originally developed in ANTs and contributed to ITK,
mitigates artifactual, low-frequency intensity variation and is accessible via
`ants.n4_bias_field_correction(...)`. Patch-based denoising [@Manjon:2010aa] has
been implemented as `ants.denoise_image(...)`.

**Image registration.** ANTsX includes a robust and flexible framework for
pairwise and groupwise image registration [@Avants:2014aa]. At its core is the
SyN algorithm [@Avants:2008aa], a symmetric diffeomorphic model with optional
B-spline regularization [@Tustison:2013ac]. In ANTsPy, registration is performed
via `ants.registration(...)` using preconfigured parameter sets (e.g.,
`antsRegistrationSyNQuick[s]`, `antsRegistrationSyN[s]`) suitable for different
imaging modalities and levels of computational demand. Resulting transformations
can be applied to new images with `ants.apply_transforms(...)`.

**Template generation.** ANTsX supports population-based template generation
through iterative pairwise registration to an evolving estimate of the mean
shape and intensity reference space across subjects [@Avants:2010aa]. This
functionality was used in generating the DevCCF templates [@Kronman:2024aa]. The
procedure, implemented as `ants.build_template(...)`, produces average images in
both shape and intensity by aligning all inputs to a common evolving template.

**Visualization.** To support visual inspection and quality control, ANTsPy
provides flexible image visualization with `ants.plot(...)`. This function
enables multi-slice and multi-orientation rendering with optional overlays and
label maps.

<!----------------------------------------------------------------------->

## Mapping fMOST data to AllenCCFv3

**Preprocessing.** Mapping fMOST data into the AllenCCFv3 presents unique
challenges due to its native ultra-high resolution and imaging artifacts common
to the fMOST modality. Each fMOST image can exceed a terabyte in size, with
spatial resolutions far exceeding those of the AllenCCFv3 (25 $\mu m$
isotropic). To reduce computational burden and prevent resolution mismatch, each
fMOST image is downsampled using cubic B-spline interpolation via
`ants.resample_image(...)` to match the template resolution.

Stripe artifacts (i.e., periodic intensity distortions caused by nonuniform
sectioning or illumination) are common in fMOST and can mislead deformable
registration algorithms. These were removed using a custom 3D notch filter
(`remove_stripe_artifact(...)`) implemented in the `CCFAlignmentToolkit` using
SciPy frequency domain filtering. The filter targets dominant stripe frequencies
along a user-specified axis in the Fourier domain. In addition, intensity
inhomogeneity across sections, often arising from variable staining or
illumination, was corrected using N4 bias field correction.

**Template-based spatial normalization.** To facilitate reproducible mapping, we
first constructed a contralaterally symmetric average template from 30 fMOST
brains and their mirrored counterparts using ANTsX template-building tools.
Because the AllenCCFv3 and fMOST data differ substantially in both intensity
contrast and morphology, direct deformable registration between individual fMOST
brains and the AllenCCFv3 was insufficiently robust.  Instead, we performed a
one-time expert-guided label-driven registration between the average fMOST
template and AllenCCFv3. This involved sequential alignment of seven manually
selected anatomical regions:  1) brain mask/ventricles, 2) caudate/putamen, 3)
fimbria, 4) posterior choroid615 plexus, 5) optic chiasm, 6) anterior choroid
plexus, and 7) habenular commissure which were prioritized to enable
coarse-to-fine correction of shape differences. Once established, this
fMOST-template-to-AllenCCFv3 transform was reused for all subsequent specimens.
Each new fMOST brain was then registered to the average fMOST template using
intensity-based registration, followed by concatenation of transforms to produce
the final mapping into AllenCCFv3 space. 

**Mapping neuron projections.** A key advantage of fMOST imaging is its ability
to support single neuron projection reconstruction across the entire brain
[@Peng:2021aa]. Because these reconstructions are stored as 3D point sets
aligned to the original fMOST volume, we applied the same composite transform
used for image alignment to the point data using ANTsX functionality. This
enables seamless integration of cellular morphology data into AllenCCFv3 space,
facilitating comparative analyses across specimens.

<!----------------------------------------------------------------------->

## Mapping MERFISH data to AllenCCFv3

**Preprocessing.** MERFISH data are acquired as a series of 2D tissue sections,
each comprising spatially localized gene expression measurements at subcellular
resolution. To enable 3D mapping to the AllenCCFv3, we first constructed
anatomical reference images by aggregating the number of detected transcripts
per voxel across all probes within each section. These 2D projections were
resampled to a resolution of 10 $\mu m$ $\times$ 10 $\mu m$ to match the in-plane
resolution of the AllenCCFv3.

Sections were coarsely aligned using manually annotated dorsal and ventral
midline points, allowing initial volumetric reconstruction. However, anatomical
fidelity remained limited by variation in section orientation, spacing, and
tissue loss. To further constrain alignment and enable deformable registration,
we derived region-level anatomical labels directly from the gene expression
data.

**Label creation.** We assigned each detected cell to one of 15 coarse
anatomical regions (e.g., hippocampus, cortex, striatum—using transcriptomic
similarity to scRNA) seq reference data. These assignments were aggregated
across spatial grids to produce probabilistic label maps for each section. To
ensure full regional coverage, morphological dilation was applied to fill gaps
between sparsely distributed cells. Finer-resolution structures (e.g., cortical
layers, habenula) were similarly labeled using marker gene enrichment and
spatial constraints.  This dual-level labeling (i.e., coarse and fine) allowed
us to construct a robust anatomical scaffold in the MERFISH coordinate system
that could be matched to AllenCCFv3 annotations.

**Section matching via global alignment.** A major challenge was compensating
for oblique cutting angles and non-uniform section thickness, which distort the
anatomical shape and spacing of the reconstructed volume. Rather than directly
warping the MERFISH data into atlas space, we globally aligned the AllenCCFv3 to
the MERFISH coordinate system. This was done via an affine transformation
followed by resampling of AllenCCFv3 sections to match the number and
orientation of MERFISH sections. This approach minimizes interpolation artifacts
in the MERFISH data and facilitates one-to-one section matching.

**Landmark-driven deformable alignment.** We used a 2.5D approach for fine
alignment of individual sections. In each MERFISH slice, deformable registration
was driven by sequential alignment of anatomical landmarks between the label
maps derived from MERFISH and AllenCCFv3. A total of nine regions—including
isocortical layers 2/3, 5, and 6, the striatum, hippocampus, thalamus, and
medial/lateral habenula—were registered in an empirically determined order.
After each round, anatomical alignment was visually assessed by an expert, and
the next structure was selected to maximize improvement in the remaining
misaligned regions.

The final transform for each section combined the global affine alignment and
the per-structure deformable registrations. These were concatenated to generate
a 3D mapping from the original MERFISH space to the AllenCCFv3 coordinate
system. Once established, the composite mapping enables direct transfer of
gene-level and cell-type data from MERFISH into atlas space, allowing
integration with other imaging and annotation datasets.

<!----------------------------------------------------------------------->

## DevCCF velocity flow transformation model

The Developmental Common Coordinate Framework (DevCCF) [@Kronman:2024aa]
provides a discrete set of age-specific templates that temporally sample the
developmental trajectory. To model this biological progression more
continuously, we introduce a velocity flow–based paradigm for inferring
diffeomorphic transformations between developmental stages. This enables
anatomically plausible estimation of intermediate templates or mappings at
arbitrary timepoints between the E11.5 and P56 endpoints of the DevCCF. Our
approach builds on established insights from time-varying diffeomorphic
registration [@Beg:2005aa], where a velocity field governs the smooth
deformation of anatomical structures over time. Importantly, the framework is
extensible and can naturally accommodate additional timepoints for the 
potential expansion of the DevCCF. 

**Point sampling and region correspondence.** We first coalesced the anatomical
labels across the seven DevCCF templates (E11.5, E13.5, E15.5, E18.5, P4, P14,
P56) into 26 common structures that could be consistently identified across
development. These include major brain regions such as the cortex, cerebellum,
hippocampus, midbrain, and ventricles. For each successive pair of templates, we
performed multi-label deformable registration using ANTsX to generate forward
and inverse transforms between anatomical label volumes.  From the P56 space, we
randomly sampled approximately 1e6 points within and along the boundaries of
each labeled region and propagated them through each pairwise mapping step
(e.g., P56 $\rightarrow$ P14, P14 $\rightarrow$ P4, \ldots, E13.5 $\rightarrow$
E11.5). This procedure created time-indexed point sets tracing the spatial
evolution of each region.

**Velocity field fitting.** Using these point sets, we fit a continuous velocity
field over developmental time using a generalized B-spline scattered data
approximation method [@Tustison:2006aa]. The field was parameterized over a
log-scaled time axis to ensure finer temporal resolution during early embryonic
stages, where morphological changes are most rapid.  Optimization proceeded for
approximately 125 iterations, minimizing the average Euclidean norm between
transformed points at each step. Ten integration points were used to ensure
numerical stability. The result is a smooth, differentiable vector field that
defines a diffeomorphic transform between any two timepoints within the template
range.

**Applications and availability.** This velocity model can be used to estimate
spatial transformations between any pair of developmental stages—even those for
which no empirical template exists—allowing researchers to create interpolated
atlases, align new datasets, or measure continuous structural changes. It also
enables developmental alignment of multi-modal data (e.g., MRI to LSFM) by
acting as a unifying spatiotemporal scaffold. The underlying components for
velocity field fitting and integration are implemented in ITK, and the complete
workflow is accessible in both ANTsPy
(``ants.fit_time_varying_transform_to_point_sets(...)``) and ANTsR. In addition 
the availability of the DevCCF use case, self-contained examples and usage 
tutorials are provided in our public codebase.

<!----------------------------------------------------------------------->

## ANTsXNet mouse brain applications

To support template-based deep learning approaches for structural brain
extraction and parcellation, we implemented dedicated pipelines using the
ANTsXNet framework. ANTsXNet comprises open-source deep learning libraries in
both Python (ANTsPyNet) and R (ANTsRNet) that interface with the broader ANTsX
ecosystem and are built on TensorFlow/Keras. Our mouse brain pipelines mirror
existing ANTsXNet tools for human imaging but are adapted for species-specific
anatomical variation, lower SNR, and heterogeneous acquisition protocols.

### Deep learning training setup

All networks were implemented in ANTsPyNet using standard 3D U-net architectures
[@Falk:2019aa] previously employed in previously published work
[@Tustison:2021aa,Tustison:2024aa,Stone:2024aa]. Training was performed on an
NVIDIA DGX system (4$\times$ Tesla V100 GPUs, 256 GB RAM). Model weights and
preprocessing routines are shared across ANTsPyNet and ANTsRNet to ensure
reproducibility and language portability. For both published and unpublished
trained networks available through ANTsXNet, all training scripts and data
augmentation generators are publicly available at
**[https://github.com/ntustison/ANTsXNetTraining](https://github.com/ntustison/ANTsXNetTraining)**.

**Data augmentation.** Robust data augmentation was critical to generalization
across scanners, contrast types, and resolutions. We applied both intensity- and
shape-based augmentation strategies:

* *Intensity augmentations:*

  * Gaussian, Poisson, and salt-and-pepper noise:  
    `ants.add_noise_to_image(...)`
  * Simulated intensity inhomogeneity via bias field modeling:  
    `antspynet.simulate_bias_field(...)`
  * Histogram warping to simulate contrast variation:   
    `antspynet.histogram_warp_image_intensities(...)`

* *Shape augmentations:*

  * Random nonlinear deformations and affine transforms:  
    `antspynet.randomly_transform_image_data(...)`
  * Anisotropic resampling across axial, sagittal, and coronal planes:  
    `ants.resample_image(...)`

### Brain extraction

We originally trained a mouse-specific brain extraction model on two manually
masked T2-weighted templates, generated from public datasets
[@Reshetnikov2021; @Hsu2021]. One of the templates was constructed from
orthogonal 2D acquisitions using B-spline–based volumetric synthesis via
`ants.fit_bspline_object_to_scattered_data(...)`. Normalized gradient magnitude
was used as a weighting function to emphasize boundaries during reconstruction
[@Tustison:2006aa].

This training strategy provides strong spatial priors despite limited
data—leveraging high-quality template images and aggressive augmentation to mimic
population variability. During the development of this work, the network was
further refined through community engagement. A user from a U.S.-based research
institute applied the publicly available (but then unpublished) brain extraction
tool to their own mouse MRI dataset. Based on feedback and iterative
collaboration with the ANTsX team, the model was retrained and improved to better
generalize to additional imaging contexts. This reflects our broader commitment
to community-driven development and responsiveness to user needs across diverse
mouse brain imaging scenarios.

The final trained network is available via ANTsXNet through the function  
`antspynet.mouse_brain_extraction(...)`. Additionally, both template/mask pairs
are accessible via ANTsXNet. For example, one such image pair is available via:

* Template:  
  `antspynet.get_antsxnet_data("bsplineT2MouseTemplate")`
* Brain mask:  
  `antspynet.get_antsxnet_data("bsplineT2MouseTemplateBrainMask")`


### Brain parcellation

For brain parcellation, we trained a 3D U-net model using the DevCCF P56
T2-weighted template and anatomical segmentations derived from AllenCCFv3. This
template-based training strategy allows the model to produce accurate,
multi-region parcellations without requiring large-scale annotated subject data.

To harmonize intensity across specimens, input images were preprocessed using
rank-based intensity normalization (`ants.rank_intensity(...)`). Spatial
harmonization was achieved by affine and deformable alignment of each extracted
brain to the P56 template prior to inference. In addition to the normalized
image input, the network also receives prior probability maps derived from the
atlas segmentations, providing additional spatial context. These resources are
available via `get_antsxnet_data(...)`.

### Evaluation and reuse

To assess model generalizability, both brain extraction and parcellation models
were evaluated on an external longitudinal dataset \[@Rahman:2023aa] with varied
scanning parameters. The pipeline demonstrated robust performance without
retraining, highlighting the utility of a template-driven, low-shot approach.
All models, training scripts, and data resources are publicly available and
designed for plug-and-play use within ANTsX workflows.


\clearpage

# Data availability {-}

 All data and software used in this work are publicly available.  The DevCCF
atlas is available at \url{https://kimlab.io/brain-map/DevCCF/}. ANTsPy, ANTsR,
ANTsPyNet, and ANTsRNet are available through GitHub at the ANTsX Ecosystem
(\url{https://github.com/ANTsX}).  Training scripts for all deep learning
functionality in ANTsXNet can also be found on GitHub
(\url{https://github.com/ntustison/ANTsXNetTraining}). A GitHub repository
specifically pertaining to the AllenCCFv3 mapping is available at
\url{https://github.com/dontminchenit/CCFAlignmentToolkit}. For the other two
contributions contained in this work, the longitudinal DevCCF mapping and mouse
cortical thickness pipeline, we refer the interested reader to
\url{https://github.com/ntustison/ANTsXMouseBrainMapping}. 


\clearpage

# Acknowledgments {-}

Support for the research reported in this work includes funding from the
National Institute of Biomedical Imaging and Bioengineering (R01-EB031722)
and National Institute of Mental Health (RF1-MH124605 and U24-MH114827).

We also acknowledge the data contribution of Dr. Adam Raikes (GitHub \@araikes) 
of the Center for Innovation in Brain Science at the University of Arizona 
for refining the weights of the mouse brain extraction network.  


\clearpage

# Author contributions {-}

N.T., M.C., and J.G. wrote the main manuscript text and figures.  M.C.,
M.K., R.D., S.S., Q.W., L.G., J.D., C.G., and J.G. developed the Allen 
registration pipelines.  N.T. and F.K. developed the time-varying velocity
transformation model for the DevCCF.  N.T. and M.T. developed the brain 
parcellation and cortical thickness methodology.  All authors reviewed 
the manuscript.
\clearpage

# References {-}