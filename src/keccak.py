from .hextools import hex_to_bytes
from sha3 import keccak_256


keccak = lambda hexstr: '0x{}'.format(keccak_256(hex_to_bytes(hexstr)).hexdigest())
