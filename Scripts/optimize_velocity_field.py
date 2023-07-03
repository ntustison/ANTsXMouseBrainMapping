import ants
import os
import pandas as pd
import numpy as np
import random

os.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = "12"

annotation_directory = "../Data/AlignedSimpleSegmentations/"
registration_directory = annotation_directory + "PairwiseRegistrations/"
output_directory = "../Data/Results/"

if not os.path.exists(output_directory):
    os.makedirs(output_directory, exist_ok=True)

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

fixed_labels_file = annotation_directory + "P56x" + template_ids[0] + "_LABELS.nii.gz"
fixed_labels = ants.image_read(fixed_labels_file)

# Extract points.  As a first-pass and proof-of-concept, we're going to use four
# sets of points (randomly sampled based on the user-selected number of points).  
# The first three are from the outer surface of each of the three regions labeled
# by Fae's "simplified segmentations."  The fourth set is combining all the regions
# into a single object to get the set of points defining the outer boundary.
# Note that these are defined in the fixed reference frame (i.e., P56 template).
# We then use the pairwise registrations to propagate these points to previous
# time points.

number_of_points_per_label = (10000, 10000, 10000, 5000)

indices = list()
for i in range(1, 5):
    if i < 4:
        single_label_image = ants.threshold_image(fixed_labels, i, i, 1, 0)
    else:
        single_label_image = ants.threshold_image(fixed_labels, 0, 0, 0, 1)
    contour_image = single_label_image - ants.iMath_ME(single_label_image, 1)
    if i == 1:
         single_label_indices = (contour_image.numpy()).nonzero()
         random_indices = random.sample(range(len(single_label_indices[0])), number_of_points_per_label[i-1])
         indices.append(single_label_indices[0][random_indices])
         indices.append(single_label_indices[1][random_indices])
         indices.append(single_label_indices[2][random_indices])
    else:
         single_label_indices = (contour_image.numpy()).nonzero()
         random_indices = random.sample(range(len(single_label_indices[0])), number_of_points_per_label[i-1])
         indices[0] = np.concatenate([indices[0], single_label_indices[0][random_indices]])
         indices[1] = np.concatenate([indices[1], single_label_indices[1][random_indices]])
         indices[2] = np.concatenate([indices[2], single_label_indices[2][random_indices]])

points_time0 = np.zeros((len(indices[0]), 3))
for i in range(len(indices[0])):
    index = (indices[0][i], indices[1][i], indices[2][i])
    points_time0[i,:] = ants.transform_index_to_physical_point(fixed_labels, index)

points_time0_df = pd.DataFrame(points_time0, columns = ('x', 'y', 'z'))

point_sets = list()
point_sets.append(points_time0_df) #P56
for i in range(1, len(template_ids)):
    print("Warping points " + str(i))
    source_template_id = template_ids[i-1]        
    target_template_id = template_ids[i]        
    output_registration_prefix = registration_directory + "P56x" + source_template_id + "x" + target_template_id + "_"
    affine = output_registration_prefix + "0GenericAffine.mat"
    warp = output_registration_prefix + "1Warp.nii.gz"
    warped_points = ants.apply_transforms_to_points(3, points=point_sets[i-1], transformlist=[warp, affine])
    point_sets.append(warped_points)

# Write the points to images to see if they match with what's expected.
check_points = True
if check_points:
    for i in range(len(template_ids)):
        print("Checking image " + str(i))
        points_image = ants.make_points_image(point_sets[i].to_numpy(), fixed_labels * 0 + 1, radius=1)
        output_prefix = output_directory + "P56x" + template_ids[i] + "_"
        ants.image_write(points_image, output_prefix + "points_image.nii.gz")

for i in range(len(point_sets)):
    point_sets[i] = point_sets[i].to_numpy()

# Normalize time points to the range [0, 1]

normalized_time_points = (time_points - time_points[0]) / (time_points[-1] - time_points[0])

initial_velocity_field = None
velocity_field_file = output_directory + "/velocity_field.nii.gz"
if os.path.exists(velocity_field_file):
    initial_velocity_field = ants.image_read(velocity_field_file)

# We could simply set the total number of iterations (i.e., "number_of_compositions")
# to 10 * 20 but just so we could check the progress, we run the optimization for 10
# iterations and then write the velocity field to disk and use it as the initial 
# velocity field for subsequent iterations.

for i in range(20):
    print("Iteration " + str(i))
    tv = ants.fit_time_varying_transform_to_point_sets(point_sets, time_points=normalized_time_points,
        initial_velocity_field=initial_velocity_field,
        number_of_time_steps=11, domain_image=fixed_labels,
        number_of_fitting_levels=4, mesh_size=4, number_of_compositions=10,
        convergence_threshold=0.0, composition_step_size=0.2,
        number_of_integration_steps=10,
        rasterize_points=False, verbose=True)
    initial_velocity_field = ants.image_clone(tv['velocity_field'])
    # ants.image_write(initial_velocity_field, output_prefix + "velocity_field_" + str(i) + ".nii.gz")
    ants.image_write(initial_velocity_field, output_directory + "velocity_field.nii.gz")
    print("\n\n\n\n\n\n")


