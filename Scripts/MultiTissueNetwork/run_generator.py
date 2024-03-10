import ants
import antspynet
import numpy as np

import os
import glob

from batch_generator import batch_generator

################################################
#
#  Load the data
#
################################################

print("Loading brain data.")

template_file = antspynet.get_antsxnet_data("DevCCF_P56_MRI-T2_50um")
labels_file = antspynet.get_antsxnet_data("DevCCF_P56_MRI-T2_50um_BrainParcellationNickMask")

template = ants.image_read(template_file)
labels = ants.image_read(labels_file)

ants.set_spacing(template, (1, 1, 1))
ants.set_spacing(labels, (1, 1, 1))

template_priors = list()
for i in range(8):
    single_label = ants.threshold_image(labels, i, i)
    prior = ants.smooth_image(single_label, sigma=3, sigma_in_physical_coordinates=True)
    template_priors.append(prior)

template_ri = ants.rank_intensity(template)

###
# 
# Set up the training generator
#

batch_size = 5

generator = batch_generator(batch_size=batch_size,
                    template=template_ri,
                    template_priors=template_priors,
                    images=[template_ri],
                    labels=[labels],
                    unique_labels=(0, 1, 2, 3, 4, 5, 6, 7),
                    do_histogram_intensity_warping=True,
                    do_simulate_bias_field=True,
                    do_add_noise=True,
                    do_random_transformation=True,
                    resample_direction="random")

X, Y = next(generator)

for i in range(X.shape[0]):
    print("Creating batch ", str(i))
    ants.image_write(ants.from_numpy(np.squeeze(X[i,:,:,:,0])), "batchX_t2_" + str(i) + ".nii.gz")
    ants.image_write(ants.from_numpy(np.squeeze(X[i,:,:,:,1])), "batchX_P1_" + str(i) + ".nii.gz")
    ants.image_write(ants.from_numpy(np.squeeze(X[i,:,:,:,2])), "batchX_P2_" + str(i) + ".nii.gz")
    ants.image_write(ants.from_numpy(np.squeeze(X[i,:,:,:,3])), "batchX_P3_" + str(i) + ".nii.gz")
    ants.image_write(ants.from_numpy(np.squeeze(X[i,:,:,:,4])), "batchX_P4_" + str(i) + ".nii.gz")
    ants.image_write(ants.from_numpy(np.squeeze(X[i,:,:,:,5])), "batchX_P5_" + str(i) + ".nii.gz")
    ants.image_write(ants.from_numpy(np.squeeze(X[i,:,:,:,6])), "batchX_P6_" + str(i) + ".nii.gz")
    ants.image_write(ants.from_numpy(np.squeeze(X[i,:,:,:,7])), "batchX_P7_" + str(i) + ".nii.gz")
    for j in range(Y.shape[-1]):
        ants.image_write(ants.from_numpy(np.squeeze(Y[i,:,:,:,j])), "batchY_y_" + str(i) + "_" + str(j) + ".nii.gz")

print(X.shape)
print(len(Y))


