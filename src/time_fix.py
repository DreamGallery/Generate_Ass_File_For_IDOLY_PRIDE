import sys
import json
from src.match import *
from src.frame import *
from src.events import ass_events
from src.adv_text import to_time
from src.read_ini import config


FONT_PATH = json.loads(config.get("File PATH", "FONT_PATH"))
CACHE_PATH = config.get("File PATH", "CACHE_PATH")
fontsize = json.loads(config.get("Font Config", "fontsize"))
strokewidth = config.getint("Font Config", "strokewidth")
kerning = config.getint("Font Config", "kerning")
threshold = config.getfloat("Arg", "threshold")


def time_fix(event: ass_events, files:list[str], start_file_index: int, target: str, stream: frame_time) ->int:
    text = event.Text
    binary, mask = draw_text(text, FONT_PATH, fontsize, strokewidth, kerning)
    for file in files[start_file_index:]:
        if compare(f"{CACHE_PATH}/{target}/{file}", binary, threshold, mask = mask):
            start_time = float(file.split(".")[0].replace("_", ".")[:-1])
            event.Start = to_time(start_time)
            break
        else:
            start_file_index = start_file_index + 1

    if start_file_index > len(files):
        print("can't find subtitle text in target files, please check or adjust parameter")
        sys.exit(1)
    
    index_plus = int (event.Duration / (1 / stream.fps) - 2)
    start_file_index = start_file_index + index_plus

    try:
        for file in files[start_file_index:]:
            if compare(f"{CACHE_PATH}/{target}/{file}", binary, threshold, mask = mask):
                start_file_index = start_file_index + 1
            else:
                end_time = float(file.split(".")[0].replace("_", ".")[:-1])
                event.End = to_time(end_time)
                break
    except(IndexError):
        print(IndexError,"\nfile start index plus index convert by time duration exceeds the number of all files")
        sys.exit(1)
    
    end_file_index = start_file_index
    return end_file_index