
\clearpage
\newpage

# Methods  

The following methods are all available as part of the ANTsX ecosystem
with analogous elements existing in both ANTsR (ANTs in R) and ANTsPy
(ANTs in Python) with an ANTs/ITK C++ core.  However, most of the 
development for the work described below was performed using ANTsPy.
For equivalent calls in ANTsR, please see the ANTsX tutorial at
\url{https://tinyurl.com/antsxtutorial}.

## General ANTsX utilities

### Preprocessing: bias field correction and denoising 

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

### Image registration 

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
type (e.g., light sheet fluorescence microscopy, Nissl staining, and the various
MRI modalities) and are adaptable to mouse image geometry and scaling.  Further
details can be found in the various documentation sources for these ANTsX
packages.

### Template generation 

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

### Visualization 

To complement the well-known visualization capabilities of R and Python, e.g.,
ggplot2 and matplotlib, respectively, image-specific visualization capabilities
are available in the ``ants.plot(...)`` function (Python).
These are capable of illustrating multiple slices in different orientations with
other image overlays and label images.  

## Mapping fMOST data to AllenCCFv3

### Preprocessing

* _Downsampling_.  The first challenge when mapping fMOST images into the
AllenCCFv3 is addressing the resolution scale of the data. Native fMOST data
from an individual specimen can range in the order of terabytes, which leads to
two main problems. First, volumetric registration methods (particularly those
estimating local deformation) have high computational complexity and typically
cannot operate on such high-resolution data under reasonable memory and runtime
constraints. Second, the resolution of the AllenCCFv3 atlas is much lower than
the fMOST data, thus the mapping process will cause much of the high-resolution
information in the fMOST images to be lost regardless. Thus, we perform a cubic
B-spline downsampling of the fMOST data to reduce the resolution of each image
to match the isotropic 25 $\mu m$ voxel resolution of the AllenCCFv3 intensity atlas
using ``ants.resample_image(...)``.  An
important detail to note is that while the fMOST images and atlas are
downsampled, the mapping learned during the registration is assumed to be
continuous. Thus, after establishing the mapping to the AllenCCFv3, we can
interpolate the learned mapping and apply it directly to the high-resolution native data
directly to transform any spatially aligned data (such as the single-cell neuron
reconstructions) into the AllenCCFv3. 

* _Stripe artifact removal_. Repetitive pattern artifacts are a common challenge
in fMOST imaging where inhomogeneity during the cutting and imaging of different
sections can leave stripes of hyper- and hypo-intensity across the image. These
stripe artifacts can be latched onto by the registration algorithm as unintended
features that are then misregistered to non-analogous structures in the
AllenCCFv3. We address these artifacts by fitting a 3D bandstop (notch) filter
to target the frequency of the stripe patterns and removing them prior to the
image registration.

* _Inhomogeneity correction_. Regional intensity inhomogeneity can also occur
within and between sections in fMOST imaging due to staining or lighting
irregularity during acquisition. Similar to stripe artifacts, intensity
gradients due to inhomogeneity can be misconstrued as features during the
mapping and result in matching of non-corresponding structures. Our pipeline
addresses these intensity inhomogeneities using N4 bias field correction
[@Tustison:2010ac], ``ants.n4_bias_field_correction(...)``.

### Steps for spatial normalization to AllenCCFv3

1. _Average fMOST atlas as an intermediate target_.  Due to the preparation of
  the mouse brain for fMOST imaging, the resulting structure in the mouse brain
  has several large morphological deviations from the AllenCCFv3 atlas. Most
  notable of these is an enlargement of the ventricles, and compression of
  cortical structures. In addition, there is poor intensity correspondence for
  the same anatomic features due to intensity dissimilarity between imaging
  modalities. We have found that standard intensity-base registration is
  insufficient to capture the significant deformations required to map these
  structures correctly into the AllenCCFv3. We address this challenge in ANTsX
  by using explicitly corresponding parcellations of the brain, ventricles and
  surrounding structures to directly recover these large morphological differences.
  However, generating these parcellations for each individual mouse brain is a
  labor-intensive task. Our solution is to create an average atlas whose mapping
  to AllenCCFv3
  encapsulates these large morphological differences to serve as an intermediate
  registration point. This has the advantage of only needing to generate one set
  of corresponding annotations which is used to register between the two atlas
  spaces. New images are first aligned to the fMOST average atlas, which shares
  common intensity and morphological features and thus can be achieved through
  standard intensity-based registration.

2. _Average fMOST atlas construction_. An intensity and shape-based
  contralaterally symmetric average of the fMOST image data is constructed from
  30 images and their contralateral flipped versions. We ran three iterations of the
  atlas construction using the default settings. Additional iterations (up to
  six) were evaluated and showed minimal changes to the final atlas
  construction, suggesting a convergence of the algorithm.

3. _fMOST atlas to AllenCCFv3 alignment_. Alignment between the fMOST average
  atlas and AllenCCFv3 was performed using a one-time annotation-driven
  approach. Label-to-label registration is used to align 7 corresponding
  annotations in both atlases in the following: 1) brain mask/ventricles, 2)
  caudate/putamen, 3) fimbria, 4) posterior choroid plexus, 5) optic chiasm, 6)
  anterior choroid plexus, and 7) habenular commissure. The alignments were
  performed sequentially, with the largest, most relevant structures being
  aligned first using coarse registration parameters, followed by other
  structures using finer parameters. This coarse-to-fine approach allows us to
  address large morphological differences (such as brain shape and ventricle
  expansion) at the start of registration and then progressively refine the
  mapping using the smaller structures. The overall ordering of these structures
  was determined manually by an expert anatomist, where anatomical
  misregistration after each step of the registration was evaluated and used to
  determine which structure should be used in the subsequent iteration to best
  improve the alignment. The transformation from this one-time expert-guided alignment is
  preserved and used as the canonical fMOST atlas to AllenCCFv3 mapping in the
  pipeline.

4. _Alignment of individual fMOST mouse brains_.  The canonical transformation
  between the fMOST atlas and AllenCCFv3 greatly simplifies the registration of
  new individual fMOST mouse brains into the AllenCCFv3. Each new image is first
  registered into the fMOST average atlas, which shares intensity, modality, and
  morphological characteristics. This allows us to leverage standard,
  intensity-based registration functionality [@Avants:2014aa] available in ANTsX
  to perform this alignment. Transformations are then concatenated to the
  original fMOST image to move it into the AllenCCFv3 space using
  ``ants.apply_transforms(...)``. 

5. _Transformation of single cell neurons_. A key feature of fMOST imaging is
  the ability to reconstruct and examine whole-brain single neuron
  projections[@Peng:2021aa]. Spatial mapping of these neurons from individual
  brains into the AllenCCFv3 allows investigators to study different neuron
  types within the same space and characterize their morphology with respect to
  their transcriptomics. Mappings found between the fMOST image and the
  AllenCCFv3 using our pipeline can be applied in this way to fMOST neuron
  reconstruction data. 

## Mapping MERFISH data to AllenCCFv3

### Preprocessing

* _Initial volume reconstruction_. Alignment of MERFISH data into a 3D atlas space
  requires an estimation of anatomical structure within the data. For each
  section, this anatomic reference image was created by aggregating the number
  of detected genetic markers (across all probes) within each pixel of a $10 
  \times 10 \mu m^2$ grid to match the resolution of the $10 \mu m$ AllenCCFv3
  atlas. These reference image sections are then coarsely reoriented and aligned
  across sections using manual annotations of the most dorsal and ventral points
  of the midline. The procedure produces an anatomic image stack that serves as
  an initialization for further global mappings into the AllenCCFv3.

* _Anatomical correspondence labeling_. Mapping the MERFISH data into the
  AllenCCFv3 requires us to establish correspondence between the anatomy
  depicted in the MERFISH and AllenCCFv3 data. Intensity-based features in
  MERFISH data are not sufficiently apparent to establish this correspondence,
  so we need to generate instead corresponding anatomical labelings of both
  images with which to drive registration. These labels are already available as
  part of the AllenCCFv3; thus, the main challenge is deriving analogous labels
  from the spatial transcriptomic maps of the MERFISH data. Toward this end, we
  assigned each cell from the scRNA-seq dataset to one of the following major
  regions: cerebellum, CTXsp, hindbrain, HPF, hypothalamus, isocortex, LSX,
  midbrain, OLF, PAL, sAMY, STRd, STRv, thalamus and hindbrain. A label map of
  each section was generated for each region by aggregating the cells assigned
  to that region within a $10 \times 10 \mu m^2$ grid. The same approach was
  used to generate more fine grained region specific landmarks (i.e., cortical
  layers, habenula, IC). Unlike the broad labels which cover large swaths of the
  section these regions are highly specific to certain parts of the section.
  Once cells in the MERFISH data are labeled, morphological dilation is used to
  provide full regional labels for alignment into the AllenCCFv3. 

* _Section matching_.  Since the MERFISH data is acquired as sections, its 3D
  orientation may not be fully accounted for during the volume reconstruction
  step, due to the particular cutting angle. This can lead to obliqueness
  artifacts in the section where certain structures can appear to be larger or
  smaller, or missing outright from the section. To address this, we first use a
  global alignment to match the orientations of the MERFISH sections to the
  atlas space. In our pipeline, this section matching is performed in the
  reverse direction by performing a global affine transformation of the
  AllenCCFv3 into the MERFISH data space, and then resampling digital sections
  from the AllenCCFv3 to match each MERFISH section. This approach limits the
  overall transformation and thus resampling that is applied to the MERFISH
  data, and, since the AllenCCFv3 is densely sampled, it also reduces in-plane
  artifacts that result from missing sections or undefined spacing in the
  MERFISH data. 

### 2.5D deformable, landmark-driven alignment to AllenCCFv3

After global alignment of the AllenCCFv3 into the MERFISH dataset, 2D per-section
deformable refinements are used to address local differences between the MERFISH
sections and the resampled AllenCCFv3 sections. Nine registrations were performed in
sequence using a single label at each iteration in the following order: 1) brain
mask, 2) isocortex (layer 2+3), 3) isocortex (layer 5), 4) isocortex (layer 6),
5) striatum, 6) medial habenula, 7) lateral habenula, 8) thalamus, and 9) hippocampus.
This ordering was determined empirically by an expert anatomist who prioritized
which structure to use in each iteration by evaluating the anatomical alignment
from the previous iteration. Global and local mappings are then all concatenated
(with appropriate inversions) to create the final mapping between the MERFISH
data and AllenCCFv3. This mapping is then used to provide a point-to-point
correspondence between the original MERFISH coordinate space and the AllenCCFv3
space, thus allowing mapping of individual genes and cell types located in the
MERFISH data to be directly mapped into the AllenCCFv3.

## DevCCF velocity flow transformation model 

Given multiple, linearly or non-linearly ordered point sets where individual
points across the sets are in one-to-one correspondence, we developed an approach for
generating a velocity flow transformation model to describe a time-varying
diffeomorphic mapping as a variant of the landmark matching solution.
Integration of the resulting velocity field can then be used to describe the
displacement between any two time points within this time-parameterized domain.
Regularization of the sparse correspondence between point sets is performed
using a generalized B-spline scattered data approximation technique
[@Tustison:2006aa], also created by the ANTsX developers and contributed to
ITK. 

### Velocity field optimization

To apply this methodology to the developmental templates [@Kronman:2023aa], we
coalesced the manual annotations of the developmental templates into 26 common
anatomical regions (see Figure \ref{fig:simplifiedannotations}).  We then used
these regions to generate invertible transformations between successive time
points. Specifically each label was used to create a pair of single region
images resulting in 26 pairs of "source" and "target" images.  The multiple
image pairs were simultaneously used to iteratively estimate a diffeomorphic
pairwise transform. Given the seven atlases E11.5, E13.5, E15.5, E18.5, P4, P14,
and P56, this resulted in 6 sets of transforms between successive time points.
Approximately 10$^6$ points were randomly sampled labelwise in the P56
template space and propagated to each successive atlas providing the point sets
for constructing the velocity flow model. Approximately 125 iterations resulted
in a steady convergence based on the average Euclidean norm between transformed
point sets.  Ten integration points were used and point sets were distributed
along the temporal dimension using a log transform for a more evenly spaced
sampling.  For additional information see the help menu for the ANTsPy function
``ants.fit_time_varying_transform_to_point_sets(...)``.

## ANTsXNet mouse brain applications 

### General notes regarding deep learning training

All network-based approaches described below were implemented and organized in
the ANTsXNet libraries comprising Python (ANTsPyNet) and R (ANTsRNet) analogs
using the Keras/Tensorflow libraries available as open-source in ANTsX GitHub
repositories. For the various applications, both share the identically trained
weights for mutual reproducibility.  For all GPU training, we used Python
scripts for creating custom batch generators which we maintain in a separate
GitHub repository for public availability
(\url{https://github.com/ntustison/ANTsXNetTraining}). These scripts provide
details such as batch size, choice of loss function, and network parameters. In
terms of GPU hardware, all training was done on a DGX (GPUs: 4X Tesla V100,
system memory: 256 GB LRDIMM DDR4).  

Data augmentation is crucial for generalizability and accuracy of the trained
networks.  Intensity-based data augmentation consisted of randomly added noise
(i.e., Gaussian, shot, salt-and-pepper), simulated bias fields based on N4 bias
field modeling, and histogram warping for mimicking well-known MRI intensity
nonlinearities [@Nyul:2000aa;@Tustison:2021aa]. These augmentation techniques
are available in ANTsXNet (only ANTsPyNet versions are listed with ANTsRNet
versions available) and include:

* image noise:  ``ants.add_noise_to_image(...)``,

* simulated bias field: ``antspynet.simulate_bias_field(...)``, and

* nonlinear intensity warping: ``antspynet.histogram_warp_image_intensities(...)``.

Shape-based data augmentation used both random linear and nonlinear
deformations in addition to anisotropic resampling in the three canonical 
orientations to mimic frequently used acquisition protocols for mice brains:

* random spatial warping: ``antspynet.randomly_transform_image_data(...)`` and

* anisotropic resampling: ``ants.resample_image(...)``.

### Brain extraction

Similar to human neuroimage processing, brain extraction is a crucial
preprocessing step for accurate brain mapping.  We developed similar
functionality for T2-weighted mouse brains.  This network uses a conventional
U-net architecture [@Falk:2019aa] and, in ANTsPyNet, this functionality is
available in the program ``antspynet.mouse_brain_extraction(...)``.  
For the two-shot T2-weighted brain extraction network, two brain templates were
generated along with their masks.  One of the templates was generated from
orthogonal multi-plane, high resolution data [@Reshetnikov2021] which were 
combined to synthesize isotropic volumetric data using the B-spline fitting algorithm
[@Tustison:2006aa].  This algorithm is encapsulated in
``ants.fit_bspline_object_to_scattered_data(...)`` where the input is the set of
voxel intensity values and associated physical location.  Since each point can
be assigned a confidence weight, we use the normalized gradient value to
more heavily weight edge regions.  Although both template/mask pairs
are available in the GitHub repository associated with this work, the synthesized
volumetric B-spline T2-weighted pair is available within ANTsXNet through the
calls:

* template: ``antspynet.get_antsxnet_data("bsplineT2MouseTemplate")`` and

* mask: ``antspynet.get_antsxnet_data("bsplineT2MouseTemplateBrainMask")``.

### Brain parcellation

The T2-weighted brain parcellation network is also based on a 3-D U-net
architecture and the T2-w DevCCF P56 template component with 
extensive data augmentation, as described previously.  Intensity
differences between the template and any brain extracted input image
are minimized through the use of the rank intensity transform 
(``ants.rank_intensity(...)``).  Shape differences are reduced 
by the additional preprocessing step of warping the brain extracted
input image to the template.  Additional input channels include the 
prior probability images created from the template parcellation.
These images are also available through the ANTsXNet 
``get_antsxnet_data(...)`` interface.

<!-- 
* template: ``antspynet.get_antsxnet_data("DevCCF_P56_MRI-T2_50um")`` and

* parcellation: ``antspynet.get_antsxnet_data(``"DevCCF_P56_MRI-T2_50um_BrainParcellationNickMask")``. 
-->

<!-- 
_Miscellaneous networks:  Super-resolution, cerebellum, and hemispherical masking._

To further enhance the data prior to designing mapping protocols, additional
networks were created.  A well-performing deep back projection network
[@Haris:2018aa] was ported to ANTsXNet and expanded to 3-D for various
super-resolution applications [@Avants:2023aa], including mouse data.  Finally,
features of anatomical significance, namely the cerebellum and hemispherical
midline were captured in these data using deep learning networks.   
-->

<!-- ## Intra-slice image registration with missing slice imputation 

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
additional steps.  -->

