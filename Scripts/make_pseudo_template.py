import ants
import os
import pandas as pd
import numpy as np
import random
import math
import glob

os.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = "12"

annotation_directory = "../Data/AlignedSimpleSegmentations/"
registration_directory = annotation_directory + "PairwiseRegistrations/"
output_directory = "../Data/Results/"
templates_directory = "../Data/P56xAlignedTemplates/"

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

pseudo_template_ids = tuple(reversed(("E16-25", "P010-33", "P20")))
pseudo_time_points = np.flip(-1.0 * np.log(np.array((16.25, 29.33, 39))))
normalized_pseudo_time_points = (pseudo_time_points - time_points[0]) / (time_points[-1] - time_points[0])


velocity_field_file = output_directory + "/velocity_field.nii.gz"
if not os.path.exists(velocity_field_file):
    raise ValueError("velocity field does not exist.")
print("Reading velocity field.")
velocity_field = ants.image_read(velocity_field_file)

for i in range(len(normalized_pseudo_time_points)):
    print("Creating pseudo-template at normalized time point: ", pseudo_template_ids[i])

    index = -1
    for j in range(1, len(time_points)):
        if time_points[j-1] < pseudo_time_points[i] and time_points[j] > pseudo_time_points[i]:
            index = j
            
    print("  Warping pre template ", template_ids[index-1])
    displacement_field = ants.integrate_velocity_field(velocity_field, normalized_pseudo_time_points[i], normalized_time_points[index-1], 10)
    xfrm = ants.transform_from_displacement_field(displacement_field)
    mask_brain = ants.image_read(glob.glob(templates_directory + template_ids[index-1] + "*/*MaskBrain*.nii.gz")[0])
    pre_image = ants.image_read(glob.glob(templates_directory + template_ids[index-1] + "*/*fa*.nii.gz")[0]) * mask_brain
    pre_image = xfrm.apply_to_image(pre_image, reference=pre_image, interpolation="linear")
    ants.image_write(pre_image, output_directory + pseudo_template_ids[i] + "x" + template_ids[index-1] + "_pseudo_fa_template_pre_image.nii.gz")

    print("  Warping post template ", template_ids[index])
    displacement_field = ants.integrate_velocity_field(velocity_field, normalized_pseudo_time_points[i], normalized_time_points[index], 10)
    xfrm = ants.transform_from_displacement_field(displacement_field)
    mask_brain = ants.image_read(glob.glob(templates_directory + template_ids[index] + "*/*MaskBrain*.nii.gz")[0])
    post_image = ants.image_read(glob.glob(templates_directory + template_ids[index] + "*/*fa*.nii.gz")[0]) * mask_brain
    post_image = xfrm.apply_to_image(post_image, reference=pre_image, interpolation="linear")
    ants.image_write(post_image, output_directory + pseudo_template_ids[i] + "x" + template_ids[index] + "_pseudo_fa_template_post_image.nii.gz")

    print("Generating pseudo-template")
    pseudo_template = ants.build_template(image_list=(pre_image, post_image), iterations=4)
    ants.image_write(pseudo_template, output_directory + pseudo_template_ids[i] + "_pseudo_fa_template.nii.gz")

