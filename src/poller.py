from .types import Types

import asyncio as aio
import logging


log = logging.getLogger(__name__)


class Poller(object):
    __slots__ = ["_eth","_callback","_maxSeenBN","_blocktime","_canary","_loop"]

    def __init__(self, eth, callback, maxSeenBN=1, blocktime=8, loop=None):
        self._loop = loop or aio.get_event_loop()
        self._callback = callback
        self._maxSeenBN = Types.uint256(maxSeenBN)
        self._blocktime = blocktime
        self._eth = eth

    async def run(self):
        self._canary = aio.Event()
        while not self._canary.is_set():
            await aio.sleep(self._blocktime/2)
            try:
                bn = await self._eth.blockNumber()
            except TimeoutError:
                pass
            while self._maxSeenBN <= bn:
                await self._callback(self._maxSeenBN)
                self._maxSeenBN+=Types.uint256(1)

    async def close(self):
        self._canary.set()
