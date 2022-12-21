import numpy as np

from ..constant import Color


__all__ = ['blank_img']


def blank_img(size, color=Color.White):
    if isinstance(color, Color):
        color = color.value
    return np.multiply(np.ones((size[0], size[1], 3)), color).astype(np.uint8)
