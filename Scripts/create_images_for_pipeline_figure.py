import ants
import antspynet

import glob
import os
import numpy as np

os.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = "4"

template_directory = "/Users/ntustison/Data/JimGee/AllenDevelopmentalVelocityFlows/MouseBrainVelocityFlow/Data/P56xAlignedTemplates/E15-5_MRI_37.5um/"
output_directory = template_directory + "DataAugmentation/"

template_id = "E15-5"
template_image_files = glob.glob(template_directory + "*.nii.gz")
templates = list()
template_modalities = list()
for i in range(len(template_image_files)):
    print("Reading", template_image_files[i])
    template_modalities.append(ants.image_read(template_image_files[i]))
templates.append(template_modalities)    

number_of_pseudo_subjects = 5


aug = antspynet.data_augmentation(templates, segmentation_image_list=None, pointset_list=None, 
                                    number_of_simulations=number_of_pseudo_subjects, 
                                    reference_image=None, 
                                    transform_type='affineAndDeformation', 
                                    noise_model='additivegaussian', 
                                    noise_parameters=(0.0, 0.005), 
                                    sd_simulated_bias_field=0.01, 
                                    sd_histogram_warping=0.05, 
                                    sd_affine=0.05, 
                                    sd_deformation = 0.1, 
                                    output_numpy_file_prefix=None, 
                                    verbose=True)

for i in range(len(aug['simulated_images'])):
    print("Writing simulated image ", str(i))
    for j in range(len(template_image_files)):
        ants.image_write(aug['simulated_images'][i][j], output_directory + "/simulated_image_" + str(i) + "_" + str(j) + ".nii.gz")


image_files = glob.glob(output_directory + "*.nii.gz")
for i in range(len(image_files)):
    print("Processing image", str(i), "of", str(len(image_files)))
    image = ants.image_read(image_files[i])
    image_n4 = ants.n4_bias_field_correction(image, rescale_intensities=True, spline_param=10)
    image_n4_file = image_files[i].replace(".nii.gz", "_n4.nii.gz")
    ants.image_write(image_n4, image_n4_file)

