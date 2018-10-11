from .structs import Structs
from .types import Types

from secrets import token_hex
import logging


log = logging.getLogger(__name__)


class Eth(object):
    __slots__=[]

    #works
    @staticmethod
    def syncing():
        method = "eth_syncing"
        params = None
        def set_result(self, result):
            try:
                if result:
                    self._result = Structs.syncing(result)
                else:
                    self._result = False
            except Exception as e:
                self.set_exception(e)
            finally:
                self._complete = True
        return AbstractMethod(set_result, method, params)

    #works
    @staticmethod
    def coinbase():
        method = "eth_coinbase"
        params = None
        def set_result(self, result):
            try:
                self._result = Types.address(result)
            except Exception as e:
                self.set_exception(e)
            finally:
                self._complete = True
        return AbstractMethod(set_result, method, params)

    #works
    @staticmethod
    def gasPrice():
        method = "eth_gasPrice"
        params = None
        def set_result(self, result):
            try:
                self._result = Types.uint256(result)
            except Exception as e:
                self.set_exception(e)
            finally:
                self._complete = True
        return AbstractMethod(set_result, method, params)

    #works
    @staticmethod
    def accounts():
        method = "eth_accounts"
        params = None
        def set_result(self, result):
            try:
                self._result = [Types.address(acct) for acct in result]
            except Exception as e:
                self._exception = e
            finally:
                self._complete = True
        return AbstractMethod(set_result, method, params)

    #works
    @staticmethod
    def blockNumber():
        method = "eth_blockNumber"
        params = None
        def set_result(self, result):
            try:
                self._result = Types.uint256(result)
            except Exception as e:
                self.set_exception(e)
            finally:
                self._complete = True
        return AbstractMethod(set_result, method, params)

    #works
    @staticmethod
    def getBalance(account, block_identifier="latest"):
        method = "eth_getBalance"
        Types.addressCheck(account)
        if block_identifier != 'latest':
            Types.bytes32Check(block_identifier)
        params = [account,block_identifier]
        def set_result(self, result):
            try:
                self._result = Types.uint256(result)
            except Exception as e:
                self.set_exception(e)
            finally:
                self._complete = True
        return AbstractMethod(set_result, method, params)

    #works
    @staticmethod
    def getBlockByHash(block_hash):#, full_transactions=False):
        full_transactions=False #TODO parse full trahsactions
        method = "eth_getBlockByHash"
        Types.bytes32Check(block_hash)
        assert type(full_transactions) is bool, 'full_transactions must be of type bool'
        params = [block_hash,full_transactions]
        def set_result(self, result):
            try:
                self._result = Structs.block(result)
            except Exception as e:
                self.set_exception(e)
            finally:
                self._complete = True
        return AbstractMethod(set_result, method, params)

    #works
    @staticmethod
    def getBlockByNumber(block_number):# full_transactions=False):
        full_transactions=False #TODO parse full trahsactions
        method = "eth_getBlockByNumber"
        Types.uint256Check(block_number)
        assert type(full_transactions) is bool, 'full_transactions must be of type bool'
        params = [block_number,full_transactions]
        def set_result(self, result):
            try:
                self._result = Structs.block(result)
            except Exception as e:
                self.set_exception(e)
            finally:
                self._complete = True
        return AbstractMethod(set_result, method, params)

    #works
    @staticmethod
    def getTransactionByHash(transaction_hash):
        method = "eth_getTransactionByHash"
        Types.bytes32Check(transaction_hash)
        params = [transaction_hash]
        def set_result(self, result):
            try:
                self._result = Structs.transaction(result)
            except Exception as e:
                self.set_exception(e)
            finally:
                self._complete = True
        return AbstractMethod(set_result, method, params)

    #works
    @staticmethod
    def getTransactionReceipt(transaction_hash):
        method = "eth_getTransactionReceipt"
        Types.bytes32Check(transaction_hash)
        params = [transaction_hash]
        def set_result(self, result):
            try:
                self._result = Structs.transactionReceipt(result)
            except Exception as e:
                self.set_exception(e)
            finally:
                self._complete = True
        return AbstractMethod(set_result, method, params)

    @staticmethod
    def sendRawTransaction(raw_transaction):
        method = "eth_sendRawTransaction"
        params = [raw_transaction]
        def set_result(self, result):
            try:
                self._result = Types.bytes32(result)
            except Exception as e:
                self.set_exception(e)
            finally:
                self._complete = True
        return AbstractMethod(set_result, method, params)

    #works
    @staticmethod
    def call(to=None, frm=None, data=None, value=0, gas=None, block_identifier='latest'):
        method = "eth_call"
        assert to, 'MUST DEFINE TO'
        transaction = Structs.transactionObject(to,frm,data,value,gas)
        params = [transaction.as_dict(), block_identifier]
        def set_result(self, result):
            try:
                self._result = result
            except Exception as e:
                self.set_exception(e)
            finally:
                self._complete = True
        return AbstractMethod(set_result, method, params)


class Personal(object):
    __slots__=[]

    @staticmethod
    def sendTransaction(to, frm, password, data=None, value=None, gas=None):
        method = "personal_sendTransaction"
        transaction = Structs.transactionObject(to,frm,data,value, gas)
        params = [transaction.as_dict(), password]
        def set_result(self, result):
            try:
                self._result = Types.bytes32(result)
            except Exception as e:
                self.set_exception(e)
            finally:
                self._complete = True
        return AbstractMethod(set_result, method, params)


class AbstractMethod(object):
    __slots__=["_method","_params","_result","_exception","_complete","_id","_set_result"]

    def __init__(self, set_result_function, method, params):
        self._set_result = set_result_function
        self._method = method
        self._params = params or []
        self._result = None
        self._exception = None
        self._complete = False
        self._id = token_hex(32)

    def set_exception(self, exception):
        self._exception = exception

    def set_result(self, result):
        self._set_result(self, result)

    def set_response(self,response):
        #log.debug('AbstractMethod got response as {}'.format(response))
        response = Structs.response(response)
        if response.error:
            self.set_exception(response.error)
        else:
            self.set_result(response.result)

    @property
    def method(self):
        return self._method

    @property
    def params(self):
        return self._params

    @property
    def id(self):
        return self._id

    @property
    def complete(self):
        return self._complete

    @property
    def result(self):
        if self._exception:
            raise self._exception
        else:
            return self._result

    def as_dict(self):
        return {"jsonrpc":"2.0","method":self._method,"id":self._id,"params":self._params}
