
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
