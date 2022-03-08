import numpy as np 
import random

from ..utils import message_to_binary, integer_to_binary

class LSBM:
    """
    Image steganography using LSB Matching algorithm.
    
    Args:
        key (int): Random seed for pixel traversal order
    """
    def __init__(self, key=2022):
        self._key = key
        random.seed(key)
    
    def _embed_pixel(self, message, binary_pixel, message_index):
        bit = message[message_index]
        pixel = int(binary_pixel, 2)
        if binary_pixel[-1] != bit:
            pixel = self._random_increment_or_decrement(pixel)
        return pixel
    
    def _random_increment_or_decrement(self, pixel):
        random_number = random.random()
        if pixel == 255:
            return 254
        if pixel == 0:
            return 1
        if random_number < 0.5:    
            pixel += 1
        else:
            pixel -= 1     
        return pixel
    
    def _binary_to_string(self, binary_message, delimiter):
        delimiter_length = len(delimiter) * -1
        delimiter_present = False
        message_bytes = [binary_message[i : i + 8] for i in range(0, len(binary_message), 8)]
        message = ""
        for byte in message_bytes:
            char = chr(int(byte, 2))
            message += char
            if message[delimiter_length:] == delimiter:   
                message = message[:delimiter_length]
                delimiter_present = True
                break
        return message, delimiter_present

    def embed(self, image, message):
        message = message + '\0'
        binary_message = message_to_binary(message)
        width = np.size(image, 1)
        height = np.size(image, 0)
        num_bytes = width * height
        message_index = 0
        message_length = len(binary_message)
        if message_length > num_bytes:
            raise ValueError("The message is too large for the image.")

        pixels = range(num_bytes)
        path = random.sample(pixels, num_bytes)
        cover_image = image 
        for i in range(len(path)):
            index = path[i]
            x = index % width
            y = index // width
            pixel = cover_image[y][x]
            embedded_pixel = pixel
            binary_pixel = integer_to_binary(pixel)
            embedded_pixel = self._embed_pixel(binary_message, binary_pixel, message_index)

            cover_image[y][x] = embedded_pixel
            message_index += 1

            if message_index == message_length:
                break
        stego_image = cover_image
        return stego_image
    
    def extract(self, image):
        binary_message = ""
        width = np.size(image, 1)
        height = np.size(image, 0)
        num_bytes = width * height
        pixels = range(num_bytes) 
        path = random.sample(pixels,num_bytes)
        for i in range(0, len(path)):
            index = path[i]
            x = index % width
            y = index // width
            stego_pixel = image[y][x]
            binary_pixel = integer_to_binary(stego_pixel)
            binary_message += binary_pixel[-1]

        extracted_message, _ = self._binary_to_string(binary_message, '\0')
        return extracted_message

    @property
    def key(self):
        return self._key