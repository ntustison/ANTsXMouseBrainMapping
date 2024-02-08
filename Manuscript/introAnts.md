
### The ANTsX Ecosystem  {-}

As noted previously, many of the existing packages designed for processing mouse
brain image data use ANTsX tools for core processing steps in various workflows,
particularly its pairwise, intensity-based image registration capabilities and
bias field correction. Historically, ANTsX development is originally based on
fundamental approaches to image mapping
[@Bajcsy:1982aa;@Bajcsy:1989aa;@Gee:2003aa], particularly in the human brain,
which has resulted in core contributions to the field such as the well-known and
highly-vetted Symmetric Normalization (SyN) algorithm [@Avants:2008aa].  Since
its development, various independent platforms have been used to evaluate ANTsX
image registration capabilities in the context of different application foci
which include multi-site brain MRI data [@Klein:2009aa], pulmonary CT data
[@Murphy:2011aa], and most recently, multi-modal brain registration in the
presence of tumors [@Baheti:2021aa]. 

\input{antsx_functionality_table}

Apart from its registration capabilities, ANTsX comprises additional
functionality such as template generation [@Avants:2010aa], point set data
approximation [@Tustison:2006aa], and deep learning networks specifically
trained for mouse data (see Table \ref{table:methods}). The comprehensive use of
the toolkit has demonstrated superb performance in multiple application areas
(e.g., consensus labeling [@Wang:2013ab], brain tumor segmentation
[@Tustison:2014aa], and cardiac motion estimation [@Tustison:2015ab] ).
Importantly, ANTs is built on the Insight Toolkit (ITK) [@McCormick:2014aa]
deriving benefit from the open-source community of scientists and programmers
and providing an open-source venue for algorithmic development, evaluation, and
improvement.

\begin{figure}[!htb]
\centering
\makebox[\textwidth][c]{\includegraphics[width=1.2\textwidth]{Figures/pipeline3.png}}%
\caption{Illustration of a mouse brain template generation workflow and related
template-based applications demonstrating the utility of different ANTsX tools.
After imaging acquisition of the study population, various preprocessing steps
are applied to the imaging data such as bias correction, denoising, and brain
extraction as dictated by the needs of the study protocol.  
Potential applications, such as in the case of the DevCCF, include gene
expression mapping and the generation of the associated velocity flow model for
continuous spatiotemporal mapping in the temporal domain.}
\label{fig:pipeline}
\end{figure}

Recently, the developmental common coordinate framework (DevCCF) was introduced
to the mouse brain research community as a public resource [@Kronman:2023aa].
These symmetric atlases, comprising both multimodal image data and anatomical
segmentations defined by developmental ontology, sample the mouse embryonic days
(E) 11.5, E13.5, E15.5, E18.5 and postnatal day (P) 4, P14, and P56.  Modalities
include light sheet flourescence miscroscopy (LSFM) and at least four MRI
contrasts per developmental stage.  Anatomical parcellations are also available
for each time point and were generated from ANTsX-based mappings of gene
expression and other cell type data.  The P56 template was integrated with the
Allen CCFv3 to further increase the practical utility of the DevCCF.  These
processes, specifically template generation and multi-modal image mapping, were
performed using ANTsX functionality in the presence of previously noted image
mapping difficulties (e.g., missing slices, tissue distortion).

Given the temporal gaps in the discrete set of developmental atlases with the
potential for additional interpolative time points, we discuss the strategy of
the current DevCCF template generation [@Kronman:2023aa] and
provide additional information for the interested reader. Related, we also
provide an open-source framework, through ANTsX, for inferring correspondence
within the temporally continuous domain sampled by the existing set of embryonic
and postnatal atlases of the DevCCF.  Although alternative approaches are
possible for interpolating between time points, this recently developed ANTsX
functionality permits the generation of a diffeomorphic velocity flow
transformation model [@Beg:2005aa], influenced by previous work
[@Tustison:2013ac].  The resulting time-parameterized velocity field spans the
stages of the DevCCF where mappings between any two continuous time points
within the span bounded by the E11.5 and P56 atlases is determined by
integration of the optimized velocity field. This functionality is available
through ANTsX (via R and Python ANTsX packages) with a dedicated GitHub
repository that contains all data, scripts, and other guidance necessary to both
reproduce what is described below and to illustrate how future researchers can
incorporate additional atlases into a more densely sampled model in a
straightforward manner.

