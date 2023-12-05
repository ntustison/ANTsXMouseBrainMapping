import ants
import os
import pandas as pd
import numpy as np
import random
import math

os.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = "12"

annotation_directory = "../Data/AlignedSimpleSegmentations/"
registration_directory = annotation_directory + "PairwiseRegistrations/"
output_directory = "../Data/Results/"

################################
#
# A couple notes:
#   * We reverse the template id's because we use P56 to define the 
#     fixed reference frame and, therefore, the positive direction 
#     of the velocity field.  This isn't necessary as we could've 
#     easily chosen the opposite direction.
#   * We take the log of the time points to get a more even distribution
#     of the velocity field samples.  The only implication of this is
#     that one would need to take into account this transform when 
#     actually using the output velocity field to determine the transform
#     at a specific time.
#   * An additional modification to get a better sampling distribution is
#     to simply use the time point for P28 = 47 and use the P56 template.
#     
###############################

template_ids = tuple(reversed(("E11-5", "E13-5", "E15-5", "E18-5", "P04", "P14", "P56")))
time_points = np.flip(-1.0 * np.log(np.array((11.5, 13.5, 15.5, 18.5, 23, 33, 47))))
normalized_time_points = (time_points - time_points[0]) / (time_points[-1] - time_points[0])

fixed_labels_file = annotation_directory + "P56x" + template_ids[0] + "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi_resampled.nii.gz"
fixed_labels = ants.image_read(fixed_labels_file)

velocity_field_file = output_directory + "/velocity_field.nii.gz"
if not os.path.exists(velocity_field_file):
    raise ValueError("velocity field does not exist.")
    
print("Reading velocity field.")
velocity_field = ants.image_read(velocity_field_file)

# about P08, I'm guessing

normalized_time_point_for_template = 0.375
log_time_point = normalized_time_point_for_template * (time_points[-1] - time_points[0]) + time_points[0]
P_time_point = math.exp(-log_time_point) - 19
print("Creating pseudo-template at normalized time point: ", str(normalized_time_point_for_template), " (~P0", str(P_time_point), ")")

print("Warping P04")
P04_field = ants.integrate_velocity_field(velocity_field, normalized_time_point_for_template, normalized_time_points[2], 10)
P04_xfrm = ants.transform_from_displacement_field(P04_field)
P04_labels_file = annotation_directory + "P56x" + template_ids[2] + "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi_resampled.nii.gz"
P04_labels = ants.image_read(P04_labels_file)
P04_warped_labels = P04_xfrm.apply_to_image(P04_labels, reference=P04_labels, interpolation="nearestneighbor")
ants.image_write(P04_warped_labels, output_directory + "P04_to_P08_warped_labels.nii.gz")

print("Warping P14")
P14_field = ants.integrate_velocity_field(velocity_field, normalized_time_point_for_template, normalized_time_points[1], 10)
P14_xfrm = ants.transform_from_displacement_field(P14_field)
P14_labels_file = annotation_directory + "P56x" + template_ids[1] + "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi_resampled.nii.gz"
P14_labels = ants.image_read(P14_labels_file)
P14_warped_labels = P14_xfrm.apply_to_image(P14_labels, reference=P14_labels, interpolation="nearestneighbor")
ants.image_write(P14_warped_labels, output_directory + "P14_to_P08_warped_labels.nii.gz")

print("Generating template")
pseudo_template = ants.build_template(image_list=(P04_warped_labels, P14_warped_labels), iterations=4)
ants.image_write(pseudo_template, output_directory + "P08_pseudo_template_labels.nii.gz")

