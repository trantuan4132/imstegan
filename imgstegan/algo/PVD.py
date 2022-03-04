import math
import numpy as np

from ..utils import *


class PVD():
    _pos = ((0, 0), (0, 2), (1, 0), (1, 2))

    def __init__(self, **kwargs):
        pass

    def _analyze_block(self, block):
        gu = block[0, 1]
        gb = block[1, 1]
        ls, us, ns = [], [], []
        for x, y in self._pos:
            du = block[x, y] - gu
            db = block[x, y] - gb
            if du > 0 and db > 0:
                l = max(gu + 1, gb + 1)
                u = 255
            elif du <= 0 and db <= 0:
                l = 0
                u = min(gu, gb)
            elif du > 0 and db <= 0:
                l = gu + 1
                u = gb
            else:
                l = gb + 1
                u = gu
            n = min(math.floor(math.log2(abs(u - l + 1))), 3)
            ls.append(l)
            us.append(u)
            ns.append(n)

        return gu, ls, us, ns


    def embed(self, image, message):
        img = image.copy().astype(np.short)
        w, h = img.shape[:2]
        msg = message + '\0'
        msg = message_to_binary(message)
        for i in range(0, h - 2, 2):
            if not msg: break
            for j in range(0, w - 3, 3):
                block = img[i:i+2, j:j+3]
                gu, ls, us, ns = self._analyze_block(block)
                for (x, y), l, u, n in zip(self._pos, ls, us, ns):
                    if not msg: break
                    if n < 1: continue
                    b = int(msg[:n], 2)
                    msg = msg[n:]
                    dmin = 256
                    cmin = -1
                    for c in range(l, u + 1):
                        if (abs(c - gu) - b) % math.pow(2, n) == 0 and abs(c - block[x, y]) < dmin:
                            dmin = abs(c - block[x, y])
                            cmin = c
                    block[x, y] = cmin

        return img.astype(np.uint8)

    def extract(self, image):
        img = image.astype(np.short)
        w, h = img.shape[:2]
        binary_msg = ''
        completed = False
        temp = 0
        for i in range(0, h - 2, 2):
            if completed: break
            for j in range(0, w - 3, 3):
                if completed: break
                block = img[i:i+2, j:j+3]
                gu, _, _, ns = self._analyze_block(block)
                for (x, y), n in zip(self._pos, ns):
                    if completed: break
                    info = None
                    for b in range(2**n):
                        if (b - abs(block[x, y] - gu)) % math.pow(2, n) == 0:
                            info = b
                            break
                    info = f"{b:b}"
                    if len(info) < n:
                        info = "0" * (n - len(info)) + info
                    binary_msg += info
                    # End of message check
                    rem = len(binary_msg) % 8
                    if binary_msg[-rem-8:-rem] == "00000000":
                        completed = True
                        binary_msg = binary_msg[:-rem-8]
                        break
        msg = binary_to_string(binary_msg)

        return msg