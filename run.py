#!/usr/bin/env python3
# coding: utf-8

"""
Connectome ABCD-XCP niBabies Imaging nnu-NET (CABINET)
Created: 2021-11-12
Updated: 2022-02-04
"""

# Import standard libraries
import argparse
from datetime import datetime 
from glob import glob
from nipype.interfaces import fsl
import os
import pandas as pd
import subprocess
import sys


def find_myself(flg):
    """
    Ensure that this script can find its dependencies if parallel processing
    :param flg: String in sys.argv immediately preceding the path to return
    :return: String, path to the directory this Python script is in
    """
    try:
        parallel_flag_pos = -2 if sys.argv[-2] == flg else sys.argv.index(flg)
        sys.path.append(os.path.abspath(sys.argv[parallel_flag_pos + 1]))
    except (IndexError, ValueError):
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    return sys.path[-1]


# Global constants: Paths to this dir and to level 1 analysis script
SCRIPT_DIR_ARG = "--script-dir"
SCRIPT_DIR = find_myself(SCRIPT_DIR_ARG)
LR_REGISTR_PATH = os.path.join(SCRIPT_DIR, "bin", "LR_mask_registration.sh")

# Custom local imports
from src.utilities import (
    as_cli_attr, as_cli_arg, copy_and_rename_file, correct_chirality,
    crop_images, ensure_dict_has, exit_with_time_info, extract_from_json,
    get_stage_name, get_subj_ID_and_session, get_subj_ses, resize_images,
    run_all_stages, valid_readable_json, validate_parameter_types,
    valid_readable_dir, warn_user_of_conditions
)


def main():
    # Time how long the script takes and get command-line arguments from user 
    start_time = datetime.now()
    STAGES = [run_preBIBSnet, run_BIBSnet, run_postBIBSnet, run_nibabies,
              run_XCPD]
    json_args = get_params_from_JSON([get_stage_name(stg) for stg in STAGES])
    print(json_args)  # TODO REMOVE LINE

    # Run every stage that the parameter file says to run
    run_all_stages(STAGES, json_args["stage_names"]["start"],
                   json_args["stage_names"]["end"], json_args)
    # TODO default to running all stages if not specified by the user
    # TODO add error if end is given as a stage that happens before start

    # Show user how long the pipeline took and end the pipeline here
    exit_with_time_info(start_time)


def get_params_from_JSON(stage_names):
    """
    :param stage_names: List of strings; each names a stage to run
    :return: Dictionary containing all parameters from parameter .JSON file
    """
    default_types_json = os.path.join(SCRIPT_DIR, "param-types.json")
    msg_json = "Valid path to existing readable parameter .json file."
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "parameter_json", type=valid_readable_json,
        help=("{} See README.md for more information on parameters."
              .format(msg_json))
        # TODO: Add description of every parameter to the README, and maybe also to this --help message
        # TODO: Add nnU-Net parameters (once they're decided on)
    )
    parser.add_argument(
        "-start", "--starting-stage", dest="start",
        choices=stage_names, default=stage_names[0]
    )
    parser.add_argument(
        "-end", "--ending-stage", dest="end",
        choices=stage_names, default=stage_names[-1]
    )
    parser.add_argument(
        "--types-json", type=valid_readable_json, default=default_types_json,
        help=("{} This file must map every CABINET parameter to its data type."
              .format(msg_json))
    )
    parser.add_argument(
        SCRIPT_DIR_ARG, dest="script_dir", type=valid_readable_dir,
        help=("Valid path to the existing parent directory of this run.py "
              "script. Include this argument if and only if you are running "
              "the script as a SLURM/SBATCH job.")
    )
    return validate_cli_args(vars(parser.parse_args()), stage_names, parser)


def validate_cli_args(cli_args, stage_names, parser):
    """
    :param cli_args: Dictionary containing all command-line input arguments
    :param stage_names: List of strings naming stages to run (in order)
    :return: Dictionary of validated parameters from parameter .JSON file
    """
    # Get command-line input arguments and use them to get .JSON parameters
    j_args = extract_from_json(cli_args["parameter_json"])
    j_args["meta"] = {SCRIPT_DIR_ARG: SCRIPT_DIR,
                      "slurm": bool(cli_args[as_cli_attr(SCRIPT_DIR_ARG)])}
    j_args["stage_names"] = {"start": cli_args["start"],
                             "end": cli_args["end"]} 

    # Verify that every parameter in the parameter .JSON file is a valid input
    validate_parameter_types(j_args, extract_from_json(cli_args["types_json"]),
                             cli_args["parameter_json"], parser, stage_names)

    j_args["common"] = ensure_dict_has(j_args["common"], "age_months",
                                       read_age_from_participants_tsv(j_args))
    # TODO Figure out which column in the participants.tsv file has age_months

    # Define (and create) default paths in derivatives directory structure for each stage
    j_args = ensure_j_args_has_bids_subdir(j_args, "derivatives")
    for deriv in stage_names:
        j_args = ensure_j_args_has_bids_subdir(j_args, "derivatives", deriv)  #  + "_output_dir")

    return j_args


def ensure_j_args_has_bids_subdir(j_args, *subdirnames):
    """
    :param j_args: Dictionary containing all args from parameter .JSON file
    :param subdirnames: Unpacked list of strings. Each names 1 part of a path
                        under j_args[common][bids_dir]. The last string is
                        mapped by j_args[optional_out_dirs] to the subdir path.
    :return: j_args, but with the (now-existing) subdirectory path
    """
    subdir_path = os.path.join(j_args["common"]["bids_dir"], *subdirnames)
    j_args["optional_out_dirs"] = ensure_dict_has(j_args["optional_out_dirs"],
                                                  subdirnames[-1], subdir_path)
    os.makedirs(j_args["optional_out_dirs"][subdirnames[-1]], exist_ok=True)
    return j_args


def read_age_from_participants_tsv(j_args):
    """
    :param j_args: Dictionary containing all args from parameter .JSON file
    :return: Int, the subject's age (in months) listed in participants.tsv
    """
    columns = {"age": "str", "participant_id": "str", "session": "str"}

    subj_ID, session = get_subj_ID_and_session(j_args)

    # Read in participants.tsv
    part_tsv_df = pd.read_csv(
        os.path.join(j_args["common"]["bids_dir"],
                     "participants.tsv"), sep="\t", dtype=columns
    )

    # Column names of participants.tsv                         
    age_months_col = "age" # TODO is there a way to ensure the age column is given in months using the participants.json (the participants.tsv's sidecar)
    sub_ID_col = "participant_id"
    ses_ID_col = "session"

    # Get and return the age_months value from participants.tsv
    subj_row = part_tsv_df[  # TODO Run ensure_prefixed on the sub_ID_col?
        part_tsv_df[sub_ID_col] == j_args["common"]["participant_label"]
    ]
    subj_row = subj_row[  # TODO Run ensure_prefixed on the ses_ID_col?
        subj_row[ses_ID_col] == j_args["common"]["session"]
    ] # select where "participant_id" and "session" match

    print(subj_row)
    return int(subj_row[age_months_col])


def run_preBIBSnet(j_args, logger):
    """
    :param j_args: Dictionary containing all args from parameter .JSON file
    :param logger: logging.Logger object to show messages and raise warnings
    :return: j_args, but with preBIBSnet working directory names added
    """
    # Get subject ID, session, and directory of subject's BIDS-valid input data
    subj_ID, session = get_subj_ID_and_session(j_args)
    subject_dir = os.path.join(j_args["common"]["bids_dir"], subj_ID)

    # Make working directories to run pre-BIBSnet processing in
    subj_work_dir = os.path.join(
        j_args["optional_out_dirs"]["preBIBSnet"], subj_ID, session
    )
    for jarg, work_dirname in j_args["preBIBSnet"].items():
        j_args["preBIBSnet"][jarg] = os.path.join(subj_work_dir, work_dirname)
        os.makedirs(j_args["preBIBSnet"][jarg], exist_ok=True)
    work_dirs = {"parent": subj_work_dir, **j_args["preBIBSnet"]}

    # Copy any file with T1 or T2 in its name from BIDS/anat dir to BIBSnet work dir
    for each_anat in (1, 2):
        for eachfile in glob(os.path.join(
            subject_dir, session, "anat", "*T{}w*.nii.gz".format(each_anat)
        )):
            new_fpath = os.path.join(
                work_dirs["input_dir"],
                rename_for_nnUNet(os.path.basename(eachfile))
            )
            copy_and_rename_file(eachfile, new_fpath)
            os.chmod(new_fpath, 0o775)

    # TODO What do we do if there's >1 T1w or >1 T2w? nnU-Net can't handle >1 rn.
    # - Average them (after crop/resize) like the pre-FreeSurfer infant pipeline
    #   does, per Fez and Luci, and do a rigid body registration while averaging
    # - If BIBSnet will ever use a model accepting multiple T1ws or T2ws, then
    #   make averaging optional
    # - Include option (in later version, e.g. 2.0) to just pick the best T?w
    #   instead of averaging? Or just assume that if they want to pick the
    #   best, then they would have picked/isolated it beforehand?

    # Crop and resize images
    crop_images(work_dirs["input_dir"], work_dirs["cropped_dir"])
    logger.info("The anatomical images have been cropped for use in BIBSnet")

    os.chmod(work_dirs["cropped_dir"], 0o775)
    ref_img = os.path.join(SCRIPT_DIR, "data", "test_subject_data", "1mo",
                           "sub-00006_T1w_acpc_dc_restore.nii.gz")
    id_mx = os.path.join(SCRIPT_DIR, "data", "identity_matrix.mat")
    j_args["transformed_images"] = resize_images(
        work_dirs["cropped_dir"], work_dirs["resized_dir"], ref_img, id_mx
    )
    logger.info("The anatomical images have been resized for use in BIBSnet")
    logger.info("PreBIBSnet has completed")
    return j_args


def rename_for_nnUNet(fname):
    """
    Given a filename, change that name to meet nnU-Net's conventions
    :param fname: String naming a .nii.gz file
    :return: String, fname but replacing the "T?w" with "000?"
    """
    return fname.replace("T1w", "0000").replace("T2w", "0001")


def run_BIBSnet(j_args, logger):
    """
    :param j_args: Dictionary containing all args from parameter .JSON file
    :param logger: logging.Logger object to show messages and raise warnings
    :return: j_args, unchanged
    """
    # TODO Test BIBSnet functionality once it's containerized
    """
    verify_image_file_names(j_args)  # TODO Ensure that the T1s have _0000 at the end of their filenames and T2s have _0001

    if j_args["common"]["age_months"] <= 8:
        j_args = copy_images_to_BIBSnet_dir(j_args)           # TODO
        j_args["segmentation"] = run_BIBSnet_predict(j_args)  # TODO
    """

    logger.info("BIBSnet has completed")
    return j_args


def run_postBIBSnet(j_args, logger):
    """
    :param j_args: Dictionary containing all args from parameter .JSON file
    :param logger: logging.Logger object to show messages and raise warnings
    :return: j_args, unchanged
    """
    sub_ses = get_subj_ses(j_args)

    # Template selection values
    age_months = j_args["common"]["age_months"]
    print(age_months)
    if age_months > 33:
        age_months = "34-38"

    # Run left/right registration script and chirality correction
    left_right_mask_nifti_fpath = run_left_right_registration(
        j_args, sub_ses, age_months, 2 if int(age_months) < 22 else 1
    )
    logger.info("Left/right image registration completed")
    chiral_out_dir = run_chirality_correction(j_args, left_right_mask_nifti_fpath)
    logger.info("The BIBSnet segmentation has had its chirality checked and "
                "registered if needed")

    masks = make_asegderived_mask(chiral_out_dir)  # NOTE Mask must be in native T1 space too
    logger.info("A mask of the BIBSnet segmentation has been produced")

    # Make nibabies input dirs
    derivs_dir = os.path.join(j_args["optional_out_dirs"]["BIBSnet"],
                              j_args["common"]["participant_label"],
                              j_args["common"]["session"])
    os.makedirs(derivs_dir, exist_ok=True)
    for eachfile in os.scandir(chiral_out_dir):
        if "aseg" in chiral_out_dir.name:
            copy_to_derivatives_dir(eachfile, derivs_dir, sub_ses, "aseg_dseg")
    for each_mask in masks:  # There should only be 1, for the record
        copy_to_derivatives_dir(each_mask, derivs_dir, sub_ses, "brain_mask")
        
    # TODO Get dataset_description.json and put it in derivs_dir
    # TODO Add padding? No, this is no longer necessary due to RobustFOV

    logger.info("PostBIBSnet has completed.")
    return j_args


def run_left_right_registration(j_args, sub_ses, age_months, t1or2):
    """
    :param j_args: Dictionary containing all args from parameter .JSON file
    :param sub_ses: String combining subject ID and session from parameter file
    :param age_months: String or int, the subject's age [range] in months
    :param t1or2: Int, 1 to use T1w image for registration or 2 to use T2w
    :return: String, path to newly created left/right registration output file
    """
    # Paths for left & right registration
    chiral_in_dir = os.path.join(SCRIPT_DIR, "data", "chirality_masks")
    tmpl_head = os.path.join(chiral_in_dir, "{}mo_T{}w_acpc_dc_restore.nii.gz")
    tmpl_mask = os.path.join(chiral_in_dir, "{}mo_template_LRmask.nii.gz")

    # Grab the first resized T1w from preBIBSnet to use for L/R registration
    subject_head_path = os.path.join(j_args["preBIBSnet"]["resized_dir"],
                                     sub_ses + "_run-*_0000.nii.gz")
    first_subject_head = glob(subject_head_path)[0]  

    # Left/right registration output file path (this function's return value)
    left_right_mask_nifti_fpath = os.path.join(
        j_args["optional_out_dirs"]["postBIBSnet"], "LRmask.nii.gz"
    )

    # Run left & right registration  # NOTE: Script ran successfully until here 2022-01-20_13:47
    subprocess.check_call((LR_REGISTR_PATH, first_subject_head,
                           tmpl_head.format(age_months, t1or2),
                           tmpl_mask.format(age_months),
                           left_right_mask_nifti_fpath))
    return left_right_mask_nifti_fpath


def run_chirality_correction(j_args, l_r_mask_nifti_fpath):
    """
    :param j_args: Dictionary containing all args from parameter .JSON file
    :param l_r_mask_nifti_fpath: String, valid path to existing left/right
                                 registration output mask file
    :return: String, valid path to existing directory containing newly created
             chirality correction outputs
    """
    subj_ID, session = get_subj_ID_and_session(j_args)

    # Define paths to dirs/files used in chirality correction script
    chiral_out_dir = os.path.join(j_args["optional_out_dirs"]["postBIBSnet"],
                                  "chirality_correction")
    os.makedirs(chiral_out_dir)
    segment_lookup_table_path = os.path.join(SCRIPT_DIR, "data", "look_up_tables",
                                             "FreeSurferColorLUT.txt")
    seg_BIBSnet_outfile = os.path.join(j_args["optional_out_dirs"]["BIBSnet"],
                                       j_args["BIBSnet"]["aseg_outfile"])
    chiral_corrected_nii_outfile_path = os.path.join(
        chiral_out_dir, j_args["BIBSnet"]["aseg_outfile"]
    ) 

    # Select an arbitrary T1w image path to use to get T1w space
    path_T1w = glob(os.path.join(j_args["common"]["bids_input_dir"], subj_ID,
                                 session, "anat", "*_T1w.nii.gz"))[0]

    # Run chirality correction script
    correct_chirality(seg_BIBSnet_outfile, segment_lookup_table_path,
                      l_r_mask_nifti_fpath, chiral_corrected_nii_outfile_path,
                      j_args["transformed_images"]["T1w"], path_T1w)
    return chiral_out_dir


def make_asegderived_mask(aseg_dir):
    """
    Create mask file(s) derived from aseg file(s) in aseg_dir
    :param aseg_dir: String, valid path to existing directory with output files
                     from chirality correction
    :return: List of strings; each is a valid path to an aseg mask file
    """
    # Only make masks from chirality-corrected nifti files
    aseg = glob(os.path.join(aseg_dir, "sub-*_aseg.nii.gz"))  
    aseg.sort()

    # binarize, fillh, and erode aseg to make mask:
    mask_out_files = list()
    for aseg_file in aseg:
        mask_out_files.append(os.path.join(
            aseg_dir, "{}_mask.nii.gz".format(aseg_file.split(".nii.gz")[0])
        ))
        maths = fsl.ImageMaths(in_file=aseg_file,  # (anat file)
                               op_string=("-bin -dilM -dilM -dilM -dilM "
                                          "-fillh -ero -ero -ero -ero"),
                               out_file=mask_out_files[-1])
        maths.run()
    return mask_out_files


def copy_to_derivatives_dir(file_to_copy, derivs_dir, sub_ses, new_fname_part):
    """
    Copy file_to_copy into derivs_dir and rename it with the other 2 arguments
    :param file_to_copy: String, path to existing file to copy to derivs_dir
    :param derivs_dir: String, path to existing directory to copy file into
    :param sub_ses: String, the subject and session connected by an underscore
    :param new_fname_part: String to add to the end of the new filename
    """
    copy_and_rename_file(file_to_copy, os.path.join(derivs_dir, (
        "{}_space-orig_desc-{}.nii.gz".format(sub_ses, new_fname_part)
    )))


def run_nibabies(j_args, logger):
    """
    :param j_args: Dictionary containing all args from parameter .JSON file
    :param logger: logging.Logger object to show messages and raise warnings
    :return: j_args, unchanged
    """
    # Get nibabies options from parameter file and turn them into flags
    nibabies_args = [j_args["common"]["age_months"], ]
    for nibabies_arg in ["cifti_output", "work_dir"]:
        nibabies_args.append(as_cli_arg(nibabies_arg))
        nibabies_args.append(j_args["nibabies"][nibabies_arg])
        # TODO Ensure that all common args required by nibabies are added

    # Check whether aseg and mask files were produced by BIBSnet
    glob_path = os.path.join(j_args["optional_out_dirs"]["BIBSnet"],
                             "*{}*.nii.gz")
    aseg_glob = glob(glob_path.format("aseg"))
    mask_glob = glob(glob_path.format("mask"))
    if aseg_glob and mask_glob:
        derivs = ["--derivatives", j_args["optional_out_dirs"]["BIBSnet"]]
    else:
        derivs = list()
        warn_user_of_conditions(
            ("Missing {{}} files in {}\nNow running nibabies with JLF but not "
             "BIBSnet.".format(j_args["optional_out_dirs"]["BIBSnet"])),
            logger, mask=mask_glob, aseg=aseg_glob
        )
    
    # Run nibabies
    subprocess.check_call([j_args["nibabies"]["script_path"],
                           j_args["common"]["bids_dir"],
                           j_args["optional_out_dirs"]["nibabies"],
                           "participant", *derivs, *nibabies_args])
    logger.info("Nibabies has completed")
    
    return j_args


def run_XCPD(j_args, logger):
    """
    :param j_args: Dictionary containing all args from parameter .JSON file
    :param logger: logging.Logger object to show messages and raise warnings
    :return: j_args, unchanged
    """
    subprocess.check_call((   # TODO Ensure that all "common" and "XCPD" args required by XCPD are added
        "singularity", "run", "--cleanenv",
        "-B", j_args["optional_out_dirs"]["nibabies"] + ":/data:ro",
        "-B", j_args["optional_out_dirs"]["XCPD"] + ":/out",
        "-B", j_args["XCPD"]["work_dir"] + ":/work",
        "/home/faird/shared/code/external/pipelines/ABCD-XCP/xcp-abcd_unstable01102022.sif",  # TODO Make this an import and/or a parameter
        "/data", "/out", "--cifti", "-w", "/work", "--participant-label",
        j_args["common"]["participant_label"]
    ))
    logger.info("XCP-D has completed")
    return j_args


if __name__ == "__main__":
    main()