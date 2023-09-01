# Generate_Ass_File_For_IDOLY_PRIDE
Auto generate subtitle file of aegisub for IDOLY PRIDE through game file.

Also Using `OPENCV2` to fix timeline of subtitle frame by frame.

This tool is based on `MalitsPlus/HoshimiToolkit`, you need to get the subtitle file in game through `HoshimiToolkit`,<br /> the name of required file will usually be `adv_***.txt`.


# Usage

## Install from the repository
```
git clone https://github.com/DreamGallery/Generate_Ass_File_For_IDOLY_PRIDE.git
cd Generate_Ass_File_For_IDOLY_PRIDE
```

## Install requirement
```
pip3 install -r requirements.txt
```

edit `[Info]` in `config.ini` first, put game subtitle file in `ass/txt`, and the `.ass` file will be saved in `adv/ass`.

## Generate .ass file without time-fix

```
python generate.py
```

to use the time-fix options you should put your video file in `ass/video`, and the recommended resolution is `[1920x1080]` or you can change the `[Font Config]` youself in `config.ini` to fit your video.

## Generate .ass file with time-fix
```
python main.py
```
How to adjust the appropriate threshold is very helpful to the runtime of this tool.<br />Maybe sometimes you need to add some distractors to game file.<br />If you want to change the threshold value after finished the Pre-Progress, you can change the value of `match_only` to `True` under section `Arg` 

## Merge game subtitle
If you need to merge two subtitle files, just fill the `Merge` section in `config.ini`, and run with
```
python tools/merge.py
```

## ※About Fonts
IDOLY PRIDE use SDF to render subtitle in story, the original fonts of `japanese(UDKakugo)`, `letters(DM Sans)` and `digit(Roboto)` are all different, the fonts in `font` folder are only possible fonts. 
<br />If you need another weight of these two fonts, you can get them through the link below
```
https://github.com/googlefonts/roboto #Roboto
https://github.com/googlefonts/dm-fonts #DeepMindSans(v1.002)
```
In addition, please note that some fonts require authorization for commercial use.