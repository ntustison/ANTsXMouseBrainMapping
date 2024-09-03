
## Automated structural parcellations of the mouse brain

<!-- One of the most well-utilized pipelines in the ANTsX toolkit is the generation
of cortical thickness maps in the human brain from T1-weighted MRI.  Starting
with the novel Diffeomorphic Registration-based Cortical Thickness (DiReCT)
algorithm [@Das:2009uv], a complete algorithmic workflow was developed for both
cross-sectional [@Tustison:2014ab] and longitudinal [@Tustison:2019aa]
T1-weighted MR image data.  This contribution was later refactored using deep
learning [@Tustison:2021aa] leveraging the earlier results [@Tustison:2014ab] 
for training data.   -->


\begin{figure}
\centering
\includegraphics[width=0.95\textwidth]{Figures/mousePipeline.pdf}
\caption{The mouse brain cortical parcellation pipeline integrating two deep
learning components for brain extraction and brain parcellation prior to
estimating cortical labels. Both deep learning networks rely heavily on
aggressive data augmentation on templates built from open data and provide an
outline for further refinement and creating alternative parcellations for
tailored research objectives.  Possible applications include
voxelwise cortical thickness measurements.}
\label{fig:mouseKK}
\end{figure}

Brain parcellation strategies for the mouse brain are pivotal for understanding
the complex organization and function of murine nervous system [@Chon:2019aa].
By dividing the brain into distinct regions based on anatomical, physiological,
or functional characteristics, researchers can investigate specific areas in
isolation and identify their roles in various behaviors and processes. For
example, such parcellation schemes can help elucidate the spatial distribution
of gene expression patterns [@Tasic:2016aa] as well as identify functional
regions involved in specific cognitive tasks [@Bergmann:2020aa]. 

Although deep learning techniques have been used to develop useful parcellation
tools for human brain research (e.g., SynthSeg [@Billot:2023aa], ANTsXNet
[@Tustison:2021aa]), analogous development for the mouse brain is limited.  In
addition, mouse data is often characterized by unique imaging issues such as
extreme anisotropic sampling which are often in sharp contrast to the high
resolution template-based resources available within the community, e.g.,
AllenCCFv3 and DevCCF. We demonstrate how one can use the ANTsX tools to develop
a complete mouse brain structural morphology pipeline as illustrated in Figure
\ref{fig:mouseKK} and detailed below. 

### Two-shot mouse brain extraction network

In order to create a generalized mouse brain extraction network, we built
whole-head templates from two publicly available datasets.  The Center for
Animal MRI (CAMRI) dataset [@Hsu2021] from the University of North Carolina at
Chapel Hill consists of 16 T2-w MRI volumes of voxel resolution $0.16
\times 0.16 \times 0.16 mm^3$.  The second high-resolution dataset
[@Reshetnikov2021] comprises 88 specimens each with three spatially aligned
canonical views with in-plane resolution of $0.08 \times 0.08 mm^2$ with a slice
thickness of $0.5 mm$.  These three orthogonal views were used to reconstruct a
single high-resolution volume per subject using a B-spline fitting algorithm
available in ANTsX [@Tustison:2006aa].  From these two datasets, two symmetric
isotropic ANTsX templates [@Avants:2010aa] were generated analogous to the
publicly available ANTsX human brain templates used in previous research
[@Tustison:2014ab]. Bias field simulation, intensity histogram warping, noise
simulation, random translation and warping, and random anisotropic resampling in
the three canonical directions were used for data augmentation in training a
T2-w brain extraction network.

### Single-shot mouse brain parcellation network

AllenCCFv3 and its hierarchical ontological labeling, along with the DevCCF,
provides the necessary data for developing a tailored structural parcellation
network for multi-modal imaging.  The ``allensdk`` Python library permits the
creation of any gross parcellation based on the AllenCCFv3 ontology.  For
example, using ``allensdk`` we coalesced the labels to the following six major
structures:  cerebral cortex, cerebral nuclei, brain stem, cerebellum, main
olfactory bulb, and hippocampal formation.  This labeling was mapped to the P56
component of the DevCCF for use with the T2-w template component. Both the T2-w
P56 DevCCF and labelings, in conjunction with the data augmentation described
previously for brain extraction, were used to train the proposed brain
parcellation network.  Note that other brain parcellation networks have also
been trained using alternative regions and parcellation schemes and are
available in the same ANTsXNet functionality.

### Evaluation

\begin{figure}
\centering
\begin{subfigure}{0.5\textwidth}
  \centering
  \includegraphics[width=\linewidth]{Figures/diceWholeBrain.png}
  \caption{}
  \label{fig:suba}
\end{subfigure}\\
\begin{subfigure}{0.5\textwidth}
  \centering
  \includegraphics[width=\linewidth]{Figures/corticoPlot.png}
  \caption{}
  \label{fig:subb}
\end{subfigure}%
\begin{subfigure}{.5\textwidth}
  \centering
  \includegraphics[width=\linewidth]{Figures/kkPlot.png}
  \caption{}
  \label{fig:subc}
\end{subfigure}
\caption{Evaluation of the ANTsX mouse brain extraction, parcellation, and
cortical thickness pipeline on an independent dataset consisting of 12 specimens
$\times$ 7 time points = 84 total images.  (a) Dice overlap comparisons with the
user-generated brain masks provide good agreement with the automated results
from the brain extraction network. (b) Cortical volume measurements show similar
average quantities over growth and development between the original anisotropic
data and interpolated isotropic data.  (c) The volumetric comparative results
contrast with the cortical thickness measurements which illustrate estimation in
anisotropic space severely underestimates the actual values in comparison with
the isotropic prediction.}
\label{fig:evaluation}
\end{figure}

Although the utility of the proposed brain parcellation framework is highly
dependent on the specific application, we demonstrate the utility through the
generation of cortical thickness maps [@Das:2009uv] which leverages both brain
parcellation and the capabilities of mouse brain-based isotropic interpolation
for anisotropic data.  Cortical thickness has demonstrated utility in both human
(e.g., [@Tustison:2014ab;@Tustison:2019aa]) and non-human data (e.g., canines
[@Grewal:2020aa], dolphins [@Avelino-de-Souza:2024aa], non-human primates
[@Demirci:2023aa]) including the mouse brain
[@Lerch:2008aa;@Lee:2011aa;@Zoller:2018aa;@zhang:2021aa].

For evaluation, we used an additional publicly available dataset
[@Rahman:2023aa] which is completely independent from the data used in training
the brain extraction and parcellation networks.  Data includes 12 specimens each
imaged at seven time points (Day 0, Day 3, Week 1, Week 4, Week 8, Week 20) with
in-house-generated brain masks.  Spacing is anistropic with an in-plane
resolution of $0.1 \times 0.1 mm^2$ and a slice thickness of $0.5 mm$.  Since
the training data is isotropic and data augmentation includes downsampling in
the canonical directions, each of the two networks learns mouse brain-specific
interpolation such that one can perform prediction on thick-sliced images, as,
for example, in these evaluation data, and return isotropic probability and
thickness maps (a choice available to the user).  Figure \ref{fig:evaluation}
summarizes the results of the evaluation and comparison between isotropic and
anisotropic cortical measurements in male and female specimens.




