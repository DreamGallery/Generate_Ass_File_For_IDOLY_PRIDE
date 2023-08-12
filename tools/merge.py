import os
import configparser

BASE_PATH = os.path.abspath(os.path.dirname(__file__)+os.path.sep+"..")
config = configparser.ConfigParser()
config.read(os.path.join(BASE_PATH ,'config.ini'), encoding="utf-8")
TXT_PATH = config.get("File PATH", "TXT_PATH")
main_file_name = config.get("Merge", "main_file_name")
sub_file_name = config.get("Merge", "sub_file_name")
merge_file_name = config.get("Merge", "merge_file_name")
mv_length = config.getfloat("Merge", "mv_length")

with open(f"{TXT_PATH}/{merge_file_name}", 'x', encoding="utf8") as f:
    with open(f"{TXT_PATH}/{main_file_name}", 'r', encoding="utf8") as wf:
        for line in wf:
            if "title" in line or "text" in line:
                f.write(line)
    f.write(f"[mark text=SkipTime:{mv_length}]\n")
    with open(f"{TXT_PATH}/{sub_file_name}", 'r', encoding="utf8") as sf:
        for line in sf:
            if "text" in line:
                f.write(line)
