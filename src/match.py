import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def to_binary(img: any, thresh: float) ->any:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,binary = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
    return binary

def draw_text(text: str, font_path: str, fontsize: int, strokewidth: int, kerning: int) ->[any, any]:
    char_width = fontsize + strokewidth
    font = ImageFont.truetype(f"{font_path}", fontsize)
    text_bbox = font.getbbox(text, stroke_width=strokewidth)
    text_size = ((char_width * len(text) + strokewidth + (len(text)-1) * kerning), (text_bbox[3] - text_bbox[1]))
    text_img = Image.new('RGBA', text_size)
    draw = ImageDraw.Draw(text_img)

    tmp_width = 0
    for char in text:
        draw.text((((char_width)//2 + tmp_width), (text_size[1] // 2)), char, anchor="mm", font=font, stroke_width=strokewidth, stroke_fill=(32,32,32))
        tmp_width = tmp_width + char_width + kerning 
    binary = to_binary(np.asarray(text_img), 127)
    mask = to_binary(np.asarray(text_img), 30)
    return binary, mask


def compare(img_path: str, binary: any, threshold: float, mask: any) ->bool:
    img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2GRAY)
    white_pixels = cv2.countNonZero(img)
    if white_pixels < 100:
        return False
    res = cv2.matchTemplate(img, binary, cv2.TM_CCORR_NORMED, mask = mask)
    res[np.isinf(res)] = 0
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val > threshold:
        return True
    else:
        return False
