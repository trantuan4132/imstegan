import numpy as np
from utils import *

class LSB():
    def __init__(self, delimiter="#####", key=2022):
        self.delimiter = delimiter
        self.key = key

    def embed(self, image, message):
        message = message + self.delimiter
        binary_message = message_to_binary(message)
        h, w, c = image.shape
        max_bits = h * w * c

        # Check if message length exceeds maximum bits for encoding
        if len(binary_message) > max_bits:
            raise ValueError("Encountered insufficient places to store data, need bigger image or less data !!")

        # Create path for embedding data using key value
        path = np.arange(max_bits)
        np.random.seed(self.key)
        np.random.shuffle(path)

        # Embed all data from message within the image
        new_image = image.copy()
        for i in range(len(binary_message)):
            index = path[i]
            
            # Index to image coordination
            z = index % c
            x = (index // c) % w
            y = (index // c) // w

            # Embed data within the last bit of the current coordination value
            binary_value = integer_to_binary(image[y][x][z])
            new_image[y][x][z] = int(binary_value[:-1] + binary_message[i], 2)

        return new_image

    def extract(self, image):
        binary_delimiter = message_to_binary(self.delimiter)
        h, w, c = image.shape
        max_bits = h * w * c

        # Create path for decoding data using key value
        path = np.arange(max_bits)
        np.random.seed(self.key)
        np.random.shuffle(path)

        # Decode all data from the image
        binary_message = ''
        for i in range(len(path)):
            index = path[i]
            
            # Index to image coordination
            z = index % c
            x = (index // c) % w
            y = (index // c) // w

            # Decode the data within the last bit of the current coordination value
            binary_message += integer_to_binary(image[y][x][z])[-1]

            # Check if reached the delimiter
            if binary_message[-len(binary_delimiter):] == binary_delimiter:
                binary_message = binary_message[:-len(binary_delimiter)]
                break

        message = binary_to_string(binary_message)    
        return message