import cv2
import os
import sys
import configparser
import threading
import numpy as np
from src.match import to_binary
from concurrent.futures import ThreadPoolExecutor

BASE_PATH = os.path.abspath(os.path.dirname(__file__)+os.path.sep+"..")
config = configparser.ConfigParser()
config.read(os.path.join(BASE_PATH ,'config.ini'), encoding="utf-8")
CACHE_PATH = config.get("File PATH", "CACHE_PATH")
VIDEO_PATH = config.get("File PATH", "VIDEO_PATH")

lock = threading.Lock()
_current_count = 0

class frame_time(object):
    fps: float

    def one_task(self, _image_folder_path: str, frame: any, milliseconds: float, total_fps: int):
        global _current_count
        seconds = '%.4f' %(milliseconds // 1000 + (milliseconds % 1000) / 1000)
        name = seconds[:-1].replace(".", "_")
        height = len(frame)
        width = len(frame[0])
        img = frame[(height * 19 // 27):height, 0:width]
        _image_path = f"{_image_folder_path}/{name}.png" 
        binary = to_binary(img)
        kernel = np.ones((3, 3), np.uint8)
        binary_erosion = cv2.erode(binary, kernel, iterations=1)
        binary_erosion_edge = cv2.Canny(binary_erosion, 150, 200)
        binary_erosion_edge_dilate = cv2.dilate(binary_erosion_edge, kernel, iterations=3)
        binary_with_mask = cv2.bitwise_and(binary, binary, mask = binary_erosion_edge_dilate)
        cv2.imwrite(_image_path, binary_with_mask)
        lock.acquire()
        _current_count += 1
        percent = round(_current_count / total_fps * 100)
        print(f"\rPre-Progress:({_current_count}/{total_fps})"+"{}%: ".format(percent), "▓" * (percent // 2), end="")
        sys.stdout.flush()
        lock.release()
        
    def to_frame(self, input: str):
        _image_folder_path = f"{CACHE_PATH}/{input.split('.')[0]}"
        os.makedirs(_image_folder_path, exist_ok=True)
        video_path = f"{VIDEO_PATH}/{input}"
        vc = cv2.VideoCapture(video_path)
        self.fps = vc.get(cv2.CAP_PROP_FPS)
        total_fps = vc.get(cv2.CAP_PROP_FRAME_COUNT)    
        executor = ThreadPoolExecutor(max_workers = 20)
        while vc.isOpened():
            status, frame = vc.read()
            if not status:
                break
            milliseconds = vc.get(cv2.CAP_PROP_POS_MSEC) 
            executor.submit(self.one_task, _image_folder_path, frame, milliseconds, total_fps)
        vc.release()

    def get_fps(self, input: str):
        video_path = f"{VIDEO_PATH}/{input}"
        vc = cv2.VideoCapture(video_path)
        self.fps = vc.get(cv2.CAP_PROP_FPS)