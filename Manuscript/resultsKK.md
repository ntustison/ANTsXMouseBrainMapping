
## The Mouse Cortical Thickness Pipeline

One of the most popular pipelines in the ANTsX toolkit is that of determining
cortical thickness in the human brain with original novel contribution being the
Diffeomorphic Registration-based Cortical Thickness (DiReCT) algorithm
[@Das:2009uv].  This expanded to a complete cortical thickness pipeline for the
human braiņ, for both cross-sectional [@Tustison:2014ab] and longitudinal
[@Tustison:2019aa] using T1-weighted MR image data which was later refactored
using deep learning [@Tustison:2021aa].

Although no current ANTsX tools exist to create adequate training data for 
pipeline creation with mouse brain data (as is the case with human data), we
can leverage publicly available d



ANTsX tools and publicly available datasets permit the 

No current tools to create training data for deep learning (in contrast to e.g., human data).
Low data quality. Data is often:
sampling issues such as anisotropy, incomplete (i.e., missing boundary structures),
T2-w only, and
limited applicability to high resolution resources (e.g., AllenCCFv3, DevCCF).
However, in historical contrast to the human domain, we can leverage these publicly available templates (i.e., AllenCCFv3 and DevCCF) and deep learning to provide tools for multiple modalities and varying degrees of isotropic sampling.

\begin{figure}
\centering
\includegraphics[width=0.9\textwidth]{Figures/mousePipeline.png}
\caption{The mouse brain cortical thickness pipeline integrating two 
deep learning components for brain extraction and brain parcellation 
prior to estimating cortical thickness.  Both brain extraction and
parcellation pipelines rely heavily on ANTsX tools for template building
and data augmentation as well as open-science data availability.}
\label{fig:mouseKK}
\end{figure}

Looking to expand 