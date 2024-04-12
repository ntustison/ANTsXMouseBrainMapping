
## The ANTsX Ecosystem for mouse brain mapping 

\input{antsx_functionality_table}

As noted previously, many of the existing packages designed for processing mouse
brain image data use ANTsX tools for core processing steps in various workflows,
particularly its pairwise, intensity-based image registration capabilities and
bias field correction. Historically, ANTsX development is originally based on
fundamental approaches to image mapping
[@Bajcsy:1982aa;@Bajcsy:1989aa;@Gee:1993aa], particularly in the human brain,
which has resulted in core contributions to the field such as the well-known
Symmetric Normalization (SyN) algorithm [@Avants:2008aa].  Since
its development, various independent platforms have been used to evaluate ANTsX
image registration capabilities in the context of different application foci
which include multi-site brain MRI data [@Klein:2009aa], pulmonary CT data
[@Murphy:2011aa], and most recently, multi-modal brain registration in the
presence of tumors [@Baheti:2021aa]. 

Apart from its registration capabilities, ANTsX comprises additional
functionality such as template generation [@Avants:2010aa], intensity-based
segmentation [@Avants:2011uf], preprocessing [@Manjon:2010aa;@Tustison:2010ac],
deep learning networks [@Tustison:2021aa], and other miscelleneous utilities (see
Table \ref{table:methods}). The comprehensive use of the toolkit has
demonstrated superb performance in multiple application areas (e.g., consensus
labeling [@Wang:2013ab], brain tumor segmentation [@Tustison:2014aa], and
cardiac motion estimation [@Tustison:2015ab] ). Importantly, ANTs is built on
the Insight Toolkit (ITK) [@McCormick:2014aa] deriving benefit from the
open-source community of scientists and programmers as well as providing an important
resource for algorithmic development, evaluation, and improvement.  We use this
functionality to demonstrate recently developed frameworks for mapping
fluorescence micro-optical sectioning tomography (fMOST) and multiplexed
error-robust fluorescence in situ hybridization (MERFISH) image data to the
AllenCCFv3 atlas space.  In addition to standard preprocessing steps (e.g., bias
correction), additional considerations are accommodated within the ANTsX
ecosystem, such as section reconstruction and landmark-based alignment with
corresponding processing scripts available at
\url{https://github.com/dontminchenit/CCFAlignmentToolkit}.  


<!-- 

\begin{figure}[!htb]
\centering
\makebox[\textwidth][c]{\includegraphics[width=1.2\textwidth]{Figures/pipeline3.png}}%
\caption{
Illustration of a mouse brain template generation workflow and related
template-based applications demonstrating the utility of different ANTsX tools,
specifically in the development of the DevCCF atlas. After imaging acquisition
of the study population, various preprocessing steps are applied to the imaging
data such as bias correction, denoising, and brain extraction for gene
expression mapping.  Also illustrated is the generation of the associated
velocity flow model for continuous spatiotemporal mapping interpolating the
sampled time points of the DevCCF.
}
\label{fig:pipeline}
\end{figure} 

-->

## ANTsX-based open-source contributions

Consistent with previous ANTsX development, the newly introduced capabilities
introduced below are available through ANTsX (specifically, via R and Python
ANTsX packages), and illustrated through self-contained examples in the ANTsX
tutorial (\url{https://tinyurl.com/antsxtutorial}) with a dedicated GitHub 
repository specific to this work
(\url{https://github.com/ntustison/ANTsXMouseBrainMapping}).

### The DevCCF velocity flow model

Recently, the Developmental Common Coordinate Framework (DevCCF) was introduced
to the mouse brain research community as a public resource [@Kronman:2023aa]
comprising symmetric atlases of multimodal image data and anatomical
segmentations defined by developmental ontology.  These templates sample the
mouse embryonic days (E) 11.5, E13.5, E15.5, E18.5 and postnatal day (P) 4, P14,
and P56.  Modalities include light sheet flourescence miscroscopy (LSFM) and at
least four MRI contrasts per developmental stage.  Anatomical parcellations are
also available for each time point and were generated from ANTsX-based mappings
of gene expression and other cell type data.  Additionally, the P56 template was
integrated with the AllenCCFv3 to further enhance the practical utility of the
DevCCF. These processes, specifically template generation and multi-modal image
mapping, were performed using ANTsX functionality in the presence of 
image mapping difficulties such as missing data and tissue distortion.[@Kronman:2023aa]  

Given the temporal gaps in the discrete set of developmental atlases, we also
provide an open-source framework for inferring correspondence
within the temporally continuous domain sampled by the existing set of embryonic
and postnatal atlases of the DevCCF.  This recently developed 
functionality permits the generation of a diffeomorphic velocity flow
transformation model [@Beg:2005aa], influenced by previous work
[@Tustison:2013ac].  The resulting time-parameterized velocity field spans the
stages of the DevCCF where mappings between any two continuous time points
within the span bounded by the E11.5 and P56 atlases is determined by
integration of the optimized velocity field. 

### Structural morphology and cortical thickness in the mouse brain

One of the most frequently utilized pipelines in the ANTsX toolkit is that of
estimating cortical thickness maps in the human brain.   Beginning with the
Diffeomorphic Registration-based Cortical Thickness (DiReCT) algorithm
[@Das:2009uv], this was later expanded to include a complete processing
framework for human brain cortical thickness estimation for both cross-sectional
[@Tustison:2014ab] and longitudinal [@Tustison:2019aa] data using T1-weighted
MRI.  These pipelines were later significantly refactored using deep learning
innovations [@Tustison:2021aa].

In contrast to the pipeline development in human data [@Tustison:2021aa], no
current ANTsX tools exist to create adequate training data for the mouse brain.
In addition, mouse brain data acquisition often has unique issues, such as lower
data quality or sampling anisotropy which limits its applicability to high
resolution resources (e.g., AllenCCFv3, DevCCF), specifically with respect to
the corresponding granular brain parcellations derived from numerous hours of
expert annotation leveraging multimodal imaging resources.

Herein, we introduce a mouse brain cortical thickness pipeline for T2-weighted (T2-w)
MRI comprising two novel deep learning components:  two-shot learning brain
extraction from data augmentation of two ANTsX templates generated from two open
datasets [@Hsu2021;@Reshetnikov2021] and single-shot brain parcellation derived
from the AllenCCFv3 labelings mapped to the corresponding DevCCF P56 T2-w
component.  Although we anticipate that this cortical thickness pipeline will be
beneficial to the research community, this work demonstrates more generally how
one can leverage ANTsX tools for developing tailored brain parcellation schemes
using these publicly available resources.  Evaluation is performed on an
independent open dataset [@Rahman:2023aa] comprising longitudinal acquisitions
of multiple specimens.  
