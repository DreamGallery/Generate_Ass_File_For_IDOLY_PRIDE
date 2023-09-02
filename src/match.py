import cv2
import numpy as np
from src.read_ini import config
from PIL import Image, ImageDraw, ImageFont

half_split_length = config.getint("Arg", "half_split_length")

def to_binary(img: any, thresh: float) ->any:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,binary = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
    return binary

def to_binary_adaptive(img: any, blocksize: int, C: float) ->any:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blocksize, C)
    return binary

def draw_text(text: str, font_path: list[str], fontsize: list[int], strokewidth: int, kerning: int) ->[list[any], list[any]]:
    font_japan = ImageFont.truetype(font_path[0], fontsize[0])
    font_alpha = ImageFont.truetype(font_path[1], fontsize[1])
    font_digit = ImageFont.truetype(font_path[2], fontsize[2])

    char_info = []
    text_height = 0
    for char in text:
        if char.encode("utf-8").isalpha():
            font = font_alpha
        elif char.encode("utf-8").isdigit():
            font = font_digit
        else:
            font = font_japan
        char_bbox = font.getbbox(char, stroke_width=strokewidth)
        char_width = char_bbox[2] - char_bbox[0] - strokewidth
        text_height = max((char_bbox[3] - char_bbox[1]), text_height)
        char_info.append([font, char_width])
    
    text_width = 0
    for info in char_info:
        text_width += info[1]
    text_size = ((text_width + (len(text)-1) * kerning), text_height)
    text_img = Image.new('RGBA', text_size)
    draw = ImageDraw.Draw(text_img)

    tmp_width = 0
    for index, char in enumerate(text):
        draw.text((((char_info[index][1]) // 2 + tmp_width), (text_size[1] // 2)), char, anchor="mm", font=char_info[index][0], stroke_width=strokewidth, stroke_fill=(32,32,32))
        tmp_width = tmp_width + char_info[index][1] + kerning
    binary = []
    mask = []
    kernel = np.ones((3,3), np.uint8)
    if len(text) >= half_split_length:
        spilt_pixel = sum(list(item[1] for item in char_info[:(len(text) // 2 - 1)]), kerning * (len(text) // 2 - 1))
        image_part = [np.asarray(text_img)[0:text_size[1], 0:spilt_pixel], np.asarray(text_img)[0:text_size[1], spilt_pixel:text_size[0]]]
        for part in image_part:
            binary.append(to_binary(part, 127))
            mask.append(cv2.erode(to_binary(part, 30), kernel, iterations=1))
    else:
        binary.append(to_binary(np.asarray(text_img), 127))
        mask.append(cv2.erode(to_binary(np.asarray(text_img), 30), kernel, iterations=1))

    return binary, mask


def compare(img_path: str, binary: list[any], threshold: float, mask: list[any]) ->bool:
    img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2GRAY)
    white_pixels = cv2.countNonZero(img)
    if white_pixels < 100:
        return False
    part_max = []
    for image in zip(binary, mask):
        res = cv2.matchTemplate(img, image[0], cv2.TM_CCORR_NORMED, mask = image[1])
        res[np.isinf(res)] = 0
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        part_max.append(max_val)
    max_avg = sum(part_max) / len(part_max)
    if max_avg > threshold:
        return True
    else:
        return False
