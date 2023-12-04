#!/usr/bin/env python
# coding: utf-8
import json
from src.seg_pipeline_class import SegmentationPipeline
from src.fake import (
    run_preBIBSnet,
    run_BIBSnet,
    run_postBIBSnet
)

def main():
    BIBSnet = SegmentationPipeline()
    stages = BIBSnet.stages

    for subject in BIBSnet.get_subjects():
        for session in BIBSnet.get_sessions(subject):
            if 'preBIBSnet' in stages:
                run_preBIBSnet(BIBSnet, subject, session)
            if 'BIBSnet' in stages:
                run_BIBSnet(BIBSnet, subject, session)
            if 'postBIBSnet' in stages:
                run_postBIBSnet(BIBSnet, subject, session)


if __name__ == "__main__":
    main()