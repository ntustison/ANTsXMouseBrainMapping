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
\centering
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

