import ants  # Import the ANTsPy library for image processing and transformation
import os    # Import the os module to interact with the file system
import pandas as pd  # Import pandas for handling point data as DataFrames
import numpy as np  # Import NumPy for numerical operations
import random  # Import random for random sampling

# Set the number of threads for parallel computation (4 threads in this case)
os.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = "4"

# Define directories for input data and output results
base_directory = "../../"  # Base directory for the project
data_directory = base_directory + "Data/Output/P56RigidTransformData/"  # Path to P56 rigid transform output
output_directory = base_directory + "Data/Output/"  # General output directory
warped_labels_directory = output_directory + "P56RigidTransformData/"  # Path to warped label images
registration_directory = output_directory + "PairwiseRegistrations/"  # Path to pairwise registration results

################################
#
# A couple notes:
#   * We reverse the template id's because we use P56 to define the fixed reference 
#     frame and, therefore, the positive direction of the velocity field.  This isn't 
#     necessary as we could've easily chosen the opposite direction.  
#   * We take the log of the time points to get a more even distribution of the velocity 
#     field samples.  The only implication of this is that one would need to take into 
#     account this transform when actually using the output velocity field to determine 
#     the transform at a specific time.
#   * Extract contour and regional points in P56.  We use the pairwise registrations to 
#     propagate these points to previous time points.
#   * An additional modification to get a better sampling distribution is to simply use 
#     the time point for P28 = 47 and use the P56 template.
#     

# Template IDs (developmental stages) in reversed order
template_ids = tuple(reversed(("E11-5", "E13-5", "E15-5", "E18-5", "P04", "P14", "P56")))

# Log-transformed time points for better distribution of the velocity field samples
time_points = np.flip(-1.0 * np.log(np.array((11.5, 13.5, 15.5, 18.5, 23, 33, 47))))

# Define contour and regional point percentages for sampling
contour_percentage = 0.1
regional_percentage = 0.01

# Read the fixed labels (P56 template)
fixed_labels_file = warped_labels_directory + "P56xP56_DevCCF_Annotations_20um_symmetric_commonROIs_hemi.nii.gz"
fixed_labels = ants.image_read(fixed_labels_file)

# There were mistakes in the labeling.  These labels don't
# exist across the longitudinal cohort in the simplified 
# version so we remove them.
remove_labels = [17735, 27735, 21558, 31558]
for j in range(len(remove_labels)):
    fixed_labels[fixed_labels == remove_labels[j]] = 0

# Extract label geometry measures and labels from the fixed template
label_geoms = ants.label_geometry_measures(fixed_labels)
label_ids = np.array(label_geoms['Label'])
number_of_labels = len(label_ids)

# Initialize list to store contour points
contour_indices = list()

# Loop through each label and extract contour points
for i in range(0, number_of_labels + 1):
    if i < number_of_labels:
        print("Extracting contour points from label ", label_ids[i])
        single_label_image = ants.threshold_image(fixed_labels, label_ids[i], label_ids[i], 1, 0)
    else:
        single_label_image = ants.threshold_image(fixed_labels, 0, 0, 0, 1)
    
    # Extract the contour points (edges of the labeled region)
    contour_image = single_label_image - ants.iMath_ME(single_label_image, 1)
    single_label_indices = (contour_image.numpy()).nonzero()

    # Select a subset of points for sampling based on contour_percentage
    number_of_points_per_label = int(len(single_label_indices[0]) * contour_percentage)
    print("  Number of points: ", number_of_points_per_label)
    random_indices = random.sample(range(len(single_label_indices[0])), number_of_points_per_label)
    
    # Append the selected indices for this label to contour_indices
    if i == 0:
         contour_indices.append(single_label_indices[0][random_indices])
         contour_indices.append(single_label_indices[1][random_indices])
         contour_indices.append(single_label_indices[2][random_indices])
    else:
         contour_indices[0] = np.concatenate([contour_indices[0], single_label_indices[0][random_indices]])
         contour_indices[1] = np.concatenate([contour_indices[1], single_label_indices[1][random_indices]])
         contour_indices[2] = np.concatenate([contour_indices[2], single_label_indices[2][random_indices]])

# Define weights for contour points (uniform weighting)
contour_weights = [1] * len(contour_indices[0])

# Initialize list to store regional points
regional_indices = list()

# Loop through each label and extract regional points
for i in range(0, number_of_labels + 1):
    if i < number_of_labels:
        print("Extracting regional points from label ", label_ids[i])
        single_label_image = ants.threshold_image(fixed_labels, label_ids[i], label_ids[i], 1, 0)
    else:
        single_label_image = ants.threshold_image(fixed_labels, 0, 0, 0, 1)
    
    # Extract the regional points (all points within the label)
    single_label_indices = (single_label_image.numpy()).nonzero()

    # Select a subset of points for sampling based on regional_percentage
    number_of_points_per_label = int(len(single_label_indices[0]) * regional_percentage)
    print("  Number of points: ", number_of_points_per_label)
    random_indices = random.sample(range(len(single_label_indices[0])), number_of_points_per_label)
    
    # Append the selected indices for this label to regional_indices
    if i == 0:
         regional_indices.append(single_label_indices[0][random_indices])
         regional_indices.append(single_label_indices[1][random_indices])
         regional_indices.append(single_label_indices[2][random_indices])
    else:
         regional_indices[0] = np.concatenate([regional_indices[0], single_label_indices[0][random_indices]])
         regional_indices[1] = np.concatenate([regional_indices[1], single_label_indices[1][random_indices]])
         regional_indices[2] = np.concatenate([regional_indices[2], single_label_indices[2][random_indices]])

# Define weights for regional points (lower weight for regional points)
regional_weights = [0.5] * len(regional_indices[0])

# Combine the contour and regional points into a single set of points
indices = contour_indices
indices[0] = np.concatenate([indices[0], regional_indices[0]])
indices[1] = np.concatenate([indices[1], regional_indices[1]])
indices[2] = np.concatenate([indices[2], regional_indices[2]])

# Combine the weights for both types of points
weights = np.concatenate([contour_weights, regional_weights])

# Print the number of contour and regional points
print("Number of contour points:  ", str(len(contour_weights)))
print("Number of regional points:  ", str(len(regional_weights)))

# Convert the indices of the points to physical coordinates in the template space
points_time0 = np.zeros((len(indices[0]), 3))
for i in range(len(indices[0])):
    index = (indices[0][i], indices[1][i], indices[2][i])
    points_time0[i,:] = ants.transform_index_to_physical_point(fixed_labels, index)

# Convert the points into a DataFrame for easier manipulation
points_time0_df = pd.DataFrame(points_time0, columns = ('x', 'y', 'z'))

# Initialize a list to store the point sets for each time point
point_sets = list()
point_sets.append(points_time0_df) # Add P56 as the first time point

# Warp the points to previous time points using the pairwise registration results
for i in range(1, len(template_ids)):
    print("Warping points " + str(i))
    source_template_id = template_ids[i-1]        
    target_template_id = template_ids[i]        
    output_registration_prefix = registration_directory + "P56x" + source_template_id + "x" + target_template_id + "_"
    
    # Read the affine and warp transforms
    affine = output_registration_prefix + "0GenericAffine.mat"
    warp = output_registration_prefix + "1Warp.nii.gz"
    
    # Apply the transforms to the points
    warped_points = ants.apply_transforms_to_points(3, points=point_sets[i-1], transformlist=[warp, affine])
    point_sets.append(warped_points)

# Optionally check and visualize the warped points by converting them into images
check_points = False
if check_points:
    for i in range(len(template_ids)):
        print("Checking image " + str(i))
        points_image = ants.make_points_image(point_sets[i].to_numpy(), fixed_labels * 0 + 1, radius=1)
        output_prefix = output_directory + "P56x" + template_ids[i] + "_"
        ants.image_write(points_image, output_prefix + "points_image.nii.gz")

# Convert the point sets back to NumPy arrays for further processing
for i in range(len(point_sets)):
    point_sets[i] = point_sets[i].to_numpy()

# Normalize the time points to the range [0, 1] for use in the velocity field optimization
normalized_time_points = (time_points - time_points[0]) / (time_points[-1] - time_points[0])

# Initialize the velocity field, if it exists, to use as the starting point for optimization
initial_velocity_field = None
velocity_field_file = output_directory + "/DevCCF_velocity_flow.nii.gz"
if os.path.exists(velocity_field_file):
    initial_velocity_field = ants.image_read(velocity_field_file)

# Perform the optimization to compute the time-varying velocity field
for i in range(20):  # Run the optimization for 20 iterations
    print("Iteration " + str(i))
    tv = ants.fit_time_varying_transform_to_point_sets(point_sets, time_points=normalized_time_points,
        displacement_weights=weights,
        initial_velocity_field=initial_velocity_field,
        number_of_time_steps=11, domain_image=fixed_labels,
        number_of_fitting_levels=4, mesh_size=4, number_of_compositions=10,
        convergence_threshold=0.0, composition_step_size=0.2,
        number_of_integration_steps=10,
        rasterize_points=False, verbose=True)
    
    # Update the velocity field after each iteration
    initial_velocity_field = ants.image_clone(tv['velocity_field'])
    
    # Write the updated velocity field to disk
    ants.image_write(initial_velocity_field, velocity_field_file)
    print("\n\n\n\n\n\n")
