import matplotlib.pyplot as plt
import numpy as np
import math
class Analyser():
    def __init__(self):
        f = open("analysis.txt", "w")
        f.close()

    def analyse(self, reps, ratios):
        
        self.rep_count(len(reps))
        
        for rep in reps:
            f = open("analysis.txt", "a")
            f.write(f"\n\n======= Rep {rep.rep_index + 1} =======\n\n")
            f.write(f"Start Position Frame: {rep.start_pose.frame_no}\n")
            f.write(f"Bottom Position Frame: {rep.bottom_pose.frame_no}\n")
            f.close()

            self.start_position_elbow(rep, ratios)
            self.start_position_shoulder_width(rep, ratios)
            self.start_position_shoulder_width(rep, ratios)
            self.bottom_position_elbow(rep, ratios)
            
        return

    def rep_count(self, reps):
        f = open("analysis.txt", "a")
        f.write(f"Number of reps counted: {reps}\n")
        f.close()

    def get_min_max(self, i, poses):
        xs = [pose.get_position(i)[1] for pose in poses if pose.get_position(i) is not None]
        ys = [pose.get_position(i)[0] for pose in poses if pose.get_position(i) is not None]
        if(len(xs) > 1):
            min_max_x = (np.min(xs), np.max(xs))
            min_max_y = (np.min(ys), np.max(ys))
            return min_max_x, min_max_y
        else:
            return None, None

    def get_point(self, ind, pose, ratios, rep_poses):
        if(pose.get_position(ind) is None):
            if(ratios[pose.frame_no] is None):
                return None
            
            min_max_x, min_max_y = self.get_min_max(ind, rep_poses)
            if(min_max_x is None):
                return None

            r = ratios[pose.frame_no]
            x = min_max_x[0] + (r * (min_max_x[1] - min_max_x[0]))
            y = min_max_y[0] + (r * (min_max_y[1] - min_max_y[0]))
            p = (int(y), int(x))
            return p
        else: 
            return pose.get_position(ind)

    def get_angle(self, p1, p2, p3):
        vec_1 = [p1[0] - p2[0], p1[1] - p2[1]]
        vec_2 = [p3[0] - p2[0], p3[1] - p2[1]]

        vec_1 = vec_1 / np.linalg.norm(vec_1)
        vec_2 = vec_2 / np.linalg.norm(vec_2)
        angle = np.dot(vec_1, vec_2)
        angle = math.degrees(np.arccos(angle))

        return int(angle)

    def start_elbow_angle(self, f, side, wrist, elbow, shoulder):
        angle = self.get_angle(wrist, elbow, shoulder)
        if(angle < 160): 
            f.write(f"The angle at your {side} elbow is {angle} degrees, which suggests your arm is not straight in that start of the rep\n")
            return True
        else:
            return False

    def vertical_arm(f, side, wrist, shoulder):
        if(wrist[1] - shoulder[1] < 20):
            f.write(f"Your {side} wrist is too far forward, move it so that your arm is vertical\n")
            return True
        elif(wrist[1] - shoulder[1] > 20):
            f.write(f"Your {side} wrist is too far back, move it forward so that your arm is vertical\n")
            return True
        else:
            return False

    def start_position_elbow(self, rep, ratios):
        problem = False

        f = open("analysis.txt", "a")

        f.write("\n-------Start Position -------\n\n")

        l_shoulder = self.get_point(5, rep.start_pose, ratios, rep.rep_poses)
        l_elbow = self.get_point(6, rep.start_pose, ratios, rep.rep_poses)
        l_wrist = self.get_point(7, rep.start_pose, ratios, rep.rep_poses)
        r_shoulder = self.get_point(2, rep.start_pose, ratios, rep.rep_poses)
        r_elbow = self.get_point(3, rep.start_pose, ratios, rep.rep_poses)
        r_wrist = self.get_point(4, rep.start_pose, ratios, rep.rep_poses)

        if(l_shoulder is None) or (l_elbow is None) or (l_wrist is None):
            f.write("Could not get information for left arm in top position\n")
            problem = True
        else:
            problem = problem or self.start_elbow_angle(f, "left", l_wrist, l_elbow, l_shoulder)
            problem = problem or self.vertical_arm(f, "left", l_wrist, l_shoulder)
        
        if(r_shoulder is None) or (r_elbow is None) or (r_wrist is None):
            f.write("Could not get information for right arm in top position\n")
            problem = True
        else: 
            problem = problem or self.start_elbow_angle(f, "right", r_wrist, r_elbow, r_shoulder)
            problem = problem or self.vertical_arm(f, "right", r_wrist, r_shoulder)
    
        if (problem is False):
            f.write("Your start position is good")
        
        f.close()

    def bottom_elbow_angle(self, f, side, wrist, elbow, shoulder):
        angle = self.get_angle(wrist, elbow, shoulder)
        if(angle > 90):
            f.write(f"The angle at your {side} elbow is greater than 90 degrees, meaning you have not done a full range of motion\n")
            return True
        else:
            return False

    def bottom_position_elbow(self, rep, ratios):

        problem = False

        f = open("analysis.txt", "a")

        f.write("\n-------Bottom Position -------\n\n")

        l_shoulder = self.get_point(5, rep.bottom_pose, ratios, rep.rep_poses)
        l_elbow = self.get_point(6, rep.bottom_pose, ratios, rep.rep_poses)
        l_wrist = self.get_point(7, rep.bottom_pose, ratios, rep.rep_poses)
        r_shoulder = self.get_point(2, rep.bottom_pose, ratios, rep.rep_poses)
        r_elbow = self.get_point(3, rep.bottom_pose, ratios, rep.rep_poses)
        r_wrist = self.get_point(4, rep.bottom_pose, ratios, rep.rep_poses)

        if(l_shoulder is None) or (l_elbow is None) or (l_wrist is None):
            f.write("Could not get information for left elbow angle in bottom position\n")
            problem = True
        else:   
            problem = problem or self.bottom_elbow_angle(f, "left", l_wrist, l_elbow, l_shoulder)

        if(r_shoulder is None) or (r_elbow is None) or (r_wrist is None):
            f.write("Could not get information for right elbow angle in bottom position\n")
            problem = True
        else:
            problem = problem or self.bottom_elbow_angle(f, "left", l_wrist, l_elbow, l_shoulder)

        if (problem is False):
            f.write("Your bottom position is good")

        f.close()

    def start_position_shoulder_width(self, rep, ratios):
        f = open("analysis.txt", "a")

        l_shoulder = self.get_point(5, rep.start_pose, ratios, rep.rep_poses)
        r_shoulder = self.get_point(2, rep.start_pose, ratios, rep.rep_poses)
        l_wrist = self.get_point(7, rep.start_pose, ratios, rep.rep_poses)
        r_wrist = self.get_point(4, rep.start_pose, ratios, rep.rep_poses)

        s_dist = abs(np.linalg.norm(l_shoulder - r_shoulder))
        w_dist = abs(np.linalg.norm(l_wrist - r_wrist))

        if(w_dist < 0.9 * s_dist):
            f.write("Your hands are too close together, they should be shoulder width apart")
        elif(w_dist > 1.1 * s_dist):
            f.write("Your hands are too close togethe, they should be shoulder width apart")
        else:
            f.write("Your hands are in the correct position")

        f.close()
        