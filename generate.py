from adv_text import *
from config import ASS_PATH
from config import game_file_name
from events import ass_events
from ass_part import script_info, garbage, style, event


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
    except:
        print(f"{input} convert failed")
        return
    
if __name__ == "__main__":
    generate_ass(game_file_name)