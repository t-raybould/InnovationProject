import sys
import argparse
import matplotlib.pyplot as plt
import numpy as np

from FrameDecomposer import FrameDecomposer
from PoseEstimator import PoseEstimator

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
    parser.add_argument('--model', default='model/model.pb', help='Path to model')
    args = parser.parse_args() 

    frame_decomposer = FrameDecomposer(args.input, args.hoz_flip)
    pose_estimator = PoseEstimator(args.thr, args.model, BODY_PARTS, POSE_PAIRS, True)
    
    frame_decomposer.decompose_video()

    if(frame_decomposer.frame_count > 0):
        frames = []
        a_points = []

        print("APPLYING POSE ESTIMATOR TO FRAMES")
        for current_frame in range(0, frame_decomposer.frame_count):
            frames.append(int(current_frame))
            pose_estimator.get_pose_estimation(current_frame)
        
        pose_estimator.analysis_loop()

        
        
        # a_points = pose_estimator_a.avg_points_detected()
        # b_points = pose_estimator_b.avg_points_detected()
        # X_axis = np.arange(len(frames))

        # print(f"Min: {np.min(a_points)}, Max: {np.max(a_points)}, Mean: {np.mean(a_points)}")
        # print(f"Min: {np.min(b_points)}, Max: {np.max(b_points)}, Mean: {np.mean(b_points)}")

        # plt.plot(X_axis, a_points, label="Rotation Applied")
        # plt.plot(X_axis, b_points, label="No Rotation")

        # plt.xlabel("Frame")
        # plt.ylabel("Number of points detected")
        # plt.legend()
        # plt.savefig('points_detected_graph.png')