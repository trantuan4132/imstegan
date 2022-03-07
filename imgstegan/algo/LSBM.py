import numpy as np 
import random 
from unidecode import unidecode

class LSBM:
    def __init__(self,key=None,n_lsb=None):
        self.key = key
        self.delimiter = "-----"
        random.seed(key)
    
    def embed_pixel(self,message, binary_pixel, message_index):
        bit = message[message_index]
        pixel = int(binary_pixel, 2)
        if binary_pixel[-1] != bit:
            pixel = self.random_increment_or_decrement(pixel)
        return pixel
    
    def random_increment_or_decrement(self, pixel):
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

    def message_to_binary(self,message):
        ascii_message = unidecode(message)
        binary_message = ''.join(format(ord(char), '08b') for char in ascii_message)
        return binary_message
    
    def integer_to_binary(self,integer):
        binary_value = format(integer, "08b")
        return binary_value
    
    def binary_to_string(self,binary_message, delimiter):
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

    def embed(self,image,message):
        message = message+self.delimiter
        binary_message = self.message_to_binary(message)
        width = np.size(image, 1)
        height = np.size(image, 0)
        num_bytes = width * height
        message_index = 0
        message_length = len(binary_message)
        if message_length > num_bytes:
            raise ValueError("The message is too large for the image.")

        pixels = [i for i in range(0,num_bytes)]   
        path = random.sample(pixels, num_bytes)
        cover_image = image 
        for i in range(0, len(path)):
            index = path[i]
            x = index % width
            y = index // width
            pixel = cover_image[y][x]
            embedded_pixel = pixel
            binary_pixel = self.integer_to_binary(pixel)
            embedded_pixel = self.embed_pixel(binary_message,binary_pixel, message_index)

            cover_image[y][x] = embedded_pixel
            message_index += 1

            if message_index == message_length:
                break
        stego_image = cover_image
        return stego_image
    
    def extract(self,image):
        binary_message = ""
        width = np.size(image, 1)
        height = np.size(image, 0)
        num_bytes = width * height
        pixels = [i for i in range(0,num_bytes)]  
        path = random.sample(pixels,num_bytes)
        for i in range(0, len(path)):
            index = path[i]
            x = index % width
            y = index // width
            stego_pixel = image[y][x]
            binary_pixel = self.integer_to_binary(stego_pixel)
            binary_message += binary_pixel[-1]

        extracted_message, _ = self.binary_to_string(binary_message, self.delimiter)
        return extracted_message



    