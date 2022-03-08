import numpy as np
from numpy.lib.stride_tricks import as_strided

def _conv2d(input, kernel):
    s = kernel.shape + tuple(np.subtract(input.shape, kernel.shape) + 1)
    windows = as_strided(input, shape = s, strides = input.strides * 2)
    return np.einsum('ij,ijkl->kl', kernel, windows)


def conv2d(img, kernel):
    assert img.ndim == 2 and kernel.size % 2 == 1
    # Force padding to keep shape
    pad = (kernel.shape[0] - 1) // 2
    img = np.pad(img, pad_width=((pad, pad), (pad, pad)), mode='constant')
    return _conv2d(img, kernel)