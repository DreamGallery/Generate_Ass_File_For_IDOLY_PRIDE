from src.adv_text import *


class ass_events(object):

    def __init__(self, layer: int = 0, start: str = "", end: str = "", duration: float = 0, style: str = "", name: str = "", marginL: int = 0, marginR: int = 0, marginV: int = 0, effect: str = "", text: str = "", narration: bool = False):
        self.layer = layer
        self.start = start
        self.end = end
        self.duration = duration
        self.style = style
        self.name = name
        self.marginL = marginL
        self.marginR = marginR
        self.marginV = marginV
        self.effect = effect
        self.text = text
        self.narration = narration
    
    def from_dialogue(self, input: str):
        self.start = to_time(get_clip(input)["_startTime"])
        self.duration = get_clip(input)["_duration"]
        self.end = end_time(get_clip(input)["_startTime"], get_clip(input)["_duration"])
        if get_text(input)[1]:
            self.style = "对帧字幕灰色"
        else:
            self.style = "对帧字幕"
        if KEY_NARRATION in input:
            self.name = ""
            self.narration = True
        else: 
            if get_name(input) == "{user}":
                self.name = "マネージャー"
            else:
                self.name = get_name(input)
        self.text = get_text(input)[0]

    def echo_dialogue(self) -> str:
        dialogue = 'Dialogue: %d,%s,%s,%s,%s,%d,%d,%d,%s,%s' %(self.layer, self.start, self.end, self.style, self.name, self.marginL, self.marginR, self.marginV, self.effect, "")
        return dialogue
    
    def echo_comment(self) -> str:
        comment = 'Comment: %d,%s,%s,%s,%s,%d,%d,%d,%s,%s' %(self.layer, self.start, self.end, self.style, self.name, self.marginL, self.marginR, self.marginV, self.effect, self.text.replace("{user}", "マネージャー"))
        return comment
    
    @classmethod
    def echo_format(self) -> str:
        _format = "Format:"
        for attribute in self.__init__.__code__.co_varnames[1:]:
            _format = _format + f" {attribute},"
        _format = _format[:-2]
        return _format


# def to_ass_dial(input: str) -> str:
#     ass_events_1 = ass_events()
#     ass_events_1.from_dialogue(input)
#     dialogue = ass_events_1.echo_dialogue()
#     return dialogue


# def to_ass_comm(input: str) -> str:
#     ass_events_1 = ass_events()
#     ass_events_1.from_dialogue(input)
#     comment = ass_events_1.echo_comment()
#     return comment