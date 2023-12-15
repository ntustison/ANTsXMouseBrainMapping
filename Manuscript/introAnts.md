
### The ANTsX Ecosystem  {-}

As noted above, many of the existing approaches for processing of mouse brain
image data use ANTsX tools for core steps in various workflows, particularly its
pairwise, intensity-based image registration tools and bias field correction.
Historically, ANTsX development is originally based on fundamental approaches to
image mapping [@Bajcsy:1982aa;@Bajcsy:1989aa;@Gee:2003aa], particularly in the
human brain, which has resulted in core contributions to the field such as the
well-known and highly-vetted Symmetric Normalization (SyN) algorithm
[@Avants:2008aa].  Since its development, various independent platforms have
been used to evaluate ANTsX image registration capabilities in the context of
different application foci which include multi-site brain MRI data
[@Klein:2009aa], pulmonary CT data [@Murphy:2011aa], and most recently
multi-modal brain registration in the presence of tumors [@Baheti:2021aa]. 

\input{antsx_functionality_table}

Apart from its registration capabilities, ANTsX is a comprehensive biological
and medical image analysis toolkit, that comprises additional functionality such
as template generation, general data approximation, and deep learning networks
specifically trained for mouse data (see Table \ref{table:methods}). The
collective use of the toolkit has demonstrated superb performance in multiple
application areas (e.g., consensus labeling [@Wang:2013ab], brain tumor
segmentation [@Tustison:2014aa], and cardiac motion estimation
[@Tustison:2015ab]).  Importantly, ANTs is built on the Insight Toolkit (ITK)
[@McCormick:2014aa] deriving benefit from a very capable open-source community
of scientists and programmers as well as providing a visible, open-source venue
for algorithmic contributions.

\begin{figure}[!htb]
\centering
\makebox[\textwidth][c]{\includegraphics[width=1.2\textwidth]{Figures/pipeline3.png}}%
\caption{Illustration of a mouse brain template generation workflow and 
related template-based applications demonstrating the utility of different 
ANTsX tools.  After imaging acquisition of the study population, various 
preprocessing steps are applied to the imaging data such as bias correction,
denoising, and brain extraction as dictated by the needs of the study 
protocol.  Not shown is the possibility of template symmetrization by 
contralaterally flipping the image data associated with each specimen.  
In the case of the DevCCF, applications include gene expression mapping 
and the associated velocity flow model for pseudo-template generation.}
\label{fig:pipeline}
\end{figure}

Recently, the developmental common coordinate framework (DevCCF) was introduced
to the mouse brain research community as a public resource [@Kronman:2023aa].
These symmetric atlases, comprising both multimodal image data and anatomical
segmentations defined by developmental ontology, span the mouse embryonic days
(E) 11.5, E13.5, E15.5, E18.5 and postnatal day (P) 4, P14, and P56.  Modalities
include at least four MRI contrasts and light sheet flourescence miscroscopy
(LSFM) per developmental stage.  Gene expression and other cell type data were
mapped to the corresponding developmental time point to guide the associated
anatomical parcellations.  To further demonstrate the practical utility of the
DevCCF, the P56 template was integrated with the Allen CCFv3 for mapping spatial
transcriptome cell-type data.  These processes, specifically template generation
and multi-modal image mapping, were performed using ANTsX functionality in the
presence of previously noted image mapping difficulties (e.g., missing slices,
tissue distortion) illustrated in Figure \ref{fig:pipeline}.

Given the temporal gaps in the discrete set of developmental atlases, we augment
the template generation explanation previously given [@Kronman:2023aa] from a
developer's perspective.  We hope that this will provide additional information
for the interested reader for potential future template generation.
Related, we also provide a complementary strategy for inferring correspondence
and mapping information within the temporally continuous domain spanned and
sampled by the existing set of embryonic and postnatal atlas brains of the
DevCCF.  Recently developed ANTsX functionality include the generation of a
diffeomorphic velocity flow transformation model [@Joshi:2000aa] spanning
developmental stages where mappings between any two continuous time points
within the span bounded by the E11.5 and P56 atlases is determined by
integration of the generated time-varying velocity field [@Christensen:1996aa].
Such transformations permit the possibility of "pseudo" templates generated
between available developmental stages.  



