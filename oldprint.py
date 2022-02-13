# from v4 by Hoyii

import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from typing import List
import math
import random
import pathlib

FONT_NAME = 'FZSSJW.TTF'
FONT_SIZE = 28
FONT = ImageFont.truetype(f'{pathlib.Path(__file__).parent.resolve()}/fonts/{FONT_NAME}', FONT_SIZE)

DEFAULT_CONVERT_RATE = 0.95
DEFAULT_SPREAD_RATE = 0.006
DEFAULT_SPACING = 1.5
DEFAULT_ROTATION = 0


def set_font(name: str, size: str) -> ImageFont.FreeTypeFont:
    """
    设置字体
    """
    return ImageFont.truetype('fonts/' + name, size)


def is_chinese(uchar: str) -> bool:
    """
    判断字符是否为汉字

    Source: http://www.nexrol.com/posts/2012/05/02/python-judge-string.html
    """

    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


def get_text_weight(text: str) -> int:
    """
    返回文本的权重
    中文记为2，英文及标点记为1
    """

    weight = 0
    for ch in text:
        if is_chinese(ch):
            weight += 2
        else:
            weight += 1
    return weight


def get_max_weight(text_list: List[str]) -> int:
    """
    返回文本列表中最高的权重
    """

    weight_list = []
    for text in text_list:
        weight_list.append(get_text_weight(text))
    return max(weight_list)


def get_max_width(text_list: List[str]) -> int:
    """
    返回最大行宽
    """

    width_list = []

    for text in text_list:
        width_list.append(FONT.getsize(text)[0])

    return math.ceil(max(width_list))


def get_multi_line_text(text: str) -> List[str]:
    """
    返回分行的文本列表
    """

    # weight_limit = 59  # 《围城》汉英对照中行宽限制
    # left_punc = '‘“([{<（【《'  # 左起标点符号
    # text_list = []
    # while len(text) > 0:
    #     line = ''
    #     line_weight = 0
    #     while len(text) > 0:
    #         if line_weight + get_text_weight(text[0]) <= weight_limit:
    #             line += text[0]
    #             line_weight += get_text_weight(line[-1])
    #             text = text[1:]
    #         else:
    #             break
    #     while len(text) > 0:
    #         if not text[0].isalnum() and text[0] not in left_punc:
    #             line += text[0]
    #             text = text[1:]
    #         else:
    #             break
    #     text_list.append(line)
    # return text_list

    WEIGHT_LIMIT = FONT.getsize('方' * 29)[0]  # 《围城》汉英对照中行宽限制
    LEFT_PUNC = '‘“([{<（【《'  # 左起标点符号

    text_list = []

    while len(text) > 0:
        line = ''
        line_weight = 0
        while len(text) > 0:
            if line_weight + FONT.getsize(text[0])[0] <= WEIGHT_LIMIT:
                line += text[0]
                line_weight += FONT.getsize(line[-1])[0]
                text = text[1:]
            else:
                break
        while len(text) > 0:
            if not text[0].isalnum() and text[0] not in LEFT_PUNC:
                line += text[0]
                text = text[1:]
            else:
                break
        text_list.append(line)

    return text_list


def strQ2B(ustring):
    """
    把字符串全角转半角

    Source: https://www.it610.com/article/1306260863568613376.htm
    """

    ss = []
    for s in ustring:
        rstring = ""
        for uchar in s:
            inside_code = ord(uchar)
            if inside_code == 12288:  # 全角空格直接转换
                inside_code = 32
            elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
                inside_code -= 65248
            rstring += chr(inside_code)
        ss.append(rstring)
    return ''.join(ss)


def strB2Q(ustring):
    """
    把字符串半角转全角

    Source: https://www.it610.com/article/1306260863568613376.htm
    """

    ss = []
    for s in ustring:
        rstring = ""
        for uchar in s:
            inside_code = ord(uchar)
            if inside_code == 32:  # 全角空格直接转换
                inside_code = 12288
            elif (inside_code >= 33 and inside_code <= 126):  # 全角字符（除空格）根据关系转化
                inside_code += 65248
            rstring += chr(inside_code)
        ss.append(rstring)
    return ''.join(ss)


def get_surronding_white_count(img: np.ndarray, row: int, col: int) -> int:
    """
    返回给定位置周围的白色格子数量
    """

    WHITE = [255, 255, 255]

    count = 0

    if list(img[row-1][col-1]) == WHITE:
        count += 1
    if list(img[row-1][col]) == WHITE:
        count += 1
    if list(img[row-1][col+1]) == WHITE:
        count += 1
    if list(img[row][col-1]) == WHITE:
        count += 1
    if list(img[row][col+1]) == WHITE:
        count += 1
    if list(img[row+1][col-1]) == WHITE:
        count += 1
    if list(img[row+1][col]) == WHITE:
        count += 1
    if list(img[row+1][col+1]) == WHITE:
        count += 1

    return count


def get_old_print(img: np.ndarray, CONVERT_RATE, SPREAD_RATE) -> np.ndarray:
    """
    老印刷品效果
    """

    WHITE = [255, 255, 255]
    BLACK = [0, 0, 0]

    new_img = img.copy()
    dimensions = list(img.shape)

    for row in range(1, dimensions[0] - 1):
        for col in range(1, dimensions[1] - 1):
            if list(new_img[row][col]) != WHITE and list(new_img[row][col]) != BLACK:
                if random.random() < CONVERT_RATE:
                    new_img[row][col] = BLACK

    for row in range(1, dimensions[0] - 1):
        for col in range(1, dimensions[1] - 1):
            if list(new_img[row][col]) == BLACK:
                white_spread_chance = SPREAD_RATE * \
                    get_surronding_white_count(img, row, col)
                if random.random() < white_spread_chance:
                    new_img[row][col] = WHITE

    return new_img


def get_text_img(*text: str, CONVERT_RATE=DEFAULT_CONVERT_RATE,
              SPREAD_RATE=DEFAULT_SPREAD_RATE, SPACING=DEFAULT_SPACING,
              ROTATION=DEFAULT_ROTATION) -> str:
    """
    绘制文本并复制到剪贴板
    """

    text_list = []

    for para in text:
        text_list += get_multi_line_text(para)  # 获得分段文字

    # proper_weight = get_max_weight(text_list)
    proper_width = get_max_width(text_list)
    proper_text = '方'  # 方曼宜
    width = FONT.getsize(proper_text)[0]
    height = FONT.getsize(proper_text)[1]

    # canvas_width = math.ceil(width * (proper_weight / 2 + 1))
    canvas_width = math.ceil(proper_width + width)  # 比最长行宽多一个字符
    canvas_height = math.ceil(
        SPACING * height * (len(text_list) - 1) + height * 2)  # 在行距基础上增加一行

    canvas = 255 * \
        np.ones(shape=[canvas_height, canvas_width, 3], dtype=np.uint8)

    canvas_pil = Image.fromarray(canvas)
    draw = ImageDraw.Draw(canvas_pil)

    for i in range(len(text_list)):
        draw.text((width * 0.5, height * (SPACING * i + 0.5)),
                  text_list[i], font=FONT, fill=(0, 0, 0, 0))
        # draw.text((width * 0.5 + 1, height * (SPACING * i + 0.5)),
        #           text_list[i], font=FONT, fill=(0, 0, 0, 0))

    canvas = np.array(canvas_pil)

    canvas = get_old_print(canvas, CONVERT_RATE, SPREAD_RATE)

    if ROTATION != 0:
        canvas_pil = Image.fromarray(canvas)

        canvas_pil = canvas_pil.rotate(ROTATION, fillcolor=(255, 255, 255))

        canvas = np.array(canvas_pil)
    return cv2.imencode('.jpg', canvas, [int(cv2.IMWRITE_JPEG_QUALITY), 95])[1].tostring()


print('使用函数 draw_text(*文本, 转换率(CONVERT_RATE)=' +
      str(DEFAULT_CONVERT_RATE) + ', 蔓延率(SPREAD_RATE)=' +
      str(DEFAULT_SPREAD_RATE) + ', 行距(SPACING)=' + str(DEFAULT_SPACING) +
      ', 旋转(ROTATION)=' + str(DEFAULT_ROTATION) + ') 生成图片')
print('使用 FONT = set_font(字体名称, 字体大小) 更换字体')
