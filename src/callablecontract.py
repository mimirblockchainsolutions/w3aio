from .abi_structs import ABIContract

import asyncio as aio
import logging


log = logging.getLogger(__name__)


class CallableContract(object):
    __slots__=["_functions_by_selector","_functions_by_name","_eth","_personal"]

    def __init__(self,eth,personal,contract):
        self._functions_by_selector = contract.functions_by_selector
        self._functions_by_name = contract.functions
        self._eth = eth
        self._personal = personal

    @property
    def functions(self):
        return self._functions_by_name

    def f(self, name):
        #if self._functions_by_name.get(name,None) is not None:
        return CallableFunction(self._eth, self._personal, self, name)
        #else:
        #    raise AttributeError


class CallableFunction(object):
    __slots__=["_contract","_eth","_personal","_name"]

    def __init__(self, eth, personal, contract, name):
        self._contract = contract
        self._eth = eth
        self._personal= personal
        self._name = name

    def __call__(self, *args):
        #TODO handle function overloading
        #types = [arg.__class__.__name__.lower() for arg in args]
        #selector = self._contract.select(name,types)
        #function = self._contract._functions_by_selector[selector]
        function = self._contract.functions[self._name]
        log.debug(args)
        calldata = function.encode(args)
        return EncodedCall(self._eth, self._personal, function, calldata)


class EncodedCall(object):
    __slots__ = ["_function","_calldata","_eth","_personal"]

    def __init__(self, eth, personal, function, calldata):
        self._function = function
        self._calldata = calldata
        self._eth = eth
        self._personal = personal

    async def call(self, **kwargs):
        kwargs = dict(kwargs)
        if self._calldata != '0x':
            kwargs.update({"data":self._calldata})
        response = await self._eth.call(**kwargs)
        return self._function.decode(response)

    async def transact(self,**kwargs):
        kwargs = dict(kwargs)
        kwargs.update({"data":self._calldata})
        response = await self._personal.sendTransaction(**kwargs)
        return response
