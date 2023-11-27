#!/usr/bin/env python
# coding: utf-8
from src.seg_pipeline_class import SegmentationPipeline

def main():
    BIBSnet = SegmentationPipeline()
    BIBSnet.get_bids()
    print(BIBSnet.filetree)

if __name__ == "__main__":
    main()