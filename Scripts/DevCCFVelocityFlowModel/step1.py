###
#
# First, rig. register all the input images to P56 as all the images need to reside 
# in a common post-linearly aligned space.  To do this, we find the common labels 
# between all the developmental stages and then use those to find a rigid transform
# to the P56 template. Save the rigid transforms and warped images.  We also resample
# to (0.05, 0.05, 0.05).
# 

import ants  # Import the ANTsPy library for image processing and transformation
import os    # Import os module to interact with the file system
import numpy as np  # Import NumPy for numerical operations

# Define directories for input data and output results
base_directory = "../../"  # Base directory for the project
data_directory = base_directory + "Data/DevCCFSimpleSegmentations/"  # Path to input data
output_directory = base_directory + "Data/Output/P56RigidTransformData/"  # Path to output data

# Create the output directory if it does not exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory, exist_ok=True)

# Define a tuple of atlas IDs for the different developmental stages
atlas_ids = tuple(reversed(("E11-5", "E13-5", "E15-5", "E18-5", "P04", "P14", "P56")))

# Initialize a variable to store common label IDs across developmental stages
common_label_ids = None

# Loop through each developmental stage and find common label IDs across stages
for i in range(len(atlas_ids)):
    print("Finding common label ids for atlas:", atlas_ids[i])
    # Read the label image for the current stage
    labels_file = data_directory + atlas_ids[i] + "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi.nii.gz"
    labels = ants.image_read(labels_file)
    label_geoms = ants.label_geometry_measures(labels)  # Extract label geometry information

    # For the first atlas, initialize common_label_ids with the labels
    if i == 0: 
        common_label_ids = np.array(label_geoms['Label'])
    else:
        # For subsequent stages, find the intersection of common labels
        common_label_ids = np.intersect1d(common_label_ids, np.array(label_geoms['Label']))

# Print the common label IDs found across all stages
print("Common label ids:", common_label_ids)      

# Read the P56 template label image
fixed_labels_file = data_directory + "P56_DevCCF_Annotations_20um_symmetric_commonROIs_hemi.nii.gz"
fixed_labels = ants.image_read(fixed_labels_file)
label_geoms = ants.label_geometry_measures(fixed_labels)  # Extract label geometry info
fixed_label_ids = np.array(label_geoms['Label'])

# Remove labels from the P56 template that are not in the common label IDs
for l in range(len(fixed_label_ids)):
    if not np.isin(fixed_label_ids[l], common_label_ids):
        fixed_labels[fixed_labels == fixed_label_ids[l]] = 0

# Extract the centroids (geometrical center) of the remaining labels in the P56 template
label_geoms = ants.label_geometry_measures(fixed_labels)
fixed_points = np.zeros((label_geoms.shape[0], 3))  # Initialize array to store centroids
fixed_points[:,0] = label_geoms['Centroid_x']
fixed_points[:,1] = label_geoms['Centroid_y']
fixed_points[:,2] = label_geoms['Centroid_z']

# Convert centroid indices to physical points in space
for n in range(fixed_points.shape[0]):
    fixed_points[n,:] = ants.transform_index_to_physical_point(fixed_labels, (fixed_points + 0.5).astype(int)[n,:])

# Now process each atlas (developmental stage)
for i in range(len(atlas_ids)):
    print("Processing ", atlas_ids[i])
    # Read the moving labels for the current developmental stage
    moving_labels_file = data_directory + atlas_ids[i] + "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi.nii.gz"
    moving_labels = ants.image_read(moving_labels_file)
    label_geoms = ants.label_geometry_measures(moving_labels)  # Extract label geometry info
    moving_label_ids = np.array(label_geoms['Label'])

    # Remove labels from the moving image that are not in the common label IDs
    for l in range(len(moving_label_ids)):
        if not np.isin(moving_label_ids[l], common_label_ids):
            moving_labels[moving_labels == moving_label_ids[l]] = 0

    # Extract centroids of the remaining labels in the moving image
    label_geoms = ants.label_geometry_measures(moving_labels)
    moving_points = np.zeros((label_geoms.shape[0], 3))  # Initialize array for moving centroids
    moving_points[:,0] = label_geoms['Centroid_x']
    moving_points[:,1] = label_geoms['Centroid_y']
    moving_points[:,2] = label_geoms['Centroid_z']

    # Convert centroid indices to physical points in space
    for n in range(moving_points.shape[0]):
        moving_points[n,:] = ants.transform_index_to_physical_point(moving_labels, (moving_points + 0.5).astype(int)[n,:])

    # Perform rigid registration between the moving image and fixed template (P56)
    xfrm = ants.fit_transform_to_paired_points(moving_points, fixed_points, transform_type='rigid')

    # Save the rigid transform matrix
    xfrm_file = output_directory + "P56x" + atlas_ids[i] + "_rigid_xfrm.mat"
    ants.write_transform(xfrm, xfrm_file)

    # Warp the moving labels using the rigid transform
    warped_labels = xfrm.apply_to_image(moving_labels, fixed_labels, interpolation='nearestneighbor') 

    # Resample the warped labels to the desired resolution (0.05mm isotropic)
    warped_labels = ants.resample_image(warped_labels, (0.05, 0.05, 0.05), False, 1)

    # Save the warped labels to the output directory
    warped_labels_file = output_directory + "P56x" + atlas_ids[i] + "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi.nii.gz"
    ants.image_write(warped_labels, warped_labels_file)
