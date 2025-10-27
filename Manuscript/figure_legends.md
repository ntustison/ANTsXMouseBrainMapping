
\clearpage

# Figure Legends {-}

__Figure 1.__ Overview of ANTsX pipelines for mapping MERFISH and fMOST data to
the AllenCCFv3. Diagram of the two ANTsX-based pipelines for mapping (a) MERFISH
and (b)fMOST data into the space of AllenCCFv3. Each generates the requisite
transforms to map individual images to the CCF.

__Figure 2.__ Continuous developmental mapping enabled by the DevCCF velocity
flow model.  The spatial transformation between any two time points within the
continuous DevCCF longitudinal developmental trajectory is available through the
use of ANTsX functionality for generating a velocity flow model.

__Figure 3.__ Common anatomical labels across developmental stages of the
DevCCF. Annotated regions representing common labels across developmental
stages, shown for both P4 and P14.

__Figure 4.__ Convergence and evaluation of the velocity flow model across the
DevCCF develop- mental trajectory. (Top left) Total displacement error over
iterations. (Top right) Median displacement error per integration point across
the optimization timeline, spanning embryonic (E11.5) to postnatal (P56) stages.
(Bottom) Dice similarity scores comparing region-level label overlap between:
(1) conventional pairwise SyN registration and (2) velocity flow-based
deformation, across intermediate timepoints. Using region-based pairwise
registration with SyN as a performance upper bound, the velocity flow model
achieves comparable accuracy while also enabling smooth, continuous deformation
across the full developmental continuum.

__Figure 5.__ Visualization of DevCCF templates warped across developmental time
points.  Mid-sagittal visualization of DevCCF templates warped to every other
time point. Each row is a reference space; each column is a warped input.
Diagonal entries show original templates.

__Figure 6.__ Generation of virtual DevCCF templates at intermediate
developmental stages.  Example of generating "virtual" DevCCF templates at
intermediate time points (e.g., P10.3, P20) by warping adjacent stages to a
shared time and averaging using ANTsX.

__Figure 7.__ Deep learning pipelines for mouse brain extraction and
parcellation.  The mouse brain cortical labeling pipeline integrates two deep
learning components for brain extraction and anatomical region segmentation.
Both networks rely heavily on data augmentation applied to templates constructed
from open datasets. The framework also supports further refinement or
alternative label sets tailored to specific research needs. Possible
applications include voxelwise cortical thickness estimation.

__Figure 8.__ Evaluation of ANTsX brain extraction across an independent
dataset. Evaluation of the ANTsX mouse brain extraction on an independent,
publicly available dataset consisting of 12 specimens $\times$ 7 time points =
84 total images. Dice overlap comparisons with the user-generated brain masks
provide good agreement with the automated results from the brain extraction
network.

__Figure 9.__ Performance of ANTsX deep learning–based mouse brain parcellation.
Evaluation of the ANTsX deep learning–based mouse brain parcellation on a
diverse MRI cohort. (a) T2-weighted DevCCF P56 template with the six-region
parcellation: cerebral cortex, nuclei, brain stem, cerebellum, main olfactory
bulb, and hippocampal formation. (b) Example segmentation result from a
representative subject (NR5, Day 0) using the proposed deep learning pipeline.
(c) Box plots show Dice overlap across subjects for each registration approach
and region. The centre line is the median; box bounds are the interquartile
range (25th–75th percentiles); whiskers extend to the minimum and maximum values
within 1.5×IQR of the lower/upper quartiles; points beyond the whiskers are
outliers.
