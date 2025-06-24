###
#
# Second, we perform pairwise registration between temporally adjacent atlases.
# We extract separate images from each fixed/moving pair and construct a separate
# MSQ metric to drive the registration.  
# 

import ants  # Import the ANTsPy library for image processing and transformation
import glob  # Import the glob module to search for files based on patterns
import os    # Import the os module to interact with the file system
import numpy as np  # Import NumPy for numerical operations

# Set the number of threads for parallel computation (4 threads in this case)
os.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = "4"

# Define directories for input data and output results
base_directory = "../../"  # Base directory for the project
data_directory = base_directory + "Data/Output/P56RigidTransformData/"  # Path to P56 rigid transform output
output_directory = base_directory + "Data/Output/PairwiseRegistrations/"  # Path to store pairwise registration results

# Create the output directory if it doesn't already exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory, exist_ok=True)

# Define a tuple of template IDs for different developmental stages
template_ids = tuple(reversed(("E11-5", "E13-5", "E15-5", "E18-5", "P04", "P14", "P56")))

# Loop through pairs of adjacent stages for pairwise registration
for i in range(1, len(template_ids)):
    # Define file paths for the fixed and moving label images (pairwise adjacent atlases)
    fixed_labels_file = data_directory + "P56x" + template_ids[i-1] + "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi.nii.gz"
    moving_labels_file = data_directory + "P56x" + template_ids[i] + "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi.nii.gz"
      
    # Print paths of the files being processed for debugging
    print("Fixed labels: ", fixed_labels_file)
    print("Moving labels: ", moving_labels_file)

    # Read the fixed and moving label images
    fixed_labels = ants.image_read(fixed_labels_file)
    moving_labels = ants.image_read(moving_labels_file)

    # Extract label geometry measures (centroids, volumes, etc.) from both fixed and moving labels
    fixed_label_geoms = ants.label_geometry_measures(fixed_labels)
    fixed_label_ids = np.array(fixed_label_geoms['Label'])
    moving_label_geoms = ants.label_geometry_measures(moving_labels)
    moving_label_ids = np.array(moving_label_geoms['Label'])
    
    # Find common labels between the fixed and moving atlases
    label_ids = np.intersect1d(moving_label_ids, fixed_label_ids)
    number_of_labels = len(label_ids)
            
    # Threshold the fixed and moving labels to create binary images (presence/absence of labels)
    fixed_image = ants.threshold_image(fixed_labels, 0, 0, 0, 1)
    moving_image = ants.threshold_image(moving_labels, 0, 0, 0, 1)

    # Initialize lists to store images for each individual label
    fixed_single_label_images = list()
    moving_single_label_images = list()

    # For each label, extract and smooth the corresponding single-label images
    for j in range(number_of_labels):
        # Extract the single-label image for the current fixed label
        single_label_image = ants.threshold_image(fixed_labels, label_ids[j], label_ids[j], 1, 0)
        single_label_image = ants.smooth_image(single_label_image, 1, False)
        fixed_single_label_images.append(ants.image_clone(single_label_image))
        
        # Extract the single-label image for the current moving label
        single_label_image = ants.threshold_image(moving_labels, label_ids[j], label_ids[j], 1, 0)
        single_label_image = ants.smooth_image(single_label_image, 1, False)
        moving_single_label_images.append(ants.image_clone(single_label_image))

    # Initialize a list for the MSQ metric inputs (multivariate extra inputs for registration)
    multivariate_extras = list()            
    for j in range(number_of_labels):
        # Each label image is treated as an MSQ (Mean Squared Error) metric for the registration
        multivariate_extras.append(["MSQ", fixed_single_label_images[j], moving_single_label_images[j], 10.0, 1])

    # Define the output prefix for the registration results
    output_registration_prefix = output_directory + "P56x" + template_ids[i-1] + "x" + template_ids[i] + "_"

    # Perform the pairwise registration using ANTs' SyN algorithm with the MSQ metrics
    reg = ants.registration(fixed_image, moving_image, type_of_transform="antsRegistrationSyN[s]", 
                            multivariate_extras=multivariate_extras, 
                            outprefix=output_registration_prefix, verbose=True)    

    # Print some blank lines for clarity in the output log
    print("\n\n\n\n")
