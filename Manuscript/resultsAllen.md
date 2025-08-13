
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
         the requisite transforms to map individual images
         to the CCF.}
\label{fig:allenpipelines}
\end{figure*}


## AllenCCFv3 brain image mapping

### Mapping multiplexed error-robust fluorescence in situ hybridization (MERFISH) data

**Overview.** We developed an ANTsX-based pipeline to map spatial transcriptomic
MERFISH data into the AllenCCFv3 (Figure \ref{fig:allenpipelines}(a)). This
approach was used in recent efforts to create a high-resolution transcriptomic
atlas of the mouse brain [@Yao:2023aa]. The pipeline maps spatial gene expression 
patterns from MERFISH onto anatomical labels in the AllenCCFv3.
It includes MERFISH-specific preprocessing steps such as section reconstruction,
label generation from spatial transcriptomic maps, and anatomical correspondence
mapping. Alignment proceeds in two stages: 1) 3D affine registration and
section matching of the AllenCCFv3 to the MERFISH data, and 2) linear + deformable 
2D section-wise alignment between matched MERFISH and atlas slices. These
transformations are concatenated to produce a complete mapping from each MERFISH 
data to AllenCCFv3.

**Data.** MERFISH imaging was performed on cryosectioned brains from C57BL/6
mice using previously described protocols [@Yao:2023aa]. Brains were placed into
an optimal cutting temperature (OCT) compound (Sakura FineTek 4583) stored at
-80$^\circ$.  The fresh frozen brain was sectioned at 10 $\mu$m on Leica 3050 S
cryostats at intervals of 200 $\mu$m to evenly cover the brain. A set of 500
genes was selected to distinguish $\sim5200$ transcriptomic clusters. Raw
MERSCOPE data were decoded using Vizgen software (v231). Cell segmentation was
performed using Cellpose [@Liu:2023aa;@Stringer:2021aa] based on DAPI and PolyT
stains which was propagated to adjacent slices across z-planes. Each MERFISH
cell was assigned a transcriptomic identity by mapping to a scRNA-seq reference
taxonomy.

**Evaluation.** Alignment quality was evaluated iteratively by an expert
anatomist, guided by expected gene-marker correspondences to AllenCCFv3 regions.
As previously reported [@Yao:2023aa], further assessment of the alignment
showed that, of the 554 terminal regions (gray matter only in the AllenCCFv3),
only seven small subregions did not contain cells from the MERFISH dataset post
registration: frontal pole, layer 1 (FRP1), FRP2/3, FRP5; accessory olfactory
bulb, glomerular layer (AOBgl); accessory olfactory bulb, granular layer
(AOBgr); accessory olfactory bulb, mitral layer (AOBmi); and accessory
supraoptic group (ASO).


### Mapping fluorescence micro-optical sectioning tomography (fMOST) data

**Overview.** We also constructed a pipeline for mapping fMOST images to the
AllenCCFv3 using ANTsX (Figure \ref{fig:allenpipelines}(b)). The approach
leverages a modality-specific average fMOST atlas as an intermediate target,
adapted from previous work in human and mouse brain mapping
[@Avants:2010aa;@jia:2011aa;@tang:2009aa;@dewey:2017aa;@perens:2023aa;@Wang:2020aa;@qu:2022aa;@Kronman:2024aa].
The atlas was constructed from 30 fMOST images selected to capture
representative variability in anatomical shape and image intensity across the
population. Preprocessing includes cubic B-spline downsampling to match the
25 $\mu$m isotropic AllenCCFv3 resolution, stripe artifact suppression using 
a 3D notch filter implemented with SciPy’s frequency-domain filtering tools, 
and N4 bias field correction [@Tustison:2010ac]. A one-time,
annotation-driven alignment registers the fMOST atlas to AllenCCFv3 using
landmark-based registration of key structures. This canonical mapping is then
reused.  New fMOST specimens are first aligned to the fMOST atlas using standard
intensity-based registration, and the concatenated transforms yield full spatial
normalization to the AllenCCFv3. This same mapping can be applied to neuron
reconstructions to facilitate population-level analysis of morphology and
spatial distribution.

**Data.** fMOST imaging was performed on 55 mouse brains with sparse transgenic
labeling of neuron populations [@Rotolo:2008aa;@Peng:2021aa] using the
high-throughput fMOST platform [@Gong:2016aa; @Wang:2021aa]. Voxel resolution
was $0.35\times 0.35\times 1.0$ $\mu$m$^3$. Two imaging channels were acquired:
GFP-labeled neuron morphology (green), and propidium iodide counterstaining for
cytoarchitecture (red). Alignment was performed using the red channel for its
greater contrast, though multi-channel mapping is also supported.

**Evaluation.** The canonical mapping from the fMOST atlas to AllenCCFv3 was
evaluated using both quantitative and qualitative approaches. Dice similarity
coefficients were computed between corresponding anatomical labels in the fMOST
atlas and AllenCCFv3 following registration. These labels were manually
annotated or adapted from existing atlas segmentations. Representative Dice
scores included: whole brain (0.99), caudate putamen (0.97), fimbria (0.91),
posterior choroid plexus (0.93), anterior choroid plexus (0.96), optic chiasm
(0.77), and habenular commissure (0.63). In addition to these quantitative
assessments, each registered fMOST specimen was evaluated qualitatively. An
expert anatomist reviewed alignment accuracy and confirmed structural
correspondence. Neuron reconstructions from individual brains were also
transformed into AllenCCFv3 space, and their trajectories were visually
inspected to confirm anatomical plausibility and preservation of known
projection patterns.
