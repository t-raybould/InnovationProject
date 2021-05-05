import cv2
from pathlib import Path

class Pose():
    def __init__(self, frame_no, frame, points):
        self.frame_no = frame_no
        self.frame = frame
        self.points = points
        self.BODY_PARTS = {"Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
        "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
        "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
        "LEye": 15, "REar": 16, "LEar": 17, "Background": 18}

        self.POSE_PAIRS = [["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
        ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
        ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
        ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
        ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"]]

    def get_position(self, body_part):
        print(self.points)

    def draw_pose(self):
        self.frame = cv2.rotate(self.frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        for pair in self.POSE_PAIRS:
            part_from = pair[0]
            part_to = pair[1]
        
            id_from = self.BODY_PARTS[part_from]
            id_to = self.BODY_PARTS[part_to]

            if self.points[id_from] and self.points[id_to]:
                cv2.line(self.frame, self.points[id_from], self.points[id_to], (0, 255, 0), 3)
                cv2.ellipse(self.frame, self.points[id_from], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)
                cv2.ellipse(self.frame, self.points[id_to], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)

        self.frame = cv2.rotate(self.frame, cv2.ROTATE_90_CLOCKWISE)

        cv2.imwrite("pose_frames/frame_%d.jpg" % self.frame_no, self.frame)