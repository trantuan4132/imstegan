import warnings
from typing import Any
import cv2
import numpy as np

from ..utils import message_to_binary, binary_to_message, rgb_to_gray, dct8x8, idct8x8


__all__ = ["DCTScale"]

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


class DCTScale():
    """A naive steganographic method for images using Discrete Cosine Transform.
    This method embeds a message in an image by changing quantized DCT coefficients.
    This is currently broken if encounter near white or black pixels."""
    def __init__(self, quantization_factor: int = 16, **kwargs: Any) -> None:
        self._factor = quantization_factor
        pass
    
    def embed(self, image: np.ndarray, message: str) -> np.ndarray:
        img = _to_grayscale(image).astype(np.short)
        h, w = img.shape[:2]
        binary_msg = message_to_binary(message + '\0')

        # Pad/resize to multiple of 8
        pad_h = 8 - h % 8 if h % 8 != 0 else 0
        pad_w = 8 - w % 8 if w % 8 != 0 else 0
        # img = np.pad(
        #     img, 
        #     ((floor(pad_h/2), ceil(pad_h/2)), (floor(pad_w/2), ceil(pad_w/2))), 
        #     'constant', constant_values=0
        # )
        img = cv2.resize(img, (w + pad_w, h + pad_h))
        h, w = img.shape[:2]
        dct_coef = np.zeros((h, w))

        for i in range(0, h, 8):
            for j in range(0, w, 8):
                dct_coef[i:i+8, j:j+8] = dct8x8(img[i:i+8, j:j+8] - 128)

        dct_coef = (dct_coef/self._factor).round().astype(np.short)

        img2 = np.zeros((h, w))

        for i in range(h):
            for j in range(w):
                if not binary_msg: break
                if abs(dct_coef[i, j]) > 2:
                    if dct_coef[i, j] % 2 != int(binary_msg[0]):
                        if dct_coef[i, j] > 0:
                            dct_coef[i, j] -= 1
                        else:
                            dct_coef[i, j] += 1
                    binary_msg = binary_msg[1:]
                elif abs(dct_coef[i, j]) == 2:
                        if dct_coef[i, j] > 0:
                            dct_coef[i, j] = 1
                        else:
                            dct_coef[i, j] = -1
        dct_coef *= self._factor
        for i in range(0, h, 8):
            for j in range(0, w, 8):
                img2[i:i+8, j:j+8] = idct8x8(dct_coef[i:i+8, j:j+8]) + 128
        return img2.clip(0, 255).astype(np.uint8)
    
    def extract(self, image: np.ndarray) -> str:
        img = image.astype(np.short)
        h, w = img.shape[:2]
        binary_msg = ''
        completed = False
        dct_coef = np.zeros((h, w))

        for i in range(0, h, 8):
            for j in range(0, w, 8):
                dct_coef[i:i+8, j:j+8] = dct8x8(img[i:i+8, j:j+8] - 128)

        dct_coef = (dct_coef/self._factor).round().astype(np.short)
        
        for i in range(h):
            if completed: break
            for j in range(w):
                if completed: break
                if abs(dct_coef[i, j]) > 1:
                    if dct_coef[i, j] % 2 == 1:
                        binary_msg += '1'
                    else:
                        binary_msg += '0'
                    # End of message check
                    rem = len(binary_msg) % 8
                    if binary_msg[-rem-8:-rem] == "00000000":
                        completed = True
                        binary_msg = binary_msg[:-rem-8]
                        break
                
        return binary_to_message(binary_msg)
