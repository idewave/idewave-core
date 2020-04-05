import re
from binascii import hexlify, unhexlify


class LogParser(object):

    ''' This class uses for parsing Mangos log file, also contains some parsing Utils for another data '''

    def __init__(self, data: str):
        self.data = data

    def parse(self, to_hex=True):
        # Currently this method parses data from mangos logfile part of dump.
        # Each line of this part contains string in format yyyy-mm-dd hh:mm:ss byte.
        # This method removes unnecessary data from data and returns bytes sequence
        bytes_str_with_spaces = re.sub(r'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d', '', self.data)
        separator = ''
        if not to_hex:
            separator = ' '

        data = separator.join(bytes_str_with_spaces.split())

        if to_hex:
            result = unhexlify(data)
        else:
            result = data

        return result

    @staticmethod
    def bytes_to_hex_string(data: bytes):
        hex_data = hexlify(data)
        str_data = hex_data.decode(encoding='utf-8')
        # returns data in form 'AA BB 00 CC ...'
        return ' '.join(a + b for a, b in zip(str_data, str_data))
