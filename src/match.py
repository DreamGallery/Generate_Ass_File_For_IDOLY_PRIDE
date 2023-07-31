import cv2
from PIL import Image, ImageDraw, ImageFont

def draw_text(text: str, font_path: str, fontsize: int, strokewidth: int, kerning: int, fillcolor: (int, int, int)) ->Image:
    char_width = fontsize + strokewidth
    font = ImageFont.truetype(f"../{font_path}", fontsize)
    text_bbox = font.getbbox(text, stroke_width=strokewidth)
    text_size = ((char_width * len(text) + strokewidth + (len(text)-1) * kerning), (text_bbox[3] - text_bbox[1]))
    text_img = Image.new('RGBA', text_size, color=fillcolor)
    draw = ImageDraw.Draw(text_img)

    tmp_width = 0
    for char in text:
        draw.text((((char_width)//2 + tmp_width), (text_size[1] // 2)), char, anchor="mm", font=font, stroke_width=strokewidth, stroke_fill=(0,0,0))
        tmp_width = tmp_width + char_width + kerning
    return text_img


def compare(img_path: str, binary: any, threshold: float) ->bool:
    img = cv2.imread(img_path)
    res = cv2.matchTemplate(img, binary, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val > threshold:
        return True
    else:
        return False
