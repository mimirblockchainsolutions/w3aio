from .keccak import keccak


def solidityKeccak(objects):
    hexstring = ''
    for obj in objects:
        hexstring += obj.as_str()
    return keccak(hexstring)
