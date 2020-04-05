from io import BytesIO


class ByteStringParser(object):

    @staticmethod
    def parse(buffer: BytesIO, decode=True):
        result = bytes()

        while True:
            char = buffer.read(1)
            if char and char != b'\x00':
                result += char
            else:
                break

        if decode:
            result = result.decode('utf-8')

        return result
