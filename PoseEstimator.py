import cv2
from pathlib import Path


from Pose import Pose

class PoseEstimator():
    def __init__(self, threshold, model):
        self.threshold = threshold
        self.BODY_PARTS = {"Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
        "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
        "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
        "LEye": 15, "REar": 16, "LEar": 17, "Background": 18}

        self.POSE_PAIRS = [["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
        ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
        ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
        ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
        ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"]]

        self.net = cv2.dnn.readNetFromTensorflow(model)
        self.poses = []

    def get_pose_estimation(self, frame_no):
        # Get the next frame to process
        path = str(Path().absolute()) + '/tmp_frames/frame_' + str(frame_no) + '.jpg'
        frame = cv2.imread(path)
        # Rotate the frame for better pose estimation
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        frame_width = frame.shape[1]
        frame_height = frame.shape[0]

        blob = cv2.dnn.blobFromImage(frame, 1.0, (368, 368), (127.5, 127.5, 127.5), swapRB=False, crop=False)
        self.net.setInput(blob)
        out = self.net.forward()

        points = []

        for i in range(len(self.BODY_PARTS)):
            heatmap = out[0, i, :, :]
            _, conf, _, point = cv2.minMaxLoc(heatmap)
            
            x = (frame_width * point[0]) / out.shape[3]
            y = (frame_height * point[1]) / out.shape[2]
            points.append((int(x), int(y)) if conf > self.threshold else None)

        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        pose = Pose(frame_no, frame, points)
        self.poses.append(pose)

        return 