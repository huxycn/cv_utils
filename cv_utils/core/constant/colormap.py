import numpy as np


__all__ = ['VOC_COLORS']


def voc_palette(N=256):
    def bit_get(val, idx):
        return (val & (1 << idx)) != 0

    ret = np.zeros((N, 3), dtype=np.uint8)
    for i in range(N):
        r = g = b = 0
        c = i
        for j in range(8):
            r |= (bit_get(c, 0) << 7 - j)
            g |= (bit_get(c, 1) << 7 - j)
            b |= (bit_get(c, 2) << 7 - j)
            c >>= 3
        ret[i, :] = [r, g, b]
    return ret.tolist()


VOC_COLORS = voc_palette()
