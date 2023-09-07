from src.adv_text import *
from src.read_ini import config

_KEY_NARRATION = config.get("Text KEY", "KEY_NARRATION")


class AssEvents(object):
    def __init__(
        self,
        Layer: int = 0,
        Start: str = "",
        End: str = "",
        Duration: float = 0,
        Style: str = "",
        Name: str = "",
        MarginL: int = 0,
        MarginR: int = 0,
        MarginV: int = 0,
        Effect: str = "",
        Text: str = "",
    ):
        self.Layer = Layer
        self.Start = Start
        self.End = End
        self.Duration = Duration
        self.Style = Style
        self.Name = Name
        self.MarginL = MarginL
        self.MarginR = MarginR
        self.MarginV = MarginV
        self.Effect = Effect
        self.Text = Text

    def from_dialogue(self, input: str):
        self.Start = to_time(get_clip(input)["_startTime"])
        self.Duration = get_clip(input)["_duration"]
        self.End = end_time(get_clip(input)["_startTime"], get_clip(input)["_duration"])
        if get_text(input)[1]:
            self.Style = "IdolyPride Gray"
        else:
            self.Style = "IdolyPride Normal"
        if _KEY_NARRATION in input:
            self.Name = ""
        else:
            if get_name(input) == "{user}":
                self.Name = "マネージャー"
            else:
                self.Name = get_name(input)
        self.Text = get_text(input)[0]

    def echo_dialogue(self) -> str:
        dialogue = "Dialogue: %d,%s,%s,%s,%s,%d,%d,%d,%s,%s" % (
            self.Layer,
            self.Start,
            self.End,
            self.Style,
            self.Name,
            self.MarginL,
            self.MarginR,
            self.MarginV,
            self.Effect,
            "",
        )
        return dialogue

    def echo_comment(self) -> str:
        comment = "Comment: %d,%s,%s,%s,%s,%d,%d,%d,%s,%s" % (
            self.Layer,
            self.Start,
            self.End,
            self.Style,
            self.Name,
            self.MarginL,
            self.MarginR,
            self.MarginV,
            self.Effect,
            self.Text.replace("{user}", "マネージャー"),
        )
        return comment

    @classmethod
    def echo_format(cls) -> str:
        format = "Format:"
        for attribute in cls.__init__.__code__.co_varnames[1:]:
            if attribute == "Duration":
                continue
            format = format + f"\u0020{attribute},"
        format = format[:-1]
        return format


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
