# allensdk.readthedocs.io/en/latest/_static/examples/nb/reference_space.html

from pathlib import Path
import os
import numpy as np

import ants

from allensdk.core.reference_space_cache import ReferenceSpaceCache

# Get template
# from allensdk.core.mouse_connectivity_cache import MouseConnectivityCache
# mcc = MouseConnectivityCache(resolution=50)
# rsp = mcc.get_reference_space()
# mcc.get_template_volume("template.nrrd")

output_dir = '.'
reference_space_key = os.path.join('annotation', 'ccf_2017')
resolution = 50

rspc = ReferenceSpaceCache(resolution, reference_space_key, manifest=Path(output_dir)/'manifest.json')
rsp = rspc.get_reference_space("reference.nrrd", "annotation.nrrd")

tree = rspc.get_structure_tree(structure_graph_id=1)

structure_names = ['Cerebral cortex', 'Cerebral nuclei', 'Brain stem', 'Cerebellum', 'Main olfactory bulb', 'Hippocampal formation']
regions = tree.get_structures_by_name(structure_names)

reference = ants.image_read("/Users/ntustison/Data/Mouse/AllenTemplate/template.nii.gz")
combined_mask = reference * 0
# combined_mask_array = combined_mask.numpy()
# hemisphere_array = np.zeros(combined_mask_array.shape)
# hemisphere_array[:,:,102:] = 1

masks = list()
for i in range(len(regions)):
    print("Making mask: ", structure_names[i])
    mask_array = rsp.make_structure_mask([regions[i]['id']])
    mask = ants.from_numpy(mask_array, origin=reference.origin,
                           spacing=reference.spacing, 
                           direction=reference.direction)
    mask = mask * (i + 1)
    combined_mask = combined_mask + mask
    
ants.image_write(combined_mask, output_dir + "/combined_mask.nii.gz")

