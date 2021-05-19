import matplotlib.pyplot as plt
import numpy as np

from scipy.signal import find_peaks
from Rep import Rep

class RepDetector():
    def __init__(self) :
        pass

    def find_reps(self, poses):
        reps = []
        frames, heights = self.distance_through_rep(poses)
        peaks, minima = self.find_peaks_and_minima(frames, heights)

        for i in range(0, len(minima)):
            start = poses[peaks[i]]
            bottom = poses[minima[i]]
            rep_poses = poses[peaks[i]:peaks[i+1]]
            reps.append(Rep(i, start, bottom, rep_poses))

        return reps, heights

    def distance_through_rep(self, poses):
        USEFUL_POINTS={"Nose": 0, "Neck": 1, "RShoulder": 2, "LShoulder": 5, "RHip": 8, "RKnee": 9, 
        "LHip": 11, "LKnee": 12, "REye": 14,"LEye": 15, "REar": 16, "LEar": 17}
        MIN_MAX_VALS={}
        ratios = []
        frames = np.arange(len(poses))

        for keypoint in USEFUL_POINTS:
            i = USEFUL_POINTS[keypoint]
            points = [pose.get_position(i)[0] for pose in poses if pose.get_position(i) is not None]
            if(len(points) > 2):
                min_max = (np.min(points), np.max(points))
                MIN_MAX_VALS.update({keypoint: min_max})
        
        for pose in poses:
            pose_ratio = []
            for keypoint in MIN_MAX_VALS:
                i = USEFUL_POINTS[keypoint]
                height = pose.get_position(i)
                if height is not None:
                    x = (height[0] - MIN_MAX_VALS[keypoint][0]) / (MIN_MAX_VALS[keypoint][1] - MIN_MAX_VALS[keypoint][0])
                    pose_ratio.append(x)
            if(len(pose_ratio) > 0):
                ratios.append(np.mean(pose_ratio))
            else:
                ratios.append(None)

        return frames, ratios

    def find_peaks_and_minima(self, frames, heights):
        inverted_heights = 1 - np.array(heights)

        peak_pos, peak_heights = self.get_peaks(frames, heights)
        minima_pos, minima_heights = self.get_peaks(frames, inverted_heights)

        minima_heights = (1 - np.array(minima_heights))
        
        peak_heights = peak_heights.tolist()
        peak_pos = peak_pos.tolist()
        minima_heights = minima_heights.tolist()
        minima_pos = minima_pos.tolist()

        if(peak_pos[0] > minima_pos[0]):
            peak_pos.insert(0, 0)
            peak_heights.insert(0, heights[0])

        key_points = self.interleave_peaks_and_minimas(peak_pos, minima_pos)
        key_points = self.average_peaks(key_points)
        key_points = self.average_minimas(key_points)

        x = len(key_points)
        if(key_points[x - 1][1] == False):
            key_points.append((frames[len(frames) - 1], True))

        new_peaks = [x[0] for x in key_points if x[1] == True]
        new_minima = [x[0] for x in key_points if x[1] == False]

        return new_peaks, new_minima

    def get_peaks(self, frames, heights):
        peaks = find_peaks(heights, height=0.8)
        peak_heights = peaks[1]['peak_heights']
        peak_pos = frames[peaks[0]]

        return peak_pos, peak_heights

    def interleave_peaks_and_minimas(self, peaks, minimas):
        i = 0
        j = 0
        all_key_frames = []

        for c in range(0, len(peaks) + len(minimas)):
            if(i == len(peaks)):
                for pos in minimas[j:]:
                    all_key_frames.append((pos, False))
                break
            
            if(j == len(minimas)):
                for pos in peaks[i:]:
                    all_key_frames.append((pos, True))
                break
                
            if(peaks[i] < minimas[j]):
                all_key_frames.append((peaks[i], True))
                i+=1
            elif(peaks[i] > minimas[j]):
                all_key_frames.append((minimas[j], False))
                j+=1
        
        return all_key_frames

    def average_peaks(self, keypoints):
        curr_peak = []
        new_keypoints = []

        for i in range(0, len(keypoints)):
            if(keypoints[i][1] == True):
                curr_peak.append(keypoints[i][0])
            else:
                if(len(curr_peak) > 0):
                    new_keypoints.append((round(np.mean(curr_peak)), True))
                    curr_peak = []
                new_keypoints.append(keypoints[i])

        return new_keypoints
    
    def average_minimas(self, keypoints):
        curr_min = []
        new_keypoints = []

        for i in range(0, len(keypoints)):
            if(keypoints[i][1] == False):
                curr_min.append(keypoints[i][0])
            else:
                if(len(curr_min) > 0):
                    new_keypoints.append((round(np.mean(curr_min)), False))
                    curr_min = []
                new_keypoints.append(keypoints[i])

        if(len(curr_min) > 0): new_keypoints.append((round(np.mean(curr_min)), False))

        return new_keypoints