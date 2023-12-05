import ants
import glob
import os
import numpy as np

os.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = "8"

template_directory = "/Users/ntustison/Data/JimGee/AllenDevelopmentalVelocityFlows/DevCCFtemplates_Lite-uint16/"
output_directory = "/Users/ntustison/Data/JimGee/AllenDevelopmentalVelocityFlows/MouseBrainVelocityFlow/Data/P56xAlignedSimpleSegmentations/"
output_directory2 = "/Users/ntustison/Data/JimGee/AllenDevelopmentalVelocityFlows/MouseBrainVelocityFlow/Data/P56xAlignedTemplates/"

template_ids = tuple(reversed(("E11-5", "E13-5", "E15-5", "E18-5", "P04", "P14", "P56")))

##
# Resample simple annotations
# 

for i in range(len(template_ids)):
    resampled_labels_file = output_directory + "P56x" + template_ids[i] + "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi_resampled.nii.gz"
    if not os.path.exists(resampled_labels_file):
        print("Resampling annotations ", template_ids[i])
        labels_file = output_directory + "P56x" + template_ids[i] + "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi.nii.gz"
        labels = ants.image_read(labels_file)
        labels_resampled = ants.resample_image(labels, resample_params=(0.05, 0.05, 0.05), use_voxels=False, interp_type=1)
        ants.image_write(labels_resampled, resampled_labels_file)

##
# Resample simple annotations
# 

reference_image = ants.image_read(output_directory + "P56xP56_DevCCF_Annotations_20um_symmetric_commonROIs_hemi_resampled.nii.gz")

for i in range(len(template_ids)):
    print("Processing", template_ids[i])
    template_stage_directory = glob.glob(template_directory + template_ids[i] + "*")[0]
    template_stage_directory_base = os.path.basename(template_stage_directory)
    template_stage_output_directory = output_directory2 + template_stage_directory_base
    if not os.path.exists(template_stage_output_directory):
        os.makedirs(template_stage_output_directory, exist_ok=True)
    template_stage_files = glob.glob(template_stage_directory + "//**.nii.gz")
    
    xfrm = ants.read_transform(output_directory + "P56x" + template_ids[i] + "_xfrm.mat")
    for j in range(len(template_stage_files)):
        print("   Warping ", template_stage_files[j])
        template_stage = ants.image_read(template_stage_files[j])
        warped_template_stage = xfrm.apply_to_image(template_stage, reference_image, interpolation='linear') 
        ants.image_write(warped_template_stage, template_stage_output_directory + "/" + os.path.basename(template_stage_files[j]))