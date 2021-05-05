import cv2
import ffmpeg
from pathlib import Path

class FrameDecomposer():
    def __init__(self, video_file_location):
        self.frame_count = 0
        self.video_file_location = video_file_location
        self.rotate_code = None

        # Make a folder to store frames captured from the video
        path = str(Path().absolute()) + '/tmp_frames'
        Path(path).mkdir(exist_ok=True)

    def check_file_exists(self):
        path = str(Path().absolute()) + '/' + self.video_file_location
        file_loc = Path(path)
        return file_loc.is_file()

    def check_rotation(self):
        rotate_code = None
        probe = ffmpeg.probe(self.video_file_location)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        rotate = int(video_stream.get('tags', [dict(tags=dict())]).get('rotate', 0))
        
        rotate_code = None
        if (rotate == 90):
            self.rotate_code = cv2.ROTATE_90_CLOCKWISE
        elif (rotate == 180):
            self.rotate_code = cv2.ROTATE_180
        elif (rotate == 270):
            self.rotate_code = cv2.ROTATE_90_COUNTERCLOCKWISE

        return 

    def decompose_video(self):
        # Check that the file actually exists
        if(self.check_file_exists()):
            # Create a VideoCapture object for the given video
            video_capture_obj = cv2.VideoCapture(self.video_file_location)
            print("VIDEO LOADED SUCCESSFULLY")
        else:
            print("File does not exist or cannot be found")
            return 
        
        self.check_rotation()

        success, frame = video_capture_obj.read()
        count = 0
        while success:
            if self.rotate_code is not None:
                frame = cv2.rotate(frame, self.rotate_code)
            cv2.imwrite("tmp_frames/frame_%d.jpg" % count, frame)
            success, frame = video_capture_obj.read()
            count += 1

        self.frame_count = count
        return
