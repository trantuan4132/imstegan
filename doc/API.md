# API

The heart of our library is the `imstegan.algo` submodule. It contains our implementation of steganography algorithms. They can be directly imported from the `imstegan` namespace (e.g., `imstegan.LSB`). All algorithms provide 2 important methods:
```py
embed(image: np.ndarray, message: str) -> np.ndarray
```
Which embeds a message into an image, and
```py
extract(image: np.ndarray) -> str
```
Which extracts a message from an image.

This documentation mainly describes use of the algorithms.

## Algorithms

### LSB

```py
imstegan.LSB(n_lsb: int = 1, key: int = 2022, delimeter: str = '\0')
```
Least Significant Bit Matching steganography algorithm. Works on colored images.

Params:
- `n_lsb`: Number of bits to hide in each pixel.
- `key`: PRNG key to get traversal order of pixels.
- `delimeter`: Character(s) to use as the delimeter of the message. For most cases you should just leave it there.

### LSBM
```py
imstegan.LSBM(key: int = 2022)
```
Least Significant Bit steganography algorithm. Works on single channel images.

Params:
- `key`: PRNG key to get traversal order of pixels and +/- 1 for each pixel.

### PVD
```py
imstegan.PVD(high_capacity: int = False)
```
Pixel-value Difference steganography algorithm. Works on single channel images.

Params:
- `high_capacity`: If `True`, use less bins and wider ranges so as to be able to embed more information. It comes with the cost of higher image distortion, though in most cases not noticeable.

### Adaptive PVD
```py
imstegan.AdaptivePVD()
```
Adaptive PVD on 2x3 blocks described in `"Adaptive PVD Steganography Using Horizontal, Vertical, and Diagonal Edges in Six-Pixel Blocks", K. Raja Sekhar, Gandharba Swain`. Works on single channel images.

Params: None

### Sobel edge + LSB
```py
imstegan.SobelLSB(n_bits: int = 2, threshold: float = 0.5)
```
Embed information using Sobel edge detection mask and LSB. Works on single channel images.

Params:
- `n_bits`: Number of bits to hide in each edge pixel.
- `threshold`: Threshold for edge detection.

### A DCT-based method
```py
imstegan.DCTScale(quantization_factor: int = 16)
```
Embed information using a DCT-based method. Works on single channel images.

Params:
- `quantization_factor`: Quantization factor for DCT. Higher means more distortion, less embedding capacity, more likely to encounter overflow in IDCT but is more resistant to image compression.