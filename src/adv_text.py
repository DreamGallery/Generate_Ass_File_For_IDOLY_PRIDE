import json
from src.read_ini import config


TXT_PATH = config.get("File PATH", "TXT_PATH")
player_name = config.get("Info", "player_name")
KEY_MASSAGE = config.get("Text KEY", "KEY_MASSAGE")
KEY_CLIP = config.get("Text KEY", "KEY_CLIP")
KEY_NAME = config.get("Text KEY", "KEY_NAME")
KEY_NARRATION = config.get("Text KEY", "KEY_NARRATION")
KEY_THUMBNIAL = config.get("Text KEY", "KEY_THUMBNIAL")
KEY_TITLE = config.get("Text KEY", "KEY_TITLE")


def extract(input: str) -> list:
    dial_list = []
    with open(f"{TXT_PATH}/{input}", 'r', encoding="utf8") as f:
        for line in f:
            if "text" in line:
                dial_list.append(line)
    return dial_list


def get_title(input: str) -> str:
    with open(f"{TXT_PATH}/{input}", 'r', encoding="utf8") as f:
        for line in f:
            if "title" in line:
                title = line[1:-2].split(KEY_TITLE)[1].replace(" ", "_")
                break
    return title


def get_text(input: str) -> [str, bool]:
    if KEY_MASSAGE in input:
        text = input[1:-2].split(KEY_MASSAGE)[1].split(f"\u0020{KEY_NAME}")[0].replace("{user}", player_name)
        if "\uff08" in text or "\uff09" in text:
            text = text.replace("\uff08", "").replace("\uff09", "")
            gray = True
        else:
            gray = False
    elif KEY_NARRATION in input:
        text = input[1:-2].split(KEY_NARRATION)[1].split(f"\u0020{KEY_CLIP}")[0]
        gray = True
    return text, gray


def get_name(input: str) -> str:
    if KEY_THUMBNIAL in input:
        name = input[1:-2].split(f"\u0020{KEY_NAME}")[1].split(f"\u0020{KEY_THUMBNIAL}")[0]
    else:
        name = input[1:-2].split(f"\u0020{KEY_NAME}")[1].split(f"\u0020{KEY_CLIP}")[0]
    return name


def get_clip(input: str) -> any:
    clip = input[1:-2].split(f"\u0020{KEY_CLIP}")[1].replace("\\", "")
    data = json.loads(clip)
    return data


def to_time(clip_time: float) -> str:
    H = clip_time // 3600
    M = (clip_time - H * 3600)//60
    S = clip_time - H * 3600 - M * 60
    _time = '%d:%02d:%05.2f' %(H,M,S)
    return _time


def end_time(_startTime: float, _duration: float) -> str:
    _end = _startTime + _duration
    _endTime = to_time(_end)
    return _endTime

