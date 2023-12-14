<!--
## The ANTs Ecosystem  {-}
-->

As noted above, many of the existing approaches for image data processing of
mouse brain use ANTsX tools for core steps in various workflows, particularly
its pairwise, intensity-based image registration tools and bias field
correction. Historically, ANTsX development is originally based on fundamental
approaches to image mapping [@Bajcsy:1982aa;@Bajcsy:1989aa;@Gee:2003aa] which
resulted in such core contributions to the field as the Symmetric Normalization
(SyN) algorithm [@Avants:2008aa].  Since its development, various independent
platforms have been used to evaluate ANTsX image registration capabilities in
the context of different application foci (e.g., multi-site brain MRI data
[@Klein:2009aa], pulmonary CT data [@Murphy:2011aa]), and most recently multi-modal
brain registration in the presence of tumors [@Baheti:2021aa]. 

\input{antsx_functionality_table}

Apart from its founding contribution, ANTsX is a comprehensive biological and
medical image analysis toolkit, that comprises additional functionality such as
template generation, general data approximation, and deep learning networks
specifically trained for mouse data (see Table \ref{table:methods}). The
collective use of the toolkit has demonstrated superb performance in multiple
application areas (e.g., consensus labeling [@Wang:2013ab], brain tumor
segmentation [@Tustison:2014aa], and cardiac motion estimation
[@Tustison:2015ab]).  Importantly, ANTs is built on the Insight Toolkit (ITK)
deriving benefit from a very capable open-source community of scientists and 
programmers as well as providing a venue for algorithmic contributions.

