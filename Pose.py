import cv2
from pathlib import Path

class Pose():
    def __init__(self, frame_no, frame, points, body_parts, pose_pairs, rotate):
        self.frame_no = frame_no
        self.frame = frame
        self.points = points
        self.BODY_PARTS = body_parts
        self.POSE_PAIRS = pose_pairs
        self.rotate = rotate

    def get_position(self, body_part): 
        return self.points[body_part]
        
    def draw_pose(self):
        if(self.rotate): self.frame = cv2.rotate(self.frame, cv2.ROTATE_90_CLOCKWISE)

        for pair in self.POSE_PAIRS:
            part_from = pair[0]
            part_to = pair[1]
        
            id_from = self.BODY_PARTS[part_from]
            id_to = self.BODY_PARTS[part_to]

            if self.points[id_from] and self.points[id_to]:
                cv2.line(self.frame, self.points[id_from], self.points[id_to], (0, 255, 0), 3)
                cv2.ellipse(self.frame, self.points[id_from], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)
                cv2.ellipse(self.frame, self.points[id_to], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)

        if(self.rotate): self.frame = cv2.rotate(self.frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        cv2.imwrite("pose_frames/frame_%d.jpg" % self.frame_no, self.frame)
    
    def get_number_of_detected_points(self):
        return sum(x is not None for x in self.points)