#!/usr/bin/env python
# coding: utf-8
from src.seg_pipeline_class import SegmentationPipeline
from src.fake import (
    run_preBIBSnet,
    run_BIBSnet,
    run_postBIBSnet
)

def main():
    ArgsAndFiles = SegmentationPipeline()
    stages = ArgsAndFiles.stages

    for subject in ArgsAndFiles.subjects:
        for session in ArgsAndFiles.get_sessions(subject):
            ArgsAndFiles.make_dirs(subject, session)
            if 'preBIBSnet' in stages:
                run_preBIBSnet(ArgsAndFiles, subject, session)
            if 'BIBSnet' in stages:
                run_BIBSnet(ArgsAndFiles, subject, session)
            if 'postBIBSnet' in stages:
                run_postBIBSnet(ArgsAndFiles, subject, session)


if __name__ == "__main__":
    main()