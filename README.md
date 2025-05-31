# [Modular strategies for spatial mapping of diverse cell type data of the mouse brain](https://www.biorxiv.org/content/10.1101/2024.05.01.592056v1)

Two novel open-source contributions:

* [Structural mouse brain morphology from T2-w imaging](https://github.com/ntustison/ANTsXMouseBrainMapping/blob/main/README.md#single-shot-learning-for-mouse-brain-cortical-thickness-measurements)
* [A general landmark-based velocity flow transformation model applied to DevCCF](https://github.com/ntustison/ANTsXMouseBrainMapping/blob/main/README.md#the-devccf-velocity-flow-transformation-model)

---

## Two- and single-shot learning for mouse brain cortical thickness measurements

<p align="middle">
  <img src="https://github.com/ntustison/DevCCF-Velocity-Flow/blob/main/Manuscript/Figures/mousePipeline.png" width="700" />
</p>

### Motivation

To develop a structural morphological processing pipeline for the mouse brain 
analogous to our [human-based tools](https://www.nature.com/articles/s41598-021-87564-6).

<details>
<summary>Elaboration</summary>

* No current tools to create training data for deep learning (in contrast to e.g., [human data](https://pubmed.ncbi.nlm.nih.gov/24879923/)).
* Low data quality.  Data is often:
    * sampling issues such as anisotropy, incomplete (i.e., missing boundary structures),
    * T2-w only, and
    * limited applicability to high resolution resources (e.g., AllenCCFv3, DevCCF).
* However, in historical contrast to the human domain, we can leverage these publicly 
available templates (i.e., AllenCCFv3 and DevCCF) and deep learning to provide 
tools for multiple modalities and varying degrees of isotropic sampling.

</details>

<details>
<summary>Results</summary>

Structural morphological tools for T2-w volumetric mouse brain images:
* [Brain extraction](https://github.com/ANTsX/ANTsPyNet/blob/master/antspynet/utilities/mouse.py#L5-L10)
* [Brain parcellation](https://github.com/ANTsX/ANTsPyNet/blob/master/antspynet/utilities/mouse.py#L301-L306)
* [Cortical thickness](https://github.com/ANTsX/ANTsPyNet/blob/master/antspynet/utilities/mouse.py#L453-L457)

This work also provides a more general framework for single-shot learning using 
existing templates specifically tailored for both isotropic and anisotropic
mouse data.  See the training scripts in this repository.

</details>

### Innovations

<details>
<summary>Two-shot brain extraction network</summary>

* Build two symmetric isotropic ANTsX templates from two publicly available datasets with different
  "defacing" aesthetics:
    * [CAMRI](https://camri.org/dissemination/mri-data/)
        * resolution = 0.16 x 0.16 x 0.16 $mm^3$
        * $n = 16$
        * [Template](https://figshare.com/ndownloader/files/44957752) and [brain mask](https://figshare.com/ndownloader/files/44957395)
    * [High resolution](https://data.mendeley.com/datasets/dz9x23fttt/1)
        * Three spatially aligned high-resolution orthogonal views
        * resolution = 0.08 x 0.08 $mm^2$ in-plane, 0.5 mm slice thickness
        * $n = 88$
        * [Combine three views using B-spline filter](https://github.com/ntustison/ANTsXMouseBrainMapping/blob/main/Scripts/MiscScripts/synthesize_image_views_bspline.py)
        * [Template](https://figshare.com/ndownloader/files/44706247) and [brain mask](https://figshare.com/ndownloader/files/44869285)

* Data augmentation of CAMRI and high resolution B-spline template:
    * bias field simulation, 
    * histogram warping, 
    * added noise, 
    * random translation and warping, and
    * random anisotropic resampling in the three canonical directions.

* [C57BI evaluation data](https://www.frdr-dfdr.ca/repo/dataset/9ea832ad-7f36-4e37-b7ac-47167c0001c1)
    * Completely *unseen* data  
    * 12 specimens
    * 7 time points (Day 0, Day 3, Week 1, Week 4, Week 8, Week 20)
    * Whole brain masks are provided
     
<p align="middle">
  <img src="https://github.com/ntustison/DevCCF-Velocity-Flow/blob/main/Manuscript/Figures/dice.png" width="400" />
</p>

</details>

<details>
<summary>Single-shot brain parcellation network</summary>

* AllenCCFv3 with labels.
* Convert labels to a gross parcellation using allensdk
  ([this](https://github.com/ntustison/ANTsXMouseBrainMapping/blob/main/Scripts/get_allen_parcellation.py) is just
  one possibility that works for computing KK cortical thickness). 
* Register AllenCCFv3 and DevCCF P56 T2-w to map to the desired
  template modality.  Note that given a similar resource for DevCCF
  (i.e., allensdk), one can use DevCCF directly.

* Data augmentation of CAMRI and high resolution B-spline template:
    * bias field simulation, 
    * histogram warping, 
    * added noise, 
    * random translation and warping, and
    * random anisotropic resampling in the three canonical directions.

* [C57BI evaluation data](https://www.frdr-dfdr.ca/repo/dataset/9ea832ad-7f36-4e37-b7ac-47167c0001c1)
    * Completely *unseen* data
    * 12 specimens
    * 7 time points (Day 0, Day 3, Week 1, Week 4, Week 8, Week 20)
     
<p align="middle">
  <img src="https://github.com/ntustison/DevCCF-Velocity-Flow/blob/main/Manuscript/Figures/kk.png" width="400" />
</p>

</details>

---

## The DevCCF velocity flow transformation model 

<p align="middle">
  <img src="https://github.com/ntustison/DevCCF-Velocity-Flow/blob/main/Manuscript/Figures/lowerLeftPanel.png" width="700" />
</p>

### Description

A multimodal 3D developmental common coordinate framework (DevCCF) spanning 
mouse embryonic day (E) 11.5, E13.5, E15.5, E18.5, and postnatal day (P) 4, 
P14, and P56 with anatomical segmentations defined by a developmental ontology
is described in [Kronman et al.](https://www.biorxiv.org/content/10.1101/2023.09.14.557789v1)
available [here](https://kimlab.io/brain-map/DevCCF/).
At each age, the DevCCF features undistorted morphologically averaged atlas 
templates created from magnetic resonance imaging and co-registered high-
resolution templates from light sheet fluorescence microscopy. Expert-curated 
3D anatomical segmentations at each age are also available. 
As part of this work, we generate a [diffeomorphic velocity flow model](https://en.wikipedia.org/wiki/Large_deformation_diffeomorphic_metric_mapping)
permitting deformations between the above mouse developmental stages and
at any continuous point within the developmental range.  The transformation
model is generated using the publicly available data provided through the
above cited work and using [ANTsX tools](https://github.com/ANTsX).  This
repository provides the code and data to reproduce and utilize the velocity
flow field.

### Preliminaries

<details>
<summary>Code</summary>

All data processing uses [ANTsPy](https://github.com/ANTsX/ANTsPy) with 
equivalent calls possible in [ANTsR](https://github.com/ANTsX/ANTsR).
Be sure to [install ANTsPy](https://github.com/ANTsX/ANTsPy#installation)
prior to attempting to reproduce the results below.  To test your installation 
in the context of this work,  please attempt to reproduce a 
[small, self-contained example](https://gist.github.com/ntustison/12a656a5fc2f6f9c4494c88dc09c5621#file-b_3_ants_velocity_flows-md)
illustrating the code and principles used.  Conceptually, this code snippet 
creates a time-parameterized velocity flow model in the range $t=[0,1]$ using 
three 2-D point sets comprising 8 points each representing a rectangle at $t=0.0$, 
a square at $t=0.5$, and a circle at $t=1.0$.  The ANTsPy example should produce the 
following plots:

<p align="middle">
  <img src="https://github.com/ntustison/MouseBrainVelocityFlow/assets/324811/dbc63553-27ad-4130-8bbf-c10cdf8fc893" width="250" />
  <img src="https://github.com/ntustison/MouseBrainVelocityFlow/assets/324811/cd78595b-1e12-47fc-b606-ae4b5012cbd6" width="250" /> 
  <img src="https://github.com/ntustison/MouseBrainVelocityFlow/assets/324811/c7ee9ad6-1f3a-4da4-832e-ba64b1b15f31" width="250" /> 
</p>

</details>

<details>
<summary>Data</summary>

For simplicity only the data used to create the velocity flow model is 
[available in this repository](https://github.com/ntustison/DevCCF-Velocity-Flow/tree/main/Data/DevCCFSimpleSegmentations).
These label images are the simplified annotations comprising common regions
across all developmental stages and are based on the DevCCF pre-released 
segmentations version 3.8.    

<p align="middle">
  <img src="https://github.com/ntustison/DevCCF-Velocity-Flow/assets/324811/3f3a4369-eb82-4dce-b1a3-3e4481f66509" width="450" />
</p>
</details>

### Reproducing the DevCCF Velocity Flow Model

```bash
# tl;dr
# * run the following to generate the flow model
# * results are in Data/Output/
$ cd Scripts/DevCCFVelocityFlowModel/
$ python step1.py
$ python step2.py
$ python step3.py
```

<details>
<summary>Step 1:  Rigidly register all label images to P56</summary>

```python
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
```
</details>

<details>
<summary>Step 2:  Perform pairwise registrations of the P56-aligned label images</summary>

```python
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
```
</details>

<details>
<summary>Step 3:  Extract points from P56 labels, propagate to all developmental atlases, and build the model</summary>

<p align="middle">
  <img src="https://github.com/ntustison/DevCCF-Velocity-Flow/assets/324811/5dc3247c-e75d-453c-979a-71775dd8d91c" width="550" />
</p>

```python
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
```

</details>


### Using the DevCCF Velocity Flow Model

<details>
<summary>Example:  Warp every template to every other template</summary>

<p align="middle">
  <img src="https://github.com/ntustison/DevCCF-Velocity-Flow/assets/324811/df61e8c6-93a7-4b1a-91b8-9deeefe700bb" width="550" />
</p>

```python
import ants
import numpy as np
import math

atlas_ids = tuple(reversed(("E11-5", "E13-5", "E15-5", "E18-5", "P04", "P14", "P56")))
time_points = np.flip(-1.0 * np.log(np.array((11.5, 13.5, 15.5, 18.5, 23, 33, 47))))
normalized_time_points = (time_points - time_points[0]) / (time_points[-1] - time_points[0])

velocity_field = ants.image_read("Data/Output/DevCCF_velocity_flow.nii.gz")

# Read template files.
# template_files = list()
# for i in range(len(atlas_ids)):
#      fa_template_files.append(glob.glob(atlas_ids[i] + "*.nii.gz")[0])

for i in range(len(atlas_ids)):
    for j in range(len(atlas_ids)):
        print("Warping ", atlas_ids[j], "to", atlas_ids[i])
        reference_template = ants.image_read(template_files[i])
        moving_template = ants.image_read(template_files[j])
        displacement_field = ants.integrate_velocity_field(velocity_field,
                                                           normalized_time_points[i],
                                                           normalized_time_points[j], 10)
        displacement_field_xfrm = ants.transform_from_displacement_field(displacement_field)
        warped_template = displacement_field_xfrm.apply_to_image(moving_template,
                                                                 interpolation="linear")
```

</details>


<details>
<summary>Example:  Warp P56 in a continuous manner from identity to E11.5</summary>

<p align="middle">
  <img src="https://github.com/ntustison/DevCCF-Velocity-Flow/assets/324811/a8412f23-9167-4cbe-9c7d-021ad97f4429" width="550" />
</p>

```python
import ants
import numpy as np
import math

velocity_field = ants.image_read("DevCCF_flow_model.nii.gz")
P56 = ants.image_read("P56.nii.gz")  

# We discretize the time domain into 50 intervals.
time_points = np.flip(-1.0 * np.log(np.linspace(11.5, 47, 50)))
normalized_time_points = (time_points - time_points[0]) / (time_points[-1] - time_points[0])

for i in range(len(normalized_time_points)):
    t = normalized_time_points[i]
    displacement_field = ants.integrate_velocity_field(velocity_field, t, 0.0, 10)
    displacement_field_xfrm = ants.transform_from_displacement_field(displacement_field)
    P56warped = displacement_field_xfrm.apply_to_image(P56, interpolation="linear")
```

</details>


