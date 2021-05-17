import sys
import argparse
import matplotlib.pyplot as plt
import numpy as np

from FrameDecomposer import FrameDecomposer
from PoseEstimator import PoseEstimator
from RepDetector import RepDetector
from Analyser import Analyser

if __name__ == '__main__':

    BODY_PARTS = {"Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
    "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
    "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
    "LEye": 15, "REar": 16, "LEar": 17, "Background": 18}

    POSE_PAIRS = [["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
    ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
    ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
    ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
    ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"]]

    # Create ArgumentParser and define arguments to the system
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='Path to video')
    parser.add_argument('--hoz-flip', help='Apply horizontal flip to images', default=0)
    parser.add_argument('--thr', default=0.25, help='Threshold confidence for pose estimation model')
    args = parser.parse_args() 

    frame_decomposer = FrameDecomposer(args.input, args.hoz_flip)
    pose_estimator = PoseEstimator(args.thr, args.model, BODY_PARTS, POSE_PAIRS)
    rep_detector = RepDetector()
    analyser = Analyser()

    print("DECOMPOSING VIDEO INTO FRAMES")
    frame_decomposer.decompose_video()

    if(frame_decomposer.frame_count > 0):
        frames = np.arange(frame_decomposer.frame_count)
        a_points = []

        print("APPLYING POSE ESTIMATOR TO FRAMES")
        for current_frame in range(0, frame_decomposer.frame_count):
            pose_estimator.get_pose_estimation(current_frame)
        
        print("IDENTIFYING REPS")
        reps = rep_detector.find_reps(pose_estimator.poses)

        print("ANALYSING REPS")
        analyser.analyse(reps)
        for rep in reps:
            rep.draw()