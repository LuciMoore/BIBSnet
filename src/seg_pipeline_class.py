import argparse
import os
import logging
import sys
from bids import BIDSLayout
import pandas as pd

from src.validate import ( 
    valid_output_dir,
    valid_readable_dir,
    valid_subj_ses_ID,
    valid_whole_number,
    valid_readable_file
)
from src.filetree import (
    filetree
)

class SegmentationPipeline():
    """
    Class that holds information on user defined paramaeters, directory structure, etc. to persist outside of any functions run.

    Attributes
    ----------
    args: argparse Namespace object, command line arguments submitted by the user. Set by get_args method.
    LOGGER: logging object, general logger for use throughout the pipeline. Created by make_logger method.
    VERBOSE_LEVEL_NUM: int, used to set logging levels in self.LOGGER
    SUBPROCESS_LEVEL_NUM: int, used to set logging levels in self.LOGGER
    filetree: dict, mimics file tree of directories used by BIBSnet.
    stage_names: list, names of all possible stages to be run.
    stages: list, names of stages the user has selected to run from stage_names
    bids: dict, dictionary mimicing the file structure of the input data. tracks sub, ses, t1/t2 scans
    """
    def __init__(self):

        self.args = None
        self.filetree = filetree
        self.bids = {}
        self.stage_names = ["preBIBSnet", "BIBSnet", "postBIBSnet"]
        self.stages = None


        # get command line arguments
        self.get_args()

        # set self.stages based on user input for start and end
        self.set_stages()

        # set log level constants, make logger
        self.VERBOSE_LEVEL_NUM = 15
        self.SUBPROCESS_LEVEL_NUM = self.VERBOSE_LEVEL_NUM -1
        self.make_logger()

        if self.args.verbose:
            self.LOGGER.setLevel(self.VERBOSE_LEVEL_NUM)
        elif self.args.debug:
            self.LOGGER.setLevel(logging.DEBUG)
        else:
            self.LOGGER.setLevel(logging.INFO)

        # output warnings for depricated arguments
        if self.args.parameter_json is not None:
            self.LOGGER.warning("Parameter JSON is deprecated.\nAll arguments formerly in this file are now flags.\nSee https://bibsnet.readthedocs.io/ for updated usage.")

        # parse bids inputs
        self.get_bids()
        self.subjects = self.get_subjects()

     
    def make_logger(self):

        # Add new logging level between DEBUG and INFO
        logging.addLevelName(self.VERBOSE_LEVEL_NUM, "VERBOSE")
        def verbose(self, message, *args, **kws):
            if self.isEnabledFor(self.VERBOSE_LEVEL_NUM):
                self._log(self.VERBOSE_LEVEL_NUM, message, args, **kws)
        logging.Logger.verbose = verbose

        # Add new logging level for subprocesses
        logging.addLevelName(self.SUBPROCESS_LEVEL_NUM, "SUBPROCESS")
        def subprocess(self, message, *args, **kws):
            if self.isEnabledFor(self.SUBPROCESS_LEVEL_NUM):
                self._log(self.SUBPROCESS_LEVEL_NUM, message, args, **kws)
        logging.Logger.subprocess = subprocess
        
        log = logging.getLogger("BIBSnet")

        # Create standard format for log statements
        format = "\n%(levelname)s %(asctime)s: %(message)s"
        formatter = logging.Formatter(format)
        subprocess_format = "%(id)s %(asctime)s: %(message)s"
        subprocess_formatter = logging.Formatter(subprocess_format)

        # Redirect INFO and DEBUG to stdout
        handle_out = logging.StreamHandler(sys.stdout)
        handle_out.setLevel(logging.DEBUG)
        handle_out.addFilter(lambda record: record.levelno <= logging.INFO)
        handle_out.addFilter(lambda record: record.levelno != self.SUBPROCESS_LEVEL_NUM)
        handle_out.setFormatter(formatter)
        log.addHandler(handle_out)

        # Set special format for subprocess level
        handle_subprocess = logging.StreamHandler(sys.stdout)
        handle_subprocess.setLevel(self.SUBPROCESS_LEVEL_NUM)
        handle_subprocess.addFilter(lambda record: record.levelno <= self.SUBPROCESS_LEVEL_NUM)
        handle_subprocess.setFormatter(subprocess_formatter)
        log.addHandler(handle_subprocess)

        # Redirect WARNING+ to stderr
        handle_err = logging.StreamHandler(sys.stderr)
        handle_err.setLevel(logging.WARNING)
        handle_err.setFormatter(formatter)
        log.addHandler(handle_err)

        self.LOGGER = log


    def get_args(self):
        """
        parses command line arguments and sets them to self.args
        """
        default_end_stage = self.stage_names[-1]
        default_fsl_bin_path = "/opt/fsl-6.0.5.1/bin/"
        default_nnUNet_configuration = "3d_fullres"
        default_nnUNet_predict_path = "/opt/conda/bin/nnUNet_predict"
        default_work_dir = os.path.abspath(os.path.join(os.sep, "tmp", "bibsnet"))

        msg_stage = ("Name of the stage to run {}. By default, this will be "
                    "the {} stage. Valid choices: {}")
        parser = argparse.ArgumentParser("BIBSnet")

        # BIDS-App required positional args, validated later in j_args
        parser.add_argument(
            "bids_dir", type=valid_readable_dir,
            help=("Valid absolute path to existing base study directory "
                "containing BIDS-valid input subject data directories. "
                "Example: /path/to/bids/input/")  # TODO Keep as j_args[common][bids_dir]
        )
        parser.add_argument(
            "output_dir", type=valid_readable_dir,  # TODO Does this dir have to already exist?
            help=("Valid absolute path to existing derivatives directory to save "
                "each stage's outputs by subject session into. Example: "
                "/path/to/output/derivatives/")
        )
        parser.add_argument(
            "analysis_level", choices=["participant"],  # TODO Will we ever need to add group-level analysis functionality? Currently this argument does absolutely nothing
            help=("Processing level. Currently the only choice is 'participant'. "
                "See BIDS-Apps specification.")
        )

        # Optional flag arguments
        parser.add_argument(
            "-participant", "--subject", "-sub", "--participant-label",
            dest="participant_label", type=valid_subj_ses_ID,
            help=("The participant's unique subject identifier, without 'sub-' "
                "prefix. Example: 'ABC12345'")  # TODO Make BIBSnet able to accept with OR without 'sub-' prefix
        )
        parser.add_argument(
            "-age", "-months", "--age-months", type=valid_whole_number,
            help=("Positive integer, the participant's age in months. For "
                "example, -age 5 would mean the participant is 5 months old. "
                "Include this argument unless the age in months is specified in "
                "each subject's sub-{}_sessions.tsv file inside its BIDS input directory "
                "or inside the participants.tsv file inside the BIDS directory at the" 
                "subject-level.")
        )
        parser.add_argument(
            "-end", "--ending-stage", dest="end",
            choices=self.stage_names, default=default_end_stage,
            help=msg_stage.format("last", default_end_stage, ", ".join(self.stage_names))
        )
        parser.add_argument(
            "--fsl-bin-path",
            type=valid_readable_dir,
            default=default_fsl_bin_path,
            help=("Valid path to fsl bin. "
                "Defaults to the path used by the container: {}".format(default_fsl_bin_path))
        )
        parser.add_argument(
            "-jargs", "-params", "--parameter-json", dest="parameter_json",
            help=("Parameter JSON is deprecated. "
                "All arguments formerly in this file are now flags. "
                "This argument does nothing. "
                "See https://bibsnet.readthedocs.io/ for updated usage.")
        )
        parser.add_argument(
            "-model", "--model-number", "--bibsnet-model",
            type=valid_whole_number, dest="model",
            help=("Model/task number for BIBSnet. By default, this will be "
                "inferred from the models.csv based on which data exists in the "
                "--bids-dir. BIBSnet will run model 514 by default for T1w-"
                "only, model 515 for T2w-only, and model 552 for both T1w and "
                "T2w.")
        )
        parser.add_argument(
            "--nnUNet", "-n", type=valid_readable_file, default=default_nnUNet_predict_path,
            help=("Valid path to existing executable file to run nnU-Net_predict. "
                "By default, this script will assume that nnU-Net_predict will "
                "be the path used by the container: {}".format(default_nnUNet_predict_path))
        )
        parser.add_argument(
            "--nnUNet-configuration", dest="nnUNet_configuration",
            choices=["2d", "3d_fullres", "3d_lowres", "3d_cascade_fullres"],
            default=default_nnUNet_configuration,
            help=("The nnUNet configuration to use."
                "Defaults to {}".format(default_nnUNet_configuration))
        )
        parser.add_argument(
            "--overwrite", "--overwrite-old",  # TODO Change this to "-skip"
            dest="overwrite", action="store_true",
            help=("Include this flag to overwrite any previous BIBSnet outputs "
                "in the derivatives sub-directories. Otherwise, by default "
                "BIBSnet will skip creating any BIBSnet output files that "
                "already exist in the sub-directories of derivatives.")
        )
        parser.add_argument(
            "-ses", "--session", "--session-id", type=valid_subj_ses_ID,
            help=("The name of the session to processes participant data for. "
                "Example: baseline_year1")
        )
        parser.add_argument(
            "-start", "--starting-stage", dest="start",
            choices=self.stage_names, default=self.stage_names[0],   # TODO Change default to start where we left off by checking which stages' prerequisites and outputs already exist
            help=msg_stage.format("first", self.stage_names[0], ", ".join(self.stage_names))
        )
        parser.add_argument(
            "-w", "--work-dir", type=valid_output_dir, dest="work_dir",
            default=default_work_dir,
            help=("Valid absolute path where intermediate results should be stored. "
                "Example: /path/to/working/directory")
        )
        parser.add_argument(
            "-z", "--brain-z-size", dest="brain_z_size", action="store_true",
            help=("Include this flag to infer participants' brain height (z) "
                "using the sub-{}_sessions.tsv or participant.tsv brain_z_size column." 
                "Otherwise, BIBSnet will estimate the brain height from the participant "
                "age and averages of a large sample of infant brain heights.")  # TODO rephrase
        )
        # Add mutually exclusive group for setting log level
        log_level = parser.add_mutually_exclusive_group()
        log_level.add_argument(
            "-v", "--verbose", action="store_true",
            help=("Include this flag to print detailed information and every "
                "command being run by BIBSnet to stdout. Otherwise BIBSnet "
                "will only print warnings, errors, and minimal output.")
        )
        log_level.add_argument(
            "-d", "--debug", action="store_true",
            help=("Include this flag to print highly detailed information to stdout. "
                "Use this to see subprocess log statements such as those for FSL, nnUNet and ANTS. "
                "--verbose is recommended for standard use.")
        )

        self.args = parser.parse_args()
    

    def get_bids(self):
        
        """
        :param j_args: Dictionary containing all args
        :param subj_or_none: String (the subject ID) or a falsey value
        :param ses_or_none: String (the session name) or a falsey value
        :return: List of dicts; each dict maps "subject" to its subject ID string
                and may also map "session" to its session ID string
        """
        layout = BIDSLayout(self.args.bids_dir)
        bids = {'subjects': {}}
        bids['participants-tsv'] = layout.get(suffix='participants', extension='tsv', return_type='filename')
        subjects = layout.get_subjects()
        sessions = layout.get_sessions()
        for subject in subjects:
            bids['subjects'][subject] = {'sessions': {}}
            bids['subjects'][subject]['sessions-tsv'] = layout.get(subject=subject, suffix='sessions', extension='tsv', return_type='filename')
            for session in sessions:
                sub_ses = layout.get(subject=subject, session=session)
                if sub_ses:
                    bids['subjects'][subject]['sessions'][session] = {'scans': {} }
                    t1s = layout.get(subject=subject, session=session, suffix='T1w', extension='nii.gz', return_type='filename')
                    t2s = layout.get(subject=subject, session=session, suffix='T2w', extension='nii.gz', return_type='filename')
                    bids['subjects'][subject]['sessions'][session]['scans']['T1w'] = t1s
                    bids['subjects'][subject]['sessions'][session]['scans']['T2w'] = t2s
        self.bids=bids


    def set_stages(self):
        """
        Set stages to run based on user input for start and end.
        Error if start is a later stage than end.
        """
        start_index = self.stage_names.index(self.args.start)
        end_index = self.stage_names.index(self.args.end) + 1
        if start_index > end_index - 1:
            sys.exit(f"Error: {self.args.end} stage must happen before {self.args.start} stage.")
        self.stages = self.stage_names[start_index:end_index]


    def get_subjects(self):
        bids_subjects = self.bids['subjects'].keys()
        user_input_subject = self.args.participant_label
        if user_input_subject:
            if user_input_subject not in bids_subjects:
                sys.exit(f"User input subject '{user_input_subject}' not found in bids_dir.")
            return [user_input_subject]
        else:
            return bids_subjects


    def get_sessions(self, subject):
        bids_sessions = self.bids['subjects'][subject]['sessions'].keys()
        user_input_session = self.args.session
        if self.args.session:
            if user_input_session not in bids_sessions:
                self.LOGGER.error(f"User input session '{user_input_session}' not found in bids_dir for subject {subject}.")
                return []
            else:
                return [user_input_session]
        else:
            return bids_sessions


    def make_dirs(self, subject, session):
        needed_dirs = {}
        self.get_needed_dirs(needed_dirs, self.filetree)
        needed_dirs = list(needed_dirs.keys())
        for path in needed_dirs:
            dir = self.fill_path_template(path, subject, session)
            try:
                os.makedirs(dir, exist_ok=True)
            except Exception as e:
                self.LOGGER.error(f"Error making required directories:\n{e}")


    def get_needed_dirs(self, needed_dirs, filetree):
        for path in filetree.values():
            if isinstance(path, str):
                dir = '/'.join(path.split('/')[:-1])
                needed_dirs[dir] = ''
            else:
                self.get_needed_dirs(needed_dirs, path)


    def fill_path_template(self, template, subject, session):
        return template.replace('{{WORK}}', self.args.work_dir).replace('{{DERIVATIVES}}', self.args.output_dir).replace('{{SUBJECT}}', subject).replace('{{SESSION}}', session)
    

    def get_age(self, subject, session):
        if self.args.age_months:
            return self.args.age_months
        else:
            if self.bids['subjects'][subject]['sessions-tsv']:
                tsv_df = pd.read_csv(self.bids['subjects'][subject]['sessions-tsv'][0], delim_whitespace=True, index_col='session_id')
                return tsv_df.at[f"ses-{session}", 'age']
            elif self.bids['participants-tsv']:
                tsv_df = pd.read_csv(self.bids['participants-tsv'][0], delim_whitespace=True, index_col='participant_id')
                return tsv_df.at[f"sub-{subject}", 'age']
            else:
                sys.exit(f"No age found for {subject}, {session}")


    def get_brain_size(self, subject, session):
        if self.args.brain_z_size:
            return self.args.brain_z_size
        else:
            # get age
            # lookup brain size from table
            pass

