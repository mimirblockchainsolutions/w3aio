from .types import Types
from .hextools import checkHex

import logging


log = logging.getLogger(__name__)



class Error(object):
    __slots__=["_message","_code"]
    def __init__(self,error):
        self._message = error["message"]
        self._code = error["code"]

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._message


class Response(object):
    __slots__=["_id","_result","_error","_method"]
    def __init__(self, response):
        if "error" in response:
            self._id = response["id"]
            self._result = None
            self._error = Error(response["error"])
            self._method = None
        else:
            if response["id"]:
                self._id = response["id"]
                self._result = response["result"]
                self._error = None
                self._method = None


    @property
    def result(self):
        return self._result

    @property
    def error(self):
        return self._error

    @property
    def id(self):
        return self._id

    @property
    def method(self):
        return self._method

    def as_dict(self):
        values = [getattr(self,v) for v in self.__slots__]
        names = [n[1:] for n in self.__slots__]
        return dict(zip(names, values))


class Block(object):
    __slots__=[ "_number","_hash","_parentHash","_sealFields","_sha3Uncles",
                "_logsBloom","_transactionsRoot","_stateRoot","_miner",
                "_difficulty","_totalDifficulty","_extraData","_size",
                "_gasLimit","_minGasPrice","_gasUsed","_timestamp",
                "_transactions","_uncles",]
    def __init__(self,block):
        self._number = Types.uint256(block["number"])
        self._hash = Types.bytes32(block["hash"])
        self._parentHash = Types.bytes32(block["parentHash"])
        self._sealFields = block["sealFields"]
        self._sha3Uncles = Types.bytes32(block["sha3Uncles"])
        self._logsBloom = block["logsBloom"]
        self._transactionsRoot = Types.bytes32(block["transactionsRoot"])
        self._stateRoot = Types.bytes32(block["stateRoot"])
        self._miner = Types.address(block["miner"])
        self._difficulty = Types.uint256(block["difficulty"])
        self._totalDifficulty = Types.uint256(block["totalDifficulty"])
        self._extraData = block["extraData"]
        self._size = Types.uint256(block["size"])
        self._gasLimit = Types.uint256(block["gasLimit"])
        self._gasUsed = Types.uint256(block["gasUsed"])
        self._timestamp = Types.uint256(block["timestamp"])
        self._transactions = [Types.bytes32(t) for t in block["transactions"]]
        self._uncles = [Types.bytes32(uncle) for uncle in block["uncles"]]

    @property
    def number(self):
        return self._number

    @property
    def hash(self):
        return self._hash

    @property
    def parentHash(self):
        return self._parentHash

    @property
    def sealFields(self):
        return self._sealFields

    @property
    def logsBloom(self):
        return self._logsBloom

    @property
    def transactionsRoot(self):
        return self._transactionsRoot

    @property
    def stateRoot(self):
        return self._stateRoot

    @property
    def miner(self):
        return self._miner

    @property
    def difficulty(self):
        return self._difficulty

    @property
    def totalDifficulty(self):
        return self._totalDifficulty

    @property
    def extraData(self):
        return self._extraData

    @property
    def size(self):
        return self._size

    @property
    def gasLimit(self):
        return self._gasLimit

    @property
    def minGasPrice(self):
        return self._minGasPrice

    @property
    def gasUsed(self):
        return self._gasUsed

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def transactions(self):
        return self._transactions

    @property
    def uncles(self):
        return self._uncles

    def as_dict(self):
        values = [getattr(self,v) for v in self.__slots__]
        names = [n[1:] for n in self.__slots__]
        return dict(zip(names, values))


class TransactionReceipt(object):
    __slots__=[ "_blockHash","_blockNumber","_contractAddress",
                "_gasUsed","_logs","_logsBloom","_root",
                "_status","_transactionHash","_transactionIndex"]
    def __init__(self,receipt):
        self._blockHash = Types.bytes32(receipt["blockHash"])
        self._blockNumber = Types.uint256(receipt["blockNumber"])
        contractAddress = receipt["contractAddress"]
        if contractAddress:
            self._contractAddress = Types.address(contractAddress)
        else:
            self._contractAddress = Types.address('0x0000000000000000000000000000000000000000')
        self._gasUsed = Types.uint256(receipt["gasUsed"])
        self._logs = [Log(l) for l in receipt["logs"]]
        self._logsBloom = receipt["logsBloom"]
        self._root = receipt.get("root",None)
        self._status = receipt.get("status",None)
        self._transactionHash = Types.bytes32(receipt["transactionHash"])
        self._transactionIndex = Types.uint256(receipt["transactionIndex"])

    @property
    def blockHash(self):
        return self._blockHash

    @property
    def contractaddress(self):
        return self._contractaddress

    @property
    def cumalitiveGasUsed(self):
        return self._cumalitiveGasUsed

    @property
    def gasUsed(self):
        return self._gasUsed

    @property
    def logs(self):
        return self._logs

    @property
    def logsBloom(self):
        return self._logsBloom

    @property
    def root(self):
        return self._root

    @property
    def status(self):
        return self._status

    @property
    def transactionHash(self):
        return self._transactionHash

    @property
    def transactionIndex(self):
        return self._transactionIndex

    def as_dict(self):
        values = [getattr(self,v) for v in self.__slots__]
        names = [n[1:] for n in self.__slots__]
        return dict(zip(names, values))


class TransactionObject(object):
    __slots__=["_to","_frm","_data","_value","_gas"]
    def __init__(self, to, frm, data, value, gas):
        Types.addressCheck(to)
        self._to = to
        if frm:
            Types.addressCheck(frm)
        self._frm = frm
        if data:
            checkHex(data)
        self._data = data
        if value:
            Types.uint256Check(value)
        self._gas = gas
        self._value = value

    @property
    def to(self):
        return self._to

    @property
    def frm(self):
        return self._from

    @property
    def data(self):
        return self._data

    @property
    def value(self):
        return self._value

    @property
    def gas(self):
        return self._gas

    def as_dict(self):
        nv = [(name,getattr(self,name)) for name in self.__slots__]
        d = {tup[0][1:]:tup[1] for tup in nv if tup[1]}
        if d.get("frm",None):
            frm = d["frm"]
            del d["frm"]
            d["from"] = frm
        return d


class Transaction(object):
    __slots__=[ "_hash","_nonce","_blockHash","_blockNumber","_transactionIndex",
    "_from","_to","_value","_gas","_gasPrice","_input"]
    def __init__(self,transaction):
        self._hash = Types.bytes32(transaction["hash"])
        self._nonce = Types.uint256(transaction["nonce"])
        self._blockHash = Types.bytes32(transaction["blockHash"])
        self._blockNumber = Types.uint256(transaction["blockNumber"])
        self._transactionIndex = Types.uint256(transaction["transactionIndex"])
        if transaction["from"]:
            self._from = Types.address(transaction["from"])
        else:
            self._from = Types.address('0x0000000000000000000000000000000000000000')
        if transaction["to"]:
            self._to = Types.address(transaction["to"])
        else:
            self._to = Types.address('0x0000000000000000000000000000000000000000')
        self._value = Types.uint256(transaction["value"])
        self._gas = Types.uint256(transaction["gas"])
        self._gasPrice = Types.uint256(transaction["gasPrice"])
        self._input = transaction["input"]

    @property
    def hash(self):
        return self._hash

    @property
    def nonce(self):
        return self._nonce

    @property
    def blockHash(self):
        return self.blockHash

    @property
    def blockNumber(self):
        return self.blockNumber

    @property
    def transactionIndex(self):
        return self.transactionIndex

    @property
    def frm(self):
        return self._from

    @property
    def to(self):
        return self._to

    @property
    def values(self):
        return self._values

    @property
    def gas(self):
        return self._gas

    @property
    def gasPrice(self):
        return self._gasPrice

    @property
    def input(self):
        return self._input

    def as_dict(self):
        values = [getattr(self,v) for v in self.__slots__]
        names = [n[1:] for n in self.__slots__]
        return dict(zip(names, values))


class Syncing(object):
    __slots__=["_startingBlock","_currentBlock","_highestBlock"]
    def __init__(self,result):
        self._startingBlock = Types.uint256(result["startingBlock"])
        self._currentBlock = Types.uint256(result["currentBlock"])
        self._highestBlock = Types.uint256(result["highestBlock"])

    @property
    def startingBlock(self):
        return self._startingBlock

    @property
    def currentBlock(self):
        return self._currentBlock

    @property
    def highestBlock(self):
        return self._highestBlock

    def as_dict(self):
        values = [getattr(self,v) for v in self.__slots__]
        names = [n[1:] for n in self.__slots__]
        return dict(zip(names, values))


class Log(object):
    __slots__=[ "_address","_blockHash","_blockNumber","_data","_logIndex",
                "_topics","_transactionHash","_transactionIndex",
                "_transactionLogIndex","_type"]
    def __init__(self,log):
        self._address = Types.address(log["address"])
        self._blockHash = Types.bytes32(log["blockHash"])
        self._blockNumber = Types.uint256(log["blockNumber"])
        self._data = log["data"]
        self._logIndex = Types.uint256(log["logIndex"])
        self._topics = log["topics"]
        if len(self._topics) > 0:
            self._topics[0] = Types.bytes32(self.topics[0])
        else:
            self._topics = [Types.bytes32(0)]
        self._transactionHash = Types.bytes32(log["transactionHash"])
        self._transactionIndex = Types.uint256(log["transactionIndex"])
        self._transactionLogIndex = Types.uint256(log["transactionLogIndex"])
        self._type = log["type"]

    @property
    def topic(self):
        return self.topics[0]

    @property
    def address(self):
        return self._address

    @property
    def blockHash(self):
        return self._blockHash

    @property
    def blockNumber(self):
        return self._blockNumber

    @property
    def data(self):
        return self._data

    @property
    def logIndex(self):
        return self._logIndex

    @property
    def topics(self):
        return self._topics

    @property
    def transactionHash(self):
        return self._transactionHash

    @property
    def transactionIndex(self):
        return self._transactionIndex

    @property
    def transactionLogIndex(self):
        return self._transactionLogIndex

    @property
    def type_(self):
        return self._type

    def parseLog(self,abi):
        return ParsedLog(self,abi)

    def as_dict(self):
        values = [getattr(self,v) for v in self.__slots__]
        names = [n[1:] for n in self.__slots__]
        return dict(zip(names, values))
