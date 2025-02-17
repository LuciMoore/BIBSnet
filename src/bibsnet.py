#!/usr/bin/env python3
# coding: utf-8

"""
Wrapper to run nnU-Net_predict trained on BCP subjects
Greg Conan: gconan@umn.edu
Created: 2022-02-08
Updated: 2022-10-24
"""
# Import standard libraries
from fnmatch import fnmatch
from glob import glob
import os
import subprocess
import sys

from src.logger import LOGGER

from src.utilities import (
    list_files,
    get_subj_ID_and_session
)


def run_BIBSnet(j_args):
    """
    :param j_args: Dictionary containing all args
    :return: j_args, unchanged
    """
    sub_ses = get_subj_ID_and_session(j_args)
    dir_BIBS = os.path.join(j_args["optional_out_dirs"]["bibsnet"],
                            *sub_ses, "{}put")
    list_files(j_args["common"]["work_dir"])
    
    # TODO Change overwrite=False to skip=True in param files because it's more intuitive 
    # Skip BIBSnet if overwrite=False and outputs already exist
    if (not j_args["common"]["overwrite"]) and glob(os.path.join(
        dir_BIBS.format("out"), "*"
    )):
        LOGGER.info("Skipping BIBSnet because outputs already exist at the "
                    "BIBSnet output path below, and --overwrite is off.\n{}"
                    .format(dir_BIBS.format("out")))

    else:  # Run BIBSnet
        try:  # Run BIBSnet
            inputs_BIBSnet = {"model": j_args["bibsnet"]["model"],
                              "nnUNet": j_args["bibsnet"]["nnUNet_predict_path"],
                              "input": dir_BIBS.format("in"),
                              "output": dir_BIBS.format("out"),
                              "task": "{:03d}".format(j_args["ID"]["model"])} #   j_args["bibsnet"]["task"])}
            os.makedirs(inputs_BIBSnet["output"], exist_ok=True)
            LOGGER.verbose("Now running BIBSnet with these parameters:\n{}\n".format(inputs_BIBSnet))
            run_nnUNet_predict(inputs_BIBSnet)

        except subprocess.CalledProcessError as e:
            # BIBSnet will crash even after correctly creating a segmentation,
            # so only crash if that segmentation is not made.
            outfpath = os.path.join(dir_BIBS.format("out"),
                                    "{}_optimal_resized.nii.gz"
                                    .format("_".join(sub_ses)))
            if not os.path.exists(outfpath):
                LOGGER.error("BIBSnet failed to create this segmentation "
                             "file...\n{}\n...from these inputs:\n{}"
                             .format(outfpath, inputs_BIBSnet))
                sys.exit(e)

        # Remove unneeded empty directories
        for unneeded_dir_name in ("nnUNet_cropped_data", "nnUNet_raw_data"):
            unneeded_dir_path = os.path.join(
                j_args["optional_out_dirs"]["derivatives"], unneeded_dir_name
            )
            LOGGER.verbose("Deleting unnecessary empty directory at {}"
                        .format(unneeded_dir_path))
            if os.path.isdir(unneeded_dir_path):
                os.removedirs(unneeded_dir_path)

    list_files(j_args["common"]["work_dir"])
    
    return j_args


def run_nnUNet_predict(cli_args):
    """
    Run nnU-Net_predict in a subshell using subprocess
    :param cli_args: Dictionary containing all command-line input arguments
    :return: N/A
    """
    to_run = [cli_args["nnUNet"], "-i",
                     cli_args["input"], "-o", cli_args["output"], "-t",
                     str(cli_args["task"]), "-m", cli_args["model"], 
                     "--disable_tta"
                     ]

    LOGGER.verbose(f"Now running nnUNet with these parameters: {to_run}")
    process = subprocess.Popen(to_run, stdout=subprocess.PIPE, universal_newlines=True)
    with process.stdout:
        for line in process.stdout:
            LOGGER.subprocess(line, extra={'id': 'nnUNet'})
    exitcode = process.wait()
    if exitcode == 0:
        LOGGER.verbose("nnUNet completed")
    else:
        LOGGER.error(f"nnUNet failed to complete, exitcode {exitcode}")
    
    # Only raise an error if there are no output segmentation file(s)
    if not glob(os.path.join(cli_args["output"], "*.nii.gz")):
        # TODO This statement should change if we add a new model
        sys.exit("Error: Output segmentation file not created at the path "
                 "below during nnUNet_predict run.\n{}\n\nFor your input files "
                 "at the path below, check their filenames and visually "
                 "inspect them if needed.\n{}\n\n"
                 .format(cli_args["output"], cli_args["input"]))

        