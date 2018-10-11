from .hextools import ( check_length_eq,
                        checkHex,
                        pad,
                        to_hex,
                        trim0x, )

from .keccak import keccak
from .soliditykeccak import solidityKeccak
from .exceptions import (BadInitialType, BadComparisonType)

import binascii
import codecs
import logging


log = logging.getLogger(__name__)


#TODO int Types
#TODO fixed types
#TODO bytes
#TODO string
#TODO dynamic?


class Bytes32(object):
    __slots__ = ["_data","_length"]

    def __init__(self, _data):
        self._length = 64
        if type(_data) == bytes:
            self._init_with_bytes(_data)
        elif type(_data) == str:
            self._init_with_string(_data)
        else:
            raise BadInitialType

    def _init_with_string(self,_data):
        _data=trim0x(_data)
        check_length_eq(_data,self._length)
        _data = pad(_data,self._length)
        if type(_data) is str:
            checkHex(_data)
            self._data = _data
        else:
            raise BadInitialType

    def _init_with_bytes(self,_data):
        _data = codecs.decode(binascii.hexlify(_data),'utf-8')
        self._init_with_string(_data)

    def _isinstance(self,other):
        if not self.__class__.__name__ == other.__class__.__name__:
            log.error('TYPE ERROR')
            raise BadComparisonType
        return other

    def as_bytes(self):
        return binascii.unhexlify(self._data)

    def as_str(self):
        return '0x'+self._data

    def as_int(self):
        return int(self._data,16)

    def hash(self):
        _data = keccak(self.as_str())
        return Bytes32(_data)

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return self.as_str()

    def __eq__(self, other):
        other = self._isinstance(other)
        return self.as_int() == other.as_int()

    def __repr__(self):
        return self.as_str()

    def __hash__(self):
        cls_hash = Bytes32(keccak(to_hex(self.__class__.__name__)))
        data_hash = self.hash()
        ident_hash = solidityKeccak([cls_hash,data_hash])
        return int(trim0x(ident_hash),16)

    def replace(self,rep,val):
        return self.as_str().replace(rep,val)

    def encode(self):
        return self.as_bytes()


class Bytes16(object):
    __slots__ = ["_data","_length"]

    def __init__(self, _data):
        self._length = 32
        if type(_data) == bytes:
            self._init_with_bytes(_data)
        elif type(_data) == str:
            self._init_with_string(_data)
        else:
            raise BadInitialType

    def _init_with_string(self,_data):
        _data=trim0x(_data)
        check_length_eq(_data,self._length)
        _data = pad(_data,self._length)
        if type(_data) is str:
            checkHex(_data)
            self._data = _data
        else:
            raise BadInitialType

    def _init_with_bytes(self,_data):
        _data = codecs.decode(binascii.hexlify(_data),'utf-8')
        self._init_with_string(_data)

    def _isinstance(self,other):
        if not self.__class__.__name__ == other.__class__.__name__:
            log.error('TYPE ERROR')
            raise BadComparisonType
        return other

    def as_bytes(self):
        return binascii.unhexlify(self._data)

    def as_str(self):
        return '0x'+self._data

    def as_int(self):
        return int(self._data,16)

    def hash(self):
        _data = keccak(trim0x(self.as_str()))
        return Bytes32(_data)

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return self.as_str()

    def __eq__(self, other):
        other = self._isinstance(other)
        return self.as_int() == other.as_int()

    def __repr__(self):
        return self.as_str()

    def __hash__(self):
        cls_hash = Bytes32(keccak(to_hex(self.__class__.__name__)))
        data_hash = self.hash()
        ident_hash = solidityKeccak([cls_hash,data_hash])
        return int(trim0x(ident_hash),16)

    def replace(self,rep,val):
        return self.as_str().replace(rep,val)

    def encode(self):
        return self.as_bytes()

class Bytes8(object):
    __slots__ = ["_data","_length"]

    def __init__(self, _data):
        self._length = 16
        if type(_data) == bytes:
            self._init_with_bytes(_data)
        elif type(_data) == str:
            self._init_with_string(_data)
        else:
            raise BadInitialType

    def _init_with_string(self,_data):
        _data=trim0x(_data)
        check_length_eq(_data,self._length)
        _data = pad(_data,self._length)
        if type(_data) is str:
            checkHex(_data)
            self._data = _data
        else:
            raise BadInitialType

    def _init_with_bytes(self,_data):
        _data = codecs.decode(binascii.hexlify(_data),'utf-8')
        self._init_with_string(_data)

    def _isinstance(self,other):
        if not self.__class__.__name__ == other.__class__.__name__:
            log.error('TYPE ERROR')
            raise BadComparisonType
        return other

    def as_bytes(self):
        return binascii.unhexlify(self._data)

    def as_str(self):
        return '0x'+self._data

    def as_int(self):
        return int(self._data,16)

    def hash(self):
        _data = keccak(trim0x(self.as_str()))
        return Bytes32(_data)

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return self.as_str()

    def __eq__(self, other):
        other = self._isinstance(other)
        return self.as_int() == other.as_int()

    def __repr__(self):
        return self.as_str()

    def __hash__(self):
        cls_hash = Bytes32(keccak(to_hex(self.__class__.__name__)))
        data_hash = self.hash()
        ident_hash = solidityKeccak([cls_hash,data_hash])
        return int(trim0x(ident_hash),16)

    def replace(self,rep,val):
        return self.as_str().replace(rep,val)

    def encode(self):
        return self.as_bytes()


class Bytes4(object):
    __slots__ = ["_data","_length"]

    def __init__(self, _data):
        self._length = 8
        if type(_data) == bytes:
            self._init_with_bytes(_data)
        elif type(_data) == str:
            self._init_with_string(_data)
        else:
            raise BadInitialType

    def _init_with_string(self,_data):
        _data=trim0x(_data)
        check_length_eq(_data,self._length)
        _data = pad(_data,self._length)
        if type(_data) is str:
            checkHex(_data)
            self._data = _data
        else:
            raise BadInitialType

    def _init_with_bytes(self,_data):
        _data = codecs.decode(binascii.hexlify(_data),'utf-8')
        self._init_with_string(_data)

    def _isinstance(self,other):
        if not self.__class__.__name__ == other.__class__.__name__:
            log.error('TYPE ERROR')
            raise BadComparisonType
        return other

    def as_bytes(self):
        return binascii.unhexlify(self._data)

    def as_str(self):
        return '0x'+self._data

    def as_int(self):
        return int(self._data,16)

    def hash(self):
        _data = keccak(trim0x(self.as_str()))
        return Bytes32(_data)

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return self.as_str()

    def __eq__(self, other):
        other = self._isinstance(other)
        return self.as_int() == other.as_int()

    def __repr__(self):
        return self.as_str()

    def __hash__(self):
        cls_hash = Bytes32(keccak(to_hex(self.__class__.__name__)))
        data_hash = self.hash()
        ident_hash = solidityKeccak([cls_hash,data_hash])
        return int(trim0x(ident_hash),16)

    def replace(self,rep,val):
        return self.as_str().replace(rep,val)

    def encode(self):
        return self.as_bytes()


class Address(object):
    __slots__ = ["_data","_length"]

    def __init__(self, _data):
        self._length = 40
        if type(_data) == bytes:
            self._init_with_bytes(_data)
        elif type(_data) == str:
            self._init_with_string(_data)
        else:
            raise BadInitialType

    def _init_with_string(self,_data):
        _data=trim0x(_data)
        check_length_eq(_data,self._length)
        _data = pad(_data,self._length)
        if type(_data) is str:
            checkHex(_data)
            self._data = _data
        else:
            raise BadInitialType

    def _init_with_bytes(self,_data):
        _data = codecs.decode(binascii.hexlify(_data),'utf-8')
        self._init_with_string(_data)

    def _isinstance(self,other):
        if not self.__class__.__name__ == other.__class__.__name__:
            log.error('TYPE ERROR')
            raise BadComparisonType
        return other

    def as_bytes(self):
        return binascii.unhexlify(self._data)

    def as_str(self):
        return '0x'+self._data

    def as_int(self):
        return int(self._data,16)

    def hash(self):
        _data = keccak(trim0x(self.as_str()))
        return Bytes32(_data)

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return self.as_str()

    def __eq__(self, other):
        other = self._isinstance(other)
        return self.as_int() == other.as_int()

    def __repr__(self):
        return self.as_str()

    def __hash__(self):
        cls_hash = Bytes32(keccak(to_hex(self.__class__.__name__)))
        data_hash = self.hash()
        ident_hash = solidityKeccak([cls_hash,data_hash])
        return int(trim0x(ident_hash),16)

    def replace(self,rep,val):
        return self.as_str().replace(rep,val)

    def encode(self):
        return self.as_str()

class Uint256(object):
    __slots__ = ["_data","_length"]

    def __init__(self, _data):
        self._length = 64
        if type(_data) == bytes:
            self._init_with_bytes(_data)
        elif type(_data) == str:
            self._init_with_string(_data)
        elif type(_data) == int:
            self._init_with_int(_data)
        else:
            raise BadInitialType
        assert self.as_int()< 2**(int(self._length*4)),"Number too large."
        assert self.as_int()>= 0,"Unsigned means positive. Try again."

    def _init_with_string(self,_data):
        _data=trim0x(_data)
        _data = pad(_data,self._length)
        if type(_data) is str:
            checkHex(_data)
            self._data = _data
        else:
            raise BadInitialType

    def _init_with_bytes(self,_data):
        _data = codecs.decode(binascii.hexlify(_data),'utf-8')
        self._init_with_string(_data)

    def _init_with_int(self,_data):
        _data = hex(_data)
        _data = trim0x(_data)
        _data = pad(_data,self._length)
        self._init_with_string(_data)

    def _isinstance(self,other):
        if not self.__class__.__name__ == other.__class__.__name__:
            log.error('TYPE ERROR')
            raise BadComparisonType
        return other

    def as_int(self):
        return int(self._data,16)

    def as_bytes(self):
        return binascii.unhexlify(self._data)

    def as_str(self):
        return '0x'+self._data

    def hash(self):
        _data = keccak(trim0x(self.as_str()))
        return Bytes32(_data)

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return self.as_str()

    def __eq__(self, other):
        other = self._isinstance(other)
        return self.as_int() == other.as_int()

    def __le__(self, other):
        other = self._isinstance(other)
        return self.as_int() <= other.as_int()

    def __ge__(self, other):
        other = self._isinstance(other)
        return self.as_int() >= other.as_int()

    def __gt__(self, other):
        other = self._isinstance(other)
        return self.as_int() > other.as_int()

    def __lt__(self, other):
        other = self._isinstance(other)
        return self.as_int() < other.as_int()

    def __add__(self, other):
        other = self._isinstance(other)
        out = other.as_int()+self.as_int()
        return self._build(out)

    def __sub__(self, other):
        other = self._isinstance(other)
        out = other.as_int()-self.as_int()
        return self._build(out)

    def __mul__(self, other):
        other = self._isinstance(other)
        out = other.as_int() * self.as_int()
        return self._build(out)

    def _build(self,_data):
        return type(self)(_data)

    def __repr__(self):
        return self.as_str()

    def __hash__(self):
        cls_hash = Bytes32(keccak(to_hex(self.__class__.__name__)))
        data_hash = self.hash()
        ident_hash = solidityKeccak([cls_hash,data_hash])
        return int(trim0x(ident_hash),16)

    def __index__(self):
        return self.as_int()

    def replace(self,rep,val):
        return self.as_str().replace(rep,val)

    def encode(self):
        return self.as_int()


class Uint128(object):
    __slots__ = ["_data","_length"]

    def __init__(self, _data):
        self._length = 2
        if type(_data) == bytes:
            self._init_with_bytes(_data)
        elif type(_data) == str:
            self._init_with_string(_data)
        elif type(_data) == int:
            self._init_with_int(_data)
        else:
            raise BadInitialType
        assert self.as_int()< 2**(int(self._length*4)),"Number too large."
        assert self.as_int()>= 0,"Unsigned means positive. Try again."

    def _init_with_string(self,_data):
        _data=trim0x(_data)
        _data = pad(_data,self._length)
        if type(_data) is str:
            checkHex(_data)
            self._data = _data
        else:
            raise BadInitialType

    def _init_with_bytes(self,_data):
        _data = codecs.decode(binascii.hexlify(_data),'utf-8')
        self._init_with_string(_data)

    def _init_with_int(self,_data):
        _data = hex(_data)
        _data = trim0x(_data)
        _data = pad(_data,self._length)
        self._init_with_string(_data)

    def _isinstance(self,other):
        if not self.__class__.__name__ == other.__class__.__name__:
            log.error('TYPE ERROR')
            raise BadComparisonType
        return other

    def as_int(self):
        return int(self._data,16)

    def as_bytes(self):
        return binascii.unhexlify(self._data)

    def as_str(self):
        return '0x'+self._data

    def hash(self):
        _data = keccak(trim0x(self.as_str()))
        return Bytes32(_data)

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return self.as_str()

    def __eq__(self, other):
        other = self._isinstance(other)
        return self.as_int() == other.as_int()

    def __le__(self, other):
        other = self._isinstance(other)
        return self.as_int() <= other.as_int()

    def __ge__(self, other):
        other = self._isinstance(other)
        return self.as_int() >= other.as_int()

    def __gt__(self, other):
        other = self._isinstance(other)
        return self.as_int() > other.as_int()

    def __lt__(self, other):
        other = self._isinstance(other)
        return self.as_int() < other.as_int()

    def __add__(self, other):
        other = self._isinstance(other)
        out = other.as_int()+self.as_int()
        return self._build(out)

    def __sub__(self, other):
        other = self._isinstance(other)
        out = other.as_int()-self.as_int()
        return self._build(out)

    def __mul__(self, other):
        other = self._isinstance(other)
        out = other.as_int() * self.as_int()
        return self._build(out)

    def _build(self,_data):
        return type(self)(_data)

    def __repr__(self):
        return self.as_str()

    def __hash__(self):
        cls_hash = Bytes32(keccak(to_hex(self.__class__.__name__)))
        data_hash = self.hash()
        ident_hash = solidityKeccak([cls_hash,data_hash])
        return int(trim0x(ident_hash),16)

    def __index__(self):
        return self.as_int()

    def replace(self,rep,val):
        return self.as_str().replace(rep,val)

    def encode(self):
        return self.as_int()


class Uint64(object):
    __slots__ = ["_data","_length"]

    def __init__(self, _data):
        self._length = 16
        if type(_data) == bytes:
            self._init_with_bytes(_data)
        elif type(_data) == str:
            self._init_with_string(_data)
        elif type(_data) == int:
            self._init_with_int(_data)
        else:
            raise BadInitialType
        assert self.as_int()< 2**(int(self._length*4)),"Number too large."
        assert self.as_int()>= 0,"Unsigned means positive. Try again."

    def _init_with_string(self,_data):
        _data=trim0x(_data)
        _data = pad(_data,self._length)
        if type(_data) is str:
            checkHex(_data)
            self._data = _data
        else:
            raise BadInitialType

    def _init_with_bytes(self,_data):
        _data = codecs.decode(binascii.hexlify(_data),'utf-8')
        self._init_with_string(_data)

    def _init_with_int(self,_data):
        _data = hex(_data)
        _data = trim0x(_data)
        _data = pad(_data,self._length)
        self._init_with_string(_data)

    def _isinstance(self,other):
        if not self.__class__.__name__ == other.__class__.__name__:
            log.error('TYPE ERROR')
            raise BadComparisonType
        return other

    def as_int(self):
        return int(self._data,16)

    def as_bytes(self):
        return binascii.unhexlify(self._data)

    def as_str(self):
        return '0x'+self._data

    def hash(self):
        _data = keccak(trim0x(self.as_str()))
        return Bytes32(_data)

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return self.as_str()

    def __eq__(self, other):
        other = self._isinstance(other)
        return self.as_int() == other.as_int()

    def __le__(self, other):
        other = self._isinstance(other)
        return self.as_int() <= other.as_int()

    def __ge__(self, other):
        other = self._isinstance(other)
        return self.as_int() >= other.as_int()

    def __gt__(self, other):
        other = self._isinstance(other)
        return self.as_int() > other.as_int()

    def __lt__(self, other):
        other = self._isinstance(other)
        return self.as_int() < other.as_int()

    def __add__(self, other):
        other = self._isinstance(other)
        out = other.as_int()+self.as_int()
        return self._build(out)

    def __sub__(self, other):
        other = self._isinstance(other)
        out = other.as_int()-self.as_int()
        return self._build(out)

    def __mul__(self, other):
        other = self._isinstance(other)
        out = other.as_int() * self.as_int()
        return self._build(out)

    def _build(self,_data):
        return type(self)(_data)

    def __repr__(self):
        return self.as_str()

    def __hash__(self):
        cls_hash = Bytes32(keccak(to_hex(self.__class__.__name__)))
        data_hash = self.hash()
        ident_hash = solidityKeccak([cls_hash,data_hash])
        return int(trim0x(ident_hash),16)

    def __index__(self):
        return self.as_int()

    def replace(self,rep,val):
        return self.as_str().replace(rep,val)

    def encode(self):
        return self.as_int()


class Uint32(object):
    __slots__ = ["_data","_length"]

    def __init__(self, _data):
        self._length = 8
        if type(_data) == bytes:
            self._init_with_bytes(_data)
        elif type(_data) == str:
            self._init_with_string(_data)
        elif type(_data) == int:
            self._init_with_int(_data)
        else:
            raise BadInitialType
        assert self.as_int()< 2**(int(self._length*4)),"Number too large."
        assert self.as_int()>= 0,"Unsigned means positive. Try again."

    def _init_with_string(self,_data):
        _data=trim0x(_data)
        _data = pad(_data,self._length)
        if type(_data) is str:
            checkHex(_data)
            self._data = _data
        else:
            raise BadInitialType

    def _init_with_bytes(self,_data):
        _data = codecs.decode(binascii.hexlify(_data),'utf-8')
        self._init_with_string(_data)

    def _init_with_int(self,_data):
        _data = hex(_data)
        _data = trim0x(_data)
        _data = pad(_data,self._length)
        self._init_with_string(_data)

    def _isinstance(self,other):
        if not self.__class__.__name__ == other.__class__.__name__:
            log.error('TYPE ERROR')
            raise BadComparisonType
        return other

    def as_int(self):
        return int(self._data,16)

    def as_bytes(self):
        return binascii.unhexlify(self._data)

    def as_str(self):
        return '0x'+self._data

    def hash(self):
        _data = keccak(trim0x(self.as_str()))
        return Bytes32(_data)

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return self.as_str()

    def __eq__(self, other):
        other = self._isinstance(other)
        return self.as_int() == other.as_int()

    def __le__(self, other):
        other = self._isinstance(other)
        return self.as_int() <= other.as_int()

    def __ge__(self, other):
        other = self._isinstance(other)
        return self.as_int() >= other.as_int()

    def __gt__(self, other):
        other = self._isinstance(other)
        return self.as_int() > other.as_int()

    def __lt__(self, other):
        other = self._isinstance(other)
        return self.as_int() < other.as_int()

    def __add__(self, other):
        other = self._isinstance(other)
        out = other.as_int()+self.as_int()
        return self._build(out)

    def __sub__(self, other):
        other = self._isinstance(other)
        out = other.as_int()-self.as_int()
        return self._build(out)

    def __mul__(self, other):
        other = self._isinstance(other)
        out = other.as_int() * self.as_int()
        return self._build(out)

    def _build(self,_data):
        return type(self)(_data)

    def __repr__(self):
        return self.as_str()

    def __hash__(self):
        cls_hash = Bytes32(keccak(to_hex(self.__class__.__name__)))
        data_hash = self.hash()
        ident_hash = solidityKeccak([cls_hash,data_hash])
        return int(trim0x(ident_hash),16)

    def __index__(self):
        return self.as_int()

    def replace(self,rep,val):
        return self.as_str().replace(rep,val)

    def encode(self):
        return self.as_int()


class Uint16(object):
    __slots__ = ["_data","_length"]

    def __init__(self, _data):
        self._length = 4
        if type(_data) == bytes:
            self._init_with_bytes(_data)
        elif type(_data) == str:
            self._init_with_string(_data)
        elif type(_data) == int:
            self._init_with_int(_data)
        else:
            raise BadInitialType
        assert self.as_int()< 2**(int(self._length*4)),"Number too large."
        assert self.as_int()>= 0,"Unsigned means positive. Try again."

    def _init_with_string(self,_data):
        _data=trim0x(_data)
        _data = pad(_data,self._length)
        if type(_data) is str:
            checkHex(_data)
            self._data = _data
        else:
            raise BadInitialType

    def _init_with_bytes(self,_data):
        _data = codecs.decode(binascii.hexlify(_data),'utf-8')
        self._init_with_string(_data)

    def _init_with_int(self,_data):
        _data = hex(_data)
        _data = trim0x(_data)
        _data = pad(_data,self._length)
        self._init_with_string(_data)

    def _isinstance(self,other):
        if not self.__class__.__name__ == other.__class__.__name__:
            log.error('TYPE ERROR')
            raise BadComparisonType
        return other

    def as_int(self):
        return int(self._data,16)

    def as_bytes(self):
        return binascii.unhexlify(self._data)

    def as_str(self):
        return '0x'+self._data

    def hash(self):
        _data = keccak(trim0x(self.as_str()))
        return Bytes32(_data)

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return self.as_str()

    def __eq__(self, other):
        other = self._isinstance(other)
        return self.as_int() == other.as_int()

    def __le__(self, other):
        other = self._isinstance(other)
        return self.as_int() <= other.as_int()

    def __ge__(self, other):
        other = self._isinstance(other)
        return self.as_int() >= other.as_int()

    def __gt__(self, other):
        other = self._isinstance(other)
        return self.as_int() > other.as_int()

    def __lt__(self, other):
        other = self._isinstance(other)
        return self.as_int() < other.as_int()

    def __add__(self, other):
        other = self._isinstance(other)
        out = other.as_int()+self.as_int()
        return self._build(out)

    def __sub__(self, other):
        other = self._isinstance(other)
        out = other.as_int()-self.as_int()
        return self._build(out)

    def __mul__(self, other):
        other = self._isinstance(other)
        out = other.as_int() * self.as_int()
        return self._build(out)

    def _build(self,_data):
        return type(self)(_data)

    def __repr__(self):
        return self.as_str()

    def __hash__(self):
        cls_hash = Bytes32(keccak(to_hex(self.__class__.__name__)))
        data_hash = self.hash()
        ident_hash = solidityKeccak([cls_hash,data_hash])
        return int(trim0x(ident_hash),16)

    def __index__(self):
        return self.as_int()

    def replace(self,rep,val):
        return self.as_str().replace(rep,val)

    def encode(self):
        return self.as_int()

class Uint8(object):
    __slots__ = ["_data","_length"]

    def __init__(self, _data):
        self._length = 2
        if type(_data) == bytes:
            self._init_with_bytes(_data)
        elif type(_data) == str:
            self._init_with_string(_data)
        elif type(_data) == int:
            self._init_with_int(_data)
        else:
            raise BadInitialType
        assert self.as_int()< 2**(int(self._length*4)),"Number too large."
        assert self.as_int()>= 0,"Unsigned means positive. Try again."

    def _init_with_string(self,_data):
        _data=trim0x(_data)
        _data = pad(_data,self._length)
        if type(_data) is str:
            checkHex(_data)
            self._data = _data
        else:
            raise BadInitialType

    def _init_with_bytes(self,_data):
        _data = codecs.decode(binascii.hexlify(_data),'utf-8')
        self._init_with_string(_data)

    def _init_with_int(self,_data):
        _data = hex(_data)
        _data = trim0x(_data)
        _data = pad(_data,self._length)
        self._init_with_string(_data)

    def _isinstance(self,other):
        if not self.__class__.__name__ == other.__class__.__name__:
            log.error('TYPE ERROR')
            raise BadComparisonType
        return other

    def as_int(self):
        return int(self._data,16)

    def as_bytes(self):
        return binascii.unhexlify(self._data)

    def as_str(self):
        return '0x'+self._data

    def hash(self):
        _data = keccak(trim0x(self.as_str()))
        return Bytes32(_data)

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return self.as_str()

    def __eq__(self, other):
        other = self._isinstance(other)
        return self.as_int() == other.as_int()

    def __le__(self, other):
        other = self._isinstance(other)
        return self.as_int() <= other.as_int()

    def __ge__(self, other):
        other = self._isinstance(other)
        return self.as_int() >= other.as_int()

    def __gt__(self, other):
        other = self._isinstance(other)
        return self.as_int() > other.as_int()

    def __lt__(self, other):
        other = self._isinstance(other)
        return self.as_int() < other.as_int()

    def __add__(self, other):
        other = self._isinstance(other)
        out = other.as_int()+self.as_int()
        return self._build(out)

    def __sub__(self, other):
        other = self._isinstance(other)
        out = other.as_int()-self.as_int()
        return self._build(out)

    def __mul__(self, other):
        other = self._isinstance(other)
        out = other.as_int() * self.as_int()
        return self._build(out)

    def _build(self,_data):
        return type(self)(_data)

    def __repr__(self):
        return self.as_str()

    def __hash__(self):
        cls_hash = Bytes32(keccak(to_hex(self.__class__.__name__)))
        data_hash = self.hash()
        ident_hash = solidityKeccak([cls_hash,data_hash])
        return int(trim0x(ident_hash),16)

    def __index__(self):
        return self.as_int()

    def replace(self,rep,val):
        return self.as_str().replace(rep,val)

    def encode(self):
        return self.as_int()
