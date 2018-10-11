from .types import Types

import logging


log = logging.getLogger(__name__)


"""
{
"addressFilter":<address> OPTIONAL,
"bnFilter":<uint256> OPTIONAL,
"abiFilters": OPTIONAL
    [
        {
            name STRING REQUIRED
            rvalue HEXSTR OR INT REQUIRED
            type STRING REQUIRED
            op STRING REQUIRED
        }
    ]
}
"""
#all and logic mapped
class EventFilter(object):
    __slots__=["_abiFilters","_bnFilter","_addressFilter","_callback"]

    def __init__(self,fltr,callback):
        self._callback = callback
        bf = fltr.get("bnFilter",None)
        self._bnFilter = BNFilter(bf) if bf else None
        af = fltr.get("addressFilter",None)
        self._addressFilter = AddressFilter(af) if af else None
        self._abiFilters = [ABIFilter(f) for f in fltr.get("abiFilters",[])]

    @property
    def topic(self):
        return self._topic

    async def test(self, event_log, event):
        if self._abiFilters:
            abitest = all([filtr.test(event) for filtr in self._abiFilters])
        else:
            abitest = True
        addrtest = self._addressFilter.test(event_log.address) if self._addressFilter else True
        bntest = self._bnFilter.test(event_log.blockNumber) if self._bnFilter else True
        return all([abitest,addrtest,bntest])

    @property
    def callback(self):
        return self._callback


class AddressFilter(object):
    __slots__=["_value"]
    def __init__(self,value):
        self._value = value

    def test(self,rvalue):
        return self._value == rvalue


class BNFilter(object):
    __slots__=["_rvalue","_op"]

    def __init__(self,rvalue,op):
        self._rvalue = rvalue
        Types.checkUint256(self._rvalue)
        self._op = op
        assert SafeOP.ops(self._op)

    def test(self,event_log):
        test = getattr(SafeOP,self._op)(event_log.blockNumber, self._rvalue)
        assert type(test) is bool
        return test


class ABIFilter(object):
    __slots__=["_rvalue","_op","_name","_type"]
    def __init__(self,fltr):
        self._name = fltr["name"]
        type_factory = getattr(Types,fltr["type"])
        self._rvalue = type_factory(fltr["rvalue"])
        self._type_factory = type_factory
        self._op = fltr["op"]
        assert SafeOP.ops(self._op)

    def test(self,event):
        lvalue = event[self._name]
        lvalue = self._type_factory(lvalue)
        result = getattr(SafeOP,self._op)(event[self._name],self._rvalue)
        return result


class SafeOP(object):
    slots = ['_ops']

    @staticmethod
    def ops(op):
        return op in ['eq','gt','lt','ge','le','ne',]

    @staticmethod
    def eq(a,b):
        return a == b

    @staticmethod
    def gt(a,b):
        return a > b

    @staticmethod
    def lt(a,b):
        return not SafeOP.gt(a,b)

    @staticmethod
    def ge(a,b):
        return SafeOP.gt(a,b) or SafeOP.eq(a,b)

    @staticmethod
    def le(a,b):
        return SafeOP.lt(a,b) or SafeOP.eq(a,b)

    @staticmethod
    def ne(a,b):
        return not SafeOP.eq(a,b)
