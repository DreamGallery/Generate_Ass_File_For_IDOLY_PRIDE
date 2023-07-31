import os, sys
import configparser
from src.adv_text import *
from src.events import ass_events
from src.ass_part import script_info, garbage, style, event
from src.time_fix import *
from src.frame import *


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR ,'config.ini'), encoding="utf-8")
ASS_PATH = config.get("File PATH", "ASS_PATH")
TXT_PATH = config.get("File PATH", "TXT_PATH")
game_file_name = config.get("Info", "game_file_name")
video_file_name = config.get("Info", "video_file_name")

stream = frame_time()
stream.to_frame(video_file_name)

list = extract(game_file_name)
count = 0
start_file_index = 0
content = script_info + "\n" + garbage + "\n" + style + "\n" + event
for dial in list:
    _event = ass_events()
    _event.from_dialogue(dial)
    next_file_index = time_fix(_event, start_file_index, video_file_name.split(".")[0], stream)
    start_file_index = next_file_index
    content = content + f"{_event.echo_dialogue()}" + "\n" + f"{_event.echo_comment()}" + "\n"
    count = count + 1
    percent = round(count / len(list) * 100)
    print(f"\rASS-Generate-Progress:({count}/{len(list)})"+"{}%: ".format(percent), "▓" * (percent // 2), end="")
    sys.stdout.flush()

try:
    title = get_title(f"{game_file_name}")
    with open(f"{ASS_PATH}/{title}.ass", "w", encoding="utf8") as fp:
        fp.write(content)
    print(f"\n{game_file_name} has been successfully converted to {title}.ass")
except:
    print(f"\n{title} convert failed")