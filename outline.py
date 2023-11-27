def main():
    BIBSnet = SegmentationPipeline()
    BIBSnet.get_args()
    BIBSnet.validate_args()
    BIBSnet.get_subses()
    BIBSnet.create_directories()

    for subject in BIBSnet.subjects:
        for session in BIBSnet.subjects[subject].sessions:
            run_preBIBSnet(BIBSnet, subject, session)
            run_BIBSnet(BIBSnet, subject, session)
            run_postBIBSnet(BIBSnet, subject, session)

class SegmentationPipeline():
    def __init__(self):
        self.args = None
        self.filetree = {}

    def get_args(self):
        # parse args
        self.args = parsed_args

    def validate_args(self):
        # validate args
        pass

    def get_subses(self):
        self.subjects = {}
        self.subjects[session] = subses

    def create_directories(self):
        # make directory
        self.filetree[directory] = {}

def run_preBIBSnet(BIBSnet, subject, session):
    # 
    pass

def run_BIBSnet(BIBSnet, subject, session):
    pass

def run_postBIBSnet(BIBSnet, subject, session):
    pass