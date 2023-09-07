from src.styles import *
from src.events import AssEvents


script_info = "\
[Script Info]\n\
; Script generated by Aegisub 3.2.2\n\
; http://www.aegisub.org/\n\
Title: IDOLY PRIDE STORY\n\
ScriptType: v4.00+\n\
WrapStyle: 0\n\
YCbCr Matrix: TV.601\n\
PlayResX: 1920\n\
PlayResY: 1080\n\
"

garbage = "\
[Aegisub Project Garbage]\n\
Last Style Storage: Default\n\
Audio File: \n\
Video File: \n\
Video AR Mode: \n\
Video AR Value: \n\
Video Zoom Percent: \n\
Scroll Position: \n\
Active Line: \n\
Video Position: \n\
"

style = f"\
[V4+ Styles]\n\
{AssStyles.echo_format()}\n\
{style_1.echo()}\n\
{style_2.echo()}\n\
"

event = f"\
[Events]\n\
{AssEvents.echo_format()}\n\
"
