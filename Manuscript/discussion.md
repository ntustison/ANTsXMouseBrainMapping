
\clearpage
\newpage

# Discussion {-}

The ANTsX ecosystem is a powerful framework that has demonstrated  
applicability to multiple species and organ systems, including the mouse brain.  
This has been demonstrated in many ways including the significant number of
external software packages that use various ANTsX components in their own
mouse-specific workflows.  The extensive functionality of ANTsX makes it
possible to create complete processing pipelines without requiring multiple
packages which often have limited cross-compatibility evaluation.  
These open-source ANTsX components not only perform well but are available
across multiple popular platforms (e.g., R and Python) which facilitates the
construction of tailored pipelines for individual study solutions. These
components are also supported by years of development not only by the ANTsX
development team but by the larger ITK community.  

In the case of the development of the DevCCF, ANTsX was crucial in providing
necessary functionality for yielding high quality output.  First, for the
generation of the individual developmental stage multi-modal, symmetric templates,
ANTsX is unique amongst image analysis software packages in providing existing
solutions for template generation which have been vetted, including being used
in several studies over the years, and which continue to be under active 
refinement.  At its core, computationally efficient and quality template 
generation requires the use of precision pairwise image mapping functionality
which, historically, is at the origins of the ANTsX ecosystem.  And these 
mapping capabilities extend beyond template generation to the mapping of 
other image data (e.g., gene expression maps) to template for providing further
insight into the mouse brain.  

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
can potentially enhance our understanding of intermediate developmental states.
To increase its impact and reproduce the results shown previously, we have made 
the data and code publicly available at \url{https://github.com/ntustison/DevCCF-Velocity-Flow}.

Although ANTsX is quite evolved in its development and functionality, there are
several areas which are currently under active development or consideration for
further expansion.  Most notably, as in our human applications, deep learning
has had a significant impact in steering our attention.  Core functionality,
such as brain extraction for mouse brain mapping, would benefit from increasing
the number of available modalities.   As with much deep learning development, 
such work will require additional data but is significantly facilitated by the 
tools that we have created in both ANTsPyNet and ANTsRNet.  Related would be the 
utility of the development of mouse brain parcellation tools such as our 
``antspynet.desikan_killiany_tourville_labeling(...)`` tool.
