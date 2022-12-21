import cv2

from matplotlib import cm
from enum import Enum, unique


__all__ = ['Color', 'Font', 'Thickness']

# reference: https://www.matplotlib.org.cn/tutorials/colors/colormaps.html#miscellaneous
_paired_colors = [[int(v * 255) for v in color][::-1] for color in cm.get_cmap('Paired').colors]


@unique
class Color(Enum):
    none = [-1, -1, -1]
    Black = [0, 0, 0]
    White = [255, 255, 255]
    blue = _paired_colors[0]
    Blue = _paired_colors[1]
    green = _paired_colors[2]
    Green = _paired_colors[3]
    red = _paired_colors[4]
    Red = _paired_colors[5]
    yellow = _paired_colors[6]
    Yellow = _paired_colors[7]
    purple = _paired_colors[8]
    Purple = _paired_colors[9]
    brown = _paired_colors[10]
    Brown = _paired_colors[11]


@unique
class Font(Enum):
    S = (cv2.FONT_HERSHEY_SIMPLEX, 0.3)
    M = (cv2.FONT_HERSHEY_SIMPLEX, 0.6)
    L = (cv2.FONT_HERSHEY_SIMPLEX, 1)
    X = (cv2.FONT_HERSHEY_SIMPLEX, 2)


@unique
class Thickness(Enum):
    Solid = -1
    Thin = 1
    Thick = 2
