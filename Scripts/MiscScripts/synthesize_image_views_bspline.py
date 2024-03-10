import ants

import numpy as np
import glob
import os
import time
import shutil
import tempfile

os.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = "8"

def bspline_approximate_volume(image_list, output_size=(256, 256, 256), bspline_epsilon=1e-4, verbose=True):

    scattered_data = None
    parametric_values = None
    weight_values = None
    for i in range(len(image_list)):     
        indices = np.meshgrid(list(range(image_list[i].shape[0])), 
                              list(range(image_list[i].shape[1])), 
                              list(range(image_list[i].shape[2])))
        indices_array = np.stack((indices[1].flatten(), 
                                  indices[0].flatten(), 
                                  indices[2].flatten()), axis=0)

        scaling = np.eye(3)
        for d in range(3):
            scaling[d, d] = image_list[i].spacing[d]
        direction = np.matmul(image_list[i].direction, scaling)

        image_parametric_values = np.matmul(direction, indices_array).transpose()
        for d in range(3):
            image_parametric_values[:, d] += image_list[i].origin[d]

        weight_array = np.zeros(image_list[i].shape)
        for d in range(3):
            weight_array += np.power(np.gradient(image_list[i].numpy(), axis=d), 2)
        weight_array = np.sqrt(weight_array)

        if i == 0:
            parametric_values = image_parametric_values
            scattered_data = np.atleast_2d(image_list[i].numpy().flatten()).transpose()
            weight_values = np.atleast_2d(weight_array.flatten()).transpose()
        else:
            parametric_values = np.concatenate((parametric_values, image_parametric_values))
            scattered_data = np.concatenate((scattered_data, np.atleast_2d(image_list[i].numpy().flatten()).transpose()))
            weight_values = np.concatenate((weight_values, np.atleast_2d(weight_array.flatten()).transpose()))

    min_parametric_values = np.min(parametric_values, axis=0)
    max_parametric_values = np.max(parametric_values, axis=0)
    spacing = np.zeros((3,))
    for d in range(3):
        spacing[d] = (max_parametric_values[d] - min_parametric_values[d]) / (output_size[d] - 1) + bspline_epsilon

    bspline_image = ants.fit_bspline_object_to_scattered_data(scattered_data, parametric_values, 
                                                              parametric_domain_origin=min_parametric_values - bspline_epsilon,
                                                              parametric_domain_spacing=spacing,
                                                              parametric_domain_size=output_size,
                                                              data_weights=weight_values,
                                                              number_of_fitting_levels=6,
                                                              mesh_size=4)   
    return bspline_image

################################################################################################

base_directory = '/Users/ntustison/Data/Mouse/HighResolution/'

subject_directories = glob.glob(base_directory + "MRI/sub*")

for i in range(len(subject_directories)):
    
    print(subject_directories[i])
    print(" ----> " + str(i) + " out of " + str(len(subject_directories)))
    
    subject_basename = os.path.basename(subject_directories[i])
    
    axial_image_file = base_directory + "MRI/" + subject_basename + "/axial/" + subject_basename + "_axial.nii.gz"
    sagittal_image_file = base_directory + "MRI/" + subject_basename + "/sagittal/" + subject_basename + "_sagittal.nii.gz"
    coronal_image_file = base_directory + "MRI/" + subject_basename + "/coronal/" + subject_basename + "_coronal.nii.gz"
    
    if not os.path.exists(axial_image_file) or not os.path.exists(sagittal_image_file) or not os.path.exists(coronal_image_file):
        raise ValueError("A file doesn't exist.")

    bspline_image_file = base_directory + "MRI/" + subject_basename + "/" + subject_basename + "_bspline.nii.gz"
    if not os.path.exists(bspline_image_file):
              
        axial_image = ants.image_read(axial_image_file)
        sagittal_image = ants.image_read(sagittal_image_file)
        coronal_image = ants.image_read(coronal_image_file)
        
        image_list = list()
        image_list.append(ants.iMath_normalize(axial_image))
        image_list.append(ants.iMath_normalize(sagittal_image))
        image_list.append(ants.iMath_normalize(coronal_image))

        bspline_image = bspline_approximate_volume(image_list=image_list)        
        ants.image_write(bspline_image, bspline_image_file)
    else:
        bspline_image = ants.image_read(bspline_image_file)
        
    sharp_image_file = base_directory + "MRI/" + subject_basename + "/" + subject_basename + "_bspline_sharpen.nii.gz"
    if not os.path.exists(sharp_image_file):
        sharp_image = ants.iMath_sharpen(bspline_image)
        ants.image_write(sharp_image, sharp_image_file)
    else:
        sharp_image = ants.image_read(sharp_image_file)
        
    reorient_image_file = base_directory + "MRI/" + subject_basename + "/" + subject_basename + "_bspline_sharpen_reoriented.nii.gz"
    if not os.path.exists(reorient_image_file):
        reorient_image = ants.from_numpy(np.flip(np.rot90(sharp_image.numpy(), k=1, axes=(1,2)), axis=2), 
                                            origin=(0, 0, 0),
                                            spacing=(bspline_image.spacing[0], bspline_image.spacing[2], bspline_image.spacing[1]), 
                                            direction=bspline_image.direction)
        ants.image_write(reorient_image, reorient_image_file)
    else:
        reorient_image = ants.image_read(reorient_image_file)    
    
    flipped_image_file = base_directory + "MRI/" + subject_basename + "/" + subject_basename + "_bspline_sharpen_reoriented_flipped.nii.gz"
    if not os.path.exists(flipped_image_file):
        flipped_image = ants.from_numpy(np.flip(reorient_image.numpy(), axis=0), 
                                            origin=reorient_image.origin,
                                            spacing=reorient_image.spacing,
                                            direction=reorient_image.direction)
        ants.image_write(flipped_image, flipped_image_file)
