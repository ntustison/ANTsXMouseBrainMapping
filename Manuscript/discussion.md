
\clearpage
\newpage

# Discussion

The diverse mouse brain cell type profiles gathered through BICCN and associated
efforts provides a rich multi-modal resource to the research community. However,
despite significant progress, optimized leveraging of these valuable resources
is ongoing. A central component to data integration is accurately mapping novel
cell type data into CCFs for subsequent
processing and analysis. To meet these needs, tools for mapping mouse cell type
data must be both generally accessible to a wide audience of investigators, and
capable of handling distinct challenges unique to each data type. In this work,
we described modular ANTsX-based pipelines developed to address the needs of
three BICCN projects that cover distinct cell type data, including spatial
transcriptomic, morphological, and developmental data.  We highlighted how a
modular toolbox like ANTsX can be tailored to address problems unique to each
modality through leveraging a variety of ready-to-use powerful tools that have
been previously validated in multiple application scenarios.

Our MERFISH pipeline provides an example of how to map high-resolution spatial
transcriptomic data into the AllenCCFv3.  While the techniques employed for
mapping the sectioned data can be generally applicable to spatially transform
other serial histology images, much of the pipeline was designed to specifically
address known alignment challenges in the MERFISH data. Thus pipeline shows how
general ANTsX tools can be adapted to target highly specialized problems in
mouse cell type data.

In contrast to the MERFISH pipeline, our fMOST pipeline was designed to be a
more general solution that can be employed in other modalities. The pipeline
primarily uses previously developed ANTsX preprocessing and atlasing tools to
map fMOST data into the AllenCCFv3. The key component of the pipeline is the use
of a fMOST-specific average shape and intensity atlas to most effectively
address image registration in this context.  The mapping between the fMOST atlas
is generated once and reused for each new fMOST image. Lastly, ANTsX provides
point set transformation tools to allow the mappings found through the pipeline
to be directly applied to associated single-cell reconstructions from the fMOST
data to study neuronal morphology. 

The pipeline for continuously mapping the DevCCF data is also available in ANTsX
and is generally applicable for spatio-temporal mapping. With specific
application to the DevCCF, despite the significant expansion of available
developmental age templates beyond what existed previously, there are still
temporal gaps in the DevCCF which can be potentially sampled by future research
efforts. However, pioneering work involving time-varying diffeomorphic
transformations allow us to continuously situate the existing templates within a
velocity flow model.  This allows one to determine the diffeomorphic
transformation from any one temporal location to any other temporal location
within the time span defined by the temporal limits of the DevCCF. This
functionality is built on multiple ITK components including the B-spline
scattered data approximation technique for field regularization and velocity
field integration. This velocity field model permits intra-template comparison
and the construction of virtual templates where a template can be estimated at
any continuous time point within the temporal domain.  This novel application
can potentially enhance our understanding of intermediate developmental stages.

We also presented a mouse brain morphological pipeline for brain extraction and
brain parcellation using single-shot and few-shot learning with aggressive data
augmentation.  This approach attempts to circumvent (or at least minimize) the
typical requirement of large training datasets as with the human ANTsX pipeline
analog. However, even given our initial success on independent data, we
anticipate that refinements will be necessary.  Given that the ANTsX toolkit is
a dynamic effort undergoing continual improvement, we manually correct cases
that fail and use them for future training and refinement of network weights as
we have done for our human-based networks.  And, as demonstrated, we welcome
contributions from the community for improving these approache which, generally,
provide a way to bootstrap training data for manual refinement and future
generation of more accurate deep learning networks in the absence of other
applicable tools.

The ANTsX ecosystem is a powerful framework that has demonstrated applicability
to diverse cell type data in the mouse brain. This is further evidenced by the
many software packages that use various ANTsX components in their own
mouse-specific workflows. The extensive functionality of ANTsX makes it possible
to create complete processing pipelines without requiring the integration of
multiple packages or lengthy software development. These open-source components
not only perform well but are available across multiple platforms which
facilitates the construction of tailored pipelines for individual study
solutions. These components are also supported by years of development not only
by the ANTsX development team but by the larger ITK community.
