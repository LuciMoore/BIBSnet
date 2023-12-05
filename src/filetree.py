filetree = {
    "derivatives": {
        "dataset-description-json": "{{DERIVATIVES}}/bibsnet/dataset_description.json",
        "T1w-aseg-json": "{{DERIVATIVES}}/bibsnet/{{SUBJECT}}/{{SESSION}}/anat/{{SUBJECT}}_{{SESSION}}_space-T1w_desc-aseg_dseg.json",
        "T1w-aseg-nii": "{{DERIVATIVES}}/bibsnet/{{SUBJECT}}/{{SESSION}}/anat/{{SUBJECT}}_{{SESSION}}_space-T1w_desc-aseg_dseg.nii.gz",
        "T1w-mask-json": "{{DERIVATIVES}}/bibsnet/{{SUBJECT}}/{{SESSION}}/anat/{{SUBJECT}}_{{SESSION}}_space-T1w_desc-brain_mask.json",
        "T1w-mask-nii": "{{DERIVATIVES}}/bibsnet/{{SUBJECT}}/{{SESSION}}/anat/{{SUBJECT}}_{{SESSION}}_space-T1w_desc-brain_mask.nii.gz",
        "T2w-aseg-json": "{{DERIVATIVES}}/bibsnet/{{SUBJECT}}/{{SESSION}}/anat/{{SUBJECT}}_{{SESSION}}_space-T2w_desc-aseg_dseg.json",
        "T2w-aseg-nii": "{{DERIVATIVES}}/bibsnet/{{SUBJECT}}/{{SESSION}}/anat/{{SUBJECT}}_{{SESSION}}_space-T2w_desc-aseg_dseg.nii.gz",
        "T2w-mask-json": "{{DERIVATIVES}}/bibsnet/{{SUBJECT}}/{{SESSION}}/anat/{{SUBJECT}}_{{SESSION}}_space-T2w_desc-brain_mask.json",
        "T2w-mask-nii": "{{DERIVATIVES}}/bibsnet/{{SUBJECT}}/{{SESSION}}/anat/{{SUBJECT}}_{{SESSION}}_space-T2w_desc-brain_mask.nii.gz"
    },
    "work": {
        "prebibsnet": {
            "averaged": {
                "T1":"{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/averaged/{{SUBJECT}}_{{SESSION}}_0000.nii.gz",
                "T2":"{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/averaged/{{SUBJECT}}_{{SESSION}}_0001.nii.gz"
            },
            "cropped": {
                "T1-mat": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/cropped/T1w/crop2full.mat",
                "T1-nii": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/cropped/T1w/{{SUBJECT}}_{{SESSION}}_0000.nii.gz",
                "T2-mat": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/cropped/T2w/crop2full.mat",
                "T2-nii": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/cropped/T2w/{{SUBJECT}}_{{SESSION}}_0001.nii.gz"
            },
            "resized":{
                "ACPC-align": {
                    "acpc-aligned-t1-nii": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/ACPC_align/ACPC_aligned_T1w.nii.gz",
                    "acpc-aligned-t2-nii": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/ACPC_align/ACPC_aligned_T2w.nii.gz",
                    "acpc-t1-registered-to-t1-nii": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/ACPC_align/ACPC_T1w_registered_to_T1w.nii.gz",
                    "acpc-t2-registered-to-t1-nii": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/ACPC_align/ACPC_T2w_registered_to_T1w.nii.gz",
                    "crop-t1-to-bibs-template-mat": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/ACPC_align/crop_T1w_to_BIBS_template.mat",
                    "crop-t2-to-crop-t1-mat": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/ACPC_align/cropT2tocropT1.mat",
                    "crop-t2-to-bibs-template-mat": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/ACPC_align/crop_T2w_to_BIBS_template.mat",
                    "prebibsnet-final-0000-nii": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/ACPC_align/preBIBSnet_final_0000.nii.gz",
                    "prebibsnet-final-0001-nii": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/ACPC_align/preBIBSnet_final_0001.nii.gz",
                    "t1-acpc-to-rigidbody-mat": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/ACPC_align/T1w_acpc2rigidbody.mat",
                    "t1-crop-to-acpc-mat": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/ACPC_align/T1w_crop2acpc.mat",
                    "t1-full-to-acpc-mat": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/ACPC_align/T1w_full2acpc.mat",
                    "t1-full-to-crop-mat": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/ACPC_align/T1w_full2crop.mat",
                    "t2-acpc-to-rigidbody-mat": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/ACPC_align/T2w_acpc2rigidbody.mat",
                    "t2-crop-to-acpc-mat": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/ACPC_align/T2w_crop2acpc.mat",
                    "t2-full-to-acpc-mat": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/ACPC_align/T2w_full2acpc.mat",
                    "t2-full-to-crop-mat": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/ACPC_align/T2w_full2crop.mat",
                    "t2-to-rigid-body-mat": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/ACPC_align/T2w_to_rigidbody.mat"
                },
                "xfms": {
                    "crop-t1-to-bibs-template-mat": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/xfms/crop_T1w_to_BIBS_template.mat",
                    "crop-t2-to-crop-t1-mat": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/xfms/cropT2tocropT1.mat",
                    "crop-t2-to-bibs-template-mat": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/xfms/crop_T2w_to_BIBS_template.mat",
                    "full-to-crop-t1-mat": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/xfms/full2cropT1w.mat",
                    "full-to-crop-t2-to-t1-mat": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/xfms/full2cropT2toT1.mat",
                    "full-to-crop-t2-mat": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/xfms/full2cropT2w.mat",
                    "full-crop-t1-to-bids-template-mat": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/xfms/full_crop_T1w_to_BIBS_template.mat",
                    "full-crop-t2-to-bids-template-mat": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/xfms/full_crop_T2w_to_BIBS_template.mat",
                    "prebibsnet-final-0000-nii": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/xfms/preBIBSnet_final_0000.nii.gz",
                    "prebibsnet-final-0001-nii": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/xfms/preBIBSnet_final_0001.nii.gz",
                    "t1-to-bibs-nii": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/xfms/T1w_to_BIBS.nii.gz",
                    "t2-registered-to-t1-nii": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/xfms/T2w_registered_to_T1w.nii.gz",
                    "t2-to-bibs-nii": "{{WORK}}/prebibsnet/{{SUBJECT}}/{{SESSION}}/resized/xfms/T2w_to_BIBS.nii.gz"
                }
            },
        },
        "bibsnet": {
            "input": {
                "optimal-resized-0000-nii": "{{WORK}}/bibsnet/{{SUBJECT}}/{{SESSION}}/input/{{SUBJECT}}_{{SESSION}}_optimal_resized_0000.nii.gz",
                "optimal-resized-0001-nii": "{{WORK}}/bibsnet/{{SUBJECT}}/{{SESSION}}/input/{{SUBJECT}}_{{SESSION}}_optimal_resized_0001.nii.gz"
            },
            "output": {
                "plans-pkl": "{{WORK}}/bibsnet/{{SUBJECT}}/{{SESSION}}/output/plans.pkl",
                "prediction-time.txt": "{{WORK}}/bibsnet/{{SUBJECT}}/{{SESSION}}/output/prediction_time.txt",
                "optimal-resized-nii": "{{WORK}}/bibsnet/{{SUBJECT}}/{{SESSION}}/output/{{SUBJECT}}_{{SESSION}}_optimal_resized.nii.gz"
            }
        },
        "postbibsnet": {
            "chirality_correction": {
                "corrected-optimal-resized-dummy-nii": "{{WORK}}/postbibsnet/{{SUBJECT}}/{{SESSION}}/chirality_correction/corrected_sub-M1003_ses-20191205_optimal_resized_dummy.nii.gz", 
                "corrected-optimal-resized-nii": "{{WORK}}/postbibsnet/{{SUBJECT}}/{{SESSION}}/chirality_correction/corrected_sub-M1003_ses-20191205_optimal_resized.nii.gz", 
                "native-T1-optimal-resized-nii": "{{WORK}}/postbibsnet/{{SUBJECT}}/{{SESSION}}/chirality_correction/native-T1_sub-M1003_ses-20191205_optimal_resized.nii.gz", 
                "native-T1-optimal-resized-T1-mask-nii": "{{WORK}}/postbibsnet/{{SUBJECT}}/{{SESSION}}/chirality_correction/native-T1_sub-M1003_ses-20191205_optimal_resized_T1_mask.nii.gz", 
                "native-T2-optimal-resized-nii": "{{WORK}}/postbibsnet/{{SUBJECT}}/{{SESSION}}/chirality_correction/native-T2_sub-M1003_ses-20191205_optimal_resized.nii.gz", 
                "native-T2-optimal-resized-T2-mask-nii": "{{WORK}}/postbibsnet/{{SUBJECT}}/{{SESSION}}/chirality_correction/native-T2_sub-M1003_ses-20191205_optimal_resized_T2_mask.nii.gz", 
                "seg-reg-to-T1w-native-mat": "{{WORK}}/postbibsnet/{{SUBJECT}}/{{SESSION}}/chirality_correction/seg_reg_to_T1w_native.mat", 
                "seg-reg-to-T2w-native-mat": "{{WORK}}/postbibsnet/{{SUBJECT}}/{{SESSION}}/chirality_correction/seg_reg_to_T2w_native.mat", 
            },
            "lrmask_dil_wd": {
                "dilated-LRmask-nii": "{{WORK}}/postbibsnet/{{SUBJECT}}/{{SESSION}}/lrmask_dil_wd/dilated_LRmask.nii.gz", 
                "Lmask-holes-filled-nii": "{{WORK}}/postbibsnet/{{SUBJECT}}/{{SESSION}}/lrmask_dil_wd/Lmask_holes_filled.nii.gz", 
                "Lmask-nii": "{{WORK}}/postbibsnet/{{SUBJECT}}/{{SESSION}}/lrmask_dil_wd/Lmask.nii.gz", 
                "LRmask-dil-nii": "{{WORK}}/postbibsnet/{{SUBJECT}}/{{SESSION}}/lrmask_dil_wd/LRmask_dil.nii.gz", 
                "Mmask-holes-filled-label3-nii": "{{WORK}}/postbibsnet/{{SUBJECT}}/{{SESSION}}/lrmask_dil_wd/Mmask_holes_filled_label3.nii.gz", 
                "Mmask-holes-filled-nii": "{{WORK}}/postbibsnet/{{SUBJECT}}/{{SESSION}}/lrmask_dil_wd/Mmask_holes_filled.nii.gz", 
                "Mmask-nii": "{{WORK}}/postbibsnet/{{SUBJECT}}/{{SESSION}}/lrmask_dil_wd/Mmask.nii.gz", 
                "recombined-mask-LR-nii": "{{WORK}}/postbibsnet/{{SUBJECT}}/{{SESSION}}/lrmask_dil_wd/recombined_mask_LR.nii.gz", 
                "Rmask-holes-filled-label2-nii": "{{WORK}}/postbibsnet/{{SUBJECT}}/{{SESSION}}/lrmask_dil_wd/Rmask_holes_filled_label2.nii.gz", 
                "Rmask-holes-filled-nii": "{{WORK}}/postbibsnet/{{SUBJECT}}/{{SESSION}}/lrmask_dil_wd/Rmask_holes_filled.nii.gz", 
                "Rmask-nii": "{{WORK}}/postbibsnet/{{SUBJECT}}/{{SESSION}}/lrmask_dil_wd/Rmask.nii.gz                ", 
            },
            "wd": {
                "ants-reg-affine-txt": "{{WORK}}/postbibsnet/{{SUBJECT}}/{{SESSION}}/wd/antsregAffine.txt",
                "ants-reg-inverse-warp-nii": "{{WORK}}/postbibsnet/{{SUBJECT}}/{{SESSION}}/wd/antsregInverseWarp.nii.gz",
                "ants-reg-warp-nii": "{{WORK}}/postbibsnet/{{SUBJECT}}/{{SESSION}}/wd/antsregWarp.nii.gz"
            },
            "LRmask-nii": "{{WORK}}/postbibsnet/{{SUBJECT}}/{{SESSION}}/LRmask.nii.gz"
        }
    }
}
