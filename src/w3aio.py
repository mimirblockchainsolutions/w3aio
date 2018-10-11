from .api import (Eth, Personal)
from .callablecontract import CallableContract
from .filter import Filter
from .hextools import HexTools
from .keccak import keccak
from .poller import Poller
from .soliditykeccak import solidityKeccak
from .structs import Structs
from .types import Types
from .w3json import w3json
from .wstransport import WSTransport
from .channel import Channel

import asyncio as aio
from attrdict import AttrDict
import logging
from functools import partial


log = logging.getLogger(__name__)


async def pipeline(transport,abstract_method,*args,**kwargs):
    abm = abstract_method(*args,**kwargs)
    try:
        response = await transport.call(abm.as_dict())
        #log.debug('Pipeline got response as {}'.format(response))
        abm.set_response(response)
    except Exception as e:
        abm.set_exception(e)
    finally:
        return abm.result

combine = lambda L: { k: v for d in L for k, v in d.items() }

pipe = lambda transport,api: combine([{method:partial(pipeline,transport,getattr(api,method))} for method in dir(api) if method[0] != '_'])


class W3AIO(object):
    __slots__=["_canary","_eth","_personal","_filter","_hextools","_abi","_transport","_poller","_types","_structs","_keccak","_solidityKeccak","_contracts","_callable_contracts"]

    def __init__(self, transport, loop=None):
        self._transport = transport

        self._eth = AttrDict(pipe(self._transport,Eth))
        self._personal = AttrDict(pipe(self._transport,Personal))

        self._filter = Filter(self._eth)
        self._poller = Poller(self._eth, self._filter.on_block)


        self._types = Types
        self._structs = Structs
        self._hextools = HexTools
        self._keccak = keccak
        self._solidityKeccak = solidityKeccak

        self._contracts = {}
        self._callable_contracts = AttrDict({})

    async def __aenter__(self):
        self.run()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    def run(self):
        transport_task = self._transport.run()
        aio.ensure_future(self.monitor([transport_task]))

    async def monitor(self, tasks):
        self._canary = aio.Event()
        tasks.append(self._canary.wait())
        done, pending = await aio.wait(tasks)
        for task in pending:
            await task.cancel()

    def register_contract(self,abi,name):
        contract = Structs.abiContract(abi)
        self._contracts[name] = contract
        self._callable_contracts[name] = CallableContract(self._eth,self._personal,contract)

    def register_event_filter_from_contract(self,contract_name,event_name,filterdictlist,callback):
        contract = self._contracts[contract_name]
        events = contract.events
        event = events[event_name]
        self._filter.set_eventFilter(event,filterdictlist,callback)

    def register_thash_filter(self,thash,callback):
        self._filter.set_thashFilter(thash,callback)

    def register_address_filter(self,address,callback):
        self._filter.set_addressFilter(address,callback)

    def unregister_address_filter(self,address):
        self._filter.set_addressFilter(address,callback)

    async def wait_for_transaction(self, thash, timeout=30):
        channel = Channel(None)
        self.register_thash_filter(thash,channel.aio_set_response)
        return await aio.wait_for(channel.get(),timeout)

    @property
    def keccak(self):
        return self._keccak

    @property
    def solidityKeccak(self):
        return self._solidityKeccak

    @property
    def types(self):
        return self._types

    @property
    def structs(self):
        return self._structs

    @property
    def hextools(self):
        return self._hextools

    @property
    def eth(self):
        return self._eth

    @property
    def contracts(self):
        return self._callable_contracts

    async def start_poller(self):
        aio.ensure_future(self._poller.run())

    async def stop_poller(self):
        await self._poller.close()

    async def close(self):
        try:
            await self._transport.close()
        except:
            pass
        try:
            await self._poller.close()
        except:
            pass
        if not self._canary.is_set():
            self._canary.set()
