
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
