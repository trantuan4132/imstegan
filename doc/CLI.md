# CLI usage

## Embed message within image

```
python main.py --image_path <image-file> \
    --message <text> \
    --algorithm_name <algorithm-name>
    --key <number> \
    --output_path <output-file>
```

**Note:** 

- If message is contained in a text file, please specify `--text_file <text-file>` argument instead of `--message <text>`
- If LSB algorithm is used and the number of least significant bits used for embedding is more than one then specify `--n_lsb <number-of-least-significant-bits>`
- Output path to save image should use extension with lossless compression (.png) to ensure that no information is lost

## Extract message from image

```
python main.py --image_path <image-file> \
    --algorithm_name <algorithm-name>
    --key <number> \
    --extract
```

**Note:** For the purpose of saving extracted message to file, please specify `--extract_to_file <extract-file>` argument