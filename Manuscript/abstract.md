
# Abstract {-}

Large-scale, international collaborative efforts by members of the BRAIN
Initiative Cell Census Network (BICCN) consortium are aggregating the most
comprehensive reference database to date for diverse cell type profiling of the
mouse brain, which encompasses over 40 different multi-modal profiling
techniques from more than 30 research groups. One central challenge for this
integrative effort has been the need to map these unique datasets into common
reference spaces such that the spatial, structural, and functional information
from different cell types can be jointly analyzed. However, significant
variation in the acquisition, tissue processing, and imaging techniques across
data types makes mapping such diverse data a multifarious problem. Different
data types exhibit unique tissue distortion and signal characteristics that
precludes a single mapping strategy from being generally applicable across all
cell type data. Tailored mapping approaches are often needed to address the
unique barriers present in each modality. This work highlights modular atlas
mapping strategies developed across separate BICCN studies using the Advanced
Normalization Tools Ecosystem (ANTsX) to map spatial transcriptomic (MERFISH)
and high-resolution morphology (fMOST) mouse brain data into the Allen Common
Coordinate Framework (AllenCCFv3), and developmental (MRI and LSFM) data into
the Developmental Common Coordinate Framework (DevCCF).  We discuss common
mapping strategies that can be shared across modalities and driven by specific
challenges from each data type.  These mapping strategies include novel
open-source contributions that are made publicly available through ANTsX.  These
include 1) a velocity flow-based approach for continuously mapping developmental
trajectories such as that characterizing the DevCCF and 2) an automated
framework for determining structural morphology solely through the leveraging of
publicly resources.  Finally, we provide general guidance to aid investigators
to tailor these strategies to address unique data challenges without the need to
develop additional specialized software.  

\clearpage