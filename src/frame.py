import cv2
import os
import sys
import threading
import numpy as np
from src.match import to_binary
from src.read_ini import config
from concurrent.futures import ThreadPoolExecutor


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
        img = frame[(height * 29 // 36):(height * 8 // 9), (width * 1 // 16):(width * 15 // 16)]
        _image_path = f"{_image_folder_path}/{name}.png"
        binary = to_binary(img, 127)
        kernel = np.ones((3,3), np.uint8)
        binary_opn = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        cv2.imwrite(_image_path, binary_opn)
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