import argparse
from PIL import Image
import numpy as np
import imstegan
import cv2 

def parse_args():
    parser = argparse.ArgumentParser(description='LSB embedding and extraction')
    parser.add_argument('--image_path', type=str, default='image.png', help='Image to be processed')
    parser.add_argument('--message', type=str, default='Hello World', help='Message to be embedded')
    parser.add_argument('--text_file', type=str, default=None, help='Message from text file to be embedded')
    parser.add_argument('--algorithm_name', type=str, default='LSB', help='Algorithm to be used')
    parser.add_argument('--key', type=int, default=2022, help='Key value to be used for embedding')
    parser.add_argument('--n_lsb', type=int, default=1, help='Number of least significant bits used for embedding if LSB is used')
    parser.add_argument('--output_path', type=str, default='output.png', help='Output path for saving image')
    parser.add_argument('--extract', action='store_true', help='Extract message from image')
    parser.add_argument('--extract_to_file', type=str, default=None, help='Output path for saving extracted message')
    return parser.parse_args()

def main():
    args = parse_args()
    if args.algorithm_name=="LSBM":
        image = cv2.imread(args.image_path,cv2.IMREAD_GRAYSCALE)        
    else:
        image = np.array(Image.open(args.image_path))

    message = args.message
    algorithm = getattr(imstegan, args.algorithm_name)
    kwargs = {
        'key': args.key,
        'n_lsb': args.n_lsb,
    }
    
    # Get message to be embedded
    if args.text_file:
        with open(args.text_file, 'r') as f:
            message = f.read()
    else:
        message = args.message

    if args.extract:    
        # Extract message from image
        message = algorithm(**kwargs).extract(image)
        if args.extract_to_file:    
            # Save extracted message to file
            with open(args.extract_to_file, 'w') as f:
                f.write(message)
        else:
            # Print extracted message to console
            print(message)
    else:
        # Otherwise embed message into image
        image = algorithm(**kwargs).embed(image, message)
        if args.algorithm_name=="LSBM":
            cv2.imwrite(args.output_path,image)
        else:
            Image.fromarray(image).save(args.output_path)

if __name__ == '__main__':
    main()