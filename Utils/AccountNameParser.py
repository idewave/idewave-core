from io import BytesIO


class AccountNameParser(object):

    @staticmethod
    def parse(buffer: BytesIO):
        result = bytes()

        while True:
            char = buffer.read(1)
            if char and char != b'\x00':
                result += char
            else:
                break

        return result.decode('utf-8')
