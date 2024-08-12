# Introduction

Over the past decade there have been significant advancements in mesoscopic single-cell analysis of the mouse brain. It is now possible to track single neurons in
mouse brains [@Keller:2015aa], observe whole brain developmental changes on a
cellular level [@La-Manno:2021aa], associate brain regions and tissues with
their genetic composition [@Wen:2022aa], and locally characterize neural
connectivity [@Oh:2014aa]. Much of these scientific achievements have been made
possible due to breakthroughs in high resolution cell profiling and imaging techniques that permit submicron, multi-modal, 3D characterizations of whole mouse brains. Among these include advanced techniques such as micro-optical sectioning tomography [@Gong:2013aa,@Li:2010aa], tissue
clearing [@Keller:2015aa;@Ueda:2020aa], spatial transcriptomics
[@Stahl:2016aa,@Burgess:2019aa], and single-cell genomic profiling[ref], which have greatly expanded the resolution and specificity of single-cell measurements in the brain. 

Recent efforts by the National Institutes of Health's Brain Research Through Advancing Innovative Neurotechnologies (BRAIN) Initiative has pushed for large-scale, international collaborative efforts to utilize these advanced single cell techniques to create a comprehensive reference database for high-resolution transcriptomic, epigenomic, structural and imaging data of the mouse brain. This consortium of laboratories and data centers, known as the BRAIN Initiative Cell Census Network (BICCN), has to date archived datasets encompassing over 40 different multi-modal profiling techniques from more than 30 research groups, each providing unique characterizations of distinct cell types in the brain.[ref] Several of these modalities have been further developed into reference atlases to facilitate spatial alignment of individual brains and different data types into a common coordinate framework (CCF), thus allowing diverse single-cell information to be integrated and analyzed in tandem. The most notable of these atlases is the Allen Mouse Brain Common Coordinate Framework (AllenCCFv3)[@Wang:2020aa], which serves as the primary target coordinate space that the majority of BICCN mouse data are mapped to. Other atlases include modality specific atlases[ref] to help improve mapping accuracy, and the Developmental Common Coordinate Framework (DevCCF)[@Kronman:2023aa] that includes spatiotemporal information for the developing mouse brain. 

## Mouse brain mapping

The cross-modality associations that can be learned from mapping different cell type data into a CCF is critical for improving our understanding of the complex relationships between cellular structure, morphology, and genetics in the brain. However, finding an accurate mapping between each individual mouse brain and the CCF is a challenging and heterogeneous task. There is significant variance in the acquisition, fixation and imaging protocols across different cell type data, and different tissue processing and imaging methods can potentially introduce modality specific tissue distortion and signal differences.[ref] Certain modalities can have poor intensity correspondence with the CCF, making image alignment less robust. Studies targeting specific regions or cell types can lead to missing anatomical correspondences. Other considerations include artifacts such as tissue distortion, holes, bubbles, folding, tears, and missing sections in the data that need to be addressed on a per-case basis. Given the diversity of these challenges, it is unlikely any single mapping approach can be generally applicable across all cell type data. Modular, and often specialized, strategies are needed to address the unique barriers present for mapping each modality.

Existing solutions to address mapping cell type data into the AllenCCFv3 falls broadly into three main categories. The first consists of integrated processing platforms that directly provide mapped data to the users. These include the Allen Brain Explorer[ref] for the Allen Reference Atlas (ARA) and associated data, the Brain Architecture Portal[ref] for combined ex vivo radiology and histology data, and the Image and Multi-Morphology Pipeline[ref] for high resolution morphology data. These platforms provide users online access to pre-processed, multi-modal cell type data that are already mapped to the AllenCCFv3. The platforms are designed such that the data is interactable by users through integrated visualization software that allow users to spatially manipulate and explore each dataset within the mapped space. While highly convenient for investigators who are interested in studying the specific modalities provided by these platforms, these system are limited in flexibility and general applicability. The mapping software and pipeline are typically developed specifically with the data type and platform in mind, and the software are rarely openly accessible to the public. Investigators will find it difficult to apply the same mapping to their own data without direct collaboration with platform owners.

The second category are specialized approaches specifically designed for mapping one or more modalities into a CCF. These approaches use combinations of manual and automated processes that address specific challenges in each modality. Examples include approaches for mapping magnetic resonance imaging (MRI)[ref], micro-computed tomography (microCT)[ref], light-sheet fluorescence microscopy (LSFM)[ref] , for fluorescence micro-optical sectioning tomography (fMOST)[ref], and volumetric imaging with synchronous on-the-fly-scan and readout (VISoR)[ref] data. As specialized approaches, these techniques tend to boast higher mapping accuracy, robustness, and ease of use when ran with applicable modalities. Conversely, their specialized designs often rely on base assumptions regarding the data that can make them rigid and difficult to adapt for new modalities or unexpected artifacts and distortions in the data. Retooling these specialize software to use with new data can require significant development and validation time and engineering expertise that may not be readily available for all investigators. 

The last category are modular mapping approaches constructed using general image analysis toolkits, which are software packages that include varied collections of image processing, segmentation and registration tools that have been previously developed, and validated for general use. Examples of such toolkits include elastix[ref], slicer3D[ref], and ANTsX[ref], which have all been applied towards mapping mouse cell type data. The main challenge for using these approaches is that the individual tools in the toolbox are not data type specific. Thus, investigators must construct pipelines that link together a variety of tools to address data specific problem, and certain tools may still require specialized input data such as landmarks or annotations to operate. Investigator need to be familiar with the toolkits and supply effort to build such pipelines for new data type. However, unlike previously listed specialized mapping approaches, which often require additional software development to address new data types, toolbox driven pipelines are easier to create, making them more accessible for the general user, and individual pieces of the pipeline have already been validated for other efforts. Using a general toolkit allows for modular mapping strategies that can handle a wide array of different data types by piecing together distinct solutions for modality specific problems. In this work, we highlight such mapping strategies designed using ANTsX to map three distinct mouse cell-type data with different characteristics into the ALLENCCFv3. 

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