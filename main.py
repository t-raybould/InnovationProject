import cv2
import sys
import argparse
import ffmpeg
from pathlib import Path
import matplotlib.pyplot as plt

def check_file_exists(file):
    path = str(Path().absolute()) + '/' + file
    file_loc = Path(path)
    return file_loc.is_file()

def check_rotation(video_file_location):
    rotate_code = None
    probe = ffmpeg.probe(video_file_location)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    rotate = int(video_stream.get('side_data_list', [dict(tags=dict())])[0].get('rotation', 0))
    
    rotate_code = None
    if (rotate == 90) or (rotate == -270):
        rotate_code = cv2.ROTATE_90_CLOCKWISE
    elif (rotate == -180) or (rotate == 180):
        rotate_code = cv2.ROTATE_180

    return rotate_code

def decompose_video(video_file_location):
    # Make a folder to store frames captured from the video
    path = str(Path().absolute()) + '/tmp_frames'
    Path(path).mkdir(exist_ok=True)

    # Check that the file actually exists
    if(check_file_exists(video_file_location)):
        # Create a VideoCapture object for the given video
        video_capture_obj = cv2.VideoCapture(video_file_location)
        print("VIDEO LOADED SUCCESSFULLY")
    else:
        print("File does not exist or cannot be found")
        return
    
    rotate_code = check_rotation(video_file_location)

    success, frame = video_capture_obj.read()
    count = 0
    while success:
        if rotate_code is not None:
            frame = cv2.rotate(frame, rotate_code)
        cv2.imwrite("tmp_frames/frame_%d.jpg" % count, frame)
        success, frame = video_capture_obj.read()

        count += 1
    
    return count

def process_frames(frame_count):
    for current_frame in range(0, 1):
        path = str(Path().absolute()) + '/tmp_frames/frame_' + str(current_frame) + '.jpg'
        frame = cv2.imread(path)
        plt.imshow(frame)
        plt.show()
        get_pose_estimation(frame)


def get_pose_estimation(frame):
    frame_width = frame.shape[0]
    frame_height = frame.shape[1]

    print(frame_width, frame_height)

if __name__ == '__main__':
    
    # Create ArgumentParser and define arguments to the system
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='Path to video')
    args = parser.parse_args() 

    video_file_location=args.input

    frame_count = decompose_video(video_file_location) 
    process_frames(frame_count)