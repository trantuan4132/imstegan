import numpy as np

def message_to_binary(message):
    return ''.join([format(ord(i), "08b") for i in message])

def integer_to_binary(integer):
    return format(integer, "08b")

def binary_to_string(binary_message):
    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        message += chr(int(byte, 2))
    return message

def rgb_to_gray(image):
    coef = np.array([[[0.299, 0.587, 0.114]]])
    return (image@coef).squeeze()


class Message():
    def __init__(self, message, format='binary'):
        assert format in ['binary', 'string']
        if format == 'string':
            self._message = message
            self.format = 'string'
            self._unicode = None
        else:
            self._message, self._unicode = self.binary_from_string(message)
            self.format = 'binary'

    def next(self, count):
        next_bits = self._message[:count]
        self._message = self._message[count:]
        return next_bits
    
    def to_string(self, message):
        return binary_to_string(message)

    @staticmethod
    def binary_from_string(message):
        unicode = False
        ords = []
        for c in message:
            if ord(c) > 127:
                unicode = True
            ords.append(ord(c))
        if unicode:
            binary_message = ''.join([f'{c:016b}' for c in ords])
        else:
            binary_message = ''.join([f'{c:08b}' for c in ords])
        return binary_message, unicode

    @staticmethod
    def binary_to_string(binary_message, unicode=False):
        message = ""
        width = 16 if unicode else 8

        for i in range(0, len(binary_message), width):
            message += chr(int(binary_message[i:i + width], 2))
        return message

    @property
    def message(self):
        return self._message
    
    @property
    def unicode(self):
        return self._unicode