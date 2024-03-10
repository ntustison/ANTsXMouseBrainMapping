import numpy as np
import random
import ants
import antspynet
import time

def batch_generator(batch_size=32,
                    template=None,
                    images=None,
                    labels=None,
                    do_histogram_intensity_warping=True,
                    do_simulate_bias_field=True,
                    do_add_noise=True,
                    do_random_transformation=True,
                    resample_direction=None
                    ):

    if images is None:
        raise ValueError("Input images must be specified.")

    if labels is None:
        raise ValueError("Input masks must be specified.")

    while True:

        template_shape = template.shape 

        X = np.zeros((batch_size, *template_shape, 1))
        Y = np.zeros((batch_size, *template_shape))

        batch_count = 0

        while batch_count < batch_size:
            i = random.sample(list(range(len(images))), k=1)[0]

            image = images[i]
            label = labels[i]

            if do_histogram_intensity_warping: # and random.sample((True, False), 1)[0]:
                tic = time.perf_counter()
                break_points = [0.2, 0.4, 0.6, 0.8]                
                displacements = list()
                for b in range(len(break_points)):
                    displacements.append(abs(random.gauss(0, 0.025)))
                    if random.sample((True, False), 1)[0]:
                        displacements[b] *= -1
                image = antspynet.histogram_warp_image_intensities(image,
                    break_points=break_points, clamp_end_points=(True, False),
                    displacements=displacements)
                toc = time.perf_counter()
                # print(f"Histogram warping {toc - tic:0.4f} seconds")

            if do_add_noise and random.sample((True, True, False), 1)[0]:
                tic = time.perf_counter()
                image = (image - image.min()) / (image.max() - image.min())
                image_ones = image * 0 + 1                
                noise_parameters = (0.0, random.uniform(0.0, 0.25))
                noise = ants.add_noise_to_image(image_ones, noise_model="additivegaussian", noise_parameters=noise_parameters)
                noise = ants.smooth_image(noise, sigma=random.uniform(0.1, 0.25))
                image = image * noise
                toc = time.perf_counter()
                # print(f"Add noise {toc - tic:0.4f} seconds")

            if do_simulate_bias_field and random.sample((True, True, False), 1)[0]:
                tic = time.perf_counter()
                log_field = antspynet.simulate_bias_field(image, number_of_points=100, sd_bias_field=0.1, number_of_fitting_levels=2, mesh_size=10)
                log_field = log_field.iMath("Normalize")
                field_array = np.power(np.exp(log_field.numpy()), random.sample((2, 3, 4), 1)[0])
                image = image * ants.from_numpy(field_array, origin=image.origin, spacing=image.spacing, direction=image.direction)
                image = (image - image.min()) / (image.max() - image.min())
                toc = time.perf_counter()
                # print(f"Sim bias field {toc - tic:0.4f} seconds")

            if do_random_transformation:
                tic = time.perf_counter()
                data_augmentation = antspynet.randomly_transform_image_data(template,
                    [[image]],
                    [label],
                    number_of_simulations=1,
                    transform_type='affineAndDeformation',
                    sd_affine=0.01,
                    deformation_transform_type="bspline",
                    number_of_random_points=1000,
                    sd_noise=5.0,
                    number_of_fitting_levels=4,
                    mesh_size=1,
                    sd_smoothing=2.0,
                    input_image_interpolator='linear',
                    segmentation_image_interpolator='nearestNeighbor')
                image = data_augmentation['simulated_images'][0][0]
                label = data_augmentation['simulated_segmentation_images'][0]

                center_of_mass_reference = ants.get_center_of_mass(label)
                translation = np.asarray(center_of_mass_reference) * 0
                for d in range(3):
                    translation[d] = random.uniform(-20, 20)
                xfrm = ants.create_ants_transform(transform_type="Euler3DTransform",
                    center=np.asarray(center_of_mass_reference), translation=translation)
                image = ants.apply_ants_transform_to_image(xfrm, image, template, interpolation="linear")
                label = ants.apply_ants_transform_to_image(xfrm, label, template, interpolation="nearestneighbor")
                
                toc = time.perf_counter()
                # print(f"Xfrms {toc - tic:0.4f} seconds")

            if resample_direction == 'random':
                resample_direction_batch = random.sample((0, 1, 2, None, None), 1)[0] 
            else:
                resample_direction_batch = resample_direction    

            if resample_direction_batch is not None:
                if resample_direction_batch == 0 or resample_direction_batch == 'sagittal':
                    resample_direction_batch = 0                    
                elif resample_direction_batch == 1 or resample_direction_batch == 'coronal':
                    resample_direction_batch = 1                    
                elif resample_direction_batch == 2 or resample_direction_batch == 'axial':
                    resample_direction_batch = 2                    
                new_spacing = list(template.spacing)
                new_spacing[resample_direction_batch] = random.uniform(3, 6)
                image = ants.resample_image(image, new_spacing, use_voxels=False, interp_type=0)
                image = ants.resample_image_to_target(image, template, interp_type='linear')

            # image = ants.rank_intensity(image)
            # image = ants.histogram_match_image(image, template)        
            image = (image - image.min()) / (image.max() - image.min())

            X[batch_count,:,:,:,0] = image.numpy()
            Y[batch_count,:,:,:] = label.numpy()
             
            # print(str(batch_count) + " out of " + str(batch_size)) 

            batch_count = batch_count + 1
            if batch_count >= batch_size:
                break

        encY = antspynet.encode_unet(Y, (0, 1))
        yield X, encY, None









