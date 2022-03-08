import numpy as np

def message_to_binary(message):
    return ''.join([format(ord(i), "08b") for i in message])

def integer_to_binary(integer):
    return format(integer, "08b")

def binary_to_message(binary_message):
    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        message += chr(int(byte, 2))
    return message

def rgb_to_gray(image):
    coef = np.array([0.299, 0.587, 0.114])[:, None]
    return (image@coef).squeeze()
