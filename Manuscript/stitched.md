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

{\bf The ANTsX Ecosystem for Mapping the Mouse Brain}

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
Quanxi Wang$^{4}$,
Lydia Ng$^{4}$,
Yongsoo Kim$^{3}$, and
James C. Gee$^{2}$

\small

$^{1}$Department of Radiology and Medical Imaging, University of Virginia, Charlottesville, VA \\
$^{2}$Department of Radiology, University of Pennsylvania, Philadelphia, PA \\
$^{3}$Department of Neural and Behavioral Sciences, Penn State University, Hershey, PA \\
$^{4}$Allen Institute for Brain Science, Seattle, WA \\

\vspace{1.2 cm}

\end{centering}

\vspace{5.5 cm}

\noindent\rule{4cm}{0.4pt}

\scriptsize
Corresponding author: \
Nicholas J. Tustison, DSc \
Department of Radiology and Medical Imaging \
University of Virginia \
ntustison@virginia.edu

\normalsize

\newpage

\setstretch{1.5}

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
brain and potential subsequent quantitation.  First, we describe ANTsX-based
workflows for mapping domain-specific image data to AllenCCFv3 accounting for
common artefacts and other confounds.  Novel contributions include recently
developed ANTsX functionality for generating a velocity flow-based mapping
spanning the spatiotemporal domain of a longitudinal trajectory which we apply
to the Developmental Common Coordinate Framework (DevCCF).  Additionally, we
present an automated structural morphological pipeline for determining
volumetric and cortical thickness measurements analogous to the well-utilized
ANTsX pipeline for human neuroanatomical structural morphology.  This latter
development also illustrates a more general open-source ANTsX framework for
determining tailored brain parcellations using the AllenCCFv3 and DevCCF
templates.

\clearpage# Introduction

Over the past two decades there have been significant advancements in mesoscopic
analysis of the mouse brain. It is currently possible to track single cell neurons in
mouse brains [@Keller:2015aa], observe whole brain developmental changes on a
cellular level [@La-Manno:2021aa], associate brain regions and tissues with
their genetic composition [@Wen:2022aa], and locally characterize neural
connectivity [@Oh:2014aa]. Much of this scientific achievement has been made
possible due to breakthroughs in high resolution imaging techniques that permit
submicron, 3-D imaging of whole mouse brains. Associated research techniques
such as micro-optical sectioning tomography [@Gong:2013aa,@Li:2010aa], tissue
clearing [@Keller:2015aa;@Ueda:2020aa], spatial transcriptomics
[@Stahl:2016aa,@Burgess:2019aa] are all well-utilized in the course of
scientific investigations of mesoscale relationships in the mouse brain. 

An important component of this research is the ability to map the various image
data to anatomical reference frames
[@MacKenzie-Graham:2004aa,@Mackenzie-Graham:2007aa] for inferring spatial
relationships between structures, cells, and genetics. This has motivated the
development of detailed structural image atlases of the mouse brain.  Notable
examples include the Allen Brain Atlas and Coordinate Frameworks (AllenCCFv3)
[@Dong:2008aa,@Wang:2020aa], the Waxholm Space [@Johnson:2010aa], and more
recently, the Developmental Common Coordinate Framework (DevCCF)
[@Kronman:2023aa]. Despite the significance of these contributions, challenges
still exist in large part due to the wide heterogeneity in associated
study-specific image data. For example, variance in the acquisition methods can
introduce artifacts such as tissue distortion, holes, bubbles, folding, tears,
and missing slices. These complicate assumed correspondence for
conventional spatial mapping approaches.

## Mouse-specific brain mapping software

To address such challenges, several software packages have been developed over
the years comprising solutions of varying comprehensibility, sophistication, and
availability.  An early contribution to the community was the Rapid Automatic
Tissue Segmentation (RATS) package [@Oguz:2014aa] for brain extraction. More
recently, several publicly available packages comprise well-established package
dependencies originally developed on human brain data. SPMMouse
[@Sawiak:2014aa], for example, is based on the well-known Statistical Parametric
Mapping (SPM) Matlab-based toolset [@Ashburner:2012aa]. The automated mouse
atlas propagation (aMAP) tool is largely a front-end for the NiftyReg image
registration package [@Modat:2010aa] applied to mouse data which is currently
available as a Python module [@Tyson:2022aa]. NiftyReg is also used by the
Atlas-based Imaging Data Analysis (AIDA) MRI pipeline [@Pallast:2019aa] as well
as the Multi Atlas Segmentation and Morphometric Analysis Toolkit (MASMAT).
Whereas the former also incorporates the FMRIB Software Library (FSL)
[@Jenkinson:2012wi] for brain extraction and DSIStudio [@Yeh:2010aa] for DTI
processing, the latter uses NiftySeg and multi-consensus labeling tools
[@Jorge-Cardoso:2013aa] for brain extraction and parcellation. In addition,
MASMAT incorporates N4 bias field correction [@Tustison:2010ac] from the
Advanced Normalization Tools Ecosystem (ANTsX) [@Tustison:2021aa] as do the
packages Multi-modal Image Registration And Connectivity anaLysis (MIRACL)
[@Goubran:2019aa], Sammba-MRI [@Celestine:2020aa], and Small Animal Magnetic
Resonance Imaging (SAMRI) [@Ioanas:2021aa].  However, whereas Saamba-MRI uses
AFNI [@Cox:2012aa] for image registration; MIRACL, SAMRI, SAMBA
[@Anderson:2019aa], and BrainsMapi [@Ni:2020aa] all use ANTsX registration
tools. Other packages use landmark-based approaches to image registration
including SMART [@Jin:2022aa]---an R package for semi-automated landmark-based
registration and segmentation of mouse brain based on WholeBrain
[@Furth:2018aa].  FriendlyClearMap [@Negwer:2022aa] uses the landmark-based
registration functionality of Elastix [@Klein:2010aa]. Finally, the widespread
adoption of deep learning techniques has also influenced development in mouse
brain imaging methodologies.  For example, if tissue deformations are not
considered problematic for a particular dataset, DeepSlice can be used to
determine affine mappings [@Carey:2023aa] with the optimal computational
efficiency associated with neural networks.

## The ANTsX Ecosystem for mouse brain mapping 

As noted previously, many of the existing packages designed for processing mouse
brain image data use ANTsX tools for core processing steps in various workflows,
particularly its pairwise, intensity-based image registration capabilities and
bias field correction. Historically, ANTsX development is originally based on
fundamental approaches to image mapping
[@Bajcsy:1982aa;@Bajcsy:1989aa;@Gee:2003aa], particularly in the human brain,
which has resulted in core contributions to the field such as the well-known
Symmetric Normalization (SyN) algorithm [@Avants:2008aa].  Since
its development, various independent platforms have been used to evaluate ANTsX
image registration capabilities in the context of different application foci
which include multi-site brain MRI data [@Klein:2009aa], pulmonary CT data
[@Murphy:2011aa], and most recently, multi-modal brain registration in the
presence of tumors [@Baheti:2021aa]. 

\input{antsx_functionality_table}

Apart from its registration capabilities, ANTsX comprises additional
functionality such as template generation [@Avants:2010aa], intensity-based
segmentation [@Avants:2011uf], preprocessing [@Manjon:2010aa;@Tustison:2010ac],
deep learning networks [@Tustison:2021aa], and other miscelleneous utilties
(see Table \ref{table:methods}). The comprehensive
use of the toolkit has demonstrated superb performance in multiple application
areas (e.g., consensus labeling [@Wang:2013ab], brain tumor segmentation
[@Tustison:2014aa], and cardiac motion estimation [@Tustison:2015ab] ).
Importantly, ANTs is built on the Insight Toolkit (ITK) [@McCormick:2014aa]
deriving benefit from the open-source community of scientists and programmers
and providing an important resource for algorithmic development, evaluation, and
improvement.  We use this functionality to demonstrate recently developed
frameworks for mapping fluorescence micro-optical sectioning tomography (fMOST)
and multiplexed error-robust fluorescence in situ hybridization (MERFISH) image
data to the AllenCCFv3 atlas space.  In addition to standard preprocessing steps
(e.g., bias correction), additional considerations are accommodated within the
ANTsX ecosystem, such as section reconstruction and landmark-based alignment.  


<!-- 

\begin{figure}[!htb]
\centering
\makebox[\textwidth][c]{\includegraphics[width=1.2\textwidth]{Figures/pipeline3.png}}%
\caption{
Illustration of a mouse brain template generation workflow and related
template-based applications demonstrating the utility of different ANTsX tools,
specifically in the development of the DevCCF atlas. After imaging acquisition
of the study population, various preprocessing steps are applied to the imaging
data such as bias correction, denoising, and brain extraction for gene
expression mapping.  Also illustrated is the generation of the associated
velocity flow model for continuous spatiotemporal mapping interpolating the
sampled time points of the DevCCF.
}
\label{fig:pipeline}
\end{figure} 

-->

## ANTsX-based open-source contributions

Consistent with previous ANTsX development, the newly introduced capabilities
introduced below are available through ANTsX (specifically, via R and Python
ANTsX packages), and illustrated through self-contained examples in the ANTsX
tutorial (\url{https://tinyurl.com/antsxtutorial}) with a dedicated GitHub 
repository specific to this work
(\url{https://github.com/ntustison/ANTsXMouseBrainMapping}).

### The DevCCF velocity flow model

Recently, the Developmental Common Coordinate Framework (DevCCF) was introduced
to the mouse brain research community as a public resource [@Kronman:2023aa]
comprising symmetric atlases of multimodal image data and anatomical
segmentations defined by developmental ontology.  These templates sample the
mouse embryonic days (E) 11.5, E13.5, E15.5, E18.5 and postnatal day (P) 4, P14,
and P56.  Modalities include light sheet flourescence miscroscopy (LSFM) and at
least four MRI contrasts per developmental stage.  Anatomical parcellations are
also available for each time point and were generated from ANTsX-based mappings
of gene expression and other cell type data.  Additionally, the P56 template was
integrated with the AllenCCFv3 to further increase the practical utility of the
DevCCF. These processes, specifically template generation and multi-modal image
mapping, were performed using ANTsX functionality in the presence of 
image mapping difficulties such as missing data and tissue distortion.  

Given the temporal gaps in the discrete set of developmental atlases, we also
provide an open-source framework for inferring correspondence
within the temporally continuous domain sampled by the existing set of embryonic
and postnatal atlases of the DevCCF.  This recently developed 
functionality permits the generation of a diffeomorphic velocity flow
transformation model [@Beg:2005aa], influenced by previous work
[@Tustison:2013ac].  The resulting time-parameterized velocity field spans the
stages of the DevCCF where mappings between any two continuous time points
within the span bounded by the E11.5 and P56 atlases is determined by
integration of the optimized velocity field. 

### Structural morphology and cortical thickness in the mouse brain

One of the most frequently utilized pipelines in the ANTsX toolkit is that of
estimating cortical thickness maps in the human brain.   Beginning with the
Diffeomorphic Registration-based Cortical Thickness (DiReCT) algorithm
[@Das:2009uv], this was later expanded to include a complete processing
framework for human brain cortical thickness estimation for both cross-sectional
[@Tustison:2014ab] and longitudinal [@Tustison:2019aa] data using T1-weighted
MRI.  These pipelines were later significantly refactored using deep learning
innovations [@Tustison:2021aa].

In contrast to the pipeline development in human data [@Tustison:2021aa], no
current ANTsX tools exist to create adequate training data for the mouse brain.
In addition, mouse brain data acquisition often has unique issues, such as lower
data quality or sampling anisotropy which limits its applicability to high
resolution resources (e.g., AllenCCFv3, DevCCF), specifically with respect to
the corresponding granular brain parcellations derived from numerous hours of
expert annotation leveraging multimodal imaging resources.

Herein, we introduce a mouse brain cortical thickness pipeline for T2-weighted
MRI comprising two novel deep learning components:  two-shot learning brain
extraction from data augmentation of two ANTsX templates generated from two open
datasets [@Hsu2021;@Reshetnikov2021] and single-shot brian parcellation derived
from the AllenCCFv3 labelings mapped to the corresponding DevCCF P56 T2-w
component.  Although we anticipate that this cortical thickness pipeline will be
beneficial to the research community, this work demonstrates more generally how
one can leverage ANTsX tools for developing tailored brain parcellation schemes
using these publicly available resources.  Evaluation is performed on an
independent open data set [@Rahman:2023aa] comprising longitudinal acquisitions
of multiple specimens.  



\clearpage
\newpage

# Results


## AllenCCFv3 brain image mapping

### Mapping fluorescence micro-optical sectioning tomography (fMOST) data

We have developed a framework for mapping fluorescence micro-optical sectioning
tomography (fMOST) mouse brain images into the AllenCCFv3. Our approach uses an
average fMOST atlas to serve as an intermediate registration target for mapping
fMOST images from individual specimens into the AllenCCFv3. First, we use a
one-time annotation-driven registration to establish a canonical mapping between
the fMOST atlas and the AllenCCFv3. This step allows us to align expert
determined landmarks to accurately map structures with large morphological
differences between the modalities, which are difficult to address using
standard approaches. Once this canonical mapping is established, standard
intensity-based registration is used to align each new fMOST image to the fMOST
specific atlas. This mapping is concatenated with the canonical atlas-to-CCFv3
mapping to further map each individual brain into the AllenCCFv3 without the
need to generate additional landmarks. Transformations learned through this
mapping can be applied to single neuron reconstructions from the fMOST images to
evaluate neuronal distributions across different specimens into the AllenCCFv3
for the purpose of cell census analyses.

__Data__ 

The high-throughput and high-resolution fluorescence micro-optical sectioning
tomography (fMOST) [@Gong:2016aa;@Wang:2021aa] platform was used to image 55
mouse brains containing gene-defined neuron populations, with sparse transgenic
expression [@Rotolo:2008aa;@Peng:2021aa]. In short, the fMOST imaging platform
results in 3D images with voxel sizes of $0.35 \times 0.35 \times 1.0 \mu m^3$
and is a two-channel imaging system where the green channel displays the GFP
labeled neuron morphology and the red channel is used to visualize the
counterstained propidium iodide cytoarchitecture. The spatial normalizations
described in this work were performed using the red channel, which offered
higher tissue contrast for alignment, although other approaches are possible
including multi-channel registration.

__Preprocessing__ 

* _Downsampling_---The first challenge when mapping fMOST images into the
  AllenCCFv3 is addressing the resolution scale of the data. Native fMOST data
  from an individual specimen can range in the order of terabytes, which leads
  to two main problems. First, volumetric registration methods (particularly
  those estimating local deformation) have high computational complexity and
  typically cannot operate on such high-resolution data under reasonable memory
  and runtime constraints. Second, the resolution of the AllenCCFv3 atlas is
  much lower than the fMOST data, thus the mapping process will cause much of
  the high-resolution information in the fMOST images to be lost regardless.
  Thus, we perform a cubic b-spline downsampling of the fMOST data to reduce the
  resolution of each image to 25 $\mu m$ isotropic to match the 25 $\mu m$
  AllenCCFv3 intensity atlas. An important detail to note is that while the
  fMOST images and atlas are downsampled, the mapping learned during the
  registration is assumed to be continuous. Thus, after establishing the mapping
  to the AllenCCFv3, we can interpolate the learned mapping and apply it to the
  high-resolution native data directly to transform any spatially aligned data
  (such as the single-cell neuron reconstructions) into the AllenCCFv3. 

* _Stripe artifact removal_---Repetitive pattern artifacts are a common
  challenge in fMOST imaging where inhomogeneity during the cutting and imaging
  of different sections can leave stripes of hyper- and hypo-intensity across
  the image. These stripe artifacts can be latched onto by the registration
  algorithm as unintended features that are then misregistered to non-analogous
  structures in the AllenCCFv3. We address these artifacts by fitting a 3D
  bandstop (notch) filter to target the frequency of the strip patterns and
  removing them prior to the image registration.

* _Inhomogeneity correction_---Regional intensity inhomogeneity can also occur
  within and between sections in fMOST imaging due to staining or lighting
  irregularity during acquisition. Similar to stripe artifacts, intensity
  gradients due to inhomogeneity can be misconstrued as features during the
  mapping and result in matching of non-corresponding structures. Our pipeline
  addresses these intensity inhomogeneities using N4 bias field
  correction [@Tustison:2010ac].

__Spatial normalization to AllenCCFv3__

The spatial mapping of the fMOST image into the AllenCCFv3 in our pipeline is
separated into three main steps: 1) First, we construct an fMOST average atlas,
which is registered into the AllenCCFv3 using a one-time, annotation-driven
registration. 2) Individual fMOST images are then registered to the fMOST
average atlas 3) finally, the atlas-to-AllenCCFv3 mapping and individual-to-atlas
mapping are concatenated to generate a final mapping from each individual image
into the AllenCCFv3. 

* _Average fMOST atlas as an intermediate target_---Due to the preparation of
  the mouse brain for fMOST imaging, the resulting structure in the mouse brain
  has several large morphological deviations from the AllenCCFv3 atlas. Most notable
  of these is an enlargement of the ventricles, and compression of cortical
  structures. In addition, there is poor intensity correspondence for the same
  anatomic features due to the difference in imaging modalities. We’ve found
  that standard intensity-base registration is insufficient to capture the
  significant deformations required to map these structures correctly into the
  AllenCCFv3. We address this challenge in ANTsX by using explicitly corresponding
  parcellations of the brain, ventricles and surrounding structures to directly
  map these large morphological differences. However, generating these
  parcellations for each individual mouse brain is a labor-intensive task. Our
  solution is to create an average atlas that encapsulates these large
  morphological differences to serve as an intermediate registration point. This
  has the advantage of only needing to generate one set of corresponding
  annotations which is used to register between the two atlas spaces. New images
  are then aligned to the fMOST average atlas, which shares common intensity and
  morphological features and thus can be achieved through standard
  intensity-based registration.

* _Average fMOST atlas construction_---An intensity and shape-based
  contralaterally symmetric average of the fMOST image data is constructed from
  30 images and their contralateral counterpart. We ran three iterations of the
  atlas construction using the default settings. Additional iterations (up to
  six) were evaluated and showed minimal changes to the final atlas
  construction, suggesting a convergence of the algorithm.

* _fMOST atlas to AllenCCFv3 alignment_---Alignment between the fMOST average
  atlas and AllenCCFv3 was performed using a one-time annotation-driven approach.
  Label-to-label registration is used to align 7 corresponding annotations in
  both atlases in the following: 1) Brain mask/ventricles, 2) caudate/putamen, 3) 
  Fimbria, 4) posterior choroid plexus, 5) optic chiasm, 6) anterior choroid
  plexus, and 7) habenular commissure. The alignments were performed
  sequentially, with the largest, most relevant structures being aligned first
  using coarse registration parameters, followed by other structures using finer
  parameters. This approach allows us to address large morphological differences
  (such as brain shape and ventricle expansion) at the start of registration and
  then refine the mapping using the smaller structures. The overall ordering of
  these structures was determined manually by an expert anatomist, where
  anatomical misregistration after each step of the registration was evaluated
  and used to determine which structure should be used in the subsequent
  iteration to best improve the alignment. The transformation from this one-time
  alignment is preserved and used as the canonical fMOST atlas to AllenCCFv3
  mapping in the pipeline.

* _Alignment of individual fMOST mouse brains_---The canonical transformation
  between the fMOST atlas and AllenCCFv3 greatly simplifies the registration of new
  individual fMOST mouse brains into the AllenCCFv3. Each new image is first
  registered into the fMOST average atlas, which shares intensity, modality, and
  morphological characteristics. This allows us to use standard, intensity-based
  alignment [@Avants:2014aa] in ANTsX to perform this alignment. Transforms are
  then concatenated to the original fMOST image to move it into the AllenCCFv3 space. 

* _Transformation of single cell neurons_---A key feature of fMOST imaging is
  the ability to reconstruct and examine whole-brain single neuron
  projections[@Peng:2021aa]. Spatial mapping of these neurons from individual
  brains into the AllenCCFv3 allows investigators to study different neuron
  types within the same space and characterize their morphology with respect to
  their transcriptomics. Mappings found between the fMOST image and the
  AllenCCFv3 using our pipeline can be applied to fMOST neuron reconstruction
  data. 

__Evaluation__

\newcommand{\ROT}[1]{\rotatebox{60}{\parbox{1.875cm}{\scriptsize #1}}}

<!-- \newcommand{\STAB}[1]{\begin{tabular}{@{}c@{}}#1\end{tabular}} -->
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

### Mapping multiplexed error-robust fluorescence in situ hybridization (MERFISH) data

We developed a full-scale ANTS pipeline for mapping multiplexed error-robust
fluorescence in situ hybridization (MERFISH) spatial transcriptomic data onto
AllenCCFv3 [@Yao:2023aa]. Mappings are performed by matching gene expression
derived region labels from the MERFISH data to corresponding anatomical
parcellations of the AllenCCFv3. The pipeline consists of MERFISH data specific
preprocessing and two main alignment steps: 1) 3D global affine mapping
and section matching of the AllenCCFv3 into the MERFISH data and 2) 2D global
and deformable mapping between each MERFISH section and matched AllenCCFv3 section.
Mappings learned via each step in the pipeline are preserved and concatenated to
provide point-to-point correspondence between the original MERFISH data and
AllenCCFv3, thus allowing individual gene expressions to be transferred into the
AllenCCFv3. 

__Data__ 

MERFISH mouse brain data was acquired using the detailed procedure
[@Yao:2023aa]. Briefly, a brain of C57BL/6 mouse was dissected according to
standard procedures and placed into an optimal cutting temperature (OCT)
compound (Sakura FineTek 4583) in which it was stored at -80°C. The fresh frozen
brain was sectioned at $10 \mu m$ on Leica 3050 S cryostats at interval of 
$200 \mu m$ to evenly cover the brain. A set of 500 genes were imaged that had been
carefully chosen to distinguish the $\sim5200$ clusters of our existing RNAseq
taxonomy. For staining the tissue with MERFISH probes, a modified version of
instructions provided by the manufacturer was used [@Yao:2023aa]. Raw MERSCOPE
data were decoded using Vizgen software (v231). Cell segmentation was performed
[@Liu:2023aa]. In brief, cells were segmented based on DAPI and PolyT staining
using Cellpose [@Stringer:2021aa]. Segmentation was performed on a median
z-plane (fourth out of seven) and cell borders were propagated to z-planes above and
below. To assign cluster identity to each cell in the MERFISH dataset, we mapped
the MERFISH cells to the scRNA-seq reference taxonomy. 

__Preprocessing__ 

* _Section reconstruction_---Alignment of MERFISH data into a 3D atlas space
  requires an estimation of anatomical structure within the data. For each
  section, this anatomic reference image was created by aggregating the number
  of detected genetic markers (across all probes) within each pixel of a $10 \mu
  m \times 10 \mu m^2$ grid to match the resolution of the $10 \mu m$ AllenCCFv3
  atlas. These reference image sections are then coarsely reoriented and aligned
  across sections using manual annotations of the most dorsal and ventral points
  of the midline. The procedure produces an anatomic image stack that serves as
  an initialization for further global mappings into the AllenCCFv3.

* _Corresponding labels_---Mapping the MERFISH data into the AllenCCFv3 requires
  us to establish correspondence between the MERFISH and AllenCCFv3 anatomy.
  Intensity-based features in MERFISH data are not apparent enough to establish
  this correspondence, so we need to generate direct corresponding anatomical
  labeling of both images. These labels are already available as part of the
  AllenCCFv3, thus the main challenge is deriving analogous labels from the
  spatial transcriptomic maps of the MERFISH data. To generate these labels, an
  we assigned each cell from the scRNA-seq dataset to one of these major
  regions: cerebellum, CTXsp, hindbrain, HPF, hypothalamus, isocortex, LSX,
  midbrain, OLF, PAL, sAMY, STRd, STRv, thalamus and hindbrain. A label map of
  each section was generated for each region by aggregating the cells assigned
  to that region within a $10 \mu m \times 10 \mu m^2$ grid. The same approach
  was used to generate more fine grained region specific landmarks (i.e.
  cortical layers, habenula, IC). Unlike the broad labels which cover the
  entirety of the section these regions are highly specific to certain parts of
  the section. Once cells in the MERFISH data are labeled, morphological
  dilation is used to provide full regional labels for alignment into the
  AllenCCFv3. 

* _Section matching_---Since the MERFISH data is acquired as sections, its 3D
  orientation may not be fulling accounted for during the reconstruction step,
  due to the cutting angle. This can lead to obliqueness artifacts in the
  section where certain structures can appear to be larger or smaller, or
  outright missing from the section. To address this, we first use a global
  alignment to match the orientations of the MERFISH sections to the atlas
  space. In our pipeline, this section matching is performed in the reverse
  direction by performing a global affine transformation of the AllenCCFv3 into
  the MERFISH data space, and then resample digital sections from the AllenCCFv3
  to match each MERFISH section. This approach limits the overall transformation
  that is applied to the MERFISH data, and, since the AllenCCFv3 is densely
  sampled, it also reduces in-plane artifacts that result from missing sections
  or undefined spacing in the MERFISH data. 

__Evaluation__

Alignment of the MERFISH data into the AllenCCFv3 was qualitatively assessed by
an expert anatomist at each iteration of the registration using known
correspondence of gene markers and their associations with the AllenCCFv3. As
previously reported [@Yao:2023aa], further assessment of the alignment showed
that of the 554 terminal regions (GM only) in the AllenCCFv3, only seven small
subregions were missed from the MERFISH dataset: frontal pole, layer 1 (FRP1),
FRP2/3, FRP5, accessory olfactory bulb, glomerular layer (AOBgl), accessory
olfactory bulb, granular layer (AOBgr), accessory olfactory bulb, mitral layer
(AOBmi) and accessory supraoptic group (ASO).

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

## The DevCCF Velocity Flow Model

\begin{figure}
\centering
\includegraphics[width=0.99\textwidth]{Figures/lowerLeftPanel.png}
\caption{The spatial transformation between any two
time points within the DevCCF longitudinal developmental trajectory
is available through the use of ANTsX functionality for generating
a velocity flow model.}
\label{fig:devccfvelocity}
\end{figure}

To continuously interpolate transformations between the different stages of the
DevCCF atlases, a velocity flow model was constructed using DevCCF derived data
and functionality recently introduced into both the ANTsR and ANTsPy
packages.  Both platforms include a complete suite of functions for determining
dense correspondence from sparse landmarks based on a variety of transformation
models ranging from standard linear models (i.e., rigid, affine) to deformable
diffeomorphic models (e.g, symmetric normalization [@Avants:2008aa]).  The
latter set includes transformation models for both the pairwise scenario and for
multiple sets, as in the case of the DevCCF. ANTsX, being built on top of ITK,
uses an ITK image data structure for the 4-D velocity field where each voxel
contains the $x$, $y$, $z$ components of the field at that point. 

### Data preparation

\begin{figure}[!htb]
\centering
\includegraphics[width=0.75\textwidth]{Figures/SimplifiedAnnotations.pdf}
\caption{Annotated regions representing common labels across developmental stages which
are illustrated for both P4 and P14.}
\label{fig:simplifiedannotations}
\end{figure}

Labeled annotations are available as part of the original DevCCF and reside
in the space of each developmental template which range in resolution from 
$31.5-50 \mu$m.  Across all atlases, the total number of labeled regions exceeds 
2500.  From these labels, a common set of 26 labels (13 per hemisphere) across 
all atlases were used for optimization and evaluation.  These regions are 
illustrated for the P4 and P14 stages in Figure \ref{fig:simplifiedannotations}.

Prior to velocity field optimization, all data were rigidly transformed to a
common space.  Using the centroids for the common label set of each DevCCF
atlas, each atlas was rigidly aligned to the space of the P56 atlas. In order to
determine the landmark correspondence across DevCCF stages, the multi-metric
capabilities of ``ants.registration(...)`` were used. Instead of performing
intensity-based pairwise registration directly on these multi-label images, each
label was used to construct a separate fixed and moving image pair resulting in
a multi-metric registration optimization scenario involving 24 binary image
pairs (each label weighted equally) for optimizing diffeomorphic correspondence
between neighboring time point atlases using the mean squares metric and the
symmetric normalization transform.

To generate the set of common point sets across all seven developmental atlases,
the label boundaries and whole regions were sampled in the P56 atlas and then
propagated to each atlas using the transformations derived from the pairwise
registrations.  We selected a sampling rate of 10\% for the contour points and
1\% for the regional points for a total number of points being per atlas being
$173303$ ($N_{contour} = 98151$ and $N_{region}=75152$). Regional boundary
points were weighted twice as those of non-boundary points during optimization.  

### Optimization

\begin{figure}[!htb]
\centering
\includegraphics[width=0.99\textwidth]{Figures/convergence.pdf}
\caption{Convergence of the optimization of the velocity field for describing the 
transformation through the developmental stages from E11.5 through P56.}
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
reproduce the results described (with possible variation in the input parameters) 
are available in the dedicated GitHub repository.

The normalized time point scalar value for each atlas/point-set in the temporal
domains $[0, 1]$ was also defined. Given the increasingly larger gaps in the
postnatal timepoint sampling, we made two adjustments.  Based on known mouse
brain development, we used 28 days for the P56 data.  We then computed the log
transform of the adjusted set of time points prior to normalization between 0
and 1 (see the right side of Figure \ref{fig:convergence}).  This log transform,
as part of the temporal normalization, significantly improved data spacing. 

The max number of iterations was set to 200 with each iteration taking six
minutes.  At each iteration we looped over the 11 integration points. At each
integration point, the velocity field estimate was updated by warping the two
immediately adjacent point sets to the integration time point and determining
the regularized displacement field between the two warped point sets.  As with
any gradient-based descent algorithm, this field was multiplied by a small step
size ($\delta = 0.2$) before adding to the current velocity field.  Convergence
is determined by the average displacement error over each of the integration
points. As can be seen in the left panel of Figure \ref{fig:convergence},
convergence occurred around 125 iterations when the average displacement error
over all integration points is minimized. The median displacement error at each
of the integration points also trends towards zero but at different rates. 

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


### The transformation model

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
bounded by E11.5 and P56.  In Figure \ref{fig:crosswarp}, we transform each
atlas to the space of every other atlas using the DevCCF transform model.
Additionally, one can use this transformation model to construct virtual
templates in the temporal gaps of the DevCCF.  This is illustrated in Figure
\ref{fig:virtual} where we used the optimized velocity field to construct
virtual templates at time point P10.3 and P20---arbitrarily chosen simply to
demonstrate the concept.  After situating these time points within the
normalized time point interval, the existing adjacent DevCCF atlases on either
chronological side can be warped to the desired time point. A subsequent call to
one of the ANTsX template building functions then permits the construction of
the template at that time point.  Note that both of these usage examples can be
found in the GitHub repository previously given.


## The Mouse Cortical Thickness Pipeline

\begin{figure}
\centering
\includegraphics[width=0.9\textwidth]{Figures/mousePipeline.png}
\caption{The mouse brain cortical thickness pipeline integrating two 
deep learning components for brain extraction and brain parcellation 
prior to estimating cortical thickness. Both deep learning networks
rely heavily on data augmentation on templates built from open 
data and provide an outline for further refinement and creating 
alternative parcellations for tailored research objectives.}
\label{fig:mouseKK}
\end{figure}

One of the most well-utilized pipelines in the ANTsX toolkit is the generation
of cortical thickness maps in the human brain from T1-weighted MRI.  Starting
with the novel Diffeomorphic Registration-based Cortical Thickness (DiReCT)
algorithm [@Das:2009uv], a complete algorithmic workflow was developed for both
cross-sectional [@Tustison:2014ab] and longitudinal [@Tustison:2019aa]
T1-weighted MR image data.  This contribution was later refactored using deep
learning [@Tustison:2021aa] leveraging the earlier results [@Tustison:2014ab] 
for training data.  

In the case of the mouse brain, the lack of training data and/or tools to
generate training data make a similar developmental trajectory difficult. In
addition, mouse data is often characterized by unique issues such as frequent
anisotropic sampling which are often in sharp contrast to the high resolution
resources available within the community, e.g., AllenCCFv3 and DevCCF. Using
ANTsX and other publicly available data resources, we developed a complete mouse
brain structural morphology pipeline as illustrated in Figure \ref{fig:mouseKK}
and detailed below. 

### Two-shot mouse brain extraction network

In order to create a generalized mouse brain extraction network, we built
whole-head templates from two publicly available datasets.  The Center for
Animal MRI (CAMRI) dataset [@Hsu2021] from UNC consists of 16 T2-weighted MRI of
voxel resolution $0.16 \times 0.16 \times 0.16 mm^3$.  The second
high-resolution data set [@Reshetnikov2021] comprises 88 specimens each with
three spatially aligned canonical views with in-plane resolution of $0.08 \times
0.08 mm^2$ with a slice thickness of 0.5 mm.  These three orthogonal views were
used to reconstruct a single high-resolution volume per subject using a B-spline
fitting algorithm developed in ANTsX [@Tustison:2006aa].  From these two
datasets, two symmetric isotropic ANTsX templates [@Avants:2010aa] were
generated having different defacing aesthetics analogous to the publicly
available ANTsX human brain templates used in previous research
[@Tustison:2014ab]. Bias field simulation, intensity histogram warping, noise
simulation, random translation and warping, and random anisotropic resampling in
the three canonical directions were used for data augmentation in creating a
T2-weighted brain extraction network.

### Single-shot mouse brain parcellation network

To create the network for generating a brain parcellation consistent with
cortical thickness estimation, we used the AllenCCFv3 and the associated
``allensdk`` Python library. Using ``allensdk``, a gross parcellation labeling
was generated from the fine Allen CCFv3 labeling which includes the cerebral
cortex, cerebral nuclei, brain stem, cerebellum, main olfactory bulb, and
hippocampal formation.  This labeling was mapped to the P56
component of the DevCCF. Both the T2-w P56 DevCCF and labelings, in
conjunction with the data augmentation described previously for brain 
extraction, was used to create a brain parcellation network.

### Evaluation

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
\caption{Evaluation of the ANTsX mouse brain extraction, parcellation, and
cortical thickness pipeline on an independent dataset 
consisting of 12 specimens $\times$ 7 time points = 
84 total images.  (a) Dice overlap comparisons with the provided brain
masks provide generally good agreement with the brain extraction network.
(b) Cortical volume measurements show similar average quantities over
the developmental trajectory between the original anisotropic data and 
interpolated isotropic data.  These results contrast with the cortical
thickness measurements which show that cortical thickness estimation 
in anisotropic space severely underestimates the actual values.}
\label{fig:evaluation}
\end{figure}

For evaluation, we used an additional publicly available dataset
[@Rahman:2023aa] which is completely independent from the data used in training
the brain extraction and parcellation networks.  Data includes 12 specimens each
imaged at seven time points (Day 0, Day 3, Week 1, Week 4, Week 8, Week 20) with
available brain masks.  In-plane resolution is $0.1 \times 0.1 mm^2$ with a
slice thickness of $0.5 mm$.  Since the training data is isotropic and data
augmentation includes downsampling in the canonical directions, each of the two 
networks learns mouse brain-specific interpolation such that one can perform prediction
on thick-sliced images, such as these evaluation data, and return isotropic
probability and thickness maps (a choice available to the user).  Figure 
\ref{fig:evaluation} summarizes the results of the evaluation and comparison between
isotropic and anisotropic cortical measurements in male and female specimens.





\clearpage
\newpage

# Discussion {-}

The ANTsX ecosystem is a powerful framework that has demonstrated applicability
to multiple species and organ systems, including the mouse brain. This is
further evidenced by the many other software packages that use various ANTsX
components in their own mouse-specific workflows.  In and of itself, the
extensive functionality of ANTsX makes it possible to create complete processing
pipelines without requiring the integration of multiple packages. These
open-source components not only perform well but are available across multiple
platforms which facilitates the construction of tailored pipelines for
individual study solutions. These components are also supported by years of
development not only by the ANTsX development team but by the larger ITK
community.  

In the case of the development of the DevCCF, ANTsX was crucial in providing
necessary functionality for yielding high quality output.  For the generation of
the individual developmental stage multi-modal, symmetric templates, ANTsX is
unique amongst image analysis software packages in providing existing solutions
for template generation which have been thoroughly vetted, including being used
in several studies over the years, and which continue to be under active
refinement.  At its core, computationally efficient and quality template
generation requires the use of precision pairwise image mapping functionality
which, historically, is at the origins of the ANTsX ecosystem. And these mapping
capabilities extend beyond template generation to the mapping of other image
data (e.g., gene expression maps) to a selected template for providing further
insight into the mouse brain.  

With respect to the DevCCF, despite the significant expansion of available
developmental age templates beyond what existed previously, there are still
temporal gaps in the DevCCF which can be potentially sampled by future research
efforts. However, pioneering work involving time-varying diffeomorphic
transformations allow us to continuously situate the existing templates within a
velocity flow model.  This allows one to determine the diffeomorphic
transformation from any one temporal location to any other temporal location
within the time span defined by the temporal limits of the DevCCF. This
functionality is built on multiple components from the Insight Segmentation and
Registration Toolkit including the B-spline scattered data approximation
technique for field regularization and velocity field integration. This velocity
field model permits intra-template comparison and the construction of virtual
templates where a template can be estimated at any continuous time point within
the temporal domain.  This novel application can potentially enhance our
understanding of intermediate developmental stages.

We also presented a mouse brain pipeline for brain extraction, parcellation, and
cortical thickness using single-shot and two-shot learning with data
augmentation.  This approach attempts to circumvent (or at least minimize) the
typical requirement of large training datasets as with the human ANTsX pipeline
analog. However, even given our initial success on independent data, we fully
anticipate that refinements will be necessary.  In fact, a current parallel
study with a separate collaborator using private data yielded three brain
extraction failures (out of 89 specimens). Given that the ANTsX toolkit is a
dynamic effort undergoing continual improvement, we manually correct such cases
and use them for future training and refinement of network weights as we have
done for our human-based networks.  Generally, these approaches provide a way to
bootstrap training data for manual refinement and future generation of more
accurate deep learning networks in the absence of corresponding non deep
learning-based tools.



\clearpage
\newpage

# Methods {-} 

The following methods are all available as part of the ANTsX ecosystem
with analogous elements existing in both ANTsR (ANTs in R) and ANTsPy
(ANTs in Python) with and ANTs/ITK C++ core.  However, most of the 
development for the work described below was performed using ANTsPy.
For equivalent calls in ANTsR, please see the ANTsX tutorial at
\url{https://tinyurl.com/antsxtutorial}.

## Preprocessing: bias field correction and denoising {-}

Bias field correction and image denoising are standard preprocessing steps in
improving overall image quality in mouse brain images. The bias field, a gradual
spatial intensity variation in images, can arise from various sources such as
magnetic field inhomogeneity or acquisition artifacts, leading to distortions
that can compromise the quality of brain images. Correcting for bias fields
ensures a more uniform and consistent representation of brain structures,
enabling more accurate quantitative analysis. Additionally, brain images are
often susceptible to various forms of noise, which can obscure subtle features
and affect the precision of measurements. Denoising techniques help mitigate the
impact of noise, enhancing the signal-to-noise ratio and improving the overall
image quality.  The well-known N4 bias field correction algorithm
[@Tustison:2010ac] has its origins in the ANTs toolkit which was implemented and
introduced into the ITK toolkit, i.e. ``ants.n4_bias_field_correction(...)``.
Similarly, ANTsX contains an implementation of a well-performing patch-based
denoising technique [@Manjon:2010aa] and is also available as an image filter to
the ITK community, ``ants.denoise_image(...)``.

## Image registration {-}

The ANTs registration toolkit is a complex framework permitting highly tailored
solutions to pairwise image registration scenarios [@Avants:2014aa].  It
includes innovative transformation models for biological modeling
[@Avants:2008aa;@Tustison:2013ac] and has proven capable of excellent
performance [@Klein:2009aa;@Avants:2011wx].  Various parameter sets targeting
specific applications have been packaged with the different ANTsX platforms,
specifically ANTs, ANTsPy, and ANTsR [@Tustison:2021aa]. In ANTsPy, the function
``ants.registration(...)`` is used to register a pair of images or a pair of
image sets where ``type_of_transform`` is a user-specified option that invokes a
specific parameter set.  For example
``type_of_transform='antsRegistrationSyNQuick[s]'`` encapsulates an oft-used
parameter set for quick registration whereas
``type_of_transform='antsRegistrationSyN[s]'`` is a more detailed alternative.
Transforming images using the derived transforms is performed via the
``ants.apply_transforms(...)`` function.

Initially, linear optimization is initialized with center of (intensity) mass
alignment typically followed by optimization of both rigid and affine transforms
using the mutual information similarity metric. This is followed by
diffeomorphic deformable alignment using symmetric normalization (SyN) with
Gaussian [@Avants:2008aa] or B-spline regularization [@Tustison:2013ac] where
the forward transform is invertible and differentiable. The similarity metric
employed at this latter stage is typically either neighborhood cross-correlation
or mutual information. Note that these parameter sets are robust to input image
type (i.e., LSFM, Nissl staining, and the various MRI modalities) and are
adaptable to mousing image geometry scaling.  Further details can be found in
the various documentation sources for these ANTsX packages.

## Template generation {-}

ANTsX provides functionality for constructing templates from a set (or
multi-modal sets) of input images as originally described [@Avants:2010aa]
and recently used to create the DevCCF templates [@Kronman:2023aa]. An
initial template estimate is constructed from an existing subject image or 
a voxelwise average derived from a rigid pre-alignment of the image population.
Pairwise registration between each subject and the current template estimate
is performed using the Symmetric Normalization (SyN) algorithm [@Avants:2008aa].
The template estimate is updated by warping all subjects to the space of the
template, performing a voxelwise average, and then performing a "shape update"
of this latter image by warping it by the average inverse deformation, thus
yielding a mean image of the population in terms of both intensity and 
shape.  The corresponding ANTsPy function is ``ants.build_template(...)``.

## Continuous developmental velocity flow transformation model {-}

Given multiple, linearly or non-linearly ordered point sets where individual
points across are in one-to-one correspondence, we developed an approach for
generating a velocity flow transformation model to describe a time-varying
diffeomorphic mapping as a variant of the inexact landmark matching solution.
Integration of the resulting velocity field can then be used to describe the
displacement between any two time points within this time-parameterized domain.
Regularization of the sparse correspondence between point sets is performed
using a generalized B-spline scattered data approximation technique
[@Tustison:2006aa], also developed by the ANTsX developers and contributed to
ITK. 

To apply this methodology to the developmental templates [@Kronman:2023aa], we
coalesced the manual annotations of the developmental templates into 26 common
anatomical regions (13 per hemisphere).  We then used these regions to generate
invertible transformations between successive time points. Specifically each
label was used to create a pair of single region images resulting in 26 pairs of
"source" and "target" images.  The multiple image pairs were used to iteratively
estimate a diffeomorphic pairwise transform. Given the seven atlases E11.5,
E13.5, E15.5, E18.5, P4, P14, and P56, this resulted in 6 sets of transforms
between successive time points. Given the relative sizes between atlases, on the
order of 10$^6$ points were randomly sampled labelwise in the P56 template space
and propagated to each successive atlas providing the point sets for
constructing the velocity flow model.  Approximately 125 iterations resulted in
a steady convergence based on the average Euclidean norm between transformed
point sets.  Ten integration points were used and point sets were distributed
along the temporal dimension using a log transform for a more evenly spaced
sampling.  For additional information see the help menu for the ANTsPy function 
``ants.fit_time_varying_transform_to_point_sets(...)``.

## ANTsXNet mouse brain applications {-}

_General notes regarding deep learning training._

All network-based approaches described below were implemented and organized in
the ANTsXNet libraries comprising Python (ANTsPyNet) and R (ANTsRNet) analogs
using the Keras/Tensorflow libraries available as open-source in ANTsX GitHub
repositories. For the various applications, both share the identically trained
weights for mutual reproducibility.  For all GPU training, we used Python
scripts for creating custom batch generators. As such batch generators tend to
be application-specific, we store them in a separate GitHub repository for
public availability (\url{https://github.com/ntustison/ANTsXNetTraining}). In
terms of GPU hardware, all training was done on a DGX (GPUs: 4X Tesla V100,
system memory: 256 GB LRDIMM DDR4).

Data augmentation is crucial for generalizability and accuracy of the trained 
networks.  Intensity-based data augmentation consisted of randomly added noise 
(i.e., Gaussian, shot, salt-and-pepper), simulated bias fields based on N4 bias 
field modeling, and histogram warping for mimicking well-known MRI intensity nonlinearities
[@Nyul:2000aa;@Tustison:2021aa]. These augmentation techniques are available in
ANTsXNet (only ANTsPyNet versions are listed with ANTsRNet versions available)
and include:

* image noise:  ``ants.add_noise_to_image(...)``,

* simulated bias field: ``antspynet.simulate_bias_field(...)``, and

* nonlinear intensity warping: ``antspynet.histogram_warp_image_intensities(...)``.

Shape-based data augmentation used both random linear and nonlinear
deformations in addition to anisotropic resampling in the three canonical 
orientations to mimic frequently used acquisition protocols for mice brains:

* random spatial warping: ``antspynet.randomly_transform_image_data(...)`` and

* anisotropic resampling: ``ants.resample_image(...)``.

_Brain extraction._

Similar to human neuroimage processing, brain extraction is a crucial
preprocessing step for accurate brain mapping.  Within ANTsXNet, we have created
several deep learning networks for brain extraction for several image modalities
(e.g., T1, FLAIR, fractional anisotropy).  Similarly, for the developmental
brain atlas work [@Kronman:2023aa] we developed similar functionality for mouse
brains of different modalities and developmental age.  All networks use a
conventional U-net architecture [@Falk:2019aa].  Whereas T2-weighted brain
extraction is volumetric-based for both isotropic and anisotropic data, coronal
and sagittal networks are available for both E13.5 and E15.5 data. In ANTsPyNet,
this functionality is available in the program
``antspynet.mouse_brain_extraction(...)``.  Even when physical brain extraction
is performed prior to image acquisition, artifacts, such as bubbles or debris,
can complicate subsequent processing.  Similar to the brain extraction networks,
a 2-D U-net architecture [@Falk:2019aa] was created to separate the background
and foreground.  For the two-shot T2-weighted brain extraction network, two brain 
templates were generated along with their masks.  Although both template/mask pairs
are available in the GitHub repository associated with this work, the synthesize
volumetric B-spline T2-weighted pair is available within ANTsXNet through the
calls:

* template: ``antspynet.get_antsxnet_data("bsplineT2MouseTemplate")`` and

* mask: ``antspynet.get_antsxnet_data("bsplineT2MouseTemplateBrainMask")``.

_Brain parcellation._

The T2-weighted brain parcellation network is also based on a 3-D U-net
architecture and the T2-w DevCCF P56 template component with 
extensive data augmentation, as described previously.  Intensity
differences between the template and any brain extracted input image
are minimized through the use of the rank intensity transform 
(``ants.rank_intensity(...)``).  Shape differences are reduced 
by the additional preprocessing step of warping the brain extracted
input image to the template.  Additional input channels include the 
prior probability images created from the template parcellation.
These images are also available through the ANTsXNet interface:

* template: ``antspynet.get_antsxnet_data("DevCCF_P56_MRI-T2_50um")`` and

* parcellation: ``antspynet.get_antsxnet_data("DevCCF_P56_MRI-T2_50um_BrainParcellationNickMask")``.


_Miscellaneous networks:  Super-resolution, cerebellum, and hemispherical masking._

To further enhance the data prior to designing mapping protocols, additional
networks were created.  A well-performing deep back projection network
[@Haris:2018aa] was ported to ANTsXNet and expanded to 3-D for various
super-resolution applications [@Avants:2023aa], including mouse data.  Finally,
features of anatomical significance, namely the cerebellum and hemispherical
midline were captured in these data using deep learning networks.  

## Intra-slice image registration with missing slice imputation {-}

Volumetric gene expression slice data was collated into 3-D volumes. Prior to
mapping this volume to the corresponding structural data and, potentially, to
the appropriate template, alignment was improved using deformable registration
on contiguous slices.  However, one of the complications associated with these
image data was the unknown number of missing slices, the number of consecutive
missing slices, and the different locations of these missing slices.  To handle
this missing data problem, we found that data interpolation using the B-spline
approximation algorithm cited earlier [@Tustison:2006aa] (ANTsPy function:
``ants.fit_bspline_object_to_scattered_data(...)``).  This provided sufficient
data interpolation fidelity to perform continuous slicewise registration.  Other
possible variants that were considered but deemed unnecessary was performing
more than one iteration cycling through data interpolation and slicewise
alignment.  The other possibility was incorporating the super-resolution
technique described earlier.  But again, our data did not require these
additional steps. 

## Synthesizing isotropic image volumes from orthogonal views  {-}

Similar to the isotropic , the multi-plane, high resolution data
[@Reshetnikov2021] was used to create single isotropic volumes using the
B-spline fitting algorithm [@Tustison:2006aa].  This algorithm is encapsulated
in ``ants.fit_bspline_object_to_scattered_data(...)`` where the input is the set
of voxel intensity values and associated physical location.  Since each point
can be assigned a confidence weight, we use the the normalized gradient value to
more heavily weight edge regions.


## Visualization {-}

To complement the well-known visualization capabilities of R and Python, e.g.,
ggplot2 and matplotlib, respectively, image-specific visualization capabilities
are available in the ``ants.plot(...)`` (Python) and ``plot.antsImage(...)`` (R).
These are capable of illustrating multiple slices in different orientations with
both other image overlays as well as label images.  

\clearpage
\newpage

<!--
__Ethical compliance.__ We complied with all relevant ethical regulations. 

__Reporting Summary.__ Further information on research design is available in
the Nature Research Reporting Summary linked to this article.

__Software availability.__ 
-->

__Data availability.__ All data and doftware used in this work are publicly
available.  The DevCCF atlas is available at
\url{https://kimlab.io/brain-map/DevCCF/}. ANTsPy, ANTsR, ANTsPyNet, and
ANTsRNet are available through GitHub at the ANTsX Ecosystem
(\url{https://github.com/ANTsX}).  Training scripts for all deep learning
functionality in ANTsXNet can also be found on GitHub 
(\url{https://github.com/ntustison/ANTsXNetTraining}).
A GitHub repository specific to the work
discussed in the manuscript was created and is available at
\url{https://github.com/ntustison/ANTsXMouseBrainMapping}.


\clearpage

# References {-}