import cv2

class Pose():
    def __init__(self, frame_no, frame, points, body_parts, pose_pairs):
        self.frame_no = frame_no
        self.frame = frame
        self.points = points
        self.BODY_PARTS = body_parts
        self.POSE_PAIRS = pose_pairs

    def get_position(self, body_part): 
        return self.points[body_part]
        
    def draw_pose(self):
        self.frame = cv2.rotate(self.frame, cv2.ROTATE_90_CLOCKWISE)

        for pair in self.POSE_PAIRS:
            part_from = pair[0]
            part_to = pair[1]
        
            id_from = self.BODY_PARTS[part_from]
            id_to = self.BODY_PARTS[part_to]

            if self.points[id_from] and self.points[id_to]:
                cv2.line(self.frame, self.points[id_from], self.points[id_to], (0, 255, 0), 3)
            if self.points[id_from]:
                cv2.ellipse(self.frame, self.points[id_from], (8, 8), 0, 0, 360, (0, 0, 255), cv2.FILLED)
            if self.points[id_to]:
                cv2.ellipse(self.frame, self.points[id_to], (8, 8), 0, 0, 360, (0, 0, 255), cv2.FILLED)

        self.frame = cv2.rotate(self.frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        cv2.imwrite("pose_frames/frame_%d.jpg" % self.frame_no, self.frame)
    
    def get_number_of_detected_points(self):
        return sum(x is not None for x in self.points)