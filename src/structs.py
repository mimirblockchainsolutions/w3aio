from .method_structs import (   Block,
                                Response,
                                Syncing,
                                Transaction,
                                TransactionObject,
                                TransactionReceipt, )

from .abi_structs import ABIContract
from .filter_structs import EventFilter


class Structs(object):
    __slots__=[]

    @staticmethod
    def block(*args,**kwargs):
        return Block(*args,**kwargs)

    @staticmethod
    def log(*args,**kwargs):
        return Log(*arg,**kwargs)

    @staticmethod
    def transaction(*args,**kwargs):
        return Transaction(*args,**kwargs)

    @staticmethod
    def transactionReceipt(*args,**kwargs):
        return TransactionReceipt(*args,**kwargs)

    @staticmethod
    def syncing(*args,**kwargs):
        return Syncing(*args,**kwargs)

    @staticmethod
    def transactionObject(*args,**kwargs):
        return TransactionObject(*args,**kwargs)

    @staticmethod
    def error(*args,**kwargs):
        return Error(*args,**kwargs)

    @staticmethod
    def response(*args,**kwargs):
        return Response(*args,**kwargs)

    @staticmethod
    def abiContract(*args,**kwargs):
        return ABIContract(*args,**kwargs)

    @staticmethod
    def eventFilter(*args,**kwargs):
        return EventFilter(*args,**kwargs)
