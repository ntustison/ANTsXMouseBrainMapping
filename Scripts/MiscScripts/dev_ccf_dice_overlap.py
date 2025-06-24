import ants
import numpy as np
import pandas as pd

atlas_ids = tuple(reversed(("E11-5", "E13-5", "E15-5", "E18-5", "P04", "P14", "P56")))
time_points = np.flip(-1.0 * np.log(np.array((11.5, 13.5, 15.5, 18.5, 23, 33, 47))))
normalized_time_points = (time_points - time_points[0]) / (time_points[-1] - time_points[0])

data_directory = "../../Data/Output/P56RigidTransformData/"

remove_labels = [17735, 27735, 21558, 31558]

df_vf = pd.DataFrame()
df_syn = pd.DataFrame()

velocity_field = ants.image_read("../../Data/Output/DevCCF_velocity_flow.nii.gz")
for i in range(len(atlas_ids)):    

    print("Processing reference id: ", atlas_ids[i])
    reference_template_file = data_directory + "P56x" + atlas_ids[i] + "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi.nii.gz"
    reference_template = ants.image_read(reference_template_file)
    for j in range(len(remove_labels)):
        reference_template[reference_template == remove_labels[j]] = 0

    if i > 0:
        tm1_file = data_directory + "P56x" + atlas_ids[i-1] + "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi.nii.gz"
        tm1 = ants.image_read(tm1_file)
        for j in range(len(remove_labels)):
            tm1[tm1 == remove_labels[j]] = 0
        print("  Warp time point before (velocity flow)... ")
        displacement_field_m1 = ants.integrate_velocity_field(velocity_field,
                                                            normalized_time_points[i],
                                                            normalized_time_points[i-1], 10)
        displacement_field_m1_xfrm = ants.transform_from_displacement_field(displacement_field_m1)
        tm1_warped = displacement_field_m1_xfrm.apply_to_image(tm1,
                                                            interpolation="nearestneighbor")
        stats_tm1 = ants.label_overlap_measures(tm1_warped, reference_template)
        dice_tm1 = stats_tm1['MeanOverlap']
        dice_tm1.name = atlas_ids[i] + "x" + atlas_ids[i-1]
        df_vf = pd.concat([df_vf, dice_tm1], axis=1)

    if i < len(atlas_ids)-1: 
        tp1_file = data_directory + "P56x" + atlas_ids[i+1] + "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi.nii.gz"
        tp1 = ants.image_read(tp1_file)
        for j in range(len(remove_labels)):
            tp1[tp1 == remove_labels[j]] = 0        
        print("  Warp time point after (velocity flow)... ")
        displacement_field_p1 = ants.integrate_velocity_field(velocity_field,
                                                            normalized_time_points[i],
                                                            normalized_time_points[i+1], 10)
        displacement_field_p1_xfrm = ants.transform_from_displacement_field(displacement_field_p1)
        tp1_warped = displacement_field_p1_xfrm.apply_to_image(tp1,
                                                            interpolation="nearestneighbor")   
        stats_tp1 = ants.label_overlap_measures(tp1_warped, reference_template)    
        dice_tp1 = stats_tp1['MeanOverlap']
        dice_tp1.name = atlas_ids[i] + "x" + atlas_ids[i+1]
        if i == 0:
            df_vf = pd.concat([df_vf, stats_tp1['Label']], axis=1)
        df_vf = pd.concat([df_vf, dice_tp1], axis=1)

    df_vf.to_csv("dev_ccf_dice_velocity_flow_overlap.csv")
    
# SyN 

for i in range(len(atlas_ids)):    

    print("Processing reference id: ", atlas_ids[i])
    reference_template_file = data_directory + "P56x" + atlas_ids[i] + "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi.nii.gz"
    reference_template = ants.image_read(reference_template_file)
    for j in range(len(remove_labels)):
        reference_template[reference_template == remove_labels[j]] = 0

    if i > 0:
        tm1_file = data_directory + "P56x" + atlas_ids[i-1] + "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi.nii.gz"
        tm1 = ants.image_read(tm1_file)
        for j in range(len(remove_labels)):
            tm1[tm1 == remove_labels[j]] = 0
        print("  Warp time point before (syn)... ")
        tm1_affine = data_directory + "../PairwiseRegistrations/P56x" + atlas_ids[i-1] + "x" + atlas_ids[i] + "_0GenericAffine.mat"
        tm1_warp = data_directory + "../PairwiseRegistrations/P56x" + atlas_ids[i-1] + "x" + atlas_ids[i] + "_1InverseWarp.nii.gz"
        tm1_warped = ants.apply_transforms(reference_template, tm1, [tm1_affine, tm1_warp], interpolator="nearestNeighbor", whichtoinvert=[True, False])
        stats_tm1 = ants.label_overlap_measures(tm1_warped, reference_template)
        dice_tm1 = stats_tm1['MeanOverlap']
        dice_tm1.name = atlas_ids[i] + "x" + atlas_ids[i-1]
        df_syn = pd.concat([df_syn, dice_tm1], axis=1)

    if i < len(atlas_ids)-1: 
        tp1_file = data_directory + "P56x" + atlas_ids[i+1] + "_DevCCF_Annotations_20um_symmetric_commonROIs_hemi.nii.gz"
        tp1 = ants.image_read(tp1_file)
        for j in range(len(remove_labels)):
            tp1[tp1 == remove_labels[j]] = 0
        print("  Warp time point after (syn)... ")
        tp1_affine = data_directory + "../PairwiseRegistrations/P56x" + atlas_ids[i] + "x" + atlas_ids[i+1] + "_0GenericAffine.mat"
        tp1_warp = data_directory + "../PairwiseRegistrations/P56x" + atlas_ids[i] + "x" + atlas_ids[i+1] + "_1Warp.nii.gz"
        tp1_warped = ants.apply_transforms(reference_template, tp1, [tp1_warp, tp1_affine], interpolator="nearestNeighbor", whichtoinvert=[False, False])
        stats_tp1 = ants.label_overlap_measures(tp1_warped, reference_template)    
        dice_tp1 = stats_tp1['MeanOverlap']
        dice_tp1.name = atlas_ids[i] + "x" + atlas_ids[i+1]
        if i == 0:
            df_syn = pd.concat([df_syn, stats_tp1['Label']], axis=1)
        df_syn = pd.concat([df_syn, dice_tp1], axis=1)

    df_syn.to_csv("dev_ccf_dice_pairwise_syn_overlap.csv")

