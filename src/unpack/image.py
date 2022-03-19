import re
import os
import cv2

from PIL import Image
from .tools import get_filename


def merge_alpha_images(color_file: str, alpha_file: str, out: str):
    split = f'{out}/{get_filename(color_file)}'.split('#')

    index = None
    if split.__len__() > 1:
        index = re.search(r'^(\d+)', split[1])

    suffix = '.png' if not split[0].endswith('.png') else ''

    out_file = split[0] + (f'_{index.group(1)}' if index else '') + suffix

    if not os.path.exists(out_file):
        image = cv2.imread(color_file)
        alpha = cv2.imread(alpha_file)

        if image.__len__() == 2048:
            alpha = cv2.resize(alpha, (2048, 2048))

        res = cv2.split(image)
        res.append(
            cv2.cvtColor(alpha, cv2.COLOR_BGR2GRAY)
        )
        res = cv2.merge(res)

        if not os.path.exists(out):
            os.makedirs(out)

        cv2.imwrite(out_file, res)


def transparency(path: str, color: tuple):
    img = Image.open(path)
    img = img.convert('RGBA')

    width, height = img.size
    array = img.load()

    for x in range(width):
        for y in range(height):
            pos = array[x, y]
            if pos == color:
                array[x, y] = (255, 255, 255, 0)

    img.save(path)
