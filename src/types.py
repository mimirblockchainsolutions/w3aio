from .solidity_types import (   Address,
                                Bytes4,
                                Bytes8,
                                Bytes16,
                                Bytes32,
                                Uint8,
                                Uint16,
                                Uint32,
                                Uint64,
                                Uint128,
                                Uint256, )

class Types(object):
    __slots__ = []

    @staticmethod
    def safeLookup(name):
        safeList = [t for t in dir(Types) if t[0] != '_']
        if name in safeList:
            return getattr(Types,name)
        else:
            raise AttributeError

    @staticmethod
    def uint(data):
        return Uint256(data)

    @staticmethod
    def uint256(data):
        return Uint256(data)

    @staticmethod
    def uint128(data):
        return Uint128(data)

    @staticmethod
    def uint64(data):
        return Uint64(data)

    @staticmethod
    def uint32(data):
        return Uint32(data)

    @staticmethod
    def uint16(data):
        return Uint16(data)

    @staticmethod
    def uint8(data):
        return Uint8(data)

    @staticmethod
    def bytes32(data):
        return Bytes32(data)

    @staticmethod
    def bytes16(data):
        return Bytes16(data)

    @staticmethod
    def bytes8(data):
        return Bytes8(data)

    @staticmethod
    def bytes4(data):
        return Bytes4(data)

    @staticmethod
    def address(data):
        return Address(data)

    @staticmethod
    def addressCheck(x):
        assert isinstance(x, Address),'{} must be instance address'.format(x)

    @staticmethod
    def uint256Check(x):
        assert isinstance(x, Uint256), '{} must be instance uint256'.format(x)

    @staticmethod
    def uint128Check(x):
        assert isinstance(x, Uint128), '{} must be instance uint128'.format(x)

    @staticmethod
    def uint64Check(x):
        assert isinstance(x, Uint64), '{} must be instance uint64'.format(x)

    @staticmethod
    def uint32Check(x):
        assert isinstance(x, Uint32), '{} must be instance uint32'.format(x)

    @staticmethod
    def uint16Check(x):
        assert isinstance(x, Uint16), '{} must be instance uint16'.format(x)

    @staticmethod
    def uint8Check(x):
        assert isinstance(x, Uint8), '{} must be instance uint8'.format(x)

    @staticmethod
    def bytes32Check(x):
        assert isinstance(x, Bytes32), '{} must be instance bytes32'.format(x)

    @staticmethod
    def bytes16Check(x):
        assert isinstance(x, Bytes16), '{} must be instance bytes16'.format(x)

    @staticmethod
    def bytes8Check(x):
        assert isinstance(x, Bytes8), '{} must be instance bytes8'.format(x)

    @staticmethod
    def bytes4Check(x):
        assert isinstance(x, Bytes4), '{} must be instance bytes4'.format(x)
