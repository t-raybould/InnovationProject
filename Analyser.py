import matplotlib.pyplot as plt
import numpy as np
import math
class Analyser():
    def __init__(self):
        f = open("analysis.txt", "w")
        f.close()

    def scale(self, actual, goal):
        rating = round(actual/goal) * 10 

        if (rating <= 3):
            return "Bad"
        elif (rating <= 5):
            return "OK"
        elif (rating <= 7):
            return "Good"
        elif (rating <= 9):
            return "Great"
        else: return "Perfect"

    def analyse(self, reps):
        
        self.rep_count(len(reps))
        
        for rep in reps:
            f = open("analysis.txt", "a")
            f.write(f"======= Rep {rep.rep_index + 1} =======\n\n")
            angle = self.start_position(rep)
            rating = self.scale(angle, 180)
            f.write(f"Start Position: {angle} degrees\n")
            f.write(f"Rating: {rating}\n")
            f.write(f"This angle is calculated at your elbow and needs to be as close to 180 degrees as possible.\n")
            if(round(angle/180) * 10  < 6):
                f.write(f"Your starting position can improve")
                f.write(f"try and make sure your arms are as straight as possible so that your shoulders, elbows, and wrists are vertically stacked")
                f.close()

        return

    def rep_count(self, reps):
        f = open("analysis.txt", "a")
        f.write(f"Number of reps counted: {reps}\n")
        f.close()

    def get_min_max(self, poses, d):
        USEFUL_POINTS={"Nose": 0,  "RShoulder": 2, "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
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
                print("Need to be savvy")

            MIN_MAX_VALS, USEABLE = self.get_min_max(rep_poses, 1)
            frames, dists = self.distance_through_rep(MIN_MAX_VALS, USEABLE, rep_poses, 1)
            if(dists[frame] is not None):
                r = dists[frame]
                min = MIN_MAX_VALS[key][0]
                max = MIN_MAX_VALS[key][1]
                x = min + (r * (max - min))
            else:
                print("Need to be savvy")

            return (int(y), int(x))
        else:
            return pose.get_position(ind)

    def get_static_point(self, ind, poses, pose):
        if(pose.get_position(ind) is None):
            points = [p.get_position(ind) for p in poses if p.get_position(ind) is not None]
            x = np.mean([p[1] for p in points])
            y = np.mean([p[0] for p in points])
            return (int(y), int(x))
        else:
            return pose.get_position(ind)

    def start_position(self, rep):
        l_shoulder = self.get_moving_point("LShoulder", 5, 0, rep.rep_poses, rep.start_pose)
        l_elbow = self.get_static_point(6, rep.rep_poses, rep.start_pose)
        l_wrist = self.get_static_point(7, rep.rep_poses, rep.start_pose)
        r_shoulder = self.get_moving_point("RShoulder", 2, 0, rep.rep_poses, rep.start_pose)
        r_elbow = self.get_static_point(3, rep.rep_poses, rep.start_pose)
        r_wrist = self.get_static_point(4, rep.rep_poses, rep.start_pose)

        if not(l_elbow[1] > r_elbow[1]) ^ (l_wrist[1] < r_wrist[1]):
            temp = l_wrist
            l_wrist = r_wrist
            r_wrist = temp
        
        vec_1 = [l_elbow[1] - l_shoulder[1], l_elbow[0] - l_shoulder[0]]
        vec_2 = [l_wrist[1] - l_elbow[1], l_wrist[0] - l_elbow[0]]
        
        vec_1 = vec_1 / np.linalg.norm(vec_1)
        vec_2 = vec_2 / np.linalg.norm(vec_2)
        angle = np.dot(vec_1, vec_2)
        angle = math.degrees(np.arccos(angle))

        return int(angle)