import numpy as np
import ants

def bspline_approximate_volume(image_list, 
                               output_size=(256, 256, 256), 
                               number_of_fitting_levels=5,
                               bspline_epsilon=1e-4, 
                               compute_weights=False, 
                               verbose=True):

    scattered_data = None
    parametric_values = None
    weight_values = None
    
    order = (1, 0, 2) 

    for i in range(len(image_list)):     
        indices = np.meshgrid(list(range(image_list[i].shape[1])), 
                              list(range(image_list[i].shape[0])), 
                              list(range(image_list[i].shape[2])))
        indices_array = np.stack((indices[1].flatten(), 
                                  indices[0].flatten(), 
                                  indices[2].flatten()), axis=0)

        scaling = np.eye(3)
        for d in range(len(order)):
            scaling[order[d], order[d]] = image_list[i].spacing[order[d]]
        direction = np.matmul(image_list[i].direction, scaling)

        image_parametric_values = np.matmul(direction, indices_array).transpose()
        for d in range(len(order)):
            image_parametric_values[:, order[d]] += image_list[i].origin[order[d]]

        weight_array = np.ones(image_list[i].shape)
        if compute_weights:
            for d in range(len(order)):
                weight_array += np.power(np.gradient(image_list[i].numpy(), axis=order[d]), 2)
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
    if verbose:
        print("Min: ", min_parametric_values)
        print("Max: ", max_parametric_values)
    spacing = np.zeros((3,))
    for d in range(len(order)):
        spacing[order[d]] = ((max_parametric_values[order[d]] - min_parametric_values[order[d]]) / 
                             (output_size[order[d]] - 1) + bspline_epsilon)
    if verbose:
        print("Spacing: ", spacing)
        print("Output size: ", output_size)

    mean_value = np.mean(scattered_data)
    bspline_image = ants.fit_bspline_object_to_scattered_data(scattered_data - mean_value, parametric_values, 
                                                              parametric_domain_origin=min_parametric_values - bspline_epsilon,
                                                              parametric_domain_spacing=spacing,
                                                              parametric_domain_size=output_size,
                                                              data_weights=weight_values,
                                                              number_of_fitting_levels=number_of_fitting_levels,
                                                              mesh_size=4)   
    bspline_image += mean_value
    return bspline_image

def bspline_randomize_segmentation(segmentation_array, number_of_fitting_levels=5):

    seg = ants.from_numpy(segmentation_array)
    dist_patch = ants.iMath_maurer_distance(seg)
    band_patch = ants.threshold_image(dist_patch, -1, 1, 1, 0)
    random_patch = np.random.randint(0, 2, size=band_patch.shape).astype("float") * band_patch.numpy()
    random_patch[(segmentation_array == 1) & (band_patch.numpy() == 0)] = 1
    random_patch = ants.from_numpy(random_patch)

    image_list=list()
    image_list.append(random_patch)
    bspline_patch = bspline_approximate_volume(image_list, 
                                               output_size=random_patch.shape,
                                               number_of_fitting_levels=number_of_fitting_levels)
    bspline_patch[bspline_patch < 0.5] = 0
    bspline_patch[bspline_patch >= 0.5] = 1
    
    return bspline_patch.numpy()

