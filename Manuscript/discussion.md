
\clearpage
\newpage

# Discussion {-}

The ANTsX ecosystem is a powerful framework that has demonstrated applicability
to multiple species and organ systems, including the mouse brain. This is
further evidenced by the many other software packages that use various ANTsX
components in their own mouse-specific workflows.  The extensive functionality
of ANTsX per se makes it possible to create complete processing pipelines
without requiring the integration of multiple packages. These open-source ANTsX
components not only perform well but are available across multiple popular
platforms which facilitates the construction of tailored pipelines for
individual study solutions. These components are also supported by years of
development not only by the ANTsX development team but by the larger ITK
community.  

In the case of the development of the DevCCF, ANTsX was crucial in providing
necessary functionality for yielding high quality output.  First, for the
generation of the individual developmental stage multi-modal, symmetric
templates, ANTsX is unique amongst image analysis software packages in providing
existing solutions for template generation which have been thoroughly vetted,
including being used in several studies over the years, and which continue to be
under active refinement.  At its core, computationally efficient and quality
template generation requires the use of precision pairwise image mapping
functionality which, historically, is at the origins of the ANTsX ecosystem.
And these mapping capabilities extend beyond template generation to the mapping
of other image data (e.g., gene expression maps) to template for providing
further insight into the mouse brain.  

Despite the significant expansion of available developmental age templates
beyond what previously existed (e.g., Allen CCFv3), there still exist temporal
gaps in the DevCCF.  However, pioneering work involving diffeomorphic
transformations allowed us to continuously situate the existing templates within
a time-varying velocity flow model.  This allows one to determine the
diffeomorphic transformation from any one temporal location to any other
temporal location within the time span defined by the E11.5 and P56 templates.
This functionality is built on multiple components from the Insight Segmentation
and Registraiton Toolkit including the B-spline scattered data approximation
technique for field regularization and velocity field integration using fourth
order Runge-Kutta. This velocity field model permits intra-template comparison
and the construction of virtual templates where a template can be estimated at
any continuous time point within the temporal domain.  This novel application
can potentially enhance our understanding of intermediate developmental stages.

We also presented a mouse brain pipeline for brain extraction, parcellation, and
cortical thickness that did not necessitate the extensive quantity of data
required for training our analogous human brain pipeline.  



To increase its impact and reproduce the results shown previously, we have made 
the data and code publicly available at \url{https://github.com/ntustison/ANTsXMouseBrainMapping}.

