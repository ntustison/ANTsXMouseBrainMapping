
\clearpage
\newpage


# Discussion

The diverse mouse brain cell type profiles gathered through BICCN and associated
efforts provide a rich multi-modal resource to the research community. However,
despite significant progress, optimal leveraging of these valuable resources
remains an ongoing challenge. A central component to data integration is
accurately mapping novel cell type data into common coordinate frameworks (CCFs)
for subsequent processing and analysis. To meet these needs, tools for mapping
mouse brain data must be both broadly accessible and capable of addressing
challenges unique to each modality. In this work, we described modular
ANTsX-based pipelines developed to support three distinct BICCN efforts
encompassing spatial transcriptomic, morphological, and developmental data. We
demonstrated how a flexible image analysis toolkit like ANTsX can be tailored to
address specific modality-driven constraints by leveraging reusable, validated
components.

As part of collaborative efforts with the Allen Institute for Brain Science and
the broader BICCN initiative, we developed two modular pipelines for mapping
MERFISH and fMOST datasets to the AllenCCFv3. These workflows were designed to
accommodate the specific requirements of high-resolution transcriptomic and
morphological data while leveraging reusable components from the ANTsX
ecosystem.  The MERFISH pipeline incorporates preprocessing and registration
steps tailored to known anatomical and imaging artifacts in multiplexed spatial
transcriptomic data. While the general mapping strategy is applicable to other
sectioned histological datasets, these refinements demonstrate how
general-purpose tools can be customized to meet the demands of specialized
modalities. The fMOST workflow, in contrast, emphasizes reusability and
consistency across large datasets. It introduces an intermediate, canonical
fMOST atlas to stabilize transformations to the AllenCCFv3, reducing the need
for repeated manual alignment and enabling standardized mapping of single-neuron
reconstructions to a common coordinate framework.

Evaluation of both workflows followed established QA/QC protocols used at the
Allen Institute, emphasizing biologically meaningful criteria such as expected
gene-marker alignment (MERFISH) and accurate reconstruction of neuronal
morphology (fMOST). These domain-informed assessments, also used in prior
large-scale mapping projects [@Yao:2023aa], prioritize task-relevant
accuracy over other possible benchmarks such as Dice coefficients or landmark
distances. While formal quantitative scores were not reported for these specific
pipelines, they both demonstrate reliable, expert-validated performance in
collaborative contexts. Additional documentation and evaluation commentary are
available in the updated CCFAlignmentToolkit GitHub repository.

For developmental data, we introduced a velocity field–based model for
continuous interpolation between discrete DevCCF timepoints. Although the DevCCF
substantially expands coverage of developmental stages relative to prior
atlases, temporal gaps remain. The velocity model enables spatio-temporal
transformations within the full developmental interval and supports the
generation of virtual templates at unsampled ages. This functionality is built
using ANTsX components for velocity field optimization and integration, and
offers a novel mechanism for interpolating across the non-linear developmental
trajectory of the mouse brain. Such interpolation has potential utility for both
anatomical harmonization and longitudinal analyses.  Interestingly, long-range
transformations (e.g., P56 to E11.5) revealed anatomy evolving in plausible ways
yet sometimes diverging from known developmental patterns (e.g., hippocampal
shape changes) reflecting the input data and offering insight into temporal
gaps. These behaviors could assist future efforts to determine which additional
time points would most improve spatiotemporal coverage.

We also introduced a template-based deep learning pipeline for mouse brain
extraction and parcellation using aggressive data augmentation. This approach is
designed to reduce the reliance on large annotated training datasets, which
remain limited in the mouse imaging domain. Evaluation on independent data
demonstrates promising generalization, though further refinement will be
necessary. As with our human-based ANTsX pipelines, failure cases can be
manually corrected and recycled into future training cycles. Community
contributions are welcomed and encouraged, providing a pathway for continuous
improvement and adaptation to new datasets.

The ANTsX ecosystem offers a powerful foundation for constructing scalable,
reproducible pipelines for mouse brain data analysis. Its modular design and
multi-platform support enable researchers to develop customized workflows
without extensive new software development. The widespread use of ANTsX
components across the neuroimaging community attests to its utility and
reliability. As a continuation of the BICCN program, ANTsX is well positioned to
support the goals of the BRAIN Initiative Cell Atlas Network (BICAN) and future
efforts to extend these mapping strategies to the human brain.

