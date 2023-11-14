import os
from src.adv_text import *
from src.events import AssEvents
from src.read_ini import config
from src.ass_part import script_info, garbage, style, event


ASS_PATH = config.get("File PATH", "ASS_PATH")

# only convert from game file without time-fix by frame
def generate_ass(filename: str):
    content = script_info + "\n" + garbage + "\n" + style + "\n" + event
    for dial in extract(filename):
        dial_event = AssEvents()
        dial_event.from_dialogue(dial)
        content = content + f"{dial_event.echo_dialogue()}" + "\n" + f"{dial_event.echo_comment()}" + "\n"
    try:
        with open(f"{ASS_PATH}/{get_title(filename)}.ass", "w", encoding="utf8") as fp:
            fp.write(content)
        print(f"{filename} has been successfully converted to {get_title(filename)}.ass")
    except Exception as e:
        print(f"{filename} convert failed. Info: {e}")
        return


if __name__ == "__main__":
    for filepath,dirnames,filenames in os.walk(ASS_PATH):
        for filename in filenames:
            if filename.endswith(".txt"):
                generate_ass(filename)
