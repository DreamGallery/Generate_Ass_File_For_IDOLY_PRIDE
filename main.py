import os
from src.adv_text import *
from src.read_ini import config
from src.time_fix import time_fix
from src.events import AssEvents
from src.frame import FrameProcess
from src.ass_part import script_info, garbage, style, event


ASS_PATH = config.get("File PATH", "ASS_PATH")
TXT_PATH = config.get("File PATH", "TXT_PATH")
CACHE_PATH = config.get("File PATH", "CACHE_PATH")
game_file_name = config.get("Info", "game_file_name")
video_file_name = config.get("Info", "video_file_name")
match_only = config.getboolean("Arg", "match_only")
need_comment = config.getboolean("Arg", "need_comment")
MV_exists = config.getboolean("Sub", "MV_exists")

stream = FrameProcess()
if match_only:
    stream.get_fps(video_file_name)
else:
    stream.to_frame(video_file_name)

dial_list = extract(game_file_name)
if MV_exists:
    sub_file_name = config.get("Sub", "sub_file_name")
    print(
        "You have set the Key of MV_exists, please input the length of MV in the video, or you can keep"
        + "\n"
        + "it empty and let the program automatically traverse the whole MV, but this will take more time."
    )
    MV_length = input("MV length[Default: 150, unit (s)]: ")
    if MV_length == "":
        MV_length = str(150)
    dial_list.append(f"SkipTime:{MV_length}")
    for dial in extract(sub_file_name):
        dial_list.append(dial)

files: list[str] = []
current_count = int(0)
start_file_index = int(0)
content = script_info + "\n" + garbage + "\n" + style + "\n" + event
print("ASS-Generate-Progress start")

target = video_file_name.split(".")[0]
for root, dirs, files in os.walk(f"{CACHE_PATH}/{target}"):
    files.sort(key=lambda x: float(x.replace("_", ".").split(".png")[0]))

for dial in dial_list:
    if "SkipTime" in dial:
        start_file_index = start_file_index + int(float(dial.split(":")[1]) * stream.fps)
        continue
    dial_event = AssEvents()
    dial_event.from_dialogue(dial)
    next_file_index = time_fix(dial_event, files, start_file_index, target, stream)
    start_file_index = next_file_index
    if need_comment:
        content = content + f"{dial_event.echo_dialogue()}" + "\n" + f"{dial_event.echo_comment()}" + "\n"
    else:
        content = (
            content + f"{dial_event.echo_dialogue()}" + dial_event.Text.replace("{user}", "マネージャー") + "\n"
        )
    current_count = current_count + 1
    percent = round(current_count / len(dial_list) * 100)
    print(
        f"ASS-Generate-Progress:({'{:0>3d}'.format(current_count)}/{'{:0>3d}'.format(len(dial_list))})"
        + "{:>3d}%: ".format(percent),
        "▮" * (percent // 2),
        end="",
    )
    print("\u0020", dial_event.Text, dial_event.Start, dial_event.End)

try:
    title = get_title(f"{game_file_name}")
    with open(f"{ASS_PATH}/{title}.ass", "w", encoding="utf8") as fp:
        fp.write(content)
    print(f"{game_file_name} has been successfully converted to {title}.ass")
except Exception as e:
    print(f"\n{title} convert failed. Info: {e}")
