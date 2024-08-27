
\clearpage
\newpage

# Results

\begin{figure*}
\centering
\begin{subfigure}[t]{0.49\textwidth}
\centering
\includegraphics[width=0.99\textwidth]{Figures/merfishPipeline.pdf}
\caption{}
\end{subfigure} 
\begin{subfigure}[t]{0.49\textwidth}
\centering
\includegraphics[width=0.99\textwidth]{Figures/fmostPipeline.pdf}
\caption{}
\end{subfigure}
\caption{Diagram of the two ANTsX-based pipelines for mapping (a) MERFISH
          and (b)fMOST data into the space of AllenCCFv3.  Each generates
         the requisite transforms, $\mathcal{T}$, to map individual images.}
\label{fig:allenpipelines}
\end{figure*}


## AllenCCFv3 brain image mapping

<!--
\newcommand{\ROT}[1]{\rotatebox{60}{\parbox{1.875cm}{\scriptsize #1}}}
\newcommand{\STAB}[1]{#1}

\begin{table}[!h]
  \centering
  \begin{tabular}{l|p{1.cm}p{1.cm}p{1.cm}p{1.cm}p{1.cm}p{1.cm}p{1.cm}p{1.cm}}
    & \STAB{\ROT{Background}}
    & \STAB{\ROT{Whole brain}}
    & \STAB{\ROT{Fimbria}}
    & \STAB{\ROT{Habenular commissure}}
    & \STAB{\ROT{Posterior choroid plexus}}
    & \STAB{\ROT{Anterior choroid plexus}}
    & \STAB{\ROT{Optic chiasm}}
    & \STAB{\ROT{Caudate putamen}}
    \\
    \hline
    {\footnotesize Dice} & {\footnotesize \bf 0.99} 
                         & {\footnotesize \bf 0.99} 
                         & {\footnotesize \bf 0.91} 
                         & {\footnotesize 0.63} 
                         & {\footnotesize \bf 0.93} 
                         & {\footnotesize \bf 0.96} 
                         & {\footnotesize 0.77} 
                         & {\footnotesize \bf 0.97}
  \end{tabular}
  \caption{Dice overlap of landmark labels between corresponding structures 
           in the fMOST average atlas and AllenCCFv3.} 
  \label{table:allenresults}
\end{table}
-->

### Mapping multiplexed error-robust fluorescence in situ hybridization (MERFISH) data

__Overview.__ The ANTsX framework was used to develop a pipeline for mapping multiplexed error-robust fluorescence in situ hybridization (MERFISH) spatial transcriptomic mouse data onto the AllenCCFv3 (see Figure \ref{fig:allenpipelines}(a)). This pipeline, used recently in creating a high-resolution transcriptomic atlas of the mouse brain[@Yao:2023aa], performs mappings by first generating anatomical labels from tissue related gene expressions in the MERFISH data, and then spatially matching these labels to corresponding anatomical tissue parcellations in the AllenCCFv3. The pipeline consists
of MERFISH data specific preprocessing which includes section reconstruction,
mapping corresponding anatomical labels between AllenCCFv3 and the spatial
transcriptomic maps of the MERFISH data, and matching MERFISH sections to the
atlas space. Following pre-processing, two main alignment steps were performed:
1) 3-D global affine mapping and section matching of the AllenCCFv3 into the
MERFISH data and 2) 2D global and deformable mapping between each MERFISH
section and matched AllenCCFv3 section. Mappings learned via each step in the
pipeline are preserved and concatenated to provide point-to-point correspondence
between the original MERFISH data and AllenCCFv3, thus allowing individual gene
expressions to be transferred into the AllenCCFv3. 

__Data.__ MERFISH mouse brain data was acquired using a previously detailed procedure
[@Yao:2023aa]. Briefly, a brain of C57BL/6 mouse was dissected according to
standard procedures and placed into an optimal cutting temperature (OCT)
compound (Sakura FineTek 4583) in which it was stored at -80°C. The fresh frozen
brain was sectioned at $10 \mu m$ on Leica 3050 S cryostats at intervals of 
$200 \mu m$ to evenly cover the brain. A set of 500 genes were imaged that had been
carefully chosen to distinguish the $\sim5200$ clusters of our existing RNAseq
taxonomy. For staining the tissue with MERFISH probes, a modified version of
instructions provided by the manufacturer was used [@Yao:2023aa]. Raw MERSCOPE
data were decoded using Vizgen software (v231). Cell segmentation was performed
[@Liu:2023aa]. In brief, cells were segmented based on DAPI and PolyT staining
using Cellpose [@Stringer:2021aa]. Segmentation was performed on a median
z-plane (fourth out of seven) and cell borders were propagated to z-planes above and
below. To assign cluster identity to each cell in the MERFISH dataset, we mapped
the MERFISH cells to the scRNA-seq reference taxonomy. 

__Evaluation.__ Alignment of the MERFISH data into the AllenCCFv3 was
qualitatively assessed by an expert anatomist at each iteration of the
registration using known correspondence of gene markers and their associations
with the AllenCCFv3. As previously reported [@Yao:2023aa], further assessment of
the alignment showed that, of the 554 terminal regions (gray matter only) in the
AllenCCFv3, only seven small subregions were missed from the MERFISH dataset:
frontal pole, layer 1 (FRP1), FRP2/3, FRP5; accessory olfactory bulb, glomerular
layer (AOBgl); accessory olfactory bulb, granular layer (AOBgr); accessory
olfactory bulb, mitral layer (AOBmi); and accessory supraoptic group (ASO).


### Mapping fluorescence micro-optical sectioning tomography (fMOST) data

__Overview.__  We developed a pipeline for mapping fluorescence micro-optical sectioning
tomography (fMOST) mouse brain images into the AllenCCFv3 (see
Figure \ref{fig:allenpipelines}(b)). The pipeline is adapted from previously developed frameworks for human brain mapping[@Avants:2010aa], and uses a modality specific (fMOST) average atlas to assist in the image registration and mapping. This approach has been well validated in human studies[@jia:2011aa;@tang:2009aa;@dewey:2017aa], and successfully used in other mouse data[@perens:2023aa;@Wang:2020aa;@qu:2022aa].
Briefly, we construct an intensity- and shape-based average fMOST
atlas using 30 fMOST images to serve as an intermediate registration target for mapping fMOST images from individual specimens into the AllenCCFv3. Preprocessing steps include
downsampling to match the $25 \mu m$ isotropic AllenCCFv3, acquisition-based
stripe artifact removal, and inhomogeneity correction [@Tustison:2010ac].
Preprocessing also includes a single annotation-driven registration to establish
a canonical mapping between the fMOST atlas and the AllenCCFv3. This step allows
us to align expert determined landmarks to accurately map structures with large
morphological differences between the modalities, which are difficult to address
using standard approaches. Once this canonical mapping is established, standard
intensity-based registration is used to align each new fMOST image to the fMOST
specific atlas. This mapping is concatenated with the canonical fMOST 
atlas-to-AllenCCFv3 mapping to further map each individual brain into the latter without
the need to generate additional landmarks. Transformations learned through this
mapping can be applied to single neuron reconstructions from the fMOST images to
evaluate neuronal distributions across different specimens into the AllenCCFv3
for the purpose of cell census analyses.

__Data.__ The high-throughput and high-resolution fluorescence micro-optical
sectioning tomography (fMOST) [@Gong:2016aa;@Wang:2021aa] platform was used to
image 55 mouse brains containing gene-defined neuron populations, with sparse
transgenic expression [@Rotolo:2008aa;@Peng:2021aa]. In short, the fMOST imaging
platform results in 3-D images with voxel sizes of $0.35 \times 0.35 \times 1.0
\mu m^3$ and is a two-channel imaging system where the green channel displays
the green fluorescent protein (GFP) labeled neuron morphology and the red
channel is used to visualize the counterstained propidium iodide
cytoarchitecture. The spatial normalizations described in this work were
performed using the red channel, which offered higher tissue contrast for
alignment, although other approaches are possible including multi-channel
registration.

__Evaluation.__  Evaluation of the canonical fMOST atlas to Allen CCFv3 mapping
was performed via quantitative comparison at each step of the registration and
qualitative assessment of structural correspondence after alignment by an expert
anatomist. Dice values were generated for the following structures: whole brain,
0.99; fimbria, 0.91; habenular commissure, 0.63; posterior choroid plexus, 0.93;
anterior choroid plexus,  0.96; optic chiasm, 0.77; caudate putamen, 0.97.
Similar qualitative assessment was performed for each fMOST specimen including
the corresponding neuron reconstruction data.