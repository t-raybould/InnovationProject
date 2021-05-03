import cv2
import sys
import argparse
import ffmpeg
from pathlib import Path
import matplotlib.pyplot as plt

BODY_PARTS = {"Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
              "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
              "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
              "LEye": 15, "REar": 16, "LEar": 17, "Background": 18}

POSE_PAIRS = [["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
              ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
              ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
              ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
              ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"]]

def check_file_exists(file):
    path = str(Path().absolute()) + '/' + file
    file_loc = Path(path)
    return file_loc.is_file()

def check_rotation(video_file_location):
    rotate_code = None
    probe = ffmpeg.probe(video_file_location)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    rotate = int(video_stream.get('side_data_list', [dict(tags=dict())])[0].get('rotation', 0))

    # TODO 

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
    net = cv2.dnn.readNetFromTensorflow('model.pb')

    for current_frame in range(0, 1):
        path = str(Path().absolute()) + '/tmp_frames/frame_' + str(current_frame) + '.jpg'
        frame = cv2.imread(path)
        frame = get_pose_estimation(net, frame)
        plt.imshow(frame)
        plt.show()

def get_pose_estimation(net, frame):
    thr = 0.4
    frame_width = frame.shape[1]
    frame_height = frame.shape[0]

    blob = cv2.dnn.blobFromImage(frame, 1.0, (368, 368), (127.5, 127.5, 127.5), swapRB=True, crop=False)
    net.setInput(blob)
    out = net.forward()

    points = []

    for i in range(len(BODY_PARTS)):
        heatmap = out[0, i, :, :]
        _, conf, _, point = cv2.minMaxLoc(heatmap)

        x = (frame_width * point[0]) / out.shape[3]
        y = (frame_height * point[1]) / out.shape[2]
        points.append((int(x), int(y)) if conf > thr else None)

    for pair in POSE_PAIRS:
        part_from = pair[0]
        part_to = pair[1]
        assert(part_from in BODY_PARTS)
        assert(part_to in BODY_PARTS)

        id_from = BODY_PARTS[part_from]
        id_to = BODY_PARTS[part_to]

        if points[id_from] and points[id_to]:
            cv2.line(frame, points[id_from], points[id_to], (0, 255, 0), 3)
            cv2.ellipse(frame, points[id_from], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)
            cv2.ellipse(frame, points[id_to], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)

    t, _ = net.getPerfProfile()
    freq = cv2.getTickFrequency() / 1000
    cv2.putText(frame, '%.2fms' % (t/freq), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    return frame

if __name__ == '__main__':
    # Create ArgumentParser and define arguments to the system
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='Path to video')
    args = parser.parse_args() 

    video_file_location=args.input

    frame_count = decompose_video(video_file_location) 
    process_frames(frame_count)