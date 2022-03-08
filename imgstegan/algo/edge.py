import math
import warnings
from typing import Any

import numpy as np

from ..utils import message_to_binary, binary_to_message, rgb_to_gray, conv2d


__all__ = ["SobelLSB"]


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


class SobelLSB():
    """Pixel-value differencing algorithm described in 
    `"A steganographic method for images by pixel-value differencing", Da-Chun Wu, Wen-Hsiang Tsai`
    """
    def __init__(self, n_bits: int = 4, sobel_threshold: float = 0.5, **kwargs: Any) -> None:
        self._n_bits = n_bits
        self._threshold = sobel_threshold
        pass

    def _sobel_magnitude(self, image):
        Gx = conv2d(image, np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]))
        Gy = conv2d(image, np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]))
        return np.sqrt(Gx ** 2 + Gy ** 2)

    def embed(self, image: np.ndarray, message: str) -> np.ndarray:
        img = _to_grayscale(image).astype(np.uint8)
        binary_msg = message_to_binary(message)
        edge_mask = self._sobel_magnitude(img/255.0)
        edge_loc = np.where(edge_mask > self._threshold)
        for x,y in zip(*edge_loc):
            if not binary_msg: break
            b = int(binary_msg[:self._n_bits], 2)
            binary_msg = binary_msg[self._n_bits:]
            img[x, y] = (img[x, y] >> self._n_bits) << self._n_bits | b
        
        return img
    
    def extract(self, image: np.ndarray) -> str:
        img = image.astype(np.short)
        h, w = img.shape[:2]
        binary_msg = ''
        completed = False

        for i in range(h - 1):
            if completed: break
            for j in range(0, w - 2, 2):
                if completed: break
                
                # End of message check
                rem = len(binary_msg) % 8
                if binary_msg[-rem-8:-rem] == "00000000":
                    completed = True
                    binary_msg = binary_msg[:-rem-8]
                    break
        
        return binary_to_message(binary_msg)