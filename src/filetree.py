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
        "bibsnet": {},
        "postbibsnet": {}
    }
}
