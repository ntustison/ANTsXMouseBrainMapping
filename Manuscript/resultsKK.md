
## Automated structural labeling of the mouse brain

\begin{figure}
\centering
\includegraphics[width=0.95\textwidth]{Figures/mousePipeline.pdf} \caption{The
mouse brain cortical labeling pipeline integrates two deep learning components
for brain extraction and anatomical region segmentation. Both networks rely
heavily on data augmentation applied to templates constructed from open
datasets. The framework also supports further refinement or alternative label
sets tailored to specific research needs. Possible applications include
voxelwise cortical thickness estimation.}
\label{fig:mouseKK}
\end{figure}

Structural labeling strategies for the mouse brain are essential for
understanding the organization and function of the murine nervous system
[@Chon:2019aa]. By dividing the brain into anatomically or functionally defined
regions, researchers can localize biological processes, relate regional features
to behavior, or quantify spatial variation in gene expression patterns
[@Tasic:2016aa; @Bergmann:2020aa]. While deep learning techniques have yielded
robust segmentation and labeling tools for the human brain (e.g., SynthSeg
[@Billot:2023aa], ANTsXNet [@Tustison:2021aa]), analogous development for mouse
data (e.g., MEMOS [@Rolfe:2023aa]) has been limited. Mouse neuroimaging often
presents unique challenges, such as highly anisotropic sampling, that complicate
transfer of existing tools. At the same time, high resolution resources like the
AllenCCFv3 and DevCCF provide reference label sets that can serve as training
data. We demonstrate how ANTsX can be used to construct a full structural
labeling pipeline for the mouse brain (Figure \ref{fig:mouseKK}), including both
whole brain segmentation (i.e., brain extraction) and the subsequent atlas-based
region segmentation.


### Template-based mouse brain extraction network

To develop a general-purpose mouse brain extraction model, we constructed
whole-head templates from two publicly available T2-weighted datasets. The first
dataset, from the Center for Animal MRI (CAMRI) at the University of North
Carolina at Chapel Hill [@Hsu2021], includes 16 isotropic MRI volumes acquired
at $0.16 \times 0.16 \times 0.16$ mm$^3$ resolution. The second dataset
[@Reshetnikov2021] comprises 88 specimens acquired in three orthogonal 2D views
(coronal, axial, sagittal) at $0.08 \times 0.08$ mm$^3$ in-plane resolution with
0.5 mm slice thickness. These orthogonal 2D acquisitions were reconstructed into
high-resolution 3D volumes using a B-spline fitting algorithm
[@Tustison:2006aa]. Using this synthesized dataset and the CAMRI images, we
created two ANTsX-based population templates [@Avants:2010aa], each paired with
a manually delineated brain mask. These served as the basis for training an
initial template-based brain extraction model.  Deep learning training of the
network employed aggressive data augmentation strategies, including bias field
simulation, histogram warping, random spatial deformation, noise injection, and
anisotropic resampling. This enabled the model to generalize beyond the two
templates. The initial model was released through ANTsXNet and made publicly
available.

Subsequent community use led to further improvements. A research group applying
the tool to their own ex vivo T2-weighted mouse brain data contributed a third
template and associated mask (acquired at 0.08 mm isotropic resolution).
Incorporating this into the training data improved robustness and accuracy to an
independent dataset and extended the model’s generalizability. The refined model
is distributed through ANTsPyNet via ``antspynet.mouse_brain_extraction(...)``.

### Template-based mouse brain anatomical labeling

The AllenCCFv3 atlas and its hierarchical ontology, along with the DevCCF,
provide a strong foundation for developing region-wise anatomical labeling
models for multi-modal mouse brain imaging. Using the `allensdk` Python library,
we generated a coarse segmentation scheme by grouping anatomical labels into six
major regions: cerebral cortex, cerebral nuclei, brainstem, cerebellum, main
olfactory bulb, and hippocampal formation. These labels were mapped onto the P56
T2-weighted DevCCF template to serve as training targets. We trained a 3D
U-net–based segmentation network using this template and the same augmentation
strategies described for brain extraction. The model is publicly available via
ANTsXNet (`antspynet.mouse_brain_parcellation(...)`) and supports robust
anatomical labeling across diverse imaging geometries and contrasts.  The
inclusion of aggressive augmentation, including simulated anisotropy, enables
the model to perform well even on thick-slice input data. Internally, the model
reconstructs isotropic probability and label maps, facilitating downstream
morphometric analyses. For example, this network integrates with the ANTsX
cortical thickness estimation pipeline
(`antspynet.mouse_cortical_thickness(...)`) to produce voxelwise cortical
thickness maps, even when applied to anisotropic or limited-resolution mouse
brain data.

### Evaluation

\begin{figure}
\centering
  \includegraphics[width=0.75\textwidth]{Figures/diceWholeBrain.png}
\caption{Evaluation of the ANTsX mouse brain extraction on an
independent, publicly available dataset consisting of 12 specimens $\times$ 7
time points = 84 total images.  Dice overlap comparisons with the
user-generated brain masks provide good agreement with the automated results
from the brain extraction network.}
\label{fig:evaluation}
\end{figure}

\begin{figure}
\centering
\begin{subfigure}{0.25\textwidth}
  \centering
  \includegraphics[width=\linewidth]{Figures/AllenCCFv3_parcellation_slice91.png}
  \caption{}
  \label{fig:subp_a}
\end{subfigure}
\begin{subfigure}{0.25\textwidth}
  \centering
  \includegraphics[width=\linewidth]{Figures/NR5_M_Day0_slice53.png}
  \caption{}
  \label{fig:subp_b}
\end{subfigure} \\
\begin{subfigure}{.75\textwidth}
  \centering
  \includegraphics[width=\linewidth]{Figures/diceAllenCCFv3.png}
  \caption{}
  \label{fig:subc}
\end{subfigure}
\caption{Evaluation of the ANTsX mouse brain parcellation on the same dataset.
(a) T2-w DevCCF P56 with the described parcellation consisting of the cerebral
cortex, nuclei, brain stem, cerebellum, main olfactory bulb, and hippocampal
formation. (b) Sample subject (NR5 Day 0) with the proposed deep learning-based
segmentation. (c) Dice overlap for comparing the regional alignments between
registration using intensity information only and using intensity with the given
parcellation scheme.}
\label{fig:evaluationParcellation}
\end{figure}

For evaluation, we used an additional publicly available dataset
[@Rahman:2023aa] that is completely independent from the data used in training
the brain extraction and parcellation networks.  Data includes 12 specimens each
imaged at seven time points (Day 0, Day 3, Week 1, Week 4, Week 8, Week 20) with
in-house-generated brain masks for a total of 84 images.  Spacing is anistropic
with an in-plane resolution of $0.1 \times 0.1$ mm$^2$ and a slice thickness of
$0.5$ mm.  

Figure \ref{fig:evaluation} summarizes the whole brain overlap between the
provided segmentations for all 84 images and the results of applying the
proposed network.   Also, since mapping to the AllenCCFv3 atlas is crucial for
many mouse studies, we demonstrate the utility of the second network by
leveraging the labeled regions to perform anatomically-explicit alignment using
ANTsX multi-component registration instead of intensity-only registration. For
these data, the whole brain extraction demonstrates excellent performance across
the large age range.  And although the intensity-only image registration
provides adequate alignment, intensity with the regional parcellations
significantly improves those measures.

