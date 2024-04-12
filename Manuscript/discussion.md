
\clearpage
\newpage

# Discussion

The ANTsX ecosystem is a powerful framework that has demonstrated applicability
to multiple species and organ systems, including the mouse brain. This is
further evidenced by the many  software packages that use various ANTsX
components in their own mouse-specific workflows.  In and of itself, the
extensive functionality of ANTsX makes it possible to create complete processing
pipelines without requiring the integration of multiple packages. These
open-source components not only perform well but are available across multiple
platforms which facilitates the construction of tailored pipelines for
individual study solutions. These components are also supported by years of
development not only by the ANTsX development team but by the larger ITK
community.  

In the case of the development of the DevCCF, ANTsX was crucial in providing
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


