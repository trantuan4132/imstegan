import numpy as np

from ..utils import *


class LSB():
    def __init__(self, n_lsb=1, delimiter="\\0", key=2022, **kwargs):
        self.n_lsb = n_lsb
        self.delimiter = delimiter
        self.key = key

    def embed(self, image, message):
        message = message + self.delimiter
        binary_message = message_to_binary(message)
        h, w, c = image.shape
        max_bits = h * w * c * self.n_lsb
        # Check if message length exceeds maximum bits for encoding
        if len(binary_message) > max_bits:
            raise ValueError("Insufficient places to store data, need bigger image or less data !!")

        # Create path for embedding data using key value
        path = np.arange(max_bits)
        np.random.seed(self.key)
        np.random.shuffle(path)

        # Embed all data from message within the image
        new_image = image.copy()
        for i in range(len(binary_message)):
            index = path[i]
            
            # Index to image coordination
            y, x, z, t = np.unravel_index(index, (h, w, c, self.n_lsb))

            # Embed data within the last bit of the current coordination value
            binary_value = integer_to_binary(image[y][x][z])
            new_binary_value = binary_value[:-t-1] + binary_message[i] + binary_value[len(binary_value)-t:]
            new_image[y][x][z] = int(new_binary_value, 2)

        return new_image

    def extract(self, image):
        binary_delimiter = message_to_binary(self.delimiter)
        h, w, c = image.shape
        max_bits = h * w * c * self.n_lsb

        # Create path for decoding data using key value
        path = np.arange(max_bits)
        np.random.seed(self.key)
        np.random.shuffle(path)

        # Decode all data from the image
        binary_message = ''
        for i in range(len(path)):
            index = path[i]
            
            # Index to image coordination
            y, x, z, t = np.unravel_index(index, (h, w, c, self.n_lsb))

            # Decode the data within the last bit of the current coordination value
            binary_message += integer_to_binary(image[y][x][z])[-t-1]

            # Check if reached the delimiter
            if binary_message[-len(binary_delimiter):] == binary_delimiter:
                binary_message = binary_message[:-len(binary_delimiter)]
                break

        message = binary_to_string(binary_message)    
        return message