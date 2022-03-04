import argparse
import matplotlib.pyplot as plt
import cv2

import steganography

def parse_args():
    parser = argparse.ArgumentParser(description='LSB embedding and extraction')
    parser.add_argument('--image_path', type=str, default='image.png', help='Image to be processed')
    parser.add_argument('--message', type=str, default='Hello World', help='Message to be embedded')
    parser.add_argument('--algorithm_name', type=str, default='LSB', help='Algorithm to be used')
    parser.add_argument('--key', type=int, default=2022, help='Key value to be used for embedding')
    parser.add_argument('--output_path', type=str, default='output.png', help='Output path for saving image')
    parser.add_argument('--extract', action='store_true', help='Extract message from image')
    return parser.parse_args()

def main():
    args = parse_args()
    image = cv2.imread(args.image_path)
    algorithm = getattr(steganography, args.algorithm_name)
    key = args.key
    extract = args.extract

    if extract:
        message = algorithm(key=key).extract(image)
        print(message)
    else:
        image = algorithm(key=key).embed_image(image, message)
        cv2.imwrite(args.output_path, image)
        plt.imshow(image[:, :, ::-1])
        plt.show()

if __name__ == '__main__':
    main()