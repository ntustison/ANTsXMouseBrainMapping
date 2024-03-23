# Introduction

Over the past two decades there have been significant advancements in mesoscopic
analysis of the mouse brain. It is currently possible to track single cell neurons in
mouse brains [@Keller:2015aa], observe whole brain developmental changes on a
cellular level [@La-Manno:2021aa], associate brain regions and tissues with
their genetic composition [@Wen:2022aa], and locally characterize neural
connectivity [@Oh:2014aa]. Much of this scientific achievement has been made
possible due to breakthroughs in high resolution imaging techniques that permit
submicron, 3-D imaging of whole mouse brains. Associated research techniques
such as micro-optical sectioning tomography [@Gong:2013aa,@Li:2010aa], tissue
clearing [@Keller:2015aa;@Ueda:2020aa], spatial transcriptomics
[@Stahl:2016aa,@Burgess:2019aa] are all well-utilized in the course of
scientific investigations of mesoscale relationships in the mouse brain. 

An important component of this research is the ability to map the various image
data to anatomical reference frames
[@MacKenzie-Graham:2004aa,@Mackenzie-Graham:2007aa] for inferring spatial
relationships between structures, cells, and genetics. This has motivated the
development of detailed structural image atlases of the mouse brain.  Notable
examples include the Allen Brain Atlas and Coordinate Frameworks (AllenCCFv3)
[@Dong:2008aa,@Wang:2020aa], the Waxholm Space [@Johnson:2010aa], and more
recently, the Developmental Common Coordinate Framework (DevCCF)
[@Kronman:2023aa]. Despite the significance of these contributions, challenges
still exist in large part due to the wide heterogeneity in associated
study-specific image data. For example, variance in the acquisition methods can
introduce artifacts such as tissue distortion, holes, bubbles, folding, tears,
and missing slices. These complicate assumed correspondence for
conventional spatial mapping approaches.

## Mouse-specific brain mapping software

To address such challenges, several software packages have been developed over
the years comprising solutions of varying comprehensibility, sophistication, and
availability.  An early contribution to the community was the Rapid Automatic
Tissue Segmentation (RATS) package [@Oguz:2014aa] for brain extraction. More
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
[@Furth:2018aa].  FriendlyClearMap [@Negwer:2022aa] uses the landmark-based
registration functionality of Elastix [@Klein:2010aa]. Finally, the widespread
adoption of deep learning techniques has also influenced development in mouse
brain imaging methodologies.  For example, if tissue deformations are not
considered problematic for a particular dataset, DeepSlice can be used to
determine affine mappings [@Carey:2023aa] with the optimal computational
efficiency associated with neural networks.
