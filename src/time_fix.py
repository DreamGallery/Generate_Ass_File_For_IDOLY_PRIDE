import sys
import json
from src.read_ini import config
from src.frame import FrameProcess
from src.events import AssEvents
from src.adv_text import to_time
from src.match import draw_text, compare


_FONT_PATH = json.loads(config.get("File Path", "FONT_PATH"))
_CACHE_PATH = config.get("File Path", "CACHE_PATH")
_font_size = json.loads(config.get("Font Config", "font_size"))
_stroke_width = config.getint("Font Config", "stroke_width")
_kerning = config.getint("Font Config", "kerning")
_threshold = config.getfloat("Arg", "threshold")


def time_fix(
    event: AssEvents,
    files: list[str],
    start_file_index: int,
    target: str,
    stream: FrameProcess,
) -> int:
    text = event.Text
    binary, mask = draw_text(text, _FONT_PATH, _font_size, _stroke_width, _kerning)
    for file in files[start_file_index:]:
        if compare(f"{_CACHE_PATH}/{target}/{file}", binary, _threshold, mask=mask):
            start_time = float(file.split(".")[0].replace("_", ".")[:-1])
            event.Start = to_time(start_time)
            break
        else:
            start_file_index = start_file_index + 1

    if start_file_index >= len(files):
        print("can't find subtitle text in target files, please check or adjust parameter")
        sys.exit(1)

    index_plus = int(event.Duration * stream.fps - 2)
    start_file_index = start_file_index + index_plus

    try:
        for file in files[start_file_index:]:
            if compare(f"{_CACHE_PATH}/{target}/{file}", binary, _threshold, mask=mask):
                start_file_index = start_file_index + 1
            else:
                end_time = float(file.split(".")[0].replace("_", ".")[:-1])
                event.End = to_time(end_time)
                break
    except IndexError:
        print(
            IndexError,
            "\nfile start index plus index convert by time duration exceeds the number of all files",
        )
        sys.exit(1)

    end_file_index = start_file_index
    return end_file_index
