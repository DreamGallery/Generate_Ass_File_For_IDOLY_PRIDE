from src.adv_text import *
from src.read_ini import config
from src.events import ass_events
from src.ass_part import script_info, garbage, style, event
from src.time_fix import *
from src.frame import *


ASS_PATH = config.get("File PATH", "ASS_PATH")
TXT_PATH = config.get("File PATH", "TXT_PATH")
game_file_name = config.get("Info", "game_file_name")
video_file_name = config.get("Info", "video_file_name")
match_only = config.getboolean("Arg", "match_only")
need_comment = config.getboolean("Arg", "need_comment")

stream = frame_time()
if match_only:
    stream.get_fps(video_file_name)
else:
    stream.to_frame(video_file_name)

list = extract(game_file_name)
count = 0
files = []
start_file_index = 0
content = script_info + "\n" + garbage + "\n" + style + "\n" + event
print("ASS-Generate-Progress start")

target = video_file_name.split(".")[0]
for root, dirs, files in os.walk(f"{CACHE_PATH}/{target}"):
    files.sort(key=lambda x:float(x.replace("_", ".").split('.png')[0]))

for dial in list:
    if "SkipTime" in dial:
        start_file_index = start_file_index + int((float(str(dial).split(":")[1][:-1]) - 1) / (1 / stream.fps))
    _event = ass_events()
    _event.from_dialogue(dial)
    next_file_index = time_fix(_event, files, start_file_index, target, stream)
    start_file_index = next_file_index
    if need_comment:
        content = content + f"{_event.echo_dialogue()}" + "\n" + f"{_event.echo_comment()}" + "\n"
    else:
        content = content + f"{_event.echo_dialogue()}" + _event.Text.replace("{user}", "マネージャー") +"\n"
    count = count + 1
    percent = round(count / len(list) * 100)
    print(f"ASS-Generate-Progress:({count}/{len(list)})"+"{}%: ".format(percent), "\033[33m▓\033[0m" * (percent // 2), end="")
    print(start_file_index, _event.Text, _event.Start, _event.End)

try:
    title = get_title(f"{game_file_name}")
    with open(f"{ASS_PATH}/{title}.ass", "w", encoding = "utf8") as fp:
        fp.write(content)
    print(f"\n{game_file_name} has been successfully converted to {title}.ass")
except:
    print(f"\n{title} convert failed")