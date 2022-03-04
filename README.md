# Steganography

## Installation

```
git clone https://github.com/trantuan4132/Image-Steganography
cd Image-Steganography
```

## Set up environment

```
pip install -r requirements.txt
```

## Embed message within image

```
python main.py --image_path <image-file> \
    --message <text> \
    --algorithm_name <algorithm-name>
    --key <number> \
    --output_path <output-file>
```

**Note:** Output path to save image should use extension with lossless compression (.png) to ensure that no information is lost

## Extract message from image

```
python main.py --image_path <image-file> \
    --algorithm_name <algorithm-name>
    --key <number> \
    --extract
```