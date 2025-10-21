
## Continuously mapping the DevCCF developmental trajectory

<!-- \begin{figure}
\centering
\includegraphics[width=0.99\textwidth]{Figures/lowerLeftPanel.pdf} 
\caption{}
\label{fig:devccfvelocity}
\end{figure}  -->

The DevCCF is an openly accessible resource for the mouse brain research
community [@Kronman:2024aa], comprising symmetric, multi-modal MRI and LSFM
templates generated using the ANTsX framework [@Avants:2010aa]. It spans key
stages of mouse brain development (E11.5, E13.5, E15.5, E18.5, P4, P14, and P56)
and includes structural labels defined by a developmental ontology. The DevCCF
was constructed in coordination with the AllenCCFv3 to facilitate integration
across atlases and data types.

Although this collection provides broad developmental coverage, its discrete
sampling limits the ability to model continuous transformations across time. To
address this, we developed a velocity flow–based modeling approach that enables
anatomically plausible, diffeomorphic transformations between any two continuous
time points within the DevCCF range. Unlike traditional pairwise interpolation,
which requires sequential warping through each intermediate stage, this model,
defined by a time-varying velocity field (i.e., a smooth vector field defined
over space and time that governs the continuous deformation of an image domain),
allows direct computation of deformations between any two time points in the
continuum which improves smoothness and enables flexible spatiotemporal
alignment. This functionality is implemented in both ANTsR and ANTsPy
(see `ants.fit_time_varying_transform_to_point_sets(...)`) and integrates seamlessly
with existing ANTsX workflows.  The velocity field is represented as a 4D ITK
image where each voxel stores the $x$,$y$,$z$ components of motion at a given
time point.  Integration of the time-varying velocity field uses uses 4$^{th}$ 
order Runge-Kutta (`ants.integrate_velocity_field(...)`) [@Avants:2014aa].

<!-- \begin{figure}[!htb]
\centering
\includegraphics[width=0.75\textwidth]{Figures/SimplifiedAnnotations.pdf}
\caption{}
\label{fig:simplifiedannotations}
\end{figure} -->

Each DevCCF template includes over 2,500 labeled anatomical regions, with
spatial resolutions ranging from 31.5 to 50$\mu$m. For the velocity flow modeling
task, we identified a common set of 26 bilateral regions (13 per hemisphere)
that were consistently labeled across all timepoints. These regions span major
developmental domains including the pallium, subpallium, midbrain, prosomeres,
hypothalamus, hindbrain subregions, and key white matter tracts
(Figure 3).

Prior to velocity field optimization, all templates were rigidly aligned to the
DevCCF P56 template using the centroids of these common label sets. Pairwise
correspondence between adjacent timepoints was then computed using ANTsX’s
multi-metric registration via `ants.registration(...)`. Instead of performing
intensity-based multi-label registration directly, we constructed 24 binary
label masks per atlas pair (one per structure) and optimized alignment using the
mean squares similarity metric with the SyN transform [@Avants:2008aa].

To generate the point sets for velocity field optimization, we sampled both
boundary (contour) and interior (region) points from the P56 labels and
propagated them to each developmental stage using the learned pairwise
transforms. Contours were sampled at 10% of available points and regions at 1%,
yielding 173,303 total points per atlas ($N_{contour} = 98{,}151$; $N_{region} =
75{,}152$). Boundary points were assigned double weight during optimization to
emphasize anatomical boundary correspondence.

<!-- \begin{figure}[!htb]
\centering
\includegraphics[width=0.99\textwidth]{Figures/convergence.pdf}
\caption{}
\label{fig:convergence}
\end{figure} -->


The velocity field was optimized using the seven corresponding point sets and
their associated weights. The field geometry was defined at $[256, 182, 360]$
with 11 integration points at 50 $\mu$m resolution, yielding a compressed velocity
model of $\sim2$ GB. This resolution balanced accuracy and computational tractability
while remaining portable. All data and code are publicly available in the
accompanying GitHub repository.

To normalize temporal spacing, we assigned scalar values in $[0, 1]$ to each
template. Given the nonlinear spacing in postnatal development, we applied a
logarithmic transform to the raw time values prior to normalization. Within this
logarithmic temporal transform, P56 was assigned a span of 28 postnatal days to
reflect known developmental dynamics (i.e., in terms of modeling the continuous
deformation, the morphological changes between Day 28 and Day 56 are
insignificant).  This improved the temporal distribution of integration points
(Figure 4, right panel).

Optimization was run for a maximum of 200 iterations using a 2020 iMac (3.6 GHz
10-Core Intel Core i9, 64 GB RAM), with each iteration taking $\sim6$ minutes.
During each iteration, the velocity field was updated across all 11 integration
points by computing regularized displacement fields between warped point sets at
adjacent time slices. Updates were applied using a step size of $\delta = 0.2$.
Convergence was assessed via average displacement error across all points, with
final convergence achieved after $\sim125$ iterations (Figure
4, left panel). Median errors across integration points also
trended toward zero, albeit at varying rates.  To benchmark performance, we
compared the velocity model’s region-based alignment to traditional pairwise
registration using SyN, a widely used diffeomorphic algorithm. The velocity
model achieved comparable Dice scores at sampled timepoints while additionally
offering smooth interpolation across the entire developmental trajectory.

<!-- \begin{figure}[!htb]
\centering
\includegraphics[width=0.8\textwidth]{Figures/CrossWarp.pdf}
\caption{}
\label{fig:crosswarp}
\end{figure}

\begin{figure}[!htb]
\centering
\includegraphics[width=0.8\textwidth]{Figures/pseudo_template.pdf}
\caption{}
\label{fig:virtual}
\end{figure} -->

Once optimized, the velocity field enables the computation of diffeomorphic
transformations between any pair of continuous time points within the DevCCF
developmental range. Figure 5 illustrates cross-warping
between all DevCCF stages using the velocity flow model. In addition to
facilitating flexible alignment between existing templates, the model also
supports the synthesis of virtual templates at intermediate, unsampled
developmental stages. As shown in Figure 6, we demonstrate the
creation of virtual age templates (e.g., P10.3 and P20) by warping adjacent
developmental atlases to a target timepoint and constructing an averaged
representation using ANTsX’s template-building functionality.

All usage examples, scripts, and supporting data for full reproducibility are
publicly available in the associated codebase.
