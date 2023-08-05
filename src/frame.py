import cv2
import os
import sys
import configparser

BASE_PATH = os.path.abspath(os.path.dirname(__file__)+os.path.sep+"..")
config = configparser.ConfigParser()
config.read(os.path.join(BASE_PATH ,'config.ini'), encoding="utf-8")
CACHE_PATH = config.get("File PATH", "CACHE_PATH")
VIDEO_PATH = config.get("File PATH", "VIDEO_PATH")


def to_binary(img: any) ->any:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    return binary


class frame_time(object):
    fps: float
        
    def to_frame(self, input: str):
        _image_folder_path = f"{CACHE_PATH}/{input.split('.')[0]}"
        os.makedirs(_image_folder_path, exist_ok=True)
        video_path = f"{VIDEO_PATH}/{input}"
        vc = cv2.VideoCapture(video_path)
        self.fps = vc.get(cv2.CAP_PROP_FPS)
        total_frame = vc.get(cv2.CAP_PROP_FRAME_COUNT)    
        count = 0
        while vc.isOpened():
            status, frame = vc.read()
            if not status:
                break
            milliseconds = vc.get(cv2.CAP_PROP_POS_MSEC) 
            seconds = '%.4f' %(milliseconds // 1000 + (milliseconds % 1000) / 1000)
            name = ('%.3f' %(int(float(seconds) * 1000) / 1000)).replace(".", "_")
            height = len(frame)
            width = len(frame[0])
            img = frame[(height*2//3):height, 0:width]
            _image_path = f"{_image_folder_path}/{name}.png" 
            binary = to_binary(img)
            cv2.imwrite(_image_path, binary)
            count = count + 1
            percent = round(count / total_frame * 100)
            print(f"\rPre-Progress:({count}/{total_frame})"+"{}%: ".format(percent), "▓" * (percent // 2), end="")
            sys.stdout.flush()
        vc.release()

