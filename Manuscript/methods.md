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

Standard preprocessing
steps in mouse brain imaging include correcting for spatial intensity
inhomogeneities and reducing image noise, both of which can impact registration
accuracy and downstream analysis. ANTsX provides implementations of widely used
methods for these tasks. The N4 bias field correction algorithm
[@Tustison:2010ac], originally developed in ANTs and contributed to ITK,
mitigates artifactual, low-frequency intensity variation and is accessible via
`ants.n4_bias_field_correction(...)`. Patch-based denoising [@Manjon:2010aa] has
been implemented as `ants.denoise_image(...)`.

ANTsX includes a robust and flexible framework for
pairwise and groupwise image registration [@Avants:2014aa]. At its core is the
SyN algorithm [@Avants:2008aa], a symmetric diffeomorphic model with optional
B-spline regularization [@Tustison:2013ac]. In ANTsPy, registration is performed
via `ants.registration(...)` using preconfigured parameter sets (e.g.,
`antsRegistrationSyNQuick[s]`, `antsRegistrationSyN[s]`) suitable for different
imaging modalities and levels of computational demand. Resulting transformations
can be applied to new images with `ants.apply_transforms(...)`.

ANTsX supports population-based template generation
through iterative pairwise registration to an evolving estimate of the mean
shape and intensity reference space across subjects [@Avants:2010aa]. This
functionality was used in generating the DevCCF templates [@Kronman:2024aa]. The
procedure, implemented as `ants.build_template(...)`, produces average images in
both shape and intensity by aligning all inputs to a common evolving template.

To support visual inspection and quality control, ANTsPy
provides flexible image visualization with `ants.plot(...)`. This function
enables multi-slice and multi-orientation rendering with optional overlays and
label maps.

<!----------------------------------------------------------------------->

## Mapping fMOST data to AllenCCFv3

Mapping fMOST data into the AllenCCFv3 presents unique
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

To facilitate reproducible mapping, we
first constructed a contralaterally symmetric average template from 30 fMOST
brains and their mirrored counterparts using ANTsX template-building tools.
Because the AllenCCFv3 and fMOST data differ substantially in both intensity
contrast and morphology, direct deformable registration between individual fMOST
brains and the AllenCCFv3 was insufficiently robust.  Instead, we performed a
one-time expert-guided label-driven registration between the average fMOST
template and AllenCCFv3. This involved sequential alignment of seven manually
selected anatomical regions:  1) brain mask/ventricles, 2) caudate/putamen, 3)
fimbria, 4) posterior choroid plexus, 5) optic chiasm, 6) anterior choroid
plexus, and 7) habenular commissure which were prioritized to enable
coarse-to-fine correction of shape differences. Once established, this
fMOST-template-to-AllenCCFv3 transform was reused for all subsequent specimens.
Each new fMOST brain was then registered to the average fMOST template using
intensity-based registration, followed by concatenation of transforms to produce
the final mapping into AllenCCFv3 space. 

A key advantage of fMOST imaging is its ability
to support single neuron projection reconstruction across the entire brain
[@Peng:2021aa]. Because these reconstructions are stored as 3D point sets
aligned to the original fMOST volume, we applied the same composite transform
used for image alignment to the point data using ANTsX functionality. This
enables seamless integration of cellular morphology data into AllenCCFv3 space,
facilitating comparative analyses across specimens.

<!----------------------------------------------------------------------->

## Mapping MERFISH data to AllenCCFv3

MERFISH data are acquired as a series of 2D tissue sections,
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

To assign region labels to the MERFISH data, we use a cell
type clustering approach previously detailed [@Yao:2023aa]. In short,
manually dissected scRNAseq data was used to establish the distribution of cell
types present in each of the following major regions: cerebellum, CTXsp,
hindbrain, HPF, hypothalamus, isocortex, LSX, midbrain, OLF, PAL, sAMY, STRd,
STRv, thalamus and hindbrain. Clusters in the scRNA-seq dataset were then used
to assign similar clusters of cell types in the MERFISH data to the regions they
are predominantly found in the scRNA-seq data. To account for clusters that were
found at low frequency in regions outside its main region we calculated for each
cell its 50 nearest neighbors in physical space and reassigned each cell to the
region annotation dominating its neighborhood.

A major challenge was compensating
for oblique cutting angles and non-uniform section thickness, which distort the
anatomical shape and spacing of the reconstructed volume. Rather than directly
warping the MERFISH data into atlas space, we globally aligned the AllenCCFv3 to
the MERFISH coordinate system. This was done via an affine transformation
followed by resampling of AllenCCFv3 sections to match the number and
orientation of MERFISH sections. This approach minimizes interpolation artifacts
in the MERFISH data and facilitates one-to-one section matching.

We used a 2.5D approach for fine
alignment of individual sections. In each MERFISH slice, deformable registration
was driven by sequential alignment of anatomical landmarks between the label
maps derived from MERFISH and AllenCCFv3. A total of nine regions, including
isocortical layers 2/3, 5, and 6, the striatum, hippocampus, thalamus, and
medial/lateral habenula, were registered in an empirically determined order.
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

We first coalesced the anatomical
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

Using these point sets, we fit a continuous velocity
field over developmental time using a generalized B-spline scattered data
approximation method [@Tustison:2006aa]. The field was parameterized over a
log-scaled time axis to ensure finer temporal resolution during early embryonic
stages, where morphological changes are most rapid.  Optimization proceeded for
approximately 125 iterations, minimizing the average Euclidean norm between
transformed points at each step. Ten integration points were used to ensure
numerical stability. The result is a smooth, differentiable vector field that
defines a diffeomorphic transform between any two timepoints within the template
range.

This velocity model can be used to estimate
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

## Automated brain extraction and parcellation with ANTsXNet

To support template-based deep learning approaches for structural brain
extraction and parcellation, we implemented dedicated pipelines using the
ANTsXNet framework. ANTsXNet comprises open-source deep learning libraries in
both Python (ANTsPyNet) and R (ANTsRNet) that interface with the broader ANTsX
ecosystem and are built on TensorFlow/Keras. Our mouse brain pipelines mirror
existing ANTsXNet tools for human imaging but are adapted for species-specific
anatomical variation, lower SNR, and heterogeneous acquisition protocols.

### Deep learning training setup

All network-based approaches were implemented using a standard U-net
[@Falk:2019aa] architecture and hyperparameters previously evaluated in ANTsXNet
pipelines for human brain imaging
[@Tustison:2021aa,Tustison:2024aa,Stone:2024aa]. This design follows the
'no-new-net' principle [@Isensee:2021aa], which demonstrates that a
well-configured, conventional U-net can achieve robust and competitive
performance across a wide range of biomedical segmentation tasks with little to
no architectural modifications from the original. Both networks use a 3D U-net
architecture implemented in TensorFlow/Keras, with five
encoding/decoding levels and skip connections. The loss
function combined Dice and categorical cross-entropy terms. Training used a
batch size of 4, Adam optimizer with an initial learning rate of 2e-4, and early
stopping based on validation loss. Training was performed on an NVIDIA DGX
system (4 $\times$ Tesla V100 GPUs, 256 GB RAM). Model weights and preprocessing
routines are shared across ANTsPyNet and ANTsRNet to ensure reproducibility and
language portability. For both published and unpublished trained networks
available through ANTsXNet, all training scripts and data augmentation
generators are publicly available at
**[https://github.com/ntustison/ANTsXNetTraining](https://github.com/ntustison/ANTsXNetTraining)**.

Robust data augmentation was critical to generalization
across scanners, contrast types, and resolutions. We applied both intensity- and
shape-based augmentation strategies:

* Intensity augmentations:

  * Gaussian, Poisson, and salt-and-pepper noise:  
    `ants.add_noise_to_image(...)`
  * Simulated intensity inhomogeneity via bias field modeling [@Tustison:2010ac]:  
    `antspynet.simulate_bias_field(...)`
  * Histogram warping to simulate contrast variation [@Tustison:2021ab]:   
    `antspynet.histogram_warp_image_intensities(...)`

* Shape augmentations:

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

This training strategy provides strong spatial priors despite limited data by
leveraging high-quality template images and aggressive augmentation to mimic
population variability. During the development of this work, the network was
further refined through community engagement. A user from a U.S.-based research
institute applied this publicly available (but then unpublished) brain extraction
tool to their own mouse MRI dataset. Based on feedback and iterative
collaboration with the ANTsX team, the model was retrained and improved to
better generalize to additional imaging contexts. This reflects our broader
commitment to community-driven development and responsiveness to user needs
across diverse mouse brain imaging scenarios.

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
template-based training strategy enables the model to produce accurate,
multi-region parcellations without requiring large-scale annotated subject data.

To normalize intensity across specimens, input images were preprocessed using
rank-based intensity normalization (`ants.rank_intensity(...)`). Spatial
harmonization was achieved through affine and deformable alignment of each
extracted brain to the P56 template prior to inference. In addition to the
normalized image input, the network also receives prior probability maps derived
from the atlas segmentations, providing additional spatial context. 

This general parcellation deep learning framework has also been applied in
collaboration with other groups pursuing related but distinct projects. In one
case, a model variant was adapted for T2-weighted MRI using an alternative
anatomical labeling scheme; in another, a separate model was developed for
serial two-photon tomography (STPT) with a different parcellation set. All three
models are accessible through a shared interface in ANTsXNet:
`antspynet.mouse_brain_parcellation(...)`. Ongoing work is further extending
this approach to embryonic mouse brain data. These independent efforts reflect
broader community interest in adaptable parcellation tools and reinforce the
utility of ANTsXNet as a platform for reproducible, extensible deep learning
workflows.

### Evaluation and reuse

To assess model generalizability, both the brain extraction and parcellation
networks were evaluated on an independent longitudinal dataset comprising
multiple imaging sessions with varied acquisition parameters [@Rahman:2023aa].
Although each label or imaging modality required retraining, the process was
streamlined by the reusable ANTsX infrastructure enabled by rapid adaptation
with minimal overhead. These results illustrate the practical benefits of a
template-based, low-shot strategy and modular deep learning framework. All
trained models, associated training scripts, and supporting resources are openly
available and designed for straightforward integration into ANTsX workflows.
