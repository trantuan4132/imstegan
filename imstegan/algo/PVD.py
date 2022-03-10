import math
import warnings
from typing import Any

import numpy as np

from ..utils import message_to_binary, binary_to_message, rgb_to_gray


__all__ = ["PVD", "AdaptivePVD"]


def _to_grayscale(image):
    if image.ndim > 2:
        if image.shape[2] == 3:
            img = rgb_to_gray(image)
            warnings.warn("Image is RGB, converting to grayscale")
        elif image.shape[2] == 1:
            img = image.squeeze()
    else:
        img = image.copy()
    
    return img


class PVD():
    """Pixel-value differencing algorithm described in 
    `"A steganographic method for images by pixel-value differencing", Da-Chun Wu, Wen-Hsiang Tsai`
    """
    def __init__(self, high_capacity: bool = False, **kwargs: Any) -> None:
        if high_capacity:
            self._range = (2, 2, 4, 4, 4, 8, 8, 16, 16, 32, 32, 64, 64)
        else:
            self._range = (8, 8, 16, 32, 64, 128)
    
    def _f(self, l, r, d, dp):
        m = dp - d
        return (l - math.ceil(m/2), r + math.floor(m/2)) if d % 2 != 0 \
            else (l - math.floor(m/2), r + math.ceil(m/2))
    
    def _analyze_pair(self, a, b):
        d = b - a
        acc = 0
        for k in range(len(self._range)):
            if acc + self._range[k] - 1 < abs(d):
                acc += self._range[k]
            else:
                l = acc
                u = acc + self._range[k] - 1
                break
        n = int(math.log2(u - l + 1))
        # Range check
        lu, ru = self._f(a, b, d, u if d >= 0 else -u)
        overflow = (lu < 0 or lu > 255 or ru < 0 or ru > 255)

        return overflow, l, d, n

    def embed(self, image: np.ndarray, message: str) -> np.ndarray:
        img = _to_grayscale(image).astype(np.short)
        h, w = img.shape[:2]
        binary_msg = message_to_binary(message + '\0')

        for i in range(h - 1):
            if not binary_msg: break
            for j in range(0, w - 2, 2):
                if not binary_msg: break
                overflow, l, d, n = self._analyze_pair(img[i, j], img[i, j + 1])
                if overflow:
                    continue
                # Embed
                b = int(binary_msg[:n], 2)
                binary_msg = binary_msg[n:]
                dp = l + b if d >= 0 else -(l + b)
                nl, nr = self._f(img[i, j], img[i, j + 1], d, dp)
                img[i, j] = nl
                img[i, j + 1] = nr
    
        return img.astype(np.uint8)
    
    def extract(self, image: np.ndarray) -> str:
        img = image.astype(np.short)
        h, w = img.shape[:2]
        binary_msg = ''
        completed = False

        for i in range(h - 1):
            if completed: break
            for j in range(0, w - 2, 2):
                if completed: break
                overflow, l, d, n = self._analyze_pair(img[i, j], img[i, j + 1])
                if overflow:
                    continue
                # Extract
                b = d - l if d >= 0 else -d - l
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
        
        return binary_to_message(binary_msg)


class AdaptivePVD():
    """Adaptive PVD on 2x3 blocks described in
    `"Adaptive PVD Steganography Using Horizontal, Vertical, and Diagonal Edges in Six-Pixel Blocks", K. Raja Sekhar, Gandharba Swain`
    """
    _pos = ((0, 0), (0, 2), (1, 0), (1, 2))

    def __init__(self, **kwargs: Any):
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


    def embed(self, image: np.ndarray, message: str) -> np.ndarray:
        img = _to_grayscale(image).astype(np.short)
        w, h = img.shape[:2]
        message = message + '\0'
        binary_msg = message_to_binary(message)
        
        for i in range(0, h - 2, 2):
            if not binary_msg: break
            for j in range(0, w - 3, 3):
                block = img[i:i+2, j:j+3]
                gu, ls, us, ns = self._analyze_block(block)
                for (x, y), l, u, n in zip(self._pos, ls, us, ns):
                    if not binary_msg: break
                    if n < 1: continue
                    b = int(binary_msg[:n], 2)
                    binary_msg = binary_msg[n:]
                    dmin = 256
                    cmin = -1
                    # NOTE: This can be solved efficiently with binary 
                    # search + pre-computed table. Will come back later
                    for c in range(l, u + 1):
                        if (abs(c - gu) - b) % math.pow(2, n) == 0 and abs(c - block[x, y]) < dmin:
                            dmin = abs(c - block[x, y])
                            cmin = c
                    block[x, y] = cmin

        return img.astype(np.uint8)

    def extract(self, image: np.ndarray) -> str:
        if image.ndim == 3 and image.shape[2] == 1:
            image = image.squeeze()
        assert image.ndim == 2, "Image must be grayscale"
        img = image.astype(np.short)
        w, h = img.shape[:2]
        binary_msg = ''
        completed = False
        
        for i in range(0, h - 2, 2):
            if completed: break
            for j in range(0, w - 3, 3):
                if completed: break
                block = img[i:i+2, j:j+3]
                gu, _, _, ns = self._analyze_block(block)
                for (x, y), n in zip(self._pos, ns):
                    if completed: break
                    info = None
                    # NOTE: This too can be solved more efficiently
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

        return binary_to_message(binary_msg)