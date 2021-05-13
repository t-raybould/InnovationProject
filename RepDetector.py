import matplotlib.pyplot as plt
import numpy as np

from scipy.signal import find_peaks

class RepDetector():
    def __init__(self) :
        pass
    
    def find_reps(self, frames, heights):
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

        print(key_points)

        new_peaks = [x[0] for x in key_points if x[1] == True]
        new_peak_heights = [heights[i] for i in new_peaks]

        new_minima = [x[0] for x in key_points if x[1] == False]
        new_minima_heights = [heights[i] for i in new_minima]

        plt.scatter(frames, heights, label='Heights')
        plt.scatter(new_peaks, new_peak_heights, label='Peaks')
        plt.scatter(new_minima, new_minima_heights, label='Minima')
        plt.legend()
        plt.show()

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

    def get_peaks(self, frames, heights):
        peaks = find_peaks(heights, height=0.8)
        peak_heights = peaks[1]['peak_heights']
        peak_pos = frames[peaks[0]]

        return peak_pos, peak_heights