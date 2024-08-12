
## The Mouse Brain Parcellation Pipeline

\begin{figure}
\centering
\includegraphics[width=0.95\textwidth]{Figures/mousePipeline.pdf}
\caption{The mouse brain cortical parcellation pipeline integrating two 
deep learning components for brain extraction and brain parcellation 
prior to estimating cortical labels. Both deep learning networks
rely heavily on data augmentation on templates built from open 
data and provide an outline for further refinement and creating 
alternative parcellations for tailored research objectives.}
\label{fig:mouseKK}
\end{figure}

One of the most well-utilized pipelines in the ANTsX toolkit is the generation
of cortical thickness maps in the human brain from T1-weighted MRI.  Starting
with the novel Diffeomorphic Registration-based Cortical Thickness (DiReCT)
algorithm [@Das:2009uv], a complete algorithmic workflow was developed for both
cross-sectional [@Tustison:2014ab] and longitudinal [@Tustison:2019aa]
T1-weighted MR image data.  This contribution was later refactored using deep
learning [@Tustison:2021aa] leveraging the earlier results [@Tustison:2014ab] 
for training data.  

In the case of the mouse brain, the lack of training data and/or tools to
generate training data making analogous algorithmic development difficult. In
addition, mouse data is often characterized by unique issues such as frequent
anisotropic sampling which are often in sharp contrast to the high resolution
resources available within the community, e.g., AllenCCFv3 and DevCCF. Using
ANTsX and other publicly available data resources, we developed a complete mouse
brain structural morphology pipeline as illustrated in Figure \ref{fig:mouseKK}
and detailed below. 

### Two-shot mouse brain extraction network

In order to create a generalized mouse brain extraction network, we built
whole-head templates from two publicly available datasets.  The Center for
Animal MRI (CAMRI) dataset [@Hsu2021] from the University of North Carolina
at Chapel Hill consists of 16 T2-weighted MRI volumes of
voxel resolution $0.16 \times 0.16 \times 0.16 mm^3$.  The second
high-resolution dataset [@Reshetnikov2021] comprises 88 specimens each with
three spatially aligned canonical views with in-plane resolution of $0.08 \times
0.08 mm^2$ with a slice thickness of $0.5 mm$.  These three orthogonal views
were used to reconstruct a single high-resolution volume per subject using a
B-spline fitting algorithm developed in ANTsX [@Tustison:2006aa].  From these
two datasets, two symmetric isotropic ANTsX templates [@Avants:2010aa] were
generated analogous to the publicly available ANTsX human brain templates used
in previous research [@Tustison:2014ab]. Bias field simulation, intensity
histogram warping, noise simulation, random translation and warping, and random
anisotropic resampling in the three canonical directions were used for data
augmentation in training a T2-weighted brain extraction network.

### Single-shot mouse brain parcellation network

To create the network for generating a brain parcellation consistent with
cortical thickness estimation, we used the AllenCCFv3 and the associated
``allensdk`` Python library. Using ``allensdk``, a gross parcellation labeling
was generated from the fine Allen CCFv3 labeling which includes the cerebral
cortex, cerebral nuclei, brain stem, cerebellum, main olfactory bulb, and
hippocampal formation.  This labeling was mapped to the P56
component of the DevCCF. Both the T2-w P56 DevCCF and labelings, in
conjunction with the data augmentation described previously for brain 
extraction, was used to train a brain parcellation network.

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
cortical thickness pipeline on an independent dataset 
consisting of 12 specimens $\times$ 7 time points = 
84 total images.  (a) Dice overlap comparisons with the provided brain
masks provide generally good agreement with the brain extraction network.
(b) Cortical volume measurements show similar average quantities over
growth and development between the original anisotropic data and 
interpolated isotropic data.  (c) These results contrast with the cortical
thickness measurements which show that cortical thickness estimation 
in anisotropic space severely underestimates the actual values.}
\label{fig:evaluation}
\end{figure}

For evaluation, we used an additional publicly available dataset
[@Rahman:2023aa] which is completely independent from the data used in training
the brain extraction and parcellation networks.  Data includes 12 specimens each
imaged at seven time points (Day 0, Day 3, Week 1, Week 4, Week 8, Week 20) with
available brain masks.  In-plane resolution is $0.1 \times 0.1 mm^2$ with a
slice thickness of $0.5 mm$.  Since the training data is isotropic and data
augmentation includes downsampling in the canonical directions, each of the two 
networks learns mouse brain-specific interpolation such that one can perform prediction
on thick-sliced images, as, for example, in these evaluation data, and return isotropic
probability and thickness maps (a choice available to the user).  Figure 
\ref{fig:evaluation} summarizes the results of the evaluation and comparison between
isotropic and anisotropic cortical measurements in male and female specimens.




