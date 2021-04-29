import cv2
import sys
import argparse
import ffmpeg
from pathlib import Path

def check_file_exists(file):
    path = str(Path().absolute()) + '/' + file
    file_loc = Path(path)
    return file_loc.is_file()

def check_rotation(video_file_location):
    rotate_code = None
    meta_data = ffmpeg.probe(video_file_location)
    rotation = int(meta_data.get('streams', [dict(tags=dict())])[0].get('tags', dict()).get('rotate', 0))
            

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
    
    # rotate_code = check_rotation(video_file_location)

    success, frame = video_capture_obj.read()
    count = 0
    while success:
        cv2.imwrite("tmp_frames/frame_%d.jpg" % count, frame)
        success, frame = video_capture_obj.read()
        count += 1
    
    return count

if __name__ == '__main__':
    
    # Create ArgumentParser and define arguments to the system
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='Path to video')
    args = parser.parse_args() 

    video_file_location=args.input

    count = decompose_video(video_file_location) 