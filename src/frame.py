import cv2
import os
import sys
import configparser


config = configparser.ConfigParser()
config.read("../config.ini", encoding="utf-8")
CACHE_PATH = config.get("File PATH", "CACHE_PATH")
VIDEO_PATH = config.get("File PATH", "VIDEO_PATH")


def to_binary(img: any) ->any:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    return binary


class frame_time(object):
    per_0_1 = []
    rate = 1
    def __to_per_0_1(self, rate:float):
        #for aegisub frame usually be 30/60
        #[0.000, 0.033, 0.066] for 30
        #[0.000, 0.016. 0.033, 0.050, 0.066, 0.083] for 60
        if rate == 30.0:
            self.per_0_1 = [0.000, 0.033, 0.066]
        elif rate == 60.0:
            self.per_0_1 = [0.000, 0.016, 0.033, 0.050, 0.066, 0.083]
        else:
            print("fps provide is not 30 or 60.")
            return
        self.rate = int(rate)
    
    def rename(self, frames: int) ->str:
        time = frames // self.rate + (frames % (self.rate) // (self.rate // 10)) / 10 + self.per_0_1[frames % (self.rate // 10)]
        name = f"{'%.3f' %(time)}".replace(".", "_")
        return name
        
    def to_frame(self, input: str):
        _image_folder_path = f"../{CACHE_PATH}/{input.split('.')[0]}"
        os.makedirs(_image_folder_path, exist_ok=True)
        video_path = f"../{VIDEO_PATH}/{input}"
        vc = cv2.VideoCapture(video_path)
        fps = vc.get(cv2.CAP_PROP_FPS)
        total_fps = vc.get(cv2.CAP_PROP_FRAME_COUNT)
        self.__to_per_0_1(fps)     
        count = 0
        while vc.isOpened():
            status, frame = vc.read()
            if not status:
                break
            height = len(frame)
            width = len(frame[0])
            img = frame[(height*2//3):height, 0:width]
            _image_path = f"{_image_folder_path}/{self.rename(count)}.png" 
            binary = to_binary(img)
            cv2.imwrite(_image_path, binary)
            count = count + 1
            percent = round(count / total_fps * 100)
            print(f"\rPre-Progress:({count}/{total_fps})"+"{}%: ".format(percent), "▓" * (percent // 2), end="")
            sys.stdout.flush()
        vc.release()

