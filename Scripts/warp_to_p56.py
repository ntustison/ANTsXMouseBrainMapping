import ants
import glob
import os

os.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = "8"

template_directory = "/Users/ntustison/Data/JimGee/AllenTesting/Templates/20230113_MRI_Templates_MaskedSymmetricBgRemovedSterotaxic/"
annotation_directory = "/Users/ntustison/Data/JimGee/AllenDevelopmentalVelocityFlows/SimpleSegmentations/"
output_directory = "/Users/ntustison/Data/JimGee/AllenDevelopmentalVelocityFlows/AlignedSimpleSegmentations/"

template_ids = tuple(reversed(("E11-5", "E13-5", "E15-5", "E18-5", "P04", "P14", "P56")))

transform_list = list()
which_to_invert = list()

fixed_labels_file = annotation_directory + template_ids[0] + "_LABELS.nii.gz"
fixed_labels = ants.image_read(fixed_labels_file)

for i in range(1, len(template_ids)):
    print("Processing ", )
    moving_labels_file = annotation_directory + template_ids[i] + "_LABELS.nii.gz"
    moving_labels = ants.image_read(moving_labels_file)

    output_registration_prefix = output_directory + template_ids[0] + "x" + template_ids[i] + "_"
    reg = ants.registration(fixed_labels, moving_labels, type_of_transform="antsRegistrationSyNQuick[r]", 
                            outprefix=output_registration_prefix, verbose=True)    
    
    warped_labels = ants.apply_transforms(fixed_labels, moving_labels, transformlist=reg['fwdtransforms'], whichtoinvert=None, interpolator="nearestNeighbor")
    ants.image_write(warped_labels, output_registration_prefix + "LABELS.nii.gz")
    
    moving_labels_file = annotation_directory + template_ids[i] + "_LABELSwVentricle.nii.gz"
    if os.path.exists(moving_labels_file):
        moving_labels = ants.image_read(moving_labels_file)
        warped_labels = ants.apply_transforms(fixed_labels, moving_labels, transformlist=reg['fwdtransforms'], whichtoinvert=None, interpolator="nearestNeighbor")
        ants.image_write(warped_labels, output_registration_prefix + "LABELSwVentricle.nii.gz")
        
