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
brain.  \textcolor{red}{First, we provide ANTsX-based protocols for mapping
MERFISH, fMOST, and lightsheet datasets to AllenCCFv3 accounting for common
artefacts and other confounds.}  Herein, novel contributions include recently
developed ANTsX functionality for generating a velocity flow-based mapping
spanning the spatiotemporal domain of a longitudinal trajectory which we
apply to the Developmental Common Coordinate Framework (DevCCF).  Additionally,
we present an automated structural morphological pipeline for determining
volumetric and cortical thickness measurements analogous to the well-utilized
ANTsX pipeline for human neuroanatomy.  This latter development also illustrates
a more general open-source ANTsX framework for determining tailored brain
parcellations using the AllenCCFv3 and DevCCF templates.

\clearpage# Introduction

Over the past two decades there have been significant advancements in mesoscopic
analysis of the mouse brain. It is now possible to track single cell neurons in
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
and missing slices. These severely complicate assumed correspondence for
conventional spatial mapping approaches.

## Mouse-specific brain mapping software

To address such challenges, several software packages have been developed over
the years comprising solutions of varying comprehensibility, sophistication, and
availability.  An early contribution to the community was the Rapid Automatic
Tissue Segmentation (RATS) package [@Oguz:2014aa] for brain extraction.
More recently, several publicly available packages comprise well-established
package dependencies originally developed on human brain data. SPMMouse
[@Sawiak:2014aa], for example, is based on the well-known Statistical Parametric
Mapping (SPM) software package [@Ashburner:2012aa]. The automated mouse atlas
propagation (aMAP) tool is largely a front-end for the NiftyReg image
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
AFNI [@Cox:2012aa] for image registration; MIRACL, SAMRI, and BrainsMapi
[@Ni:2020aa] all use ANTsX registration tools. Other packages use landmark-based
approaches to image registration including SMART [@Jin:2022aa]---an R package
for semi-automated landmark-based registration and segmentation of mouse brain
based on WholeBrain [@Furth:2018aa].  FriendlyClearMap [@Negwer:2022aa] uses the
landmark-based registration functionality of Elastix [@Klein:2010aa]. Finally,
the widespread adoption of deep learning techniques has also influenced
development in mouse brain imaging methodologies.  For example, if tissue
deformations are not considered problematic for a particular dataset, DeepSlice
can be used to determine affine mappings [@Carey:2023aa] with the optimal
computational efficiency associated with neural networks.

## The ANTsX Ecosystem for mouse brain mapping 

As noted previously, many of the existing packages designed for processing mouse
brain image data use ANTsX tools for core processing steps in various workflows,
particularly its pairwise, intensity-based image registration capabilities and
bias field correction. Historically, ANTsX development is originally based on
fundamental approaches to image mapping
[@Bajcsy:1982aa;@Bajcsy:1989aa;@Gee:2003aa], particularly in the human brain,
which has resulted in core contributions to the field such as the well-known and
highly-vetted Symmetric Normalization (SyN) algorithm [@Avants:2008aa].  Since
its development, various independent platforms have been used to evaluate ANTsX
image registration capabilities in the context of different application foci
which include multi-site brain MRI data [@Klein:2009aa], pulmonary CT data
[@Murphy:2011aa], and most recently, multi-modal brain registration in the
presence of tumors [@Baheti:2021aa]. 

\input{antsx_functionality_table}

Apart from its registration capabilities, ANTsX comprises additional
functionality such as template generation [@Avants:2010aa], point set data
approximation [@Tustison:2006aa], and deep learning networks specifically
trained for mouse data (see Table \ref{table:methods}). The comprehensive use of
the toolkit has demonstrated superb performance in multiple application areas
(e.g., consensus labeling [@Wang:2013ab], brain tumor segmentation
[@Tustison:2014aa], and cardiac motion estimation [@Tustison:2015ab] ).
Importantly, ANTs is built on the Insight Toolkit (ITK) [@McCormick:2014aa]
deriving benefit from the open-source community of scientists and programmers
and providing an open-source venue for algorithmic development, evaluation, and
improvement.

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
ANTsX packages) with a dedicated GitHub repository specific to this work
(https://github.com/ntustison/ANTsXMouseBrainMapping).

### The DevCCF velocity flow model

Recently, the Developmental Common Coordinate Framework (DevCCF) was introduced
to the mouse brain research community as a public resource [@Kronman:2023aa]
comprising symmetric atlases of multimodal image data and anatomical
segmentations defined by developmental ontology.  These templates sample the
mouse embryonic days (E) 11.5, E13.5, E15.5, E18.5 and postnatal day (P) 4, P14,
and P56.  Modalities include light sheet flourescence miscroscopy (LSFM) and at
least four MRI contrasts per developmental stage.  Anatomical parcellations are
also available for each time point and were generated from ANTsX-based mappings
of gene expression and other cell type data.  The P56 template was integrated
with the Allen CCFv3 to further increase the practical utility of the DevCCF.
These processes, specifically template generation and multi-modal image mapping,
were performed using ANTsX functionality in the presence of previously noted
image mapping difficulties such as missing slices, tissue distortion.  

Given the temporal gaps in the discrete set of developmental atlases, we also
provide an open-source framework, through ANTsX, for inferring correspondence
within the temporally continuous domain sampled by the existing set of embryonic
and postnatal atlases of the DevCCF.  This recently developed ANTsX
functionality permits the generation of a diffeomorphic velocity flow
transformation model [@Beg:2005aa], influenced by previous work
[@Tustison:2013ac].  The resulting time-parameterized velocity field spans the
stages of the DevCCF where mappings between any two continuous time points
within the span bounded by the E11.5 and P56 atlases is determined by
integration of the optimized velocity field. 

### Structural morphology and cortical thickness in the mouse brain

We also describe a structural morphological pipeline for calculating image-based
cortical thickness measurements [@Das:2009uv] analogous to the well-known and
heavily utilized ANTsX cortical thickness pipeline  for cross-sectional and
longitudinal human brain studies
[@Tustison:2014ab;@Tustison:2019aa;@Tustison:2021aa].  Two integral pipeline
components are brain extraction and brian parcellation derived from,
respectively, two-shot and single-shot deep learning, leveraging only publicly
available resources, including AllenCCFv3 and DevCCF.  Although we anticipate
that this cortical thickness pipeline will be beneficial to the research
community, this work demonstrates more generally how one can leverage ANTsX
tools for developing tailored brain parcellation schemes.  Evaluation is
performed on an independent open-source data set [@Rahman:2023aa] comprising
longitudinal acquisitions of multiple specimens.  


\clearpage
\newpage

# Results

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
\includegraphics[width=0.99\textwidth]{Figures/lowerLeftPanel.png}
\caption{Using a velocity flow model, the transformation between any two
temporal time points within the DevCCF is possible.}
\label{fig:devccfvelocity}
\end{figure}

To continuously interpolate transformations between the different stages of the
DevCCF atlases, a velocity flow model was constructed using DevCCF derived data
and ANTsX functionality recently introduced into both the ANTsR and ANTsPy
packages.  Both platforms include a complete suite of functions for determining
dense correspondence from sparse landmarks based on a variety of transformation
models ranging from standard linear models (i.e., rigid, affine) to deformable
diffeomorphic models (e.g, symmetric normalization [@Avants:2008aa]).  The
latter set includes velocity flow models for both the pairwise scenario
(``ants.fit_transform_to_paired_points(...)``) and for multiple sets
(``ants.fit_time_varying_transform_to_point_sets(...)``), as in the case of the
DevCCF. Several self-contained tutorials illustrating usage for these functions 
are available at \url{https://tinyurl.com/antsxtutorial}.

ANTsX, being built on top of ITK, uses an ITK image data structure for the 4-D
velocity field where each voxel contains the $x$, $y$, $z$ components of the
field at that point. Field regularization is provided by a B-spline scattered
data approximation technique [@Tustison:2006aa,@Tustison:2013ac] which permits
individual point weighting.  Both field regularization and integration of
the velocity field are built on ITK functions contributed from ANTsX
development.  

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

``ants.fit_time_varying_transform_to_point_sets(...)`` from the ANTsPy package
was used to optimize the velocity field. Input is composed of the seven corresponding
point sets and their associated weight values, the selected number of
integration points for the velocity field ($N=11$), and the parameters defining
the geometry of the spatial dimensions of the velocity field.  Thus, the optimized 
velocity field described here is of size $[256, 182, 360]$
($50 \mu$m isotropic) $\times 11$ integration points for a total compressed
size of a little over 2 GB.  This choice represented weighing the trade-off 
between tractability, portability, and accuracy.  However,  all
data and code to reproduce the results described are available in the dedicated 
GitHub repository.

The normalized time point scalar value for each atlas/point-set in the temporal
domains $[0, 1]$ was also defined. Given the increasingly larger gaps in the
postnatal timepoint sampling, we made two adjustments.  Based on known mouse
brain development, we used 28 days for the P56 data.  We then computed the log
transform of the adjusted set of time points prior to normalization between 0
and 1 (see the right side of Figure \ref{fig:convergence}).  This log transform,
as part of the temporal normalization, significantly improved data spacing. 

The max number of iterations was set to 200.  At each iteration we looped over
the 11 integration points. At each integration point, the velocity field
estimate was updated by warping the two immediately adjacent point sets to the
integration time point and determining the regularized displacement field
between the two warped point sets.  As with any gradient-based descent
algorithm, this field was multiplied by a small step size ($\delta = 0.2$)
before adding to the current velocity field.  Using multithreading, each
iteration took about six minutes. Convergence is determined by the average
displacement error over each of the integration points. As can be seen in the
left panel of Figure \ref{fig:convergence}, convergence occurred around 125
iterations when the average displacement error over all integration points is
minimized. The median displacement error at each of the integration points also
trends towards zero but at different rates. 

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



### The DevCCF transform model

\begin{figure}[!htb]
\centering
\includegraphics[width=0.99\textwidth]{Figures/CrossWarp.pdf}
\caption{Mid-sagittal visualization of the effects of the transformation model in
warping every developmental stage to the time point of every other developmental
stage.  The original images are located along the diagonal.  Columns correspond
to the warped original image whereas the rows represent the reference space to which
each image is warped.}
\label{fig:crosswarp}
\end{figure}

Once optimized, the resulting velocity field can be used to generate the
deformable transform between any two continuous points within the time interval
bounded by E11.5 and P56.  In Figure \ref{fig:crosswarp}, we transform each
atlas to the space of every other atlas using the DevCCF transform model.
Additionally, one can use this transformation model to construct virtual
templates in the temporal gaps of the DevCCF.  This is illustrated in Figure
\ref{fig:virtual} where we used the optimized velocity field to construct
virtual-templates at time point P10.3 and P20---arbitrarily chosen simply to
demonstrate the concept.  After situating these time points within the
normalized time point interval, the existing adjacent DevCCF atlases on either
chronological side can be warped to the desired time point. A subsequent call to
one of the ANTsX template building functions then permits the construction of
the template at that time point.  Note that both of these usage examples can be
found on the GitHub repository given above.

\begin{figure}[!htb]
\centering
\includegraphics[width=0.99\textwidth]{Figures/pseudo_template.pdf}
\caption{Illustration of the use of the velocity flow model for creating virtual templates
at continuous time points not represented in one of the existing DevCCF time points.
For example, FA templates at time point P10.3 and P20 can be generated by warping the 
existing temporally adjacent developmental templates to the target time point and using 
those images in the ANTsX template building process.}
\label{fig:virtual}
\end{figure}

## The Mouse Cortical Thickness Pipeline

\begin{figure}
\includegraphics[width=0.9\textwidth]{Figures/mousePipeline.png}
\caption{}
\label{fig:mouseKK}
\end{figure}


\clearpage
\newpage

# Discussion {-}

The ANTsX ecosystem is a powerful framework that has demonstrated applicability
to multiple species and organ systems, including the mouse brain. This is
further evidenced by the many other software packages that use various ANTsX
components in their own mouse-specific workflows.  The extensive functionality
of ANTsX per se makes it possible to create complete processing pipelines
without requiring the integration of multiple packages. These open-source ANTsX
components not only perform well but are available across multiple popular
platforms which facilitates the construction of tailored pipelines for
individual study solutions. These components are also supported by years of
development not only by the ANTsX development team but by the larger ITK
community.  

In the case of the development of the DevCCF, ANTsX was crucial in providing
necessary functionality for yielding high quality output.  First, for the
generation of the individual developmental stage multi-modal, symmetric
templates, ANTsX is unique amongst image analysis software packages in providing
existing solutions for template generation which have been thoroughly vetted,
including being used in several studies over the years, and which continue to be
under active refinement.  At its core, computationally efficient and quality
template generation requires the use of precision pairwise image mapping
functionality which, historically, is at the origins of the ANTsX ecosystem.
And these mapping capabilities extend beyond template generation to the mapping
of other image data (e.g., gene expression maps) to template for providing
further insight into the mouse brain.  

Despite the significant expansion of available developmental age templates
beyond what previously existed (e.g., Allen CCFv3), there still exist temporal
gaps in the DevCCF.  However, pioneering work involving diffeomorphic
transformations allowed us to continuously situate the existing templates within
a time-varying velocity flow model.  This allows one to determine the
diffeomorphic transformation from any one temporal location to any other
temporal location within the time span defined by the E11.5 and P56 templates.
This functionality is built on multiple components from the Insight Segmentation
and Registraiton Toolkit including the B-spline scattered data approximation
technique for field regularization and velocity field integration using fourth
order Runge-Kutta. This velocity field model permits intra-template comparison
and the construction of virtual templates where a template can be estimated at
any continuous time point within the temporal domain.  This novel application
can potentially enhance our understanding of intermediate developmental stages.
To increase its impact and reproduce the results shown previously, we have made 
the data and code publicly available at \url{https://github.com/ntustison/DevCCF-Velocity-Flow}.

Although ANTsX is quite evolved in its development and functionality, there are
several areas which are currently under active development or consideration for
further expansion.  Most notably, as in our human applications, deep learning
has had a significant impact in steering our attention.  Core functionality,
such as brain extraction for mouse brain mapping, would benefit from increasing
the number of available modalities.   Additionally, as with much deep learning development, 
such work will require additional data but is significantly facilitated by the 
tools that we have created in both ANTsPyNet and ANTsRNet.  

<!--
Related would be the 
utility of the development of mouse brain parcellation tools such as our 
``antspynet.desikan_killiany_tourville_labeling(...)`` tool.
-->
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

As in human studies, bias field correction and image denoising are standard
preprocessing steps in improving overall image quality in mouse brain images.
The bias field, a gradual spatial intensity variation in images, can arise from
various sources such as magnetic field inhomogeneity or acquisition artifacts,
leading to distortions that can compromise the quality of brain images.
Correcting for bias fields ensures a more uniform and consistent representation
of brain structures, enabling accurate quantitative analysis. Additionally,
brain images are often susceptible to various forms of noise, which can obscure
subtle features and affect the precision of measurements. Denoising techniques
help mitigate the impact of noise, enhancing the signal-to-noise ratio and
improving the overall image quality.  The well-known N4 bias field correction
algorithm [@Tustison:2010ac] has its origins in the ANTs toolkit which was
implemented and introduced into the ITK toolkit.  Similarly, ANTsX contains an
implementation of a well-performing patch-based denoising technique
[@Manjon:2010aa] and is also available as an image filter to the ITK community.

## ANTsXNet mouse brain applications {-}

_General notes regarding deep learning training._

All network-based approaches described below were implemented and organized in
the ANTsXNet libraries comprising Python (ANTsPyNet) and R (ANTsRNet) analogs
using the Keras/Tensorflow libraries available as open-source in ANTsX GitHub
repositories. For the various applications, both share the identically trained
weights for mutual reproducibility.  Training data was provided by manual
labeling by various co-authors and expanded using both intensity-based and
shape-based data augmentation techniques.

Intensity-based data augmentation consisted of randomly added noise based on ITK
functionality, simulated bias fields based on N4 bias field modeling, and
histogram warping for mimicking well-known MRI intensity nonlinearities
[@Nyul:2000aa;@Tustison:2021aa]. These augmentation techniques are available in
ANTsXNet (only ANTsPyNet versions are listed):  simulated bias field:
``antspynet.simulate_bias_field(...)``, image noise:
``antspyhet.add_noise_to_image(...)``, and MRI intensity nonlinear
characterization: ``antspynet.histogram_warp_image_intensities(...)``.
Shape-based data augmentation used both random linear and nonlinear
deformations.  This functionality is also instantiated within ANTsXNet in terms
of random spatial warping: ``antspynet.randomly_transform_image_data(...)``.

For all GPU training, we used Python scripts for creating custom batch
generators. As such batch generators tend to be application-specific, we store
them in a separate GitHub repository for public availability
(\url{https://github.com/ntustison/ANTsXNetTraining}). In terms of GPU hardware, all
training was done on a DGX (GPUs: 4X Tesla V100, system memory: 256 GB LRDIMM
DDR4).

_Brain extraction._

Similar to human neuroimage processing, brain extraction is a crucial
preprocessing step for accurate brain mapping.  Within ANTsXNet, we have created
several deep learning networks for brain extraction for several image modalities
(e.g., T1, FLAIR, fractional anisotropy).  Similarly, for the developmental
brain atlas work [@Kronman:2023aa] we developed similar functionality for mouse
brains of different modalities and developmental age.  All networks use a
conventional 2-D U-net architecture [@Falk:2019aa] and perform prediction in a
slice-wise fashion given the limitations of the acquisition protocols (e.g.,
missing slices, slice thickness).  Currently, coronal and sagittal networks are
available for both E13.5 and E15.5 data and coronal network for T2-weighted MRI.
In ANTsPyNet, this functionality is available in the program
``antspynet.mouse_brain_extraction(...)``.  Even when physical brain extraction is
performed prior to image acquisition, artifacts, such as bubbles or debris, can
complicate subsequent processing.  Similar to the brain extraction networks, a
2-D U-net architecture [@Falk:2019aa] was created to separate the background and
foreground.  

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
``type_of_transform='antsRegistrationSyNQuick[s]'`` is an oft-used parameter
set.

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
shape.  

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
coalesced the manual parcellations of the developmental templates into 26 common
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
sampling.  

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
(\url{https://github.com/ANTsX}).  A GitHub repository specific to the work
discussed in the manuscript was created and is available at
\url{https://github.com/ntustison/ANTsXMouseBrainMapping}.


\clearpage

# References {-}