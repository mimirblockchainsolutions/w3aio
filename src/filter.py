from .structs import Structs

import asyncio as aio
from functools import partial
import logging


log = logging.getLogger(__name__)


class Filter(object):
    __slots__ = ["_eth","_eventAbis","_eventFilters","_thashFilters","_addressFilters","loop"]

    def __init__(self, eth, loop=None):
        self.loop = loop or aio.get_event_loop()
        self._eth = eth
        self._eventAbis = {}
        self._eventFilters = {}
        self._thashFilters = {}
        self._addressFilters = {}

    @property
    def eventFilters(self):
        return self._eventFilters

    def del_eventFilter(self, topic):
        return self._eventFilters.pop(topic,None)

    def set_eventFilter(self, abi, filterdictlist, callback):
        self._eventFilters[abi.topic] = Structs.eventFilter(filterdictlist,callback)
        self._eventAbis[abi.topic] = abi

    def set_thashFilter(self, t_hash, callback, timeout=30):
        self._thashFilters[t_hash] = partial(self._thash_filter_cleanup, t_hash, callback)

    def set_addressFilter(self, address, callback):
        self._addressFilters[address] = callback

    def del_addressFilter(self, address, callback):
        return self._addressFilters.pop(address,None)

    async def _thash_filter_cleanup(self, t_hash, callback, receipt):
        await callback(receipt)
        self._thashFilters.pop(t_hash,None)

    async def _handle_thash_filters(self, receipts):
        reciept_thashes = [reciept.transactionHash for reciept in receipts]
        for thash in reciept_thashes:
            fltr = self._thashFilters.get(thash,None)
            if fltr:
                log.debug("CALLBACK ABOUT TO HAPPEN")
                await fltr(receipts[reciept_thashes.index(thash)])

    async def _handle_event_filters(self, receipts):
        for reciept in receipts:
            logs = reciept.logs
            for l in logs:
                event_abi = self._eventAbis.get(l.topic,None)
                if event_abi:
                    event = event_abi.decode(l)
                fltr = self._eventFilters.get(l.topic,None)
                if fltr:
                    test_result = await fltr.test(l,event)
                    if test_result:
                        await fltr.callback(event,l)

    async def _handle_address_filters(self,transactions):
        for transaction in transactions:
            frm_cback = self._addressFilters.get(transaction.frm ,None)
            to_cback = self._addressFilters.get(transaction.to ,None)
            if frm_cback:
                await frm_cback(transaction.hash)
            elif to_cback:
                await to_cback(transaction.hash)

    async def on_block(self, blocknumber):
        block = await self._eth.getBlockByNumber(blocknumber)
        receipts = await aio.gather(*[self._eth.getTransactionReceipt(thash) for thash in block.transactions])
        await self._handle_thash_filters(receipts)
        await self._handle_event_filters(receipts)
        transactions = await aio.gather(*[self._eth.getTransactionByHash(thash) for thash in block.transactions])
        await self._handle_address_filters(transactions)
