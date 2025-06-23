
## The Advanced Normalization Tools Ecosystem (ANTsX)

The Advanced Normalization Tools Ecosystem (ANTsX) has been used in a number of
applications for mapping mouse brain data as part of core processing steps in
various workflows
[@pagani:2016aa;@Anderson:2019aa;@Ni:2020aa;@allan:2019aa;@Yao:2023aa],
particularly its pairwise, intensity-based image registration capabilities
[@Avants:2008aa] and bias field correction [@Tustison:2010ac]. Historically,
ANTsX development is based on foundational approaches to image mapping
[@Bajcsy:1982aa;@Bajcsy:1989aa;@Gee:1993aa], especially in the human brain, with
key contributions such as the Symmetric Normalization (SyN) algorithm
[@Avants:2008aa]. It has been independently evaluated in diverse imaging domains
including multi-site brain MRI [@Klein:2009aa], pulmonary CT [@Murphy:2011aa],
and multi-modal brain tumor registration [@Baheti:2021aa].

Beyond registration, ANTsX provides functionality for template generation
[@Avants:2010aa], intensity-based segmentation [@Avants:2011uf], preprocessing
[@Manjon:2010aa;@Tustison:2010ac], and deep learning [@Tustison:2021aa]. It has
demonstrated strong performance in consensus labeling [@Wang:2013ab], brain
tumor segmentation [@Tustison:2014aa], and cardiac motion estimation
[@Tustison:2015ab]. Built on the Insight Toolkit (ITK) [@McCormick:2014aa],
ANTsX benefits from open-source contributions while supporting continued
algorithm evaluation and innovation.  In the context of mouse brain data, ANTsX
provides a robust platform for developing modular pipelines to map diverse
imaging modalities into CCFs. These tools span multiple classes of mapping
problems: cross-modality image registration, landmark-driven alignment, temporal
interpolation across developmental stages, and deep learning–based segmentation.
As such, they also serve as illustrative case studies for adapting ANTsX tools
to other use cases We describe both shared infrastructure and targeted
strategies adapted to the specific challenges of each modality.  This paper
highlights usage across distinct BICCN projects such as spatial transcriptomic
data from MERFISH, structural data from fMOST, and multimodal developmental data
from LSFM and MRI. 

## Novel ANTsX-based open-source contributions

We introduce two novel contributions to ANTsX developed as part of collabortive
efforts in creating the Developmental Common Coordinate Framework (DevCCF)
[@Kronman:2024aa]. First, we present an open-source velocity field–based
interpolation framework for continuous mapping across the sampled embryonic and
postnatal stages of the DevCCF atlas [@Kronman:2024aa]. This functionality
enables biologically plausible interpolation between timepoints via a
time-parameterized diffeomorphic velocity model [@Beg:2005aa], inspired by
previous work [@Tustison:2013ac]. Second, we present a deep learning pipeline
for structural parcellation of the mouse brain from multimodal MRI data. This
includes two novel components: 1) a template-derived brain extraction model
using augmented data from two ANTsX-derived template datasets
[@Hsu2021;@Reshetnikov2021], and 2) a template-derived parcellation model
trained on DevCCF P56 labelings mapped from the AllenCCFv3. This pipeline
demonstrates how ANTsX tools and public resources can be leveraged to build
robust anatomical segmentation pipelines with minimal annotated data. We
independently evaluate this framework using a longitudinal external dataset
[@Rahman:2023aa], demonstrating generalizability across specimens and imaging
protocols. All components are openly available through the R and Python ANTsX
packages, with general-purpose functionality documented in a reproducible,
cross-platform tutorial (https://tinyurl.com/antsxtutorial). Code specific to
this manuscript, including scripts to reproduce the novel contributions 
and all associated evaluations, is provided in a dedicated repository
(https://github.com/ntustison/ANTsXMouseBrainMapping). Additional tools for
mapping spatial transcriptomic (MERFISH) and structural (fMOST) data to the
AllenCCFv3 are separately available 
at (https://github.com/dontminchenit/CCFAlignmentToolkit).

