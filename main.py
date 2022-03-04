import argparse
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

import imgstegan

def parse_args():
    parser = argparse.ArgumentParser(description='LSB embedding and extraction')
    parser.add_argument('--image_path', type=str, default='image.png', help='Image to be processed')
    parser.add_argument('--message', type=str, default='Hello World', help='Message to be embedded')
    parser.add_argument('--text_file', type=str, default=None, help='Message from text file to be embedded')
    parser.add_argument('--algorithm_name', type=str, default='LSB', help='Algorithm to be used')
    parser.add_argument('--key', type=int, default=2022, help='Key value to be used for embedding')
    parser.add_argument('--output_path', type=str, default='output.png', help='Output path for saving image')
    parser.add_argument('--extract', action='store_true', help='Extract message from image')
    parser.add_argument('--extract_to_file', type=str, default=None, help='Output path for saving extracted message')
    return parser.parse_args()

def main():
    args = parse_args()
    image = np.array(Image.open(args.image_path))
    message = args.message
    algorithm = getattr(imgstegan, args.algorithm_name)
    key = args.key
    
    # Get message to be embedded
    if args.text_file:
        with open(args.text_file, 'r') as f:
            message = f.read()
    else:
        message = args.message

    # Extract message from image if extract argument is set
    if args.extract:
        message = algorithm(key=key).extract(image)

        # Save extracted message to file if extract_to_file argument is set
        if args.extract_to_file:
            with open(args.extract_to_file, 'w') as f:
                f.write(message)

        # Otherwise print extracted message to console
        else:
            print(message)

    # Otherwise embed message into image
    else:
        image = algorithm(key=key).embed(image, message)
        Image.fromarray(image).save(args.output_path)
        plt.imshow(image)
        plt.show()

if __name__ == '__main__':
    main()