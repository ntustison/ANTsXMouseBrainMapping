import ants
import antspynet

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
os.environ["ITK_DEFAULT_GLOBAL_NUMBER_OF_THREADS"] = "4"

import numpy as np

import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.backend as K

from batch_generator import batch_generator

K.clear_session()
# gpus = tf.config.experimental.list_physical_devices("GPU")
# if len(gpus) > 0:
#     tf.config.experimental.set_memory_growth(gpus[0], True)
# tf.compat.v1.disable_eager_execution()

# tf.config.run_functions_eagerly(True)


base_directory = '/home/ntustison/Data/Mouse/MultiTissue/'

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

template = ants.resample_image(template, (75, 75, 75), use_voxels=False, interp_type=4)
labels = ants.resample_image(labels, (75, 75, 75), use_voxels=False, interp_type=1)

template = antspynet.pad_or_crop_image_to_size(template, (176, 128, 240))
labels = antspynet.pad_or_crop_image_to_size(labels, (176, 128, 240))

ants.set_spacing(template, (1, 1, 1))
ants.set_spacing(labels, (1, 1, 1))

image_size = template.shape
unique_labels = np.unique(labels.numpy())
number_of_classification_labels = len(unique_labels)
number_of_nonzero_labels = number_of_classification_labels - 1
channel_size = 1 + number_of_nonzero_labels

print("Unique labels: ", unique_labels)

template_priors = list()
for i in range(number_of_nonzero_labels):
    single_label = ants.threshold_image(labels, i+1, i+1)
    prior = ants.smooth_image(single_label, sigma=3, sigma_in_physical_coordinates=True)
    template_priors.append(prior)

template_ri = ants.rank_intensity(template)

################################################
#
#  Create the model and load weights
#
################################################

# number_of_filters = (16, 32, 64, 96, 128)
number_of_filters = (16, 32, 64, 128, 256)

unet_model = antspynet.create_unet_model_3d((*image_size, channel_size),
   number_of_outputs=number_of_classification_labels, mode="classification", 
   number_of_filters=number_of_filters,
   convolution_kernel_size=(3, 3, 3), deconvolution_kernel_size=(2, 2, 2))
  # ,
  # dropout_rate=0.0, weight_decay=1e-5, additional_options=("attentionGating",))


dice_loss = antspynet.multilabel_dice_coefficient(dimensionality = 3, smoothing_factor=0.0)
ce_loss = antspynet.weighted_categorical_crossentropy((1, *tuple([10] * (number_of_classification_labels - 1 ))))

weights_filename = base_directory + "weights_cuda1_round2.h5"
if os.path.exists(weights_filename):
    unet_model.load_weights(weights_filename)

unet_model.compile(optimizer=tf.keras.optimizers.legacy.Adam(learning_rate=2e-4),
                    loss=dice_loss,
                    metrics=[dice_loss])

###
#
# Set up the training generator
#

batch_size = 4

generator = batch_generator(batch_size=batch_size,
                    template=template_ri,
                    template_priors=template_priors,
                    images=[template_ri],
                    labels=[labels],
                    unique_labels=unique_labels,
                    do_histogram_intensity_warping=True,
                    do_simulate_bias_field=True,
                    do_add_noise=True,
                    do_random_transformation=True,
                    resample_direction="random")

track = unet_model.fit(x=generator, epochs=100, verbose=1, steps_per_epoch=32,
    callbacks=[
       keras.callbacks.ModelCheckpoint(weights_filename, monitor='loss',
           save_best_only=True, save_weights_only=True, mode='auto', verbose=1),
       keras.callbacks.ReduceLROnPlateau(monitor='loss', factor=0.95,
          verbose=1, patience=20, mode='auto'),
    #    keras.callbacks.EarlyStopping(monitor='loss', min_delta=0.000001,
    #       patience=20)
       ]
   )

unet_model.save_weights(weights_filename)


