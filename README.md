# Generate Ass File For IDOLY PRIDE

Auto generate subtitle file of aegisub(.ass) for IDOLY PRIDE.<br />
Also using `OPENCV` to fix timeline of subtitle frame by frame.<br />

※This tool is based on [MalitsPlus/HoshimiToolkit](https://github.com/MalitsPlus/HoshimiToolkit), you need to get subtitle files in the game through this project first, the names of required files are usually `adv_***.txt`.

# Usage(GPU_noCache Version)

## Install from the repository

```
git clone https://github.com/DreamGallery/Sibyl-System-For-IDOLY-PRIDE.git Sibyl
cd Sibyl
```

## Install requirements

```
pip3 install -r requirements.txt
```

## Before running

There are still some args need you to fill in, please read the comments in `config.ini` to get more information.

## Generate .ass file without time-fix

Edit `[Info]` in `config.ini` first, put game subtitle file in `adv/txt`, run the following command and the `.ass` file will be saved in `adv/ass`.

```
python generate.py
```

## Generate .ass file with time-fix

To use time-fix option you need to put the recorded video in `adv/video`, and the recommended resolution is `[1920x1080]` or you can change the `[Font Config]` in `config.ini` to fit your video(compare in PS is a good idea).<br />
If your resolution ratio is not `16:9`, you may also have to modify the cutting area of frames in `src/frame.py`.

```
python main.py
```

Adjust the appropriate threshold is very helpful to the running of this tool.<br />
Maybe sometimes you need to increase the threshold instead of decreasing it.<br />

## In the case of two subtitle files

Because some event stories will include MV of new song, the subtitle will be divided into two files.<br />
If you set `MV_exists = True` under section `[Sub]`, you will need to input the length of MV during running, more information will be printed before input.<br />

※Generating .ass file without time-fix doesn't work in this situation, or you will lose the information of subtitles part 2.

## ※About Fonts

IDOLY PRIDE is using SDF to render subtitle, the original fonts of `japanese(UDKakugo)`, `letters` and `digit` are all different, the fonts in `font` folder are only possible fonts.<br />
If you need another weight of these two fonts(`Roboto` for digit and `DM Sans` for letters), you can get them through the link below

```
https://github.com/googlefonts/roboto #Roboto
https://github.com/googlefonts/dm-fonts #DeepMindSans(v1.002)
```

In addition, please note that some fonts require authorization for commercial use.
