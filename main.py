import sys
import argparse

from FrameDecomposer import FrameDecomposer
from PoseEstimator import PoseEstimator

if __name__ == '__main__':
    # Create ArgumentParser and define arguments to the system
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='Path to video')
    parser.add_argument('--thr', default=0.25, help='Threshold confidence for pose estimation model')
    parser.add_argument('--model', default='model/model.pb', help='Path to model')
    args = parser.parse_args() 

    frame_decomposer = FrameDecomposer(args.input)
    pose_estimator = PoseEstimator(args.thr, args.model)
    
    frame_decomposer.decompose_video()
    
    if(frame_decomposer.frame_count > 0):

        print("APPLYING POSE ESTIMATOR TO FRAMES")
        for current_frame in range(0, frame_decomposer.frame_count):
            pose_estimator.get_pose_estimation(current_frame)
        
        pose = pose_estimator.poses[0]
        pose.get_position(0)

        # print("DRAWING POSE ONTO FRAMES")
        # for pose in pose_estimator.poses:
        #     pose.draw_pose()