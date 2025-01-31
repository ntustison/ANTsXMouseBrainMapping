# Introduction

Over the past decade there have been significant advancements in mesoscopic
single-cell analysis of the mouse brain. It is now possible to track single
neurons in mouse brains [@Keller:2015aa], observe whole brain developmental
changes on a cellular level [@La-Manno:2021aa], associate brain regions and
tissues with their genetic composition [@Wen:2022aa], and locally characterize
neural connectivity [@Oh:2014aa]. Much of these scientific achievements have
been made possible due to breakthroughs in high resolution cell profiling and
imaging techniques that permit submicron, multi-modal, 3-D characterizations of
whole mouse brains. Among these include advanced techniques such as
micro-optical sectioning tomography [@Gong:2013aa,@Li:2010aa], tissue clearing
[@Keller:2015aa;@Ueda:2020aa], spatial transcriptomics
[@Stahl:2016aa,@Burgess:2019aa], and single-cell genomic
profiling [@hardwick:2022aa], which have greatly expanded the resolution and
specificity of single-cell measurements in the brain. 

Recent efforts by the National Institutes of Health's Brain Research Through
Advancing Innovative Neurotechnologies (BRAIN) Initiative has pushed for
large-scale, international collaborative efforts to utilize these advanced
single-cell techniques to create a comprehensive reference database for
high-resolution transcriptomic, epigenomic, structural and imaging data of the
mouse brain. This consortium of laboratories and data centers, known as the
BRAIN Initiative Cell Census Network (BICCN), has archived datasets encompassing
over 40 different multi-modal profiling techniques from more than 30 research
groups, each providing unique characterizations of distinct cell types in the
brain [@hawrylycz:2023aa]. Several of these modalities have been further
developed into reference atlases to facilitate spatial alignment of individual
brains and different data types into a common coordinate framework (CCF), thus
allowing diverse single-cell information to be analyzed in an integrated manner.
The most notable of these atlases is the Allen Mouse Brain Common Coordinate
Framework (AllenCCFv3) [@Wang:2020aa], which serves as a primary target
coordinate space for much of the work associated with the BICCN. Other atlases
include modality-specific atlases [@perens:2021aa;@ma:2005aa;@qu:2022aa], and
spatiotemporal atlases [@Kronman:2024aa;@chuang:2011aa] for the developing mouse
brain. 

## Mouse brain mapping

The cross-modality associations that can be learned from mapping different cell
type data into a CCF is critical for improving our understanding of the complex
relationships between cellular structure, morphology, and genetics in the brain.
However, finding an accurate mapping between each individual mouse brain and a
CCF is a challenging and heterogeneous task. There is significant variance in
the imaging protocols across different cell type data as well as different
tissue processing and imaging methods which can potentially introduce
tissue distortion and signal differences
[@dries:2021aa;@ricci:2022aa]. Certain modalities can have poor intensity
correspondence with the CCF, negatively impacting image alignment accuracy. Studies
targeting specific regions or cell types can lead to missing anatomical
correspondences. Other considerations include artifacts such as tissue
distortion, holes, bubbles, folding, tears, and missing sections in the data
that often require manual correction
[@agarwal:2016aa;@agarwal:2017aa;@tward:2019aa;@cahill:2012aa]. Given the
diversity of these challenges, it is unlikely any single mapping approach can be
generally applicable across all cell type data. Diverse, and often specialized,
strategies are needed to address the unique barriers present for mapping each
modality.

Existing solutions to address mapping cell type data into the AllenCCFv3 falls
broadly into three main categories. The first consists of integrated processing
platforms that directly provide mapped data to the users. These include the
Allen Brain Cell Atlas [@sunkin:2012] for the Allen Reference Atlas (ARA) and
associated data, the Brain Architecture Portal [@kim:2017aa] for combined ex
vivo radiology and histology data, OpenBrainMap [@Furth:2018aa] for connectivity
data, and the Image and Multi-Morphology Pipeline [@li:2022aa] for high
resolution morphology data. These platforms provide users online access to
pre-processed, multi-modal cell type data that are already mapped to the
AllenCCFv3. The platforms are designed such that the data is interactively
manipulated by users through integrated visualization software that allow users
to spatially manipulate and explore each dataset within the mapped space. While
highly convenient for investigators who are interested in studying the specific
modalities provided by these platforms, these systems can be limited in flexibility,
general applicability, and public availability. As a result, investigators often 
find it difficult to apply the same mapping solutions to their own data.

The second category comprises specialized approaches specifically designed for
mapping one or more modalities into a CCF. These approaches use combinations of
specialized manual and automated processes that address specific challenges in
each modality. Examples include approaches for mapping histology
[@puchades:2019aa;@eastwood:2019aa;@Ni:2020aa], magnetic resonance imaging (MRI)
[@Pallast:2019aa;@Celestine:2020aa;@Ioanas:2021aa;@perens:2023aa;@aggarwal:2009aa;@Goubran:2019aa@chandrashekhar:2021aa;@Ni:2020aa],
micro-computed tomography (microCT) [@aggarwal:2009aa;@chandrashekhar:2021aa],
light-sheet fluorescence microscopy (LSFM)
[@Jin:2022aa;@Negwer:2022aa;@perens:2023aa;@Goubran:2019aa;@chandrashekhar:2021aa],
fluorescence micro-optical sectioning tomography (fMOST)
[@qu:2022aa;@lin:2023aa] and transcriptomic data
[@zhang:2021aa;@shi:2023aa;@zhang:2023aa]. As specialized approaches, these
techniques tend to boast higher mapping accuracy, robustness, and ease of use.
Conversely, their specialized designs often rely on base assumptions regarding
the data type that can make them rigid and difficult to adapt for new modalities
or unexpected artifacts and distortions in the data. Adapting these specialize
software tools to use with new data can require significant development,
validation time, and engineering expertise that may not be readily available for
all investigators. 

The last category consists of modular mapping approaches constructed using
general image analysis toolkits, which are software packages that include
modular image processing, segmentation and registration tools that have
been previously developed, and validated for multiple application areas.
Examples of such toolkits include elastix [@Klein:2010aa], Slicer3D
[@fedorov:2012aa], ANTsX [@Tustison:2021aa], and several others which have all
been applied towards mouse brain spatial mapping. The main challenge, in these
mouse-specific study scenarios, is that tailored pipelines often need be
constructed from available software components.  Investigators must therefore be
familiar with the these tools for formulating new or adapting existing
pipelines. However, in comparison to previously described specialized mapping
approaches, these approaches are often easier to create and prone to robustness,
being typically constructed from pipeline components which have been previously
vetted in other contexts. In this work, we highlight such mapping strategies
designed using the ANTsX framework to map distinct mouse cell type data
with different characteristics into existing CCFs. 

<!--
More
recently, several publicly available packages comprise well-established package
dependencies originally developed on human brain data. SPMMouse
[@Sawiak:2014aa], for example, is based on the well-known Statistical Parametric
Mapping (SPM) Matlab-based toolset [@Ashburner:2012aa]. The automated mouse
atlas propagation (aMAP) tool is largely a front-end for the NiftyReg image
registration package [@Modat:2010aa] applied to mouse data which is currently
available as a Python module [@Tyson:2022aa]. NiftyReg is also used by the
Atlas-based Imaging Data Analysis (AIDA) MRI pipeline [@Pallast:2019aa] as well
as the Multi Atlas Segmentation and Morphometric Analysis Toolkit (MASMAT).
Whereas the former also incorporates the FMRIB Software Library (FSL)
[@Jenkinson:2012wi] for brain extraction and DSIStudio [@Yeh:2010aa] for DTI
processing, the latter uses NiftySeg and multi-consensus labeling tools
[@Jorge-Cardoso:2013aa] for brain extraction and parcellation. In addition,
MASMAT incorporates N4 bias field correction [@Tustison:2010ac] from the
Advanced Normalization Tools Ecosystem (ANTsX) [@Tustison:2021aa] as do the
packages Multi-modal Image Registration And Connectivity anaLysis (MIRACL)
[@Goubran:2019aa], Sammba-MRI [@Celestine:2020aa], and Small Animal Magnetic
Resonance Imaging (SAMRI) [@Ioanas:2021aa].  However, whereas Saamba-MRI uses
AFNI [@Cox:2012aa] for image registration; MIRACL, SAMRI, SAMBA
[@Anderson:2019aa], and BrainsMapi [@Ni:2020aa] all use ANTsX registration
tools. Other packages use landmark-based approaches to image registration
including SMART [@Jin:2022aa]---an R package for semi-automated landmark-based
registration and segmentation of mouse brain based on WholeBrain
[@Furth:2018aa].  Relatedly, FriendlyClearMap [@Negwer:2022aa] and mBrainAligner
[@Qu:2022aa] are both landmark-based approaches to mapping of the mouse brain.
Whereas the former employs Elastix [@Klein:2010aa] functionality, the latter is
based on developed methodology referred to as _coherent landmark
mapping_. Finally, the widespread adoption of deep learning techniques has also
influenced development in mouse brain imaging methodologies.  For example, if
tissue deformations are not considered problematic for a particular dataset,
DeepSlice can be used to determine affine mappings [@Carey:2023aa] with the
optimal computational efficiency associated with neural networks.
-->
