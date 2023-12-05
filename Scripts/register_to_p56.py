import ants
import glob
import os
import numpy as np

os.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = "8"

annotation_directory = "/Users/ntustison/Data/JimGee/AllenDevelopmentalVelocityFlows/20231021_DevCCF_SimpleSegmentationsv3/"
template_directory = "/Users/ntustison/Data/JimGee/AllenDevelopmentalVelocityFlows/DevCCFtemplates_Lite-uint16/"
output_directory = "/Users/ntustison/Data/JimGee/AllenDevelopmentalVelocityFlows/MouseBrainVelocityFlow/Data/P56xAlignedSimpleSegmentations/"

template_ids = tuple(reversed(("E11-5", "E13-5", "E15-5", "E18-5", "P04", "P14", "P56")))

transform_list = list()
which_to_invert = list()

###
#
# Original labels are across hemispheres so we take advantage of the 
# symmetry and create left/right versions.  For the right hemisphere 
# we replace the leading '1' with a '2'.  So in the end, we have 
# 
# Left labels:  [15622, 15751, 15903, 16211, 16309, 16375, 16509, 16649, 16809, 17092, 17220, 17352, 17735]
# Right labels:  [25622, 25751, 25903, 26211, 26309, 26375, 26509, 26649, 26809, 27092, 27220, 27352, 27735]
# 
for i in range(len(template_ids)):
    print("Processing ", template_ids[i])
    labels_file = annotation_directory + template_ids[i] + "_DevCCF_Annotations_20um_symmetric_commonROIs.nii.gz"
    labels_hemi_file = labels_file.replace("commonROIs", "commonROIs_hemi")
    if not os.path.exists(labels_hemi_file):
        labels = ants.image_read(labels_file)    
        labels_array = labels.numpy()
        shape = labels.shape
        labels_array[:int(labels.shape[0] * 0.5 + 0.5),:,:] = labels_array[:int(labels.shape[0] * 0.5 + 0.5),:,:] + 10000
        labels_array[labels_array <= 10000] = 0
        labels_hemi = ants.from_numpy(labels_array, origin=labels.origin, spacing=labels.spacing, direction=labels.direction)
        ants.image_write(labels_hemi, labels_hemi_file)

####
#
#  Now get common label ids
#

common_label_ids = None
for i in range(len(template_ids)):
    print("Finding common label ids ", template_ids[i])
    labels_file = annotation_directory + template_ids[i] + "_DevCCF_Annotations_20um_symmetric_commonROIs.nii.gz"
    labels_hemi_file = labels_file.replace("commonROIs", "commonROIs_hemi")
    labels = ants.image_read(labels_hemi_file)
    label_geoms = ants.label_geometry_measures(labels)
    if i == 0: 
        common_label_ids = np.array(label_geoms['Label'])
    else:
        common_label_ids = np.intersect1d(common_label_ids, np.array(label_geoms['Label']))
print("Common label ids: ", common_label_ids)      

###
#
# Rigidly register everything to P56 using label centroids.
# 

fixed_labels_file = annotation_directory + template_ids[0] + "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi.nii.gz"
fixed_labels = ants.image_read(fixed_labels_file)
label_geoms = ants.label_geometry_measures(fixed_labels)
fixed_label_ids = np.array(label_geoms['Label'])
for l in range(len(fixed_label_ids)):
    if not np.isin(fixed_label_ids[l], common_label_ids):
        fixed_labels[fixed_labels == fixed_label_ids[l]] = 0
label_geoms = ants.label_geometry_measures(fixed_labels)
fixed_points = np.zeros((label_geoms.shape[0], 3))
fixed_points[:,0] = label_geoms['Centroid_x']
fixed_points[:,1] = label_geoms['Centroid_y']
fixed_points[:,2] = label_geoms['Centroid_z']
for n in range(fixed_points.shape[0]):
    fixed_points[n,:] = ants.transform_index_to_physical_point(fixed_labels, (fixed_points + 0.5).astype(int)[n,:])

for i in range(len(template_ids)):
    print("Processing ", template_ids[i])

    moving_labels_file = annotation_directory + template_ids[i] + "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi.nii.gz"
    moving_labels = ants.image_read(moving_labels_file)
    label_geoms = ants.label_geometry_measures(moving_labels)
    moving_label_ids = np.array(label_geoms['Label'])
    for l in range(len(moving_label_ids)):
        if not np.isin(moving_label_ids[l], common_label_ids):
            moving_labels[moving_labels == moving_label_ids[l]] = 0
    label_geoms = ants.label_geometry_measures(moving_labels)
    print( "    Matching fixed labels:", fixed_label_ids)
    print( "    Matching moving labels:", moving_label_ids)
    moving_points = np.zeros((label_geoms.shape[0], 3))
    moving_points[:,0] = label_geoms['Centroid_x']
    moving_points[:,1] = label_geoms['Centroid_y']
    moving_points[:,2] = label_geoms['Centroid_z']
    for n in range(moving_points.shape[0]):
        moving_points[n,:] = ants.transform_index_to_physical_point(moving_labels, (moving_points + 0.5).astype(int)[n,:])

    xfrm = ants.fit_transform_to_paired_points(moving_points, fixed_points, transform_type='rigid')
    xfrm_file = output_directory + "P56x" + template_ids[i] + "_xfrm.mat"
    ants.write_transform(xfrm, xfrm_file)
    moving_labels_file = annotation_directory + template_ids[i] + "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi.nii.gz"
    moving_labels = ants.image_read(moving_labels_file)
    warped_labels = xfrm.apply_to_image(moving_labels, fixed_labels, interpolation='nearestneighbor') 
    warped_labels_file = output_directory + "P56x" + template_ids[i] + "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi.nii.gz"
    ants.image_write(warped_labels, warped_labels_file)
    
    
