import cv2
import os
import configparser
import numpy as np
from src.match import *
from src.frame import *
from src.events import ass_events
from src.adv_text import to_time


BASE_PATH = os.path.abspath(os.path.dirname(__file__)+os.path.sep+"..")
config = configparser.ConfigParser()
config.read(os.path.join(BASE_PATH ,'config.ini'), encoding="utf-8")
FONT_PATH = config.get("File PATH", "FONT_PATH")
CACHE_PATH = config.get("File PATH", "CACHE_PATH")
fontsize = config.getint("Font Config", "fontsize")
strokewidth = config.getint("Font Config", "strokewidth")
kerning = config.getint("Font Config", "kerning")
threshold = config.getfloat("Font Config", "threshold")


def time_fix(event: ass_events, start_file_index: int, target: str, stream: frame_time) ->int:
    text = event.text
    if event.narration:
        fillcolor = (0,0,0)
    else:
        fillcolor = (255,255,255)
    img = np.asarray(draw_text(text, FONT_PATH, fontsize, strokewidth, kerning, fillcolor))
    binary = to_binary(img)
    for root, dirs, files in os.walk(f"{CACHE_PATH}/{target}"):
        files.sort(key=lambda x:float(x.replace("_", ".").split('.png')[0]))
        for file in files[start_file_index:]:
            if compare(f"{CACHE_PATH}/{target}/{file}", binary, threshold):
                start_time = float(file.split(".")[0].replace("_", ".")[:-1])
                event.start = to_time(start_time)
                break
            else:
                start_file_index = start_file_index + 1

        if start_file_index > len(files):
            print("can't find subtitle text in target files, please check or adjust parameter")
            return
        
        index_plus = int (event.duration / (1 / stream.fps) - 1)
        start_file_index = start_file_index + index_plus

        try:
            for file in files[start_file_index:]:
                if compare(f"{CACHE_PATH}/{target}/{file}", binary, threshold):
                    start_file_index = start_file_index + 1
                else:
                    if float(file.split(".")[0].replace("_", ".")[:-1]) == float(file.split(".")[0].replace("_", ".")):
                        end_time = float(file.split(".")[0].replace("_", ".")[:-1])
                    else:
                        end_time = float(file.split(".")[0].replace("_", ".")[:-1]) + 0.01
                    event.end = to_time(end_time)
                    break
        except(IndexError):
            print(IndexError,"\nfile start index plus index convert by time duration exceeds the number of all files")
            return
        
        end_file_index = start_file_index
        break
    return end_file_index