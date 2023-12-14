import ants
import os
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import glob

os.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = "12"

annotation_directory = "../Data/P56xAlignedSimpleSegmentations/"
templates_directory = "../Data/P56xAlignedTemplates/"
output_directory = "../Data/Results/"

template_ids = tuple(reversed(("E11-5", "E13-5", "E15-5", "E18-5", "P04", "P14", "P56")))
time_points = np.flip(-1.0 * np.log(np.array((11.5, 13.5, 15.5, 18.5, 23, 33, 47))))

velocity_field = ants.image_read(output_directory + "velocity_field.nii.gz")

fixed_labels_file = annotation_directory + "P56x" + template_ids[0] + "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi_resampled.nii.gz"
fixed_labels = ants.image_read(fixed_labels_file)

##
# Warp P56 in a continuous manner from identity to E11.5
#

time_points = np.flip(-1.0 * np.log(np.linspace(11.5, 47, 50)))
normalized_time_points = (time_points - time_points[0]) / (time_points[-1] - time_points[0])

for i in range(len(normalized_time_points)):
    t = normalized_time_points[i]
    print("time point: ", str(t))
    displacement_field = ants.integrate_velocity_field(velocity_field, t, 0.0, 10)
    displacement_field_xfrm = ants.transform_from_displacement_field(displacement_field)
    warped_labels = displacement_field_xfrm.apply_to_image(fixed_labels, interpolation="nearestneighbor")
    geoms = ants.label_geometry_measures(warped_labels)    
    geoms.to_csv(output_directory + "P56WarpedVolumes_" + str(i) + ".csv")
    
