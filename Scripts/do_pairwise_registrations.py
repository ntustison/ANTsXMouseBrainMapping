import ants
import glob
import os
import numpy as np

os.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = "12"

annotation_directory = "/Users/ntustison/Data/JimGee/AllenDevelopmentalVelocityFlows/MouseBrainVelocityFlow/Data/P56xAlignedSimpleSegmentations/"
output_directory = annotation_directory + "/PairwiseRegistrations/"

template_ids = tuple(reversed(("E11-5", "E13-5", "E15-5", "E18-5", "P04", "P14", "P56")))

for i in range(1, len(template_ids)):
    fixed_labels_file = annotation_directory + template_ids[0] + "x" + template_ids[i-1] + "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi_resampled.nii.gz"
    moving_labels_file = annotation_directory + template_ids[0] + "x" + template_ids[i] + "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi_resampled.nii.gz"
      
    print("Fixed labels: ", fixed_labels_file)
    print("Moving labels: ", moving_labels_file)

    fixed_labels = ants.image_read(fixed_labels_file)
    moving_labels = ants.image_read(moving_labels_file)
    
    fixed_label_geoms = ants.label_geometry_measures(fixed_labels)
    fixed_label_ids = np.array(fixed_label_geoms['Label'])
    moving_label_geoms = ants.label_geometry_measures(moving_labels)
    moving_label_ids = np.array(moving_label_geoms['Label'])
    
    label_ids = np.intersect1d(moving_label_ids,fixed_label_ids)
    number_of_labels = len(label_ids)
            
    fixed_image = ants.threshold_image(fixed_labels, 0, 0, 0, 1)
    moving_image = ants.threshold_image(moving_labels, 0, 0, 0, 1)

    fixed_single_label_images = list()
    moving_single_label_images = list()
    for j in range(number_of_labels):
        single_label_image = ants.threshold_image(fixed_labels, label_ids[j], label_ids[j], 1, 0)
        single_label_image = ants.smooth_image(single_label_image, 1, False)
        fixed_single_label_images.append(ants.image_clone(single_label_image))
        single_label_image = ants.threshold_image(moving_labels, label_ids[j], label_ids[j], 1, 0)
        single_label_image = ants.smooth_image(single_label_image, 1, False)
        moving_single_label_images.append(ants.image_clone(single_label_image))

    multivariate_extras = list()            
    for j in range(number_of_labels):
        multivariate_extras.append(["MSQ", fixed_single_label_images[j], moving_single_label_images[j], 10.0, 1])

    output_registration_prefix = output_directory + template_ids[0] + "x" + template_ids[i-1] + "x" + template_ids[i] + "_"

    # output_file = output_registration_prefix + "Warped.nii.gz"
    # if os.path.exists(output_file):
    #     continue
    
    reg = ants.registration(fixed_image, moving_image, type_of_transform="antsRegistrationSyN[s]", 
                            multivariate_extras=multivariate_extras, 
                            outprefix=output_registration_prefix, verbose=True)    

    warped_fixed_labels = ants.apply_transforms(fixed_image, moving_labels, transformlist=reg['fwdtransforms'], interpolator="nearestNeighbor")
    warped_moving_labels = ants.apply_transforms(moving_image, fixed_labels, transformlist=reg['invtransforms'], whichtoinvert=[True, False], interpolator="nearestNeighbor")
    ants.image_write(warped_fixed_labels, output_registration_prefix + "Warped.nii.gz")
    ants.image_write(warped_moving_labels, output_registration_prefix + "InverseWarped.nii.gz")

    print("\n\n\n\n")
    

