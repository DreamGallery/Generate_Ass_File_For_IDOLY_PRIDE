from src.adv_text import *
from src.events import ass_events
from src.read_ini import config
from src.ass_part import script_info, garbage, style, event


ASS_PATH = config.get("File PATH", "ASS_PATH")
game_file_name = config.get("Info", "game_file_name")


#only convert from game file without time-fix by frame
def generate_ass(input: str):
    content = script_info + "\n" + garbage + "\n" + style + "\n" + event
    for dial in extract(input):
        _event = ass_events()
        _event.from_dialogue(dial)
        content = content + f"{_event.echo_dialogue()}" + "\n" + f"{_event.echo_comment()}" + "\n"
    try:
        with open(f"{ASS_PATH}/{get_title(input)}.ass", "w", encoding="utf8") as fp:
            fp.write(content)
        print(f"{input} has been successfully converted to {get_title(input)}.ass")
    except Exception as e:
        print(f"{input} convert failed. Info: {e}")
        return
    
if __name__ == "__main__":
    generate_ass(game_file_name)
