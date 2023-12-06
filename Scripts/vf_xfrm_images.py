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
normalized_time_points = (time_points - time_points[0]) / (time_points[-1] - time_points[0])

velocity_field = ants.image_read(output_directory + "velocity_field.nii.gz")

fixed_labels_file = annotation_directory + "P56x" + template_ids[0] + "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi_resampled.nii.gz"
fixed_labels = ants.image_read(fixed_labels_file)
fixed_image_file = "../Data/P56xAlignedTemplates/P56_MRI_50um/P56_MRI-fa_50um.nii.gz"
fixed_image = ants.image_read(fixed_image_file)
grid = ants.create_warped_grid(fixed_labels)

##
# Warp P56 in a continuous manner from identity to E11.5
#

time_points = np.array(np.linspace(0, 1, 20))
log_time_points = np.array(np.linspace(0, 1, 20))
for i in range(len(time_points)):
    log_time_points[i] = (math.exp(time_points[i]) - 1.0) / (math.exp(1) - 1.0)

for i in range(len(time_points)):
    t = (math.exp(time_points[i]) - 1.0) / (math.exp(1) - 1.0)
    print("time point: ", str(t))
    displacement_field = ants.integrate_velocity_field(velocity_field, t, 0.0, 10)
    displacement_field_xfrm = ants.transform_from_displacement_field(displacement_field)
    warped_labels = displacement_field_xfrm.apply_to_image(fixed_labels, interpolation="nearestneighbor")
    ants.image_write(warped_labels, output_directory + "P56xVelocityFieldWarped_" + "{:02d}".format(i) + ".nii.gz")
    warped_grid = displacement_field_xfrm.apply_to_image(grid, interpolation="linear")
    ants.image_write(warped_grid, output_directory + "P56xVelocityFieldWarpedGrid_" + "{:02d}".format(i) + ".nii.gz")
    warped_image = displacement_field_xfrm.apply_to_image(fixed_image, interpolation="linear")
    ants.image_write(warped_image, output_directory + "P56_MRI-faxVelocityFieldWarped_" + "{:02d}".format(i) + ".nii.gz")
    
##
# Warp each FA template to every other template
#

fa_template_files = list()
mask_brain_template_files = list()
for i in range(len(template_ids)):
    fa_template_files.append(glob.glob(templates_directory + template_ids[i] + "*/*fa*.nii.gz")[0])
    mask_brain_template_files.append(glob.glob(templates_directory + template_ids[i] + "*/*MaskBrain*.nii.gz")[0])

for i in range(len(template_ids)):
    for j in range(len(template_ids)):
        print("Warping ", template_ids[j], "to", template_ids[i])
        reference_template_mask_brain = ants.image_read(mask_brain_template_files[i])
        reference_template = ants.image_read(fa_template_files[i]) * reference_template_mask_brain
        moving_template_mask_brain = ants.image_read(mask_brain_template_files[j])
        moving_template = ants.image_read(fa_template_files[j]) * moving_template_mask_brain
        displacement_field = ants.integrate_velocity_field(velocity_field, normalized_time_points[i], normalized_time_points[j], 10)
        displacement_field_xfrm = ants.transform_from_displacement_field(displacement_field)
        warped_template = displacement_field_xfrm.apply_to_image(moving_template, interpolation="linear")
        ants.image_write(warped_template, output_directory + template_ids[i] + "fax" + template_ids[j] + "fa.nii.gz")

