import matplotlib.pyplot as plt
import numpy as np
import math
class Analyser():
    def __init__(self):
        f = open("analysis.txt", "w")
        f.close()

    def analyse(self, reps):
        
        self.rep_count(len(reps))
        
        for rep in reps:
            f = open("analysis.txt", "a")
            f.write(f"======= Rep {rep.rep_index + 1} =======\n\n")
            f.write(f"Start Position Frame: {rep.start_pose.frame_no}\n")
            f.write(f"Bottom Position Frame: {rep.bottom_pose.frame_no}\n")
            f.write(f"End Position Frame: {rep.end_pose.frame_no}\n\n")
            f.close()

            self.start_position_elbow(rep)
            self.bottom_position_elbow(rep)
            

        return

    def rep_count(self, reps):
        f = open("analysis.txt", "a")
        f.write(f"Number of reps counted: {reps}\n")
        f.close()

    def get_min_max(self, poses, d):
        USEFUL_POINTS={"Nose": 0, "Neck": 1, "RShoulder": 2, "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
        "LHip": 11, "LKnee": 12, "REye": 14,"LEye": 15, "REar": 16, "LEar": 17}
        MIN_MAX_VALS={}
        USEABLE_POINTS = {}

        for keypoint in USEFUL_POINTS:
            i = USEFUL_POINTS[keypoint]
            points = [pose.get_position(i)[d] for pose in poses if pose.get_position(i) is not None]
            if(len(points) > 0):
                min = np.min(points)
                max = np.max(points)
                if(min != max):
                    MIN_MAX_VALS.update({keypoint: (min, max)})
                    USEABLE_POINTS.update({keypoint: i})

        return MIN_MAX_VALS, USEABLE_POINTS

    def distance_through_rep(self, MIN_MAX_VALS, USEABLE_POINTS, poses, d):
        ratios = []
        frames = np.arange(len(poses))

        for pose in poses:
            pose_ratio = []
            for keypoint in USEABLE_POINTS:
                i = USEABLE_POINTS[keypoint]
                pos = pose.get_position(i)
                if pos is not None:
                    y_1 = float(pos[d] - MIN_MAX_VALS[keypoint][0])
                    y_2 = float(MIN_MAX_VALS[keypoint][1] - MIN_MAX_VALS[keypoint][0])
                    y = y_1 / y_2
                    pose_ratio.append(y)
            if(len(pose_ratio) > 0):
                ratios.append(np.mean(pose_ratio))
            else:
                ratios.append(None)

        return frames, ratios

    def get_moving_point(self, key, ind, frame, rep_poses,  pose):
        if(pose.get_position(ind) is None):
            MIN_MAX_VALS, USEABLE = self.get_min_max(rep_poses, 0)
            frames, heights = self.distance_through_rep(MIN_MAX_VALS, USEABLE, rep_poses, 0)
            if(heights[frame] is not None):
                r = heights[frame]
                min = MIN_MAX_VALS[key][0]
                max = MIN_MAX_VALS[key][1]
                y = min + (r * (max - min))
            else:
                return None

            MIN_MAX_VALS, USEABLE = self.get_min_max(rep_poses, 1)
            frames, dists = self.distance_through_rep(MIN_MAX_VALS, USEABLE, rep_poses, 1)
            if(dists[frame] is not None):
                r = dists[frame]
                min = MIN_MAX_VALS[key][0]
                max = MIN_MAX_VALS[key][1]
                x = min + (r * (max - min))
            else:
                return None

            return (int(y), int(x))
        else:
            return pose.get_position(ind)

    def get_static_point(self, ind, poses, pose):
        if(pose.get_position(ind) is None):
            points = [p.get_position(ind) for p in poses if p.get_position(ind) is not None]
            if(len(points) > 0):
                x = np.mean([p[1] for p in points])
                y = np.mean([p[0] for p in points])
                return (int(y), int(x))
            else: return None
        else: return pose.get_position(ind)

    def get_angle(self, p1, p2, p3):
        vec_1 = [p1[0] - p2[0], p1[1] - p2[1]]
        vec_2 = [p3[0] - p2[0], p3[1] - p2[1]]

        vec_1 = vec_1 / np.linalg.norm(vec_1)
        vec_2 = vec_2 / np.linalg.norm(vec_2)
        angle = np.dot(vec_1, vec_2)
        angle = math.degrees(np.arccos(angle))

        return int(angle)

    def start_position_elbow(self, rep):
        f = open("analysis.txt", "a")
        l_shoulder = self.get_moving_point("LShoulder", 5, 0, rep.rep_poses, rep.start_pose)
        l_elbow = self.get_static_point(6, rep.rep_poses, rep.start_pose)
        l_wrist = self.get_static_point(7, rep.rep_poses, rep.start_pose)

        r_shoulder = self.get_moving_point("RShoulder", 2, 0, rep.rep_poses, rep.start_pose)
        r_elbow = self.get_static_point(3, rep.rep_poses, rep.start_pose)
        r_wrist = self.get_static_point(4, rep.rep_poses, rep.start_pose)
        
        if(l_shoulder is None) or (l_elbow is None) or (l_wrist is None):
            f.write("Could not get information for left elbow angle in top position\n")
        else:  
            f.write(f"Angle at left elbow in top position: {self.get_angle(l_wrist, l_elbow, l_shoulder)} degrees\n")

        if(r_shoulder is None) or (r_elbow is None) or (r_wrist is None):
            f.write("Could not get information for right elbow angle in top position\n")
        else:   
            f.write(f"Angle at right elbow in top position: {self.get_angle(r_wrist, r_elbow, r_shoulder)} degrees\n")
        f.close()

    def bottom_position_elbow(self, rep):
        f = open("analysis.txt", "a")

        l_shoulder = self.get_moving_point("LShoulder", 5, 0, rep.rep_poses, rep.bottom_pose)
        l_elbow = self.get_static_point(6, rep.rep_poses, rep.bottom_pose)
        l_wrist = self.get_static_point(7, rep.rep_poses, rep.bottom_pose)
        
        r_shoulder = self.get_moving_point("RShoulder", 2, 0, rep.rep_poses, rep.bottom_pose)
        r_elbow = self.get_static_point(3, rep.rep_poses, rep.bottom_pose)
        r_wrist = self.get_static_point(4, rep.rep_poses, rep.bottom_pose)

        if(l_shoulder is None) or (l_elbow is None) or (l_wrist is None):
            f.write("Could not get information for left elbow angle in bottom position\n")
        else:   
            f.write(f"Angle at left elbow in bottom position: {self.get_angle(l_wrist, l_elbow, l_shoulder)} degrees\n")

        if(r_shoulder is None) or (r_elbow is None) or (r_wrist is None):
            f.write("Could not get information for right elbow angle in bottom position\n")
        else:
            print(r_shoulder, r_elbow, r_wrist)   
            f.write(f"Angle at right elbow in bottom position: {self.get_angle(r_wrist, r_elbow, r_shoulder)} degrees\n")
        f.close()