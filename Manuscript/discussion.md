
\clearpage
\newpage

# Discussion

The diverse mouse brain cell type profiles gathered through BICCN and associated efforts provides a rich multi-modal resource to the community. However, despite significant progress, full integration of these valuable resources is not yet complete. Central to the data integration is a continued need to accurately map each unique dataset into common coordinate frameworks (CCFs) so that they can be accessed in connection with each other. Additionally, the ability to map novel cell type data in the future to these existing BICCN resources is vital for effective utilization of this endeavor and the continuation of its goals. To meet these needs, tools for mapping mouse cell type data must be both generally accessible to a wide audience of investigators, and still capable of handling distinct challenges unique to each data type.

In this work, we describe modular ANTsX-based pipelines developed to address the needs of three BICCN projects that cover distinct cell type data, including spatial transcriptomic, morphology, and developmental data. We highlight how a modular toolbox like ANTsX can be tailored to address problems unique to each modality while still leveraging a variety of ready-to-use powerful tools that have been externally validated.

Our MERFISH pipeline provides an example of how to map high-resolution spatial transcriptomic data into the AllenCCFv3. Since full brain large-scale transcriptomics is still rare and difficult to collect, the pipeline focuses on achieving the best possible anatomical alignment and fully utilizing the available data. While the techniques employed for mapping the sectioned data can be generally applicable to map other serial histology images, many parts of the pipeline were designed to address very specific known alignment challenges in the MERFISH data using a series of iterative registration steps. The pipeline shows how general tools available in ANTsX can be adapted to target highly specialized problems in mouse cell type data.

In contrast to the MERFISH pipeline, our fMOST pipeline was designed to be a more general solution that can be employed in other modalities. The pipeline primarily uses previously developed ANTsX preprocessing and atlasing tools to map fMOST data into the AllenCCFv3. The key component of the pipeline is the use of a fMOST specific average atlas to greatly simplify the image registration problem. This average atlas, also constructed using pre-existing ANTsX tools, allows for a one-time canonical alignment from the fMOST atlas to the AllenCCFv3 to be transferred and used for mapping new fMOST images. Lastly, ANTsX provides point set transformation tools to allow the mappings found through the pipeline to be directly applied to associated single-cell reconstructions from the fMOST data to study neuronal morphology. 

Our DevCCF pipeline shows the application of the toolkit for temporospatial developmental data. ANTsX was crucial in providing
necessary functionality for yielding high quality output.  For the generation of
the individual developmental stage multi-modal, symmetric templates, ANTsX is
unique amongst image analysis software packages in providing existing solutions
for template generation which have been thoroughly vetted, including being used
in several studies over the years, and which continue to be under active
refinement.  At its core, computationally efficient and quality template
generation requires the use of precision pairwise image mapping functionality
which, historically, is at the origins of the ANTsX ecosystem. Moreover, these
mapping capabilities extend beyond template generation to the mapping of other
image data (e.g., gene expression maps) to a selected template for providing
further insight into the mouse brain.  

With respect to the DevCCF, despite the significant expansion of available
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

We also presented a mouse brain pipeline for brain extraction, parcellation, and
cortical thickness using single-shot and two-shot learning with data
augmentation.  This approach attempts to circumvent (or at least minimize) the
typical requirement of large training datasets as with the human ANTsX pipeline
analog. However, even given our initial success on independent data, we fully
anticipate that refinements will be necessary.  Given that the ANTsX toolkit is a
dynamic effort undergoing continual improvement, we manually correct cases that fail
and use them for future training and refinement of network weights as we have
done for our human-based networks.  Generally, these approaches provide a way to
bootstrap training data for manual refinement and future generation of more
accurate deep learning networks in the absence of other applicable tools.

The ANTsX ecosystem is a powerful framework that has demonstrated applicability
to diverse cell type data in the mouse brain. This is
further evidenced by the many software packages that use various ANTsX
components in their own mouse-specific workflows. In and of itself, the extensive functionality of ANTsX makes it possible to create complete processing
pipelines without requiring the integration of multiple packages or lengthy software development. These
open-source components not only perform well but are available across multiple
platforms which facilitates the construction of tailored pipelines for
individual study solutions. These components are also supported by years of
development not only by the ANTsX development team but by the larger ITK
community.
