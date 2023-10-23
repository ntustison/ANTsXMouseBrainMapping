import ants
import os
import pandas as pd
import numpy as np

os.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = "4"

annotation_directory = "/Users/ntustison/Data/JimGee/AllenDevelopmentalVelocityFlows/AlignedSimpleSegmentations/"
output_directory = "/Users/ntustison/Data/JimGee/AllenDevelopmentalVelocityFlows/Registrations/"

template_ids = tuple(reversed(("E11-5", "E13-5", "E15-5", "E18-5", "P04", "P14", "P56")))
velocity_field = ants.image_read(output_directory + "P56xE11-5_velocity_field.nii.gz")

total_field = ants.compose_displacement_fields(ants.integrate_velocity_field(velocity_field, 0.33, 0.85, 10),
                                               ants.integrate_velocity_field(velocity_field, 0.85, 0.33, 10))
total_field = ants.compose_displacement_fields(ants.integrate_velocity_field(velocity_field, 0.0, 1.0, 100),
                                               ants.integrate_velocity_field(velocity_field, 1.0, 0.0, 100))
ants.image_write(total_field, "~/Desktop/total_field.nii.gz")




updated_fixed_points = np.zeros(point_sets[0].shape)
updated_moving_points = np.zeros(point_sets[0].shape)
t_index = 1
t = 0.5
time_points = np.array((0, 0.5, 1.0))
number_of_integration_steps = 10

integrated_forward_field = ants.integrate_velocity_field(velocity_field, time_points[t_index-1], t, number_of_integration_steps)
integrated_forward_field_xfrm = ants.transform_from_displacement_field(integrated_forward_field)
for j in range(updated_fixed_points.shape[0]):
    updated_fixed_points[j,:] = integrated_forward_field_xfrm.apply_to_point(tuple(point_sets[t_index-1][j,:]))

integrated_inverse_field = ants.integrate_velocity_field(velocity_field, time_points[t_index], t, number_of_integration_steps)
integrated_inverse_field_xfrm = ants.transform_from_displacement_field(integrated_inverse_field)
for j in range(updated_moving_points.shape[0]):
    updated_moving_points[j,:] = integrated_inverse_field_xfrm.apply_to_point(tuple(point_sets[t_index][j,:]))

error = np.mean(np.sqrt(np.sum(np.square(updated_moving_points - updated_fixed_points), axis=1, keepdims=True)))


grid = ants.create_warped_grid(fixed_labels)
inverse_warped_grid = integrated_inverse_field_xfrm.apply_to_image(grid, interpolation="linear")
ants.plot(inverse_warped_grid)
forward_warped_grid = integrated_forward_field_xfrm.apply_to_image(grid, interpolation="linear")
ants.plot(forward_warped_grid)


fixed_labels_file = annotation_directory + "P56x" + template_ids[0] + "_LABELS.nii.gz"
fixed_labels = ants.image_read(fixed_labels_file)
fixed_labels = ants.resample_image(fixed_labels, resample_params=velocity_field.shape[:3], use_voxels=True, interp_type=0)
grid = ants.create_warped_grid(fixed_labels)

# time_points = np.array(np.linspace(1, 0, len(template_ids)))
time_points = np.array(np.linspace(1, 0, 50))
for i in range(len(time_points)):
    print(i)
    displacement_field = ants.integrate_velocity_field(velocity_field, time_points[i], 0.0, 10)
    displacement_field_xfrm = ants.transform_from_displacement_field(displacement_field)
    warped_image = displacement_field_xfrm.apply_to_image(fixed_labels, interpolation="nearestneighbor")
    ants.image_write(warped_image, output_directory + "WarpedImages/" + "warped_" + template_ids[0] + "_" + "{:02d}".format(i) + ".nii.gz")
    warped_grid = displacement_field_xfrm.apply_to_image(grid, interpolation="linear")
    ants.image_write(warped_grid, output_directory + "WarpedImages/" + "warpedgrid_" + template_ids[0] + "_" + "{:02d}".format(i) + ".nii.gz")
