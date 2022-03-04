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
    --key <number> \
    --output_path <output-file>
```

## Extract message from image

```
python main.py --image_path <image-file> \
    --key <number> \
    --extract
```