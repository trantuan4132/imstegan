<img src="doc/logo.png" width="100%">

---

*"Steganography is the study and practice of concealing information within objects in such a way that it deceives the viewer as if there is no information hidden within the object. Simply put, it is hiding information in plain sight, such that only the intended recipient would get to see it."*

**Imstegan** is an open source Python package implementing various image steganography techniques, including but not limited to Least Significant Bits (LSB), LSB Matching, Pixel-value Difference (PVD), Adaptive PVD, Edge-LSB, ...

## Installation

### Install from PyPI

```bash
pip install imstegan
```

### Install the latest version from main branch on GitHub

```bash
pip install git+https://github.com/trantuan4132/imstegan.git
```

## Usage

### As an API

All algorithms can be imported directly from namespace `imstegan`. Any algorithm contains `embed()` and `extract()` methods. For example, to embed a message into an image:

```py
import cv2

from imstegan import LSB

image = cv2.imread('image.png', cv2.IMREAD_COLOR)[..., ::-1]  # BGR to RGB
message = "Tea is leaf juice."

# Embed message into image
steg_image = LSB(n_bits=2, key=1337).embed(image, mesesage)

cv2.imwrite('steg_image.png', steg_image)
```

Conversely, to extract the message from an image, given that you know the relevant information:

```py
import cv2

from imstegan import LSB

steg_image = cv2.imread('steg_image.png', cv2.IMREAD_COLOR)[..., ::-1]  # BGR to RGB

# Extract message
message = LSB(n_bits=2, key=1337).extract(steg_image)

print(message)
```

Some algorithms natively support RGB images, but most of them work on single channel images. We provide utilities to seperate the channels or convert to grayscale so that they can be processed by the algorithms. More details can be found in our [API documentation](doc/API.md).

### As a CLI

We also provide a CLI tool to embed and extract messages from images. For example, to embed a message into an image:

```bash
python -m imstegan
    --image_path image.png \
    --message "Tea is leaf juice" \
    --algorithm_name LSB \
    --key 1337 \
    --output_path steg_image.png \
```

To extract the message from an image:
```bash
python -m imstegan
    --image_path steg_image.png \
    --algorithm_name LSB \
    --key 1337 \
    --extract
```

More details can be found in our [CLI documentation](doc/CLI.md).

## Contributing

If you plan to contribute new features, just open an issue and send a PR.

## License

This project is under [MIT License](LICENSE.md).