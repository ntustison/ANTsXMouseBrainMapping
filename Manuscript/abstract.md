
# Abstract {-}

Large-scale, international collaborative efforts by members of the BRAIN
Initiative Cell Census Network (BICCN) consortium have recently begun
aggregating the most comprehensive reference database to date for diverse cell
type profiling of the mouse brain, which encompasses over 40 different
multi-modal profiling techniques from more than 30 research groups. One central
challenge for this integrative effort across different investigators and
laboratories has been the need to map these unique datasets into common
reference spaces such that the spatial, structural, and functional information
from different cell types can be jointly analyzed across modalities. However,
significant variations in the acquisition, tissue processing, and imaging
techniques across data types makes mapping such diverse data a multifarious
problem. Different data types exhibit unique tissue distortion and signal
characteristics that precludes a single mapping strategy from being generally
applicable across all cell type data. Diverse, and often specialized, mapping
approaches are needed to address the unique barriers present in each modality.
This work highlights modular atlas mapping strategies developed across three
separate BICCN studies using the Advanced Normalization Tools Ecosystem (ANTsX)
to map spatial transcriptomic (MERFISH) and high-resolution morphology (fMOST)
mouse brain data into the Allen Common Coordinate Framework (AllenCCFv3), and
developmental (MRI and LSFM) data into the Developmental Common Coordinate
Framework (DevCCF).  We discuss both common mapping strategies that can be
shared across modalities, and targeted strategies driven by specific challenges
from each data type.  Novel open-source contributions are also made publicly
available through ANTSX.  These include a velocity flow-based approach for
continuously mapping developmental trajectories such as that characterizing the
DevCCF and an automated framework for determining structural morphology solely
through the leveraging of publicly resources.  Finally, we provide general
guidance to aid investigators in their efforts to tailor these strategies to
address unique challenges in their data without the need to develop additional
specialized software.  

\clearpage