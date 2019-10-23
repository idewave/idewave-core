from io import BytesIO

from Exceptions.Wrappers.ProcessException import ProcessException


class AccountNameParser(object):

    @staticmethod
    @ProcessException
    def parse(buffer: BytesIO):
        result = bytes()

        while True:
            char = buffer.read(1)
            if char and char != b'\x00':
                result += char
            else:
                break

        return result.decode('utf-8')
