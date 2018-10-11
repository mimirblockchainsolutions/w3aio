import binascii
import codecs
from .exceptions import BadLength

class HexTools(object):
    __slots__=[]

    @staticmethod
    def hex_to_bytes(hexstr):
        return hex_to_bytes(hexstr)

    @staticmethod
    def to_hex(string):
        return to_hex(string)

    @staticmethod
    def add0x(hexstr):
        return add0x(hexstr)

    @staticmethod
    def trim0x(hexstr):
        return trim0x(hexstr)

    @staticmethod
    def pad(hexstr):
        return pad(hexstr)

    @staticmethod
    def from_hex(hexstr):
        return from_hex(hexstr)

    @staticmethod
    def bytes_to_hex(b):
        return bytes_to_hex(b)

    @staticmethod
    def bytes_to_string(b):
        return bytes_to_string(b)

bytes_to_string = lambda string: codecs.decode(string)

hex_to_bytes = lambda hexstr: binascii.unhexlify(trim0x(hexstr))

to_hex = lambda string: codecs.decode(binascii.hexlify(codecs.encode(string,'utf-8')))

trim0x = lambda x: '{}'.format(x.replace('0x',''))

add0x = lambda x: '0x{}'.format(x)

pad = lambda obj,length: obj.rjust(length,'0')

from_hex = lambda string: codecs.decode(binascii.unhexlify(string))

bytes_to_hex = lambda string: codecs.decode(binascii.hexlify(string))

def checkHex(h):
    try:
        int(h,16)
    except:
        raise Exception('{} IS NOT PROPERLY HEX ENCODED'.format(h))

def check_length_eq(obj,length):
    try:
        assert len(obj) == length
    except AssertionError:
        raise BadLength
