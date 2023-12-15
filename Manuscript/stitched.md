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

{\bf The ANTsX Ecosystem for Spatiotemporal Mapping of the Mouse Brain}

\vspace{1.0 cm}

\normalsize

Nicholas J. Tustison$^{1}$,
Min Chen$^{2}$,
Fae N. Kronman$^{3}$,
Jeffrey T. Duda$^{2}$,
Clare Gamlin$^{4}$,
Lydia Ng$^{4}$,
Yongsoo Kim$^{3}$, and
James C. Gee$^{2}$

\small

$^{1}$Department of Radiology and Medical Imaging, University of Virginia, Charlottesville, VA \\
$^{2}$Department of Radiology, University of Pennsylvania, Philadelphia, PA \\
$^{3}$Department of Neural and Behavioral Sciences, Penn State University, Hershey, PA \\
$^{4}$Allen Institute for Brain Science, Seattle, WA \\

\vspace{1.5 cm}

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
Coordinate Framework version 3 (CCFv3), and the ability to map to such reference
atlases.   The Advanced Normalization Tools Ecosystem (ANTsX) is a comprehensive
open-source software image analysis toolkit with applicability to multiple organ
systems, modalities, and animal species.  Herein, we illustrate the utility of
ANTsX for generating precision spatial mappings of the mouse brain of different
developmental ages including the prerequisite preprocessing steps. Additionally,
as a further illustration of ANTsX capabilities, we use these publicly available 
mouse brain atlases to generate a velocity flow-based mapping encompassing the 
entire developmental trajectory, which we also make available to the public. 

\clearpage# Introduction {-}

Over the past two decades there has been a notable increase in significant
advancements in mesoscopic analysis of the mouse brain. It is now possible to
track single cell neurons in 3-D across full mouse brains [@Keller:2015aa],
observe whole brain developmental changes on a cellular level
[@La-Manno:2021aa], associate brain regions and tissues with their genetic
composition [@Wen:2022aa], and locally characterize neural connectivity
[@Oh:2014aa]. Much of this scientific achievement has been made possible due to
breakthroughs in high resolution imaging techniques that permit submicron, 3-D
imaging of whole mouse brains. Associated research techniques such as
micro-optical sectioning tomography [@Gong:2013aa,@Li:2010aa], tissue clearing
[@Keller:2015aa;@Ueda:2020aa], spatial transcriptomics
[@Stahl:2016aa,@Burgess:2019aa] are all well-utilized in the course of
scientific investigations of mesoscale relationships in the mouse brain. 

An important component of these research programs is the ability to map the
various image data to anatomical reference frames
[@MacKenzie-Graham:2004aa,@Mackenzie-Graham:2007aa] for inferring spatial
relationships between structures, cells, and genetics in the brain. This has
motivated the development of detailed structural image atlases of the mouse
brain.  Notable examples include the Allen Brain Atlas and Coordinate Frameworks
[@Dong:2008aa,@Wang:2020aa] and the Waxholm Space [@Johnson:2010aa]. Despite the
significance of these contributions, challenges still exist in large part due
to the wide heterogeneity in associated study-specific image data. Variance in
the acquisition methods can introduce artifacts such as tissue distortion,
holes, bubbles, folding, tears, and missing slices. These severely complicate
assumed correspondence for registration.

To address such challenges, several software packages have been developed over
the years comprising solutions of varying comprehensibility, sophistication, and
availability.  An early contribution to the community was the Rapid Automatic
Tissue Segmentation (RATS) package [@Oguz:2014aa] for brain extraction
(available upon request).  Of the publicly available packages, most, if not all
rely on well-established package dependencies originally developed on human
brain data. Another early tool was SPMMouse [@Sawiak:2014aa] based on the
well-known Statistical Parametric Mapping (SPM) software package
[@Ashburner:2012aa]. The automated mouse atlas propagation (aMAP) tool is
largely a front-end for the NiftyReg image registration package [@Modat:2010aa]
applied to mouse data which is currently available as a Python module
[@Tyson:2022aa]. NiftyReg is also used by the Atlas-based Imaging Data Analysis
(AIDA) MRI pipeline [@Pallast:2019aa] as well as the Multi Atlas Segmentation
and Morphometric Analysis Toolkit (MASMAT). Whereas the former also incorporates
the FMRIB Software Library (FSL) [@Jenkinson:2012wi] for brain extraction and
DSIStudio [@Yeh:2010aa] for DTI processing, the latter uses NiftySeg and
multi-consensus labeling tools [@Jorge-Cardoso:2013aa] for brain extraction and
parcellation. In addition, MASMAT incorporates N4 bias field correction
[@Tustison:2010ac] from the Advanced Normalization Tools Ecosystem (ANTsX)
[@Tustison:2021aa] as do the packages Multi-modal Image Registration And
Connectivity anaLysis (MIRACL) [@Goubran:2019aa], Sammba-MRI
[@Celestine:2020aa], and Small Animal Magnetic Resonance Imaging (SAMRI)
[@Ioanas:2021aa].  However, whereas Saamba-MRI uses AFNI [@Cox:2012aa] for image
registration; MIRACL, SAMRI, and BrainsMapi [@Ni:2020aa] all use ANTsX tools for
computing image-based correspondences. Other packages use landmark-based
approaches to image registration including SMART [@Jin:2022aa]---an R package
for semi-automated landmark-based registration and segmentation of mouse brain
based on WholeBrain [@Furth:2018aa].  FriendlyClearMap [@Negwer:2022aa] uses the
landmark-based registration functionality of Elastix [@Klein:2010aa]. Finally,
the widespread adoption of deep learning techniques has also influenced
development in mouse brain imaging methodologies.  For example, if tissue
deformations are not considered problematic for a particular dataset, DeepSlice
can be used to determine affine mappings [@Carey:2023aa] with the optimal
computational efficiency associated with neural networks.

### The ANTsX Ecosystem  {-}

As noted above, many of the existing approaches for processing of mouse brain
image data use ANTsX tools for core steps in various workflows, particularly its
pairwise, intensity-based image registration tools and bias field correction.
Historically, ANTsX development is originally based on fundamental approaches to
image mapping [@Bajcsy:1982aa;@Bajcsy:1989aa;@Gee:2003aa], particularly in the
human brain, which has resulted in core contributions to the field such as the
well-known and highly-vetted Symmetric Normalization (SyN) algorithm
[@Avants:2008aa].  Since its development, various independent platforms have
been used to evaluate ANTsX image registration capabilities in the context of
different application foci which include multi-site brain MRI data
[@Klein:2009aa], pulmonary CT data [@Murphy:2011aa], and most recently
multi-modal brain registration in the presence of tumors [@Baheti:2021aa]. 

\input{antsx_functionality_table}

Apart from its registration capabilities, ANTsX is a comprehensive biological
and medical image analysis toolkit, that comprises additional functionality such
as template generation, general data approximation, and deep learning networks
specifically trained for mouse data (see Table \ref{table:methods}). The
collective use of the toolkit has demonstrated superb performance in multiple
application areas (e.g., consensus labeling [@Wang:2013ab], brain tumor
segmentation [@Tustison:2014aa], and cardiac motion estimation
[@Tustison:2015ab]).  Importantly, ANTs is built on the Insight Toolkit (ITK)
[@McCormick:2014aa] deriving benefit from a very capable open-source community
of scientists and programmers as well as providing a visible, open-source venue
for algorithmic contributions.

\begin{figure}[!htb]
\centering
\makebox[\textwidth][c]{\includegraphics[width=1.3\textwidth]{Figures/pipeline3.png}}%
\caption{Illustration of a mouse brain template generation workflow and 
related template-based applications demonstrating the utility of different 
ANTsX tools.  After imaging acquisition of the study population, various 
preprocessing steps are applied to the imaging data such as bias correction,
denoising, and brain extraction as dictated by the needs of the study 
protocol.  Not shown is the possibility of template symmetrization by 
contralaterally flipping the image data associated with each specimen.  
In the case of the DevCCF, applications include gene expression mapping 
and the associated velocity flow model for pseudo-template generation.}
\label{fig:pipeline}
\end{figure}

Recently, the developmental common coordinate framework (DevCCF) was introduced
to the mouse brain research community as a public resource [@Kronman:2023aa].
These symmetric atlases, comprising both multimodal image data and anatomical
segmentations defined by developmental ontology, span the mouse embryonic days
(E) 11.5, E13.5, E15.5, E18.5 and postnatal day (P) 4, P14, and P56.  Modalities
include at least four MRI contrasts and light sheet flourescence miscroscopy
(LSFM) per developmental stage.  Gene expression and other cell type data were
mapped to the corresponding developmental time point to guide the associated
anatomical parcellations.  To further demonstrate the practical utility of the
DevCCF, the P56 template was integrated with the Allen CCFv3 for mapping spatial
transcriptome cell-type data.  These processes, specifically template generation
and multi-modal image mapping, were performed using ANTsX functionality in the
presence of previously noted image mapping difficulties (e.g., missing slices,
tissue distortion) illustrated in Figure \ref{fig:pipeline}.

Given the temporal gaps in the discrete set of developmental atlases, we augment
the template generation explanation previously given [@Kronman:2023aa] from a
developer's perspective.  We hope that this will provide additional information
for the interested reader for potential future template generation.
Related, we also provide a complementary strategy for inferring correspondence
and mapping information within the temporally continuous domain spanned and
sampled by the existing set of embryonic and postnatal atlas brains of the
DevCCF.  Recently developed ANTsX functionality include the generation of a
diffeomorphic velocity flow transformation model [@Joshi:2000aa] spanning
developmental stages where mappings between any two continuous time points
within the span bounded by the E11.5 and P56 atlases is determined by
integration of the generated time-varying velocity field [@Christensen:1996aa].
Such transformations permit the possibility of "pseudo" templates generated
between available developmental stages.  



\clearpage
\newpage

# Results {-}

## Template building {-}

Template building using ANTsX tools was first described in [@Avants:2010aa].
Subsequently, multi-modal and symmetrical variants were more explicitly 
described as part of the brain tumor segmentation approach [@Tustison:2015vl].

<!--
Each symmetric template is an intensity and morphological average of multiple
male and female samples with a sample size ranging from 6 to 14 (Extended Data
Table 1). After stitching, images were preprocessed for template construction.
MRI data preprocessing involved (1) digital postnatal brain extraction and (2)
sample orientation correction. LSFM data preprocessing involved (1) image
resampling to 3 sizes: 50 μm, 20 μm, and 10 μm isotropic voxel resolution, and
(2) sample orientation correction to ensure all images were facing the same
direction. To ensure template symmetry, each preprocessed image was duplicated
and reflected across the sagittal midline, doubling the number of input datasets
used in the template construction pipeline. Template construction, using
functionality contained in ANTs34,74, was employed on Penn State’s
High-Performance Computing system (HPC). Briefly, starting from an initial
template estimate derived as the average image of the input cohort, this
function iteratively performed three steps: (1) non-linearly registered each
input image to the current estimate of the template, (2) voxel-wise averaged the
warped images, and (3) applied the average transform to the resulting image from
step 2 to update the morphology of the current estimate of the template.
Iterations continued until the template shape and intensity values stabilized.
MRI templates were constructed at their imaged resolution using ADC MRI
contrasts for initial postnatal templates and diffusion weighted imaging (DWI)
contrasts for embryonic templates. Once the initial MRI template was
constructed, the sample to template warp fields were applied to all MRI
contrasts for each sample. Warped samples were averaged to construct templates
for each contrast. LSFM templates were constructed from autofluorescence data
collected from C57bl/6J mice and transgenic mice with a C57bl/6J background. To
save memory and improve speed, LSFM templates were initially constructed at 50
μm isotropic resolution. This template was resampled for template construction
initialization at 20 μm isotropic resolution, a process repeated to construct
the final LSFM template with 10 μm isotropic resolution input images.
-->

## The DevCCF Velocity Flow Model {-}

To continuously link the DevCCF atlases, a velocity flow model was constructed
using Dev-CCF derived data and ANTsX functionality available in both ANTsR
and ANTsPy.  Although many implementations optimize variations of this transformtion 
model (and others) using various image intensity similarity metrics, we opted to 
to implement a separate determination of iterative correspondence and transformation 
optimization.  This decision was based on existing ANTsX functionality and wanting 
complementary utility for the toolkit.

ANTsX, being built on top of ITK, uses an ITK image data structure for the 4-D
velocity field where each voxel contains the $x$, $y$, $z$ components of the
field at that point. Field regularization is provided by a novel B-spline
scattered data approximation technique [@Tustison:2006aa] which permits
individual point-based weighting.  Both field regularization and integration of
the velocity field are built on ITK functions written by ANTsX developers.  

The optimized velocity field described here is of size $[256, 182, 360]$
(or $50 \mu$m isotropic) $\times 11$ integration points for a total compressed
size of a little over 2 GB.  This choice represented weighing the trade-off 
between tractability, portability, and accuracy.  However,  all
data and code to reproduce the results described are available in a dedicated 
GitHub repository (\url{https://github.com/ntustison/DevCCF-Velocity-Flow}).

### Data preparation {-}

\begin{figure}[!htb]
\centering
\includegraphics[width=0.75\textwidth]{Figures/SimplifiedAnnotations.pdf}
\caption{Annotated regions representing common labels across developmental stages which
are illustrated for both P4 and P14.}
\label{fig:simplifiedannotations}
\end{figure}

Labeled annotations are available as part of the original DevCCF and reside
in the space of each developmental template which range in resolution from 
$31.5-50 \mu$m.  Across all atlases, the total number of labels exceeded 
2500 without taken into account per hemispherical enumeration.  From this 
set of labels, there were a common set of 24 labels (12 per hemisphere) across 
all atlases that were used for optimization and evaluation.  These regions are 
illustrated for the P4 and P14 stages in Figure \ref{fig:simplifiedannotations}.

Prior to velocity field optimization, the data was rigidly transformed
to a common space.  Using the centroids for the common label set of each CCFDev
atlas, the ANTsPy ``ants.fit_transform_to_paired_points(...)`` function was used to
warp each atlas to the space of the P56 atlas and then downsampled to $50 \mu$m
isotropic resolution.  In order to determine the common point sets across
stages, ``ants.registration(...)`` and its multi-metric capabilities were used.
Instead of performing intensity-based registration directly on these multi-label
images, each label was used to construct a separate fixed and moving image pair
resulting in a multi-metric registration optimization scenario involving 24
image pairs (each label weighted equally) for optimizing correspondence between 
neighboring atlases.

### Optimization {-}

\begin{figure}[!htb]
\centering
\includegraphics[width=0.99\textwidth]{Figures/convergence.pdf}
\caption{Convergence of the optimization of the velocity field for describing the 
transformation through the developmental stages from E11.5 through P56.}
\label{fig:convergence}
\end{figure}

### Applications {-}

\begin{figure}[!htb]
\centering
\includegraphics[width=0.99\textwidth]{Figures/warpedP56Volumes.pdf}
\caption{Warped P56.}
\label{fig:warpedP56}
\end{figure}

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

\begin{figure}[!htb]
\centering
\includegraphics[width=0.99\textwidth]{Figures/pseudo_template.pdf}
\caption{Illustration of the use of the velocity flow model for creating pseudo-templates
at continuous time points not represented in one of the existing developmental stages.
For example, FA templates at time point P10.3 and P20 can be generated by warping the 
existing temporally adjacent developmental templates to the target time point and using 
those images in the ANTsX template building process.}
\label{fig:pseudo}
\end{figure}



\clearpage
\newpage

# Methods {-} 

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
[@Manjon:2010aa] and is also available as a image filter to the ITK community.

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
``simulate_bias_field(...)``, image noise: ``add_noise_to_image(...)``, and MRI
intensity nonlinear characterization: ``histogram_warp_image_intensities(...)``.
Shape-based data augmentation used both random linear and nonlinear
deformations.  This functionality is also instantiated within ANTsXNet in terms
of random spatial warping: ``randomly_transform_image_data(...)``.

For all GPU training, we used Python scripts for creating custom batch
generators. As such batch generators tend to be application-specific, we store
them in a separate GitHub repository for public availability
(https://github.com/ntustison/ANTsXNetTraining). In terms of GPU hardware, all
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
``brain_extraction(...)``.  Even when physical brain extraction is
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

## Image registration {-}

## Intra-slice image registration with missing slice imputation {-}

Volumetric gene expression slice data was collated into 3-D volumes using ...
(ask Jeff). Prior to mapping this volume to the corresponding structural data
and, potentially, to the appropriate template, alignment was improved using
deformable registration on contiguous slices.  However, one of the complications
associated with these image data was the unknown number of missing slices, the
number of consecutive missing slices, and the different locations of these
missing slices.  To handle this missing data problem, we found that data
interpolation using the B-spline approximation algorithm cited earlier
[@Tustison:2006aa] (ANTsPy function:
``fit_bspline_object_to_scattered_data(...)``).  This provided sufficient data
interpolation fidelity to perform continuous slicewise registration.  Other
possible variants that were considered but deemed unnecessary was performing
more than one iteration cycling through data interpolation and slicewise
alignment.  The other possibility was incorporating the super-resolution
technique described earlier.  But again, our data did not require these
additional steps. 

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
yielding a mean image of the population in terms of both the intensity and 
shape.  

## Continuous developmental velocity flow transformation model {-}

Given multiple, linearly or non-linearly ordered point sets where individual
points across are in one-to-one correspondence, we developed an approach for
generating a velocity flow transformation model to describe a time-varying
diffeomorphic mapping as a variant of the inexact landmark matching solution of
Joshi and Miller [@Joshi:2000aa].  Integration of the resulting velocity field
can then be used to describe the displacement between any two time points within
this time-parameterized domain.  Regularization of the sparse correspondence
between point sets is performed using a generalized B-spline scattered data
approximation technique [@Tustison:2006aa], also developed by the ANTsX
developers and contributed to ITK. 

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
constructing the velocity flow model.  Approximately 200 iterations resulted in
a steady convergence based on the average Euclidean norm between transformed
point sets.  Ten integration points were used and point sets were distributed
along the temporal dimension using a log transform for a more evenly spaced
sampling.  Further details including links to data and scripts to reproduce our
reported results is found in the associated GitHub repository [^1]. 

[^1]: https://github.com/ntustison/MouseBrainVelocityFlow/

One potential application is the possible construction of "pseudo"-templates
at currently non-existing developmental stages.

## Visualization {-}

To complement the well-known visualization capabilities of R and Python, e.g.,
ggplot2 and matplotlib, respectively, image-specific visualization capabilities
are available in the ``ants.plot(...)`` (Python) and ``plot.antsImage(...)`` (R).
These are capable of illustrating multiple slices in different orientations with
both other image overlays as well as label images.  

\clearpage

# References {-}