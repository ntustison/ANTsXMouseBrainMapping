import ants
import antspynet

import numpy as np
import glob
import os
import time
import shutil
import tempfile

os.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = "4"
os.environ["intra_op_parallelism_threads"] = "4"
os.environ["inter_op_parallelism_threads"] = "4"

def preprocess_original_subject_image(subject_image, denoise=False, verbose=True):
    subject_channels = ants.split_channels(subject_image)

    subject_channels_preprocessed = list()
    for i in range(len(subject_channels)):

        if verbose:
            print("Inverting channel", i, "\n")

        subject_preprocessed = subject_channels[i] * -1.0 + subject_channels[i].max()
        subject_preprocessed_array = subject_preprocessed.numpy()

        number_of_slices = subject_preprocessed_array.shape[2]  

        for j in range(number_of_slices):
            if verbose:
                print("  slice " + str(j) + " out of " + str(number_of_slices))
            slice = subject_preprocessed_array[:,:,j]
            if slice.std() < 0.001 :
                subject_preprocessed_array[:,:,j] = 0

        subject_channels_preprocessed.append(ants.from_numpy(subject_preprocessed_array, 
            origin=subject_image.origin, spacing=subject_image.spacing, direction=subject_image.direction))

    if denoise:
        for i in range(len(subject_channels_preprocessed)):
            if verbose:
                print("Denoising channel", i, "\n")
            subject_channel_array = subject_channels_preprocessed[i].numpy()
            for j in range(subject_channel_array.shape[2]):
                if verbose:
                    print("  slice " + str(j) + " out of " + str(number_of_slices))
                slice = ants.from_numpy(np.squeeze(subject_channel_array[:,:,j]))
                slice_denoised = ants.denoise_image(slice, noise_model="Gaussian")
                subject_channel_array[:,:,j] = slice_denoised.numpy()
            subject_channels_preprocessed[i] = ants.from_numpy(subject_channel_array, 
                origin=subject_channels_preprocessed[i].origin, spacing=subject_channels_preprocessed[i].spacing,
                direction=subject_channels_preprocessed[i].direction)  
             
    subject_preprocessed = ants.merge_channels(subject_channels_preprocessed)
    return subject_preprocessed

def resample_multichannel_volume(image, output_size):

    image_channels = ants.split_channels(image)
    image_resampled_channels = list()
    for c in range(len(image_channels)):
        image_resampled_channels.append(ants.resample_image(image_channels[c], output_size, 
                                                            use_voxels=True, interp_type=0))
    image_resampled = ants.merge_channels(image_resampled_channels)        
    return image_resampled

def bspline_approximate_volume(image, missing_slices=None, verbose=True):
    array = image.numpy()
    parametric_indices = None
    scattered_data = None
    is_multichannel = False
    if image.components > 1:
        is_multichannel = True
               
    for j in range(array.shape[2]):
        if missing_slices is not None and j in missing_slices:
            continue 
        if is_multichannel:
           slice = array[:,:,j,:]    
        else:   
           slice = array[:,:,j]    
        slice_indices = np.meshgrid(list(range(slice.shape[0])), list(range(slice.shape[1])), j)
        slice_indices = (np.stack((slice_indices[1].flatten(), slice_indices[0].flatten(), slice_indices[2].flatten()), axis=0)).transpose()
        if is_multichannel:
            slice_values = (np.stack((slice[:,:,0].flatten(), slice[:,:,1].flatten(), slice[:,:,2].flatten()))).transpose()
        else:    
            slice_values = np.atleast_2d(slice.flatten()).transpose()
        if parametric_indices is None:
            parametric_indices = slice_indices
            scattered_data = slice_values
        else:    
            parametric_indices = np.concatenate((parametric_indices, slice_indices))
            scattered_data = np.concatenate((scattered_data, slice_values))
    bspline_image = ants.fit_bspline_object_to_scattered_data(scattered_data, parametric_indices, 
                                                              parametric_domain_origin=(0, 0, 0),
                                                              parametric_domain_spacing=(1.0, 1.0, 1.0),
                                                              parametric_domain_size=array.shape[:3],
                                                              number_of_fitting_levels=6,
                                                              mesh_size=8)   
    
    bspline_image.set_spacing(image.spacing)
    bspline_image.set_origin(image.origin)
    bspline_image.set_direction(image.direction)    

    return bspline_image

def super_resolution_refine_volume(image, replacement_image=None, missing_slices=None, verbose=True):

    sr_array = image.numpy()
    slice_list = list()
    slice_index_list = list()
    for j in range(image.shape[2]):
        if missing_slices is None or j in missing_slices:
            slice_channels = list()
            for c in range(sr_array.shape[-1]):
                slice_channels.append(ants.from_numpy(sr_array[:,:,j,c]))
            slice_list.append(ants.merge_channels(slice_channels))    
            slice_index_list.append(j)
    
    if replacement_image is not None:
        sr_array = replacement_image.array()
        
    slice_list_sr = antspynet.allen_histology_super_resolution(slice_list, verbose=verbose)
    for j in range(len(slice_index_list)):
        slice_sr = slice_list_sr[j]
        slice_sr_resampled = resample_multichannel_volume(slice_sr, image.shape[0:2])
        sr_array[:,:,slice_index_list[j],:] = slice_sr_resampled.numpy()
        
    sr_image = ants.from_numpy(sr_array, has_components=True)
    sr_image.set_spacing(image.spacing)
    sr_image.set_origin(image.origin)
    sr_image.set_direction(image.direction)    
    
    return sr_image

def register_template(image, template, which_channel='avg', hemisphere_only=True, 
                      hemisphere_subject_midline_slice=None, template_lateral_slice=None, 
                      transform_type="linear", verbose=True):
    
    if which_channel != "scalar":
        image_channels = ants.split_channels(image)
        if which_channel == 'avg':
            scalar_image = (image_channels[0] + image_channels[1] + image_channels[2]) / 3
        else:
            scalar_image = image_channels[which_channel]
    else:
        scalar_image = image             

    subject_for_reg = ants.image_clone(scalar_image)
    if isinstance(template, ants.core.ants_image.ANTsImage):
        template_for_reg = ants.image_clone(template)
    else: 
        template_for_reg = ants.image_clone(template[0])

    if hemisphere_only:
        
        if transform_type == "labels":
        
            if template_lateral_slice is not None:
                lower_crop_region = (template_lateral_slice, 0, 0)
                upper_crop_region = (template_for_reg.shape[0] - template_lateral_slice + 1, template_for_reg.shape[1], template_for_reg.shape[2])
                template_for_reg = ants.crop_indices(template_for_reg, lower_crop_region, upper_crop_region)
                subject_for_reg = ants.crop_indices(subject_for_reg, lower_crop_region, upper_crop_region)

            subject_for_reg_array = subject_for_reg.numpy()
            subject_for_reg_array_flipped = np.flip(subject_for_reg_array, 1)
            subject_for_reg = ants.from_numpy( 
                subject_for_reg_array + subject_for_reg_array_flipped,
                spacing=subject_for_reg.spacing, origin=subject_for_reg.origin, 
                direction=subject_for_reg.direction)

        else:         

            if hemisphere_subject_midline_slice is not None:
                lower_crop_region = (0, 0, 0)
                upper_crop_region = (subject_for_reg.shape[0], subject_for_reg.shape[1], hemisphere_subject_midline_slice)
                subject_for_reg = ants.crop_indices(subject_for_reg, lower_crop_region, upper_crop_region)
            
            if template_lateral_slice is not None:
                # lower_crop_region = (template_lateral_slice, 0, 0)
                # upper_crop_region = (template_for_reg.shape[0] - template_lateral_slice + 1, template_for_reg.shape[1], template_for_reg.shape[2])
                lower_crop_region = (0, template_lateral_slice, 0)
                upper_crop_region = (template_for_reg.shape[0],  template_for_reg.shape[1] - template_lateral_slice + 1, template_for_reg.shape[2])
                template_for_reg = ants.crop_indices(template_for_reg, lower_crop_region, upper_crop_region)
                                            
            subject_for_reg_array = subject_for_reg.numpy()
            subject_for_reg_array_flipped = np.flip(subject_for_reg_array, 2)
            subject_for_reg = ants.from_numpy( 
                np.concatenate([subject_for_reg_array, subject_for_reg_array_flipped], axis=2),
                spacing=subject_for_reg.spacing, origin=subject_for_reg.origin, 
                direction=subject_for_reg.direction)

            # ants.image_write(subject_for_reg, "~/Desktop/subject_for_reg.nii.gz")
            # ants.image_write(template_for_reg, "~/Desktop/template_for_reg.nii.gz")
            # raise ValueError("HERE")


    if transform_type == "linear":
        affine_reg = ants.registration(subject_for_reg, template_for_reg,
                    type_of_transform="antsRegistrationSyNQuick[a]", verbose=verbose)        
        return affine_reg['fwdtransforms'][0]
    elif transform_type == "deformable":
        reg = ants.registration(subject_for_reg, template_for_reg,
                                type_of_transform="antsRegistrationSyNQuick[s,2]", 
                                verbose=verbose)        
        return reg
    elif transform_type == "labels":
        reg = ants.registration(subject_for_reg, template_for_reg,
                                type_of_transform="antsRegistrationSyN[s,2]", 
                                verbose=verbose)        
        return reg
    else:
        raise ValueError("Unrecognized transform_type")

def warp_to_template(image, template, transform_list, which_to_invert=None, 
                     hemisphere_only=True, hemisphere_subject_midline_slice=None, 
                     verbose=True):

    image_channels = ants.split_channels(image)

    template_x_image_channels = list()
    for c in range(len(image_channels)):
                
        if hemisphere_only:
            if hemisphere_subject_midline_slice is not None:
                lower_crop_region = (0, 0, 0)
                upper_crop_region = (image_channels[c].shape[0], image_channels[c].shape[1], hemisphere_subject_midline_slice)
                image_channels[c] = ants.crop_indices(image_channels[c], lower_crop_region, upper_crop_region)
                                        
            image_channel_array = image_channels[c].numpy()
            # image_channel_array_flipped = np.flip(image_channel_array, 2)
            image_channel_array_flipped = np.zeros_like(image_channel_array)
            slice_index = image_channel_array.shape[2] - hemisphere_subject_midline_slice
            image_channel_array_flipped[0:slice_index] = image_channel_array[hemisphere_subject_midline_slice:image_channel_array.shape[2]]
            image_channels[c] = ants.from_numpy( 
                np.concatenate([image_channel_array, image_channel_array_flipped], axis=2),
                spacing=image_channels[c].spacing, origin=image_channels[c].origin, 
                direction=image_channels[c].direction)
            
        template_x_image_channel = ants.apply_transforms(template, image_channels[c], transformlist=transform_list, 
                                         whichtoinvert=which_to_invert, verbose=verbose) 
        template_x_image_channels.append(template_x_image_channel)
        
    template_x_image = ants.merge_channels(template_x_image_channels)
    
    return template_x_image

        


def within_slice_registration(image, image_mask=None, template_mask=None, is_sagittal=True,
                              which_channel='avg', start_largest_intensity_slice=False, verbose=True):

    image_channels = ants.split_channels(image)
    number_of_slices = image.shape[2]

    warped_image_array = image.numpy()    

    use_masks = False
    if image_mask is not None and template_mask is not None:
        use_masks = True

    if which_channel == 'avg':
        scalar_image = (image_channels[0] + image_channels[1] + image_channels[2]) / 3
    else:
        scalar_image = image_channels[which_channel]
    scalar_array = scalar_image.numpy()
      
    current_fixed_slice = number_of_slices - 1

    if start_largest_intensity_slice:
        largest_intensity_mass = 0
        largest_intensity_index = -1         
        if verbose:
            print("Finding largest intensity mass slice.")
        for i in range(number_of_slices):
            tmp_slice = scalar_array[:,:,i]
            if tmp_slice.sum() > largest_intensity_mass:
                largest_intensity_index = i
                largest_intensity_mass = tmp_slice.sum()
        if verbose:
            print("Largest intensity mass slice: ", largest_intensity_index)
        current_fixed_slice = largest_intensity_index

    i = current_fixed_slice - 1
    fixed_slice = ants.slice_image(scalar_image, axis=2, idx=i+1, collapse_strategy=1)
    while fixed_slice.sum() < 100:
        i = i - 1
        if i == -1:
            raise ValueError("Problem with the image.  Zero intensity values for entire volume.")
        fixed_slice = ants.slice_image(scalar_image, axis=2, idx=i+1, collapse_strategy=1)

    fixed_mask_slice = None
    moving_mask_slice = None

    field = np.zeros((*scalar_image.shape, 3))

    transform_type = "antsRegistrationSyNQuick[bo,32,8]"
    while i >= 0:
        moving_slice = ants.slice_image(scalar_image, axis=2, idx=i, collapse_strategy=1)
        if moving_slice.sum() < 100 or fixed_slice.sum() < 100:
            i = i - 1
            continue
        if use_masks:
            moving_mask_slice = ants.slice_image(image_mask, axis=2, idx=i, collapse_strategy=1)
            fixed_mask_slice = ants.slice_image(template_mask, axis=2, idx=i, collapse_strategy=1)
        if verbose:
            print(f"Registering slice (reverse) {i+1} <--> {i}, use_masks = {use_masks}")
        multivariate_extras = None    
        if use_masks and fixed_mask_slice.sum() > 0 and moving_mask_slice.sum() > 0:
            multivariate_extras = list()            
            multivariate_extras.append(["MSQ", fixed_mask_slice, moving_mask_slice, 2, 1])
        reg = ants.registration(fixed_slice, moving_slice, type_of_transform=transform_type, multivariate_extras=multivariate_extras, verbose=False)
        for c in range(len(image_channels)):
            moving_channel_slice = ants.slice_image(image_channels[c], axis=2, idx=i, collapse_strategy=1)
            warped_image_array[:,:,i,c] = (ants.apply_transforms(fixed_slice, moving_channel_slice,
                    reg['fwdtransforms'])).numpy()
        if use_masks:
            fixed_mask_slice = ants.apply_transforms(fixed_slice, moving_mask_slice, 
                                                     reg['fwdtransforms'], interpolator="nearestNeighbor")
        fixed_slice = reg['warpedmovout']            

        compose_xfrm_file = tempfile.NamedTemporaryFile(delete=False)
        ants.apply_transforms(fixed_slice, moving_slice, transformlist=reg['fwdtransforms'], compose=compose_xfrm_file.name)
        xfrm = ants.image_read(compose_xfrm_file.name + "comptx.nii.gz")
        xfrm_channels = ants.split_channels(xfrm)

        # Based on the direction matrix of the fixed space
        if is_sagittal:
            field[:,:,i,1] = xfrm_channels[0].numpy()
            field[:,:,i,2] = xfrm_channels[1].numpy() * -1.0
        else: 
            field[:,:,i,0] = xfrm_channels[0].numpy()
            field[:,:,i,2] = xfrm_channels[1].numpy() * -1.0

        i = i - 1

    if start_largest_intensity_slice:
        current_fixed_slice = largest_intensity_index
        i = largest_intensity_index
        fixed_slice = ants.slice_image(scalar_image, axis=2, idx=i, collapse_strategy=1)
        fixed_mask_slice = None

        # go forward
        while i < number_of_slices - 1:
            moving_slice = ants.slice_image(scalar_image, axis=2, idx=i+1, collapse_strategy=1)
            if moving_slice.sum() < 100 or fixed_slice.sum() < 100:
                i = i + 1
                continue
            if use_masks:
                moving_mask_slice = ants.slice_image(image_mask, axis=2, idx=i, collapse_strategy=1)
                fixed_mask_slice = ants.slice_image(template_mask, axis=2, idx=i, collapse_strategy=1)
            if verbose:
                print(f"Registering slice (forward) {i} <--> {i+1}, use_masks = {use_masks}")
            multivariate_extras = None    
            if use_masks and fixed_mask_slice.sum() > 0 and moving_mask_slice.sum() > 0:
                multivariate_extras = list()            
                multivariate_extras.append(["MSQ", fixed_mask_slice, moving_mask_slice, 0.5, 1])
            reg = ants.registration(fixed_slice, moving_slice, type_of_transform=transform_type, multivariate_extras=multivariate_extras, verbose=False)
            for c in range(len(image_channels)):
                moving_channel_slice = ants.slice_image(image_channels[c], axis=2, idx=i+1, collapse_strategy=1)
                warped_image_array[:,:,i+1,c] = (ants.apply_transforms(fixed_slice, moving_channel_slice,
                        reg['fwdtransforms'])).numpy()
            fixed_slice = reg['warpedmovout']            

            compose_xfrm_file = tempfile.NamedTemporaryFile(delete=False)
            ants.apply_transforms(fixed_slice, moving_slice, transformlist=reg['fwdtransforms'], compose=compose_xfrm_file.name)
            xfrm = ants.image_read(compose_xfrm_file.name + "comptx.nii.gz")
            xfrm_channels = ants.split_channels(xfrm)

            # Based on the direction matrix of the fixed space
            if is_sagittal:
                field[:,:,i,1] = xfrm_channels[0].numpy()
                field[:,:,i,2] = xfrm_channels[1].numpy() * -1.0
            else: 
                field[:,:,i,0] = xfrm_channels[0].numpy()
                field[:,:,i,2] = xfrm_channels[1].numpy() * -1.0

            i = i + 1

    # warped_image = ants.from_numpy(warped_image_array, origin=image.origin,
    #                                spacing=image.spacing, direction=image.direction,
    #                                has_components=True)  

    field_image = ants.from_numpy(data=field, origin=image.origin,
                      spacing=image.spacing, direction=image.direction,
                      has_components=True)

    return field_image



#################################################################################################
#################################################################################################
#################################################################################################
#################################################################################################
#################################################################################################



base_directory = "/Users/ntustison/Data/JimGee/AllenTesting/"
input_directory = base_directory + "subjects_reconstructed_resampled/"
input_template_space_labels_directory = base_directory + "subjects_reconstructed_resampled_label_masks_template_space/"
input_expression_directory = base_directory + "subjects_individual_genes_extracted/"
output_directory = base_directory + "subjects_reconstructed_processed2/"

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

use_mask = True
templates = list()
template_labels = None
template_space_labels_files = None
warp_expression_data = True

which_age_to_process = "E11x5"

if which_age_to_process == "E11x5":

    template_directory = base_directory + "Templates/20230113_MRI_Templates_MaskedSymmetricBgRemovedSterotaxic/E11-5_MRI_SymmetricTemplates_31.5um/"

    template_ADC_file = template_directory + "T_E11-5_MRI-adc_SymmetricTemplate_31.5um.nii.gz"
    template_FA_file = template_directory + "T_E11-5_MRI-fa_SymmetricTemplate_31.5um.nii.gz"
    template_left_right_mask_file = template_directory + "T_E11-5_MRI-left_right_mask_SymmetricTemplate_31.5um.nii.gz"
    template_left_right_mask = ants.image_read(template_left_right_mask_file)

    template_ADC = ants.image_read(template_ADC_file) * ants.threshold_image(template_left_right_mask, 0, 0, 0, 1)
    template_FA = ants.image_read(template_FA_file) * ants.threshold_image(template_left_right_mask, 0, 0, 0, 1)
    templates_E11x5 = [template_ADC, template_FA]

    templates.append(templates_E11x5)

    # files = [
    #         "2974_E11x5_sagittal_section_resampled.nii.gz",
    #         "701324_E11x5_sagittal_section_resampled.nii.gz",
    #         "713009_E11x5_sagittal_section_resampled.nii.gz",
    #         "3247_E11x5_coronal_section_resampled.nii.gz",
    #         "703790_E11x5_coronal_section_resampled.nii.gz"
    #         ]
    # midline_slice = [69, 71, 48, None, None]
    # template_lateral_slice = [64, 70, 70, None, None]

    files = [
            "2974_E11x5_sagittal_section_resampled.nii.gz",
            "701324_E11x5_sagittal_section_resampled.nii.gz"
            ]
    midline_slice = [69, 71]
    template_lateral_slice = [64, 70]

elif which_age_to_process == "E13x5":
    
    template_directory = base_directory + "Templates/20230113_MRI_Templates_MaskedSymmetricBgRemovedSterotaxic/E13-5_MRI_SymmetricTemplates_34um/"

    template_E13x5_ADC_file = template_directory + "T_E13-5_MRI-adc_SymmetricAvg_34um.nii.gz"
    template_E13x5_FA_file = template_directory + "T_E13-5_MRI-fa_SymmetricAvg_34um.nii.gz"
    template_E13x5_left_right_mask_file = template_directory + "T_E13-5_MRI-left_right_mask_SymmetricAvg_34um.nii.gz"
    template_left_right_mask = ants.image_read(template_E13x5_left_right_mask_file)

    template_labels = ants.image_read(template_directory + "T_E13-5_MRI-labels.nii.gz")

    template_E13x5_ADC = ants.image_read(template_E13x5_ADC_file) * ants.threshold_image(template_left_right_mask, 0, 0, 0, 1)
    template_E13x5_FA = ants.image_read(template_E13x5_FA_file) * ants.threshold_image(template_left_right_mask, 0, 0, 0, 1)
    templates_E13x5 = [template_E13x5_ADC, template_E13x5_FA]

    templates.append(templates_E13x5)

    files = [
            "5269_E13x5_coronal_section_resampled.nii.gz",
            "5273_E13x5_coronal_section_resampled.nii.gz",
            "702959_E13x5_coronal_section_resampled.nii.gz",
            "702276_E13x5_sagittal_section_resampled.nii.gz",
            "702957_E13x5_sagittal_section_resampled.nii.gz"
            ]
    midline_slice = [None, None, None, 81, 77]
    template_lateral_slice = [None, None, None, 76, 76]
    
    template_x_subject_space_labels_files = [
            "5269_E13x5_coronal_section_resampled_to_template_ch1_labels.nii.gz", 
            "5273_E13x5_coronal_section_resampled_to_template_ch1_labels.nii.gz", 
            "702959_E13x5_coronal_section_resampled_to_template_ch1_labels.nii.gz",
            "702276_E13x5_sagittal_section_resampled_to_template_ch1_labels.nii.gz", 
            "702957_E13x5_sagittal_section_resampled_to_template_ch1_labels.nii.gz"
            ]
    template_x_subject_space_labels_files = [input_template_space_labels_directory + s for s in template_x_subject_space_labels_files]  
     
elif which_age_to_process == "P28":

    template_directory = base_directory + "Templates/20230113_MRI_Templates_MaskedSymmetricBgRemovedSterotaxic/P56_MRI_SymmetricTemplates_50um_StereotaxicAligned/"

    template_P56_FA_file = template_directory + "T_P56_MRI-fa_SymmetricStereotaxicTemplate_50um.nii.gz"
    template_P56_ADC_file = template_directory + "T_P56_MRI-adc_SymmetricStereotaxicTemplate_50um.nii.gz"
    template_P56_left_right_mask_file = template_directory + "T_P56_MRI-left_right_mask_SymmetricStereotaxicTemplate_50um.nii.gz"
    template_left_right_mask = ants.image_read(template_P56_left_right_mask_file)

    template_P56_mask = ants.threshold_image(template_left_right_mask, 1, 2, 1, 0)

    template_P56_FA = ants.image_read(template_P56_FA_file) * template_P56_mask
    template_P56_ADC = ants.image_read(template_P56_ADC_file) * template_P56_mask
    templates_P56 = [template_P56_ADC, template_P56_FA]
    templates.append(templates_P56)

    files = [
            "948_P28_sagittal_section_resampled.nii.gz",
            "949_P28_sagittal_section_resampled.nii.gz",
            "2402_P28_sagittal_section_resampled.nii.gz",
            "4885_P28_coronal_section_resampled.nii.gz",
            "4889_P28_coronal_section_resampled.nii.gz"
            ]
    midline_slice = [126, 153, 155, None, None]
    template_lateral_slice = [68, 52, 55, None, None]


files = [input_directory + s for s in files]

for i in range(len(files)):
    print("Processing" + files[i] + " (" + str(i+1) + " out of " + str(len(files)) + ")")
 
    image = ants.image_read(files[i])
    image_channels = ants.split_channels(image)   
    image_mask = None
    if use_mask:
        image_mask_file = files[i].replace("resampled.nii.gz", "resampled_mask.nii.gz")
        image_mask = ants.image_read(image_mask_file)

    age_template = templates[0]
    # if "_P56_" in subject_files[i]:
    #     age_template = templates[1]

    use_hemisphere = True
    age_template_left_right_mask = template_left_right_mask
    if "coronal" in files[i]:
        use_hemisphere = False

   # Preprocess image (invert intensities and optional denoise)
    print(" ********************************* ")
    print(" Preprocess image ")
    print(" ********************************* ")
    preprocessed_file = output_directory + os.path.basename(files[i]).replace(".nii.gz","_preprocessed.nii.gz")

    if os.path.exists(preprocessed_file):
        preprocessed_image = ants.image_read(preprocessed_file)
    else:
        preprocessed_image = preprocess_original_subject_image(image, denoise=True, verbose=True)
        if use_mask:
            preprocessed_channels = ants.split_channels(preprocessed_image)
            for j in range(len(preprocessed_channels)):
                preprocessed_channels[j] = preprocessed_channels[j] * image_mask
            preprocessed_image = ants.merge_channels(preprocessed_channels)
        ants.image_write(preprocessed_image, preprocessed_file)

    # Find missing slices
    print(" ********************************* ")
    print(" Find missing slices.")                
    print(" ********************************* ")
    array = preprocessed_image.numpy()
    missing_slices = list()
    for j in range(array.shape[2]):
        slice = array[:,:,j,:]
        slice_sum = slice.sum()
        if slice_sum < 100.0:
            print( "        Missing slice " + str(j) + ", intensity sum = " + str(slice_sum))
            missing_slices.append(j)
            
    # B-spline interpolation
    print(" ********************************* ")
    print(" Begin B-spline interpolation.")                
    print(" ********************************* ")
    bspline_file = output_directory + os.path.basename(files[i]).replace(".nii.gz","_bspline.nii.gz")
    bspline_mask_file = output_directory + os.path.basename(files[i]).replace(".nii.gz","_bsplineMask.nii.gz")
    if os.path.exists(bspline_file) and os.path.exists(bspline_mask_file):
        bspline_image = ants.image_read(bspline_file)
        bspline_image_mask = ants.image_read(bspline_mask_file)
    else:
        tic = time.perf_counter()
        preprocessed_image_downsampled = resample_multichannel_volume(preprocessed_image, (256, 256, image.shape[2]))
        image_mask_downsampled = ants.resample_image(image_mask, (256, 256, image.shape[2]), use_voxels=True, interp_type=1)
        bspline_image_mask = bspline_approximate_volume(image_mask_downsampled, missing_slices=missing_slices, verbose=True)
        ants.image_write(bspline_image_mask, bspline_mask_file)
        bspline_image = bspline_approximate_volume(preprocessed_image_downsampled, missing_slices=missing_slices, verbose=True)
        ants.image_write(bspline_image, bspline_file)
        toc = time.perf_counter()
        print(f"    Elapsed time: {toc - tic:0.1f} seconds.")     

    bspline_image_mask = ants.threshold_image(bspline_image_mask, 0.5, 1.5, 1, 0)

    # template to subject registration (linear)
    print(" ********************************* ")
    print(" template to subject registration (linear)")
    print(" ********************************* ")
    age_template_warped_file_prefix = output_directory + os.path.basename(files[i]).replace(".nii.gz","_x_template")
    age_template_files = glob.glob(age_template_warped_file_prefix + "?.nii.gz")

    age_template_warped_left_right_mask_file = age_template_warped_file_prefix + "_left_right_mask_warped.nii.gz"
    image_x_template_affine = age_template_warped_file_prefix + "_subjectxTemplateGenericAffine.mat"

    age_template_warped = list()
    if not os.path.exists(image_x_template_affine):
        tic = time.perf_counter()
        tmp_affine = register_template(bspline_image, age_template, which_channel='avg', 
                                       hemisphere_only=use_hemisphere, 
                                       hemisphere_subject_midline_slice=midline_slice[i],
                                       template_lateral_slice=template_lateral_slice[i], 
                                       transform_type="linear")
        toc = time.perf_counter()
        print(f"    Elapsed time: {toc - tic:0.1f} seconds.")     
        image_x_template_affine = shutil.copy(tmp_affine, image_x_template_affine) 

    bspline_image_channels = ants.split_channels(bspline_image)

    age_template_warped = list() 
    for j in range(len(age_template)):
        age_template_warped.append(ants.apply_transforms(bspline_image_channels[0], age_template[j], transformlist=[image_x_template_affine]))
        ants.image_write(age_template_warped[j], age_template_warped_file_prefix + str(j) + ".nii.gz")

    age_template_left_right_mask_warped = ants.apply_transforms(bspline_image_channels[0], 
        age_template_left_right_mask, transformlist=[image_x_template_affine], 
        interpolator="nearestNeighbor")
    ants.image_write(age_template_left_right_mask_warped, age_template_warped_left_right_mask_file)

    # Slicewise image registration
    print(" ********************************* ")
    print(" Within-subject slicewise registration.")                
    print(" ********************************* ")
    
    bspline_refined_file = output_directory + os.path.basename(files[i]).replace(".nii.gz","_bsplineRefined.nii.gz")
    bspline_refined_xfrm_file = output_directory + os.path.basename(files[i]).replace(".nii.gz","_bsplineRefinedXfrm.nii.gz")
    if os.path.exists(bspline_refined_file):
        bspline_refined = ants.image_read(bspline_refined_file)
        bspline_refined_xfrm = ants.image_read(bspline_refined_xfrm_file)
    else:
        tic = time.perf_counter()
        template_mask_downsampled = ants.resample_image(age_template_left_right_mask_warped, (256, 256, image.shape[2]), 
                                                        use_voxels=True, interp_type=1)
        template_mask_downsampled = ants.threshold_image(template_mask_downsampled, 0, 0, 0, 1)
        bspline_refined_xfrm = within_slice_registration(bspline_image, bspline_image_mask, template_mask_downsampled, is_sagittal=use_hemisphere,
                                                         which_channel="avg", start_largest_intensity_slice=False, verbose=True)

        ants.image_write(bspline_refined_xfrm, bspline_refined_xfrm_file)
        bspline_refined_ants_xfrm = ants.transform_from_displacement_field(bspline_refined_xfrm)
        bspline_image_channels = ants.split_channels(bspline_image)
        for c in range(len(bspline_image_channels)):
            bspline_image_channels[c] = bspline_refined_ants_xfrm.apply_to_image(bspline_image_channels[c])
        bspline_refined = ants.merge_channels(bspline_image_channels)    
        ants.image_write(bspline_refined, bspline_refined_file)

        toc = time.perf_counter()
        print(f"    Elapsed time: {toc - tic:0.1f} seconds.")     


    # # Super-resolution
    # print(" ********************************* ")
    # print(" Super-resolution.")                
    # print(" ********************************* ")

    # bspline_refined_sr_file = output_directory + os.path.basename(files[i]).replace(".nii.gz","_bsplineRefinedSR.nii.gz")
    # if os.path.exists(bspline_refined_sr_file):
    #     bspline_sr_refined = ants.image_read(bspline_refined_sr_file)
    # else:
    #     tic = time.perf_counter()
    #     bspline_sr_refined = super_resolution_refine_volume(bspline_refined, missing_slices=missing_slices, verbose=True)
    #     toc = time.perf_counter()
    #     print(f"    Elapsed time: {toc - tic:0.1f} seconds.")     
    #     ants.image_write(bspline_sr_refined, bspline_refined_sr_file)

    # template to subject registration (deformable)
    print(" ********************************* ")
    print(" template to subject registration (deformable)")
    print(" ********************************* ")
    age_template_warped_file_prefix = output_directory + os.path.basename(files[i]).replace(".nii.gz","_xdef_template")
    age_template_files = glob.glob(age_template_warped_file_prefix + "?.nii.gz")
    image_xdef_template_affine = age_template_warped_file_prefix + "_subjectxTemplateGenericAffine.mat"
    image_xdef_template_warp = age_template_warped_file_prefix + "_subjectxTemplateWarp.nii.gz"
    image_xdef_template_invwarp = age_template_warped_file_prefix + "_subjectxTemplateInverseWarp.nii.gz"

    age_template_warped = list()
    if not os.path.exists(image_xdef_template_affine):
        tic = time.perf_counter()
        reg = register_template(bspline_refined, age_template, which_channel='avg', 
                                hemisphere_only=use_hemisphere, 
                                hemisphere_subject_midline_slice=midline_slice[i],
                                template_lateral_slice=template_lateral_slice[i], 
                                transform_type="deformable")
        toc = time.perf_counter()
        print(f"    Elapsed time: {toc - tic:0.1f} seconds.")     
        image_xdef_template_affine = shutil.copy(reg['fwdtransforms'][1], image_xdef_template_affine) 
        image_xdef_template_warp = shutil.copy(reg['fwdtransforms'][0], image_xdef_template_warp) 
        image_xdef_template_invwarp = shutil.copy(reg['invtransforms'][1], image_xdef_template_invwarp) 
        
    for j in range(len(age_template)):
        warped_age_template = ants.apply_transforms(bspline_image_mask, age_template[j], 
                                                    transformlist=[image_xdef_template_warp, image_xdef_template_affine],
                                                    verbose=False)
        ants.image_write(warped_age_template, age_template_warped_file_prefix + str(j) + ".nii.gz")

    print(" ********************************* ")
    print(" Warp each specimen to the space of the template")
    print(" ********************************* ")

    template_x_image_file = output_directory + os.path.basename(files[i]).replace(".nii.gz","_to_template.nii.gz") 
    image_downsampled_file = output_directory + os.path.basename(files[i]).replace(".nii.gz","_downsampled.nii.gz") 

    if not os.path.exists(template_x_image_file):

        if template_labels is None or template_x_subject_space_labels_files[i] is None:

            total_transform_list = [
                                    image_xdef_template_affine,
                                    image_xdef_template_invwarp, 
                                    bspline_refined_xfrm_file
                                    ]    
            bool_invert = [True, False, False]

        else: 

            print(" ********************************* ")
            print(" Refine the subject-to-template normalization with labels (if they exist)")
            print(" ********************************* ")

            image_xdef_template_refined_affine = age_template_warped_file_prefix + "_subjectxTemplateRefinedGenericAffine.mat"
            image_xdef_template_refined_warp = age_template_warped_file_prefix + "_subjectxTemplateRefinedWarp.nii.gz"
            image_xdef_template_refined_invwarp = age_template_warped_file_prefix + "_subjectxTemplateRefinedInverseWarp.nii.gz"

            template_x_subject_space_labels = ants.image_read(template_x_subject_space_labels_files[i])

            reg = register_template(template_x_subject_space_labels, template_labels, 
                                    which_channel='scalar', 
                                    hemisphere_only=use_hemisphere, 
                                    hemisphere_subject_midline_slice=midline_slice[i],
                                    template_lateral_slice=template_lateral_slice[i], 
                                    transform_type="labels")

            image_xdef_template_refined_affine = shutil.copy(reg['fwdtransforms'][1], image_xdef_template_refined_affine) 
            image_xdef_template_refined_warp = shutil.copy(reg['fwdtransforms'][0], image_xdef_template_refined_warp) 
            image_xdef_template_refined_invwarp = shutil.copy(reg['invtransforms'][1], image_xdef_template_refined_invwarp) 

            total_transform_list = [
                                    image_xdef_template_refined_affine,
                                    image_xdef_template_refined_invwarp,                   
                                    image_xdef_template_affine,
                                    image_xdef_template_invwarp, 
                                    bspline_refined_xfrm_file
                                    ]    
            bool_invert = [True, False, True, False, False]

        image_downsampled = resample_multichannel_volume(preprocessed_image, bspline_image.shape[0:3]) 
        image_downsampled_array = image_downsampled.numpy()
        bspline_array = bspline_image.numpy()
        for j in range(image_downsampled_array.shape[2]):
            if j in missing_slices:
                image_downsampled_array[:,:,j,:] = bspline_array[:,:,j,:]    
        image_downsampled = ants.from_numpy(image_downsampled_array, origin=image_downsampled.origin,
                                            spacing=image_downsampled.spacing, direction=image_downsampled.direction,
                                            has_components=True)           
        ants.image_write(image_downsampled, image_downsampled_file)

        template_x_image = warp_to_template(image_downsampled, age_template[0],
                                            transform_list=total_transform_list,
                                            which_to_invert=bool_invert,                                             
                                            hemisphere_only=use_hemisphere,  
                                            hemisphere_subject_midline_slice=midline_slice[i],
                                            verbose=False)
        
        ants.image_write(template_x_image, template_x_image_file)
            
    else:
        template_x_image = ants.image_read(template_x_image_file)
        

    print(" ********************************* ")
    print(" Warp each gene expression to the space of the template")
    print(" ********************************* ")
    
    specimen_id = (os.path.basename(files[i])).split('_')[0]
    gene_image_files = glob.glob(input_expression_directory + "/" + specimen_id + "*expression*.nii.gz")
    for g in range(len(gene_image_files)):

        template_x_gene_file = output_directory + os.path.basename(gene_image_files[g]).replace(".nii.gz", "_to_template.nii.gz")
        if not os.path.exists(template_x_gene_file):
            print("  Processing gene: " + os.path.basename(gene_image_files[g]))
            gene_image = ants.image_read(gene_image_files[g])
            gene_image_resampled = resample_multichannel_volume(gene_image, bspline_image.shape[0:3])

            gene_array = gene_image_resampled.numpy()
            missing_gene_slices = list()
            for jj in range(array.shape[2]):
                slice = gene_array[:,:,jj,:]
                slice_sum = slice.sum()
                if slice_sum < 100.0:
                    missing_gene_slices.append(jj)

            if use_mask:
                image_mask_resampled = ants.resample_image(image_mask, bspline_image.shape[0:3], use_voxels=True, interp_type=1)
                gene_image_resampled_channels = ants.split_channels(gene_image_resampled)
                for c in range(len(gene_image_resampled_channels)):
                    gene_image_resampled_channels[c] = gene_image_resampled_channels[c] * image_mask_resampled
                gene_image_resampled = ants.merge_channels(gene_image_resampled_channels)
            
            gene_image_bspline = bspline_approximate_volume(gene_image_resampled, missing_slices=missing_gene_slices, verbose=True)
            
            template_x_gene = warp_to_template(gene_image_bspline, age_template[0],
                                                transform_list=total_transform_list,
                                                which_to_invert=bool_invert,                                             
                                                hemisphere_only=use_hemisphere,  
                                                hemisphere_subject_midline_slice=midline_slice[i],
                                                verbose=False)
            
            ants.image_write(template_x_gene, template_x_gene_file)
    
    
