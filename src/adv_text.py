import json
from src.read_ini import config


_TXT_PATH = config.get("File PATH", "TXT_PATH")
_player_name = config.get("Info", "player_name")
_KEY_MASSAGE = config.get("Text KEY", "KEY_MASSAGE")
_KEY_CLIP = config.get("Text KEY", "KEY_CLIP")
_KEY_NAME = config.get("Text KEY", "KEY_NAME")
_KEY_NARRATION = config.get("Text KEY", "KEY_NARRATION")
_KEY_THUMBNIAL = config.get("Text KEY", "KEY_THUMBNIAL")
_KEY_TITLE = config.get("Text KEY", "KEY_TITLE")


def extract(filename: str) -> list[str]:
    dial_list: list[str] = []
    with open(f"{_TXT_PATH}/{filename}", "r", encoding="utf8") as f:
        for line in f:
            if "text" in line:
                dial_list.append(line)
    return dial_list


def get_title(filename: str) -> str:
    with open(f"{_TXT_PATH}/{filename}", "r", encoding="utf8") as f:
        for line in f:
            if "title" in line:
                title = line[1:-2].split(_KEY_TITLE)[1].replace(" ", "_")
                break
    return title


def get_text(content: str) -> tuple[str, bool]:
    if _KEY_MASSAGE in content:
        text = (
            content[1:-2]
            .split(_KEY_MASSAGE)[1]
            .split(f"\u0020{_KEY_NAME}")[0]
            .replace("{user}", _player_name)
        )
        if "\uff08" in text or "\uff09" in text:
            text = text.replace("\uff08", "").replace("\uff09", "")
            gray = True
        else:
            gray = False
    elif _KEY_NARRATION in content:
        text = content[1:-2].split(_KEY_NARRATION)[1].split(f"\u0020{_KEY_CLIP}")[0]
        gray = True
    return (text, gray)


def get_name(content: str) -> str:
    if _KEY_THUMBNIAL in content:
        name = content[1:-2].split(f"\u0020{_KEY_NAME}")[1].split(f"\u0020{_KEY_THUMBNIAL}")[0]
    else:
        name = content[1:-2].split(f"\u0020{_KEY_NAME}")[1].split(f"\u0020{_KEY_CLIP}")[0]
    return name


def get_clip(content: str):
    clip = content[1:-2].split(f"\u0020{_KEY_CLIP}")[1].replace("\\", "")
    data = json.loads(clip)
    return data


def to_time(clip_time: float) -> str:
    H = clip_time // 3600
    M = (clip_time - H * 3600) // 60
    S = clip_time - H * 3600 - M * 60
    format_time = "%d:%02d:%05.2f" % (H, M, S)
    return format_time


def end_time(startTime: float, duration: float) -> str:
    end_ = startTime + duration
    endTime = to_time(end_)
    return endTime
