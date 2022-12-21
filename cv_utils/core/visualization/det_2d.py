from ...basic import _cv2
from ..constant.attributes import Color, Font


__all__ = ['draw_bbox2d', 'draw_point', 'put_text', 'draw_table']


def draw_bbox2d(img, coords, color, label=''):
    if isinstance(color, Color):
        color = color.value
    text_color = Color.Black if sum(color) > 128 * 3 else Color.White

    _cv2._rectangle(img, coords, color, 1)

    if label:
        _cv2._put_text(img, coords[:2], label, *Font.S.value, color=text_color.value, thickness=1, bg_alpha=0.5, bg_color=color)


def draw_point(img, coord, color, label=''):

    x0, y0 = coord

    text_color = Color.Black if sum(color) > 128 * 3 else Color.White

    if label:
        w, h, _ = _cv2._get_text_size_and_offset(label, *Font.S.value, 1)

        _cv2._put_text(img, (x0-w/2, y0-h/2), label, *Font.S.value, color=text_color.value, thickness=1, bg_alpha=0.5, bg_color=color, bg_shape='circle')
        # _put_text(img, (100, 100), '1', cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1, bg_alpha=0.5, bg_color=(0, 0, 255), bg_shape='circle')
    else:
        _cv2._circle(img, coord, 3, color, thickness=0, bg_alpha=1)


def put_text(img, coord, text, font, color, thickness=1, bg_alpha=0, bg_color=None):
    _cv2._put_text(img, coord, text, *font.value, color.value, thickness, bg_alpha, bg_color.value)


def draw_table(img, table, start_pos, col_colors):
    _, text_h, _ = _cv2._get_text_size_and_offset('dummy', *Font.M.value, 1)

    cell_widths = [0] * len(table[0])
    for j, row in enumerate(table):
        for i, col in enumerate(row):
            text_width, _, _ = _cv2._get_text_size_and_offset(col, *Font.M.value, 1)
            cell_widths[i] = max(cell_widths[i], text_width)
    cell_widths = [w + 10 for w in cell_widths]

    for j, row in enumerate(table):
        for i, col in enumerate(row):
            tx = start_pos[0] + sum(cell_widths[:i])
            ty = start_pos[1] + j * text_h
            _cv2._put_text(img, (tx, ty), col, *Font.M.value, col_colors[i].value, 1)

    return img
