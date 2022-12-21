import cv2
import functools

import numpy as np


def _valid_coords(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        img = args[0]
        coords = args[1]
        h, w, _ = img.shape

        if isinstance(coords, tuple) or isinstance(coords, list):
            coords = np.array(coords).astype(np.int32)
        elif isinstance(coords, np.ndarray):
            if not np.issubdtype(coords.dtype, np.integer):
                coords = coords.astype(np.int32)
        else:
            raise TypeError(f'not supported coords type: {type(coords)}')
        
        coords[::2] = np.clip(coords[::2], 0, w)
        coords[1::2] = np.clip(coords[1::2], 0, h)
        
        args = list(args)
        args[1] = coords
        args = tuple(args)
        return func(*args, **kwargs)
    return wrapper


@_valid_coords
def _lines(img, coords, color, thickness=1, close=True):
    start_points = coords.reshape((-1, 2))
    end_points = np.roll(start_points, -1, axis=0)
    for start_point, end_point in zip(start_points[:-1], end_points[:-1]):
        cv2.line(img, start_point, end_point, color, thickness)
    if close and len(coords) > 4:
        cv2.line(img, start_points[-1], end_points[-1], color, thickness)


@_valid_coords
def _rectangle(img, coords, color, thickness=1, bg_alpha=0, bg_color=None):
    x0, y0, x1, y1 = coords
    rect_w, rect_h = x1 - x0, y1 - y0
    bg_color = color if bg_color is None else bg_color

    bg = np.zeros((rect_h, rect_w, 3), np.uint8)
    cv2.rectangle(bg, (0, 0), (rect_w, rect_h), bg_color, thickness=-1)
    img[y0:y1, x0:x1] = cv2.addWeighted(img[y0:y1, x0:x1], 1-bg_alpha, bg, bg_alpha, 0)

    if thickness > 0:
        cv2.rectangle(img, (x0, y0), (x1, y1), color, thickness)


@_valid_coords
def _circle(img, coord, radius, color, thickness=1, bg_alpha=0, bg_color=None):
    x0, y0 = coord
    r = int(radius)
    
    bg = np.ones((2*r, 2*r, 3), np.uint8)
    cv2.circle(bg, (r, r), r, bg_color, thickness=-1)
    img[y0-r:y0+r, x0-r:x0+r] = np.where(bg==1, img[y0-r:y0+r, x0-r:x0+r], cv2.addWeighted(img[y0-r:y0+r, x0-r:x0+r], 1-bg_alpha, bg, bg_alpha, 0))
    if thickness > 0:
        cv2.circle(img, coord, radius, color, thickness)


def _get_text_size_and_offset(text, fontFace, fontScale, thickness):
    """ opencv text

               left_top ___________
            putText.org|_abcdefghi_| text_size[1]  \ height
                       |___________| baseline      /
                        text_size[0]
                           width
    """
    text_size, baseline = cv2.getTextSize(text, fontFace, fontScale, thickness)
    width = text_size[0]
    height = text_size[1] + baseline
    offset = text_size[1]
    return width, height, offset


@_valid_coords
def _put_text(img, coord, text, fontFace, fontScale, color, thickness=1, bg_alpha=0, bg_color=None, bg_shape='rectangle'):
    x0, y0 = coord
    w, h, o = _get_text_size_and_offset(text, fontFace, fontScale, thickness)

    if bg_shape == 'rectangle':
        _rectangle(img, (x0, y0, x0+w, y0+h), color=(0, 0, 0), thickness=0, bg_alpha=bg_alpha, bg_color=bg_color)
    elif bg_shape == 'circle':
        r = (w ** 2 + h ** 2) ** 0.5 / 2
        _circle(img, (x0+w/2, y0+h/2), r, color=(0, 0, 0), thickness=0, bg_alpha=bg_alpha, bg_color=bg_color)

    cv2.putText(img, text, (x0, y0 + o), fontFace, fontScale, color, thickness)
    return x0 + w, y0 + h
