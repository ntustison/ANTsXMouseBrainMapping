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

Prior to velocity field optimization, the data was rigidly transformed to a
common space.  Using the centroids for the common label set of each CCFDev
atlas, the ANTsPy ``ants.fit_transform_to_paired_points(...)`` function was used
to warp each atlas to the space of the P56 atlas and then downsampled to $50
\mu$m isotropic resolution.  In order to determine the common point sets across
stages, the multi-metric capabilities of ``ants.registration(...)`` were used.
Instead of performing intensity-based pairwise registration directly on these
multi-label images, each label was used to construct a separate fixed and moving
image pair resulting in a multi-metric registration optimization scenario
involving 24 binary image pairs (each label weighted equally) for optimizing
correspondence between neighboring atlases using the mean squares metric and 
the SyN transform.  

To provide the common point sets across all seven developmental atlases, the
label boundaries and whole regions were sampled in the P56 atlas and then
propagated to each atlas using the transformations derived from the pairwise
registrations.  Based on previous experience as both the developers of users of
these tools, we selected a sampling rate of 10\% for the contour points and 1\%
for the regional points for a total number of points being per atlas being
$173303$ ($N_{contour} = 98151$ and $N_{region}=75152$). Boundary points were
weighted twice as those of regional points for the B-spline data approximation
optimization.  

### Optimization {-}

\begin{figure}[!htb]
\centering
\includegraphics[width=0.99\textwidth]{Figures/convergence.pdf}
\caption{Convergence of the optimization of the velocity field for describing the 
transformation through the developmental stages from E11.5 through P56.}
\label{fig:convergence}
\end{figure}

``fit_time_varying_transform_to_point_sets(...)`` from the ANTsPy package was used 
to optimize the velocity field. Input comprised the seven
corresponding point sets and their associated weight values, the selected number
of integration points for the velocity field ($N=11$), and the parameters
defining the geometry of the spatial dimensions of the velocity field (same as
the downsampled P56 atlas noted above). In addition, the normalized time point
for each atlas/point-set was also defined. Given the increasingly larger gaps in
the postnatal timepoint sampling, we made two adjustments.  Based on known mouse
brain development, we used 28 days for the P56 data.  We then computed the log
transform of the adjusted set of time points prior to normalization between 0
and 1 (see the right side of Figure \ref{fig:convergence}.)  This log transform,
as part of the temporal normalization, significantly improved data spacing. 

The max number of iterations was set to 200.  At each iteration we looped over
the 11 integration points. At each integration point, the velocity field
estimate was updated by warping the two immediately adjacent point sets to the
integration time point and determining the regularized displacement field
between the two warped point sets.  As with any gradient-based descent
algorithm, this field was multiplied by a small step size ($\delta = 0.2$)
before adding to the current velocity field.  Using multithreading, each
iteration took about six minutes.

\begin{figure}[!htb]
\centering
\includegraphics[width=0.75\textwidth]{Figures/warpedP56Volumes.pdf}
\caption{After the velocity field is generated, we can use it to warp
the simplified labels of the P56 atlas continuously over the interval
$[0, 1]$ and plot the volumes of the atlas regions.  Note how they 
compare with the volumes of the same regions in the other atlases.}
\label{fig:warpedP56}
\end{figure}

Convergence is determined by the average displacement error over each of the
integration points. As can be seen in the left panel of Figure
\ref{fig:convergence}, convergence occurred around 125 iterations when the
average displacement error is minimized. The median displacement error at each
of the integration points also trends towards zero but at different rates.
After optimization, we use the velocity field to warp the P56 set of labels
to each of the other atlas time points to compare the volumes of the different
simplified annotated regions.  This is shown in Figure \ref{fig:warpedP56}.

### The DevCCF transform model {-}

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

Once optimized, the resulting velocity field can be used to generate the deformable 
transform between any two continuous points within the time interval bounded by 
E11.5 and P56.  So, for example, one can transform each atlas to the space of every
other atlas.  This is illustrated in Figure \ref{fig:crosswarp} where we render a 
mid-sagittal location for each atlas and the results of warping every atlas to 
that space.  

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

One potential application for this particular transformation model is
facilitating the construction of pseudo-templates in the temporal gaps of the
DevCCF.  This is illustrated in Figure \ref{fig:pseudo} where we used the
optimized velocity field to construct pseudo-templates at time point P10.3 and
P20---arbitrarily chosen simply to demonstrate the concept.  After situating
these time points within the normalized time point interval, the existing
adjacent DevCCF atlases on either side can be warped to the desired time point.
A subsequent call to one of the ANTsX template building functions then permits
the construction of the template at that time point.  

