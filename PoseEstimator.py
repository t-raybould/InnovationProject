import cv2
from pathlib import Path

from Pose import Pose

class PoseEstimator():
    def __init__(self, threshold, model, body_parts, pose_pairs):
        self.threshold = threshold
        self.BODY_PARTS = body_parts
        self.POSE_PAIRS = pose_pairs
        self.net = cv2.dnn.readNetFromTensorflow(model)
        self.poses = []

    def get_pose_estimation(self, frame_no):
        # Get the next frame to process
        path = str(Path().absolute()) + '/tmp_frames/frame_' + str(frame_no) + '.jpg'
        frame = cv2.imread(path)
        # Rotate the frame for better pose estimation

        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        frame_width = frame.shape[1]
        frame_height = frame.shape[0]

        blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224), (127.5, 127.5, 127.5), swapRB=False, crop=False)
        self.net.setInput(blob)
        out = self.net.forward()        

        points = []

        for i in range(len(self.BODY_PARTS)):
            heatmap = out[0, i, :, :]
            _, conf, _, point = cv2.minMaxLoc(heatmap)
            
            x = (frame_width * point[0]) / out.shape[3]
            y = (frame_height * point[1]) / out.shape[2]
            points.append((int(x), int(y)) if conf > self.threshold else None)

        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        pose = Pose(frame_no, frame, points, self.BODY_PARTS, self.POSE_PAIRS)
        self.poses.append(pose)

        return 
    
    def avg_points_detected(self):
        lst = []
        for pose in self.poses:
            lst.append(pose.get_number_of_detected_points())
        return lst
        