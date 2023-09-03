# Generate Ass File For IDOLY PRIDE
Auto generate subtitle file of aegisub(.ass) for IDOLY PRIDE through game files.

Also Using `OPENCV` to fix timeline of subtitle frame by frame.

※This tool is based on [MalitsPlus/HoshimiToolkit](https://github.com/MalitsPlus/HoshimiToolkit), you need to get subtitle files in the game and the names of required files are usually `adv_***.txt`.


# Usage

## Install from the repository
```
git clone https://github.com/DreamGallery/Sibyl-System-For-IDOLY-PRIDE.git Sibyl
cd Sibyl
```

## Install requirement
```
pip3 install -r requirements.txt
```

## Generate .ass file without time-fix
edit `[Info]` in `config.ini` first, put game subtitle file in `adv/txt`, and the `.ass` file will be saved in `adv/ass`.

```
python generate.py
```

## Generate .ass file with time-fix
to use the time-fix options you should put your video file in `adv/video`, and the recommended resolution is `[1920x1080]` or you can change the `[Font Config]` in `config.ini` to fit your video(compare in PS is a good idea).
```
python main.py
```
Adjust the appropriate threshold is very helpful to the runtime of this tool.<br />Maybe sometimes you need to increase the threshold instead of decreasing it.<br />If you want to change the threshold value after finished the Pre-Progress, you can change the value of `match_only` to `True` under section `Arg`. 

## Merge game subtitle
If you need to merge two subtitle files, just fill the `Merge` section in `config.ini`, and run with
```
python tools/merge.py
```

## ※About Fonts
IDOLY PRIDE use SDF to render subtitle in story, the original fonts of `japanese(UDKakugo)`, `letters` and `digit` are all different, the fonts in `font` folder are only possible fonts. 
<br />If you need another weight of these two fonts(`Roboto` for digit and `DM Sans` for letters), you can get them through the link below
```
https://github.com/googlefonts/roboto #Roboto
https://github.com/googlefonts/dm-fonts #DeepMindSans(v1.002)
```
In addition, please note that some fonts require authorization for commercial use.
