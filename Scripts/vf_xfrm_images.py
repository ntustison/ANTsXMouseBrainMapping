import ants
import os
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

os.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = "12"

annotation_directory = "../Data/P56xAlignedSimpleSegmentations/"
output_directory = "../Data/Results/"

template_ids = tuple(reversed(("E11-5", "E13-5", "E15-5", "E18-5", "P04", "P14", "P56")))
velocity_field = ants.image_read(output_directory + "velocity_field.nii.gz")

fixed_labels_file = annotation_directory + "P56x" + template_ids[0] + "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi_resampled.nii.gz"
fixed_labels = ants.image_read(fixed_labels_file)
fixed_image_file = "../Data/P56xAlignedTemplates/P56_MRI_50um/P56_MRI-fa_50um.nii.gz"
fixed_image = ants.image_read(fixed_image_file)
grid = ants.create_warped_grid(fixed_labels)

time_points = np.array(np.linspace(0, 1, 20))
log_time_points = np.array(np.linspace(0, 1, 20))
for i in range(len(time_points)):
    log_time_points[i] = (math.exp(time_points[i]) - 1.0) / (math.exp(1) - 1.0)

fig, ax = plt.subplots()
ax.plot(time_points, log_time_points)
ax.set(xlabel="time_point", ylabel="log_time_point", title="XX")
ax.grid()
fig.savefig("/Users/ntustison/Desktop/time_point.png")

for i in range(len(time_points)):
    t = (math.exp(time_points[i]) - 1.0) / (math.exp(1) - 1.0)
    print("time point: ", str(t))
    displacement_field = ants.integrate_velocity_field(velocity_field, t, 0.0, 10)
    displacement_field_xfrm = ants.transform_from_displacement_field(displacement_field)
    # warped_labels = displacement_field_xfrm.apply_to_image(fixed_labels, interpolation="nearestneighbor")
    # ants.image_write(warped_labels, output_directory + "P56xVelocityFieldWarped_" + "{:02d}".format(i) + ".nii.gz")
    # warped_grid = displacement_field_xfrm.apply_to_image(grid, interpolation="linear")
    # ants.image_write(warped_grid, output_directory + "P56xVelocityFieldWarpedGrid_" + "{:02d}".format(i) + ".nii.gz")
    warped_image = displacement_field_xfrm.apply_to_image(fixed_image, interpolation="linear")
    ants.image_write(warped_image, output_directory + "P56_MRI-faxVelocityFieldWarped_" + "{:02d}".format(i) + ".nii.gz")
