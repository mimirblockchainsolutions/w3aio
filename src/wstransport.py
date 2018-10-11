from .channel import Channel

import asyncio as aio
import logging
#TODO cleanup exception importing
import websockets
from websockets.exceptions import *


log = logging.getLogger(__name__)


class MessageError(Exception):
    """
    Indicates exception was raised due to a bad message format.
    """

class ConnectionFailure(Exception):
    """
    This Exception is raised for a failed websocket connection.
    """

"""
These are exceptions that may be ignored and another connection opened
so long as the total failures is below the threshold amount in any given
interval
"""
RECONNECT_EXCEPTIONS = [
    'AbortHandshake',
    'NegotiationError',
    'WebSocketProtocolError',
]


"""
These are the exceptions that should always be raised.
"""
RAISE_EXCEPTIONS = [
    'DuplicateParameter',
    'InvalidState',
    'InvalidHandshake',
    'InvalidStatusCode',
    'InvalidMessage',
    'InvalidHeader',
    'InvalidUpgrade',
    'InvalidHeaderValue',
    'InvalidHeaderFormat',
    'InvalidParameterName',
    'InvalidParameterValue',
    'InvalidURI',
    'InvalidOrigin',
    'PayloadTooBig',
]


"""
This is the connection closed exception. This exception has sub-codes
that determine if this exception may be ignored or should be raised.
"""
BASED_ON_CODE = ['ConnectionClosed']


"""
These are the codes of ConnectionClosed that may be ignored and reconnected.
"""
RECONNECT_CODES = [
    1000, #"OK"
    1001, #"going away"
    1002, #"protocol error"
    1003, #"unsupported type"
    1005, #"no status code [internal]"
    1006, #"connection closed abnormally [internal]"
    1008, #"policy violation"
]


"""
These are the ConnectionClosed codes that should always be raised.
"""
RAISE_CODES = [
    1007, #"invalid data"
    1009, #"message too big"
    1010, #"extension required"
    1011, #"unexpected error"
    1015, #"TLS failure [internal]"
]

HIGHPRIORITY = 1
LOWPRIORITY = 2

class WSTransport(object):
    __slots__ = ["loop","_host","_port","_request_q","_canary","_encoder","_fail_count","_fail_threshold","_restart"]

    def __init__(self, host, port, fail_threshold = 10, restart=True, encoder=None, loop=None):
        self.loop = loop or aio.get_event_loop()
        self._host = host
        self._port = port
        self._request_q = aio.Queue()
        self._encoder = encoder
        self._canary = aio.Event()
        self._fail_count = 0
        self._fail_threshold = 10
        self._restart = restart

    async def close(self):
        log.debug("Websocket close called")
        if not self._canary.is_set():
            self._canary.set()
        await aio.sleep(1)

    async def call(self, msg):
        log.debug("Websocket call with message {}".format(msg))
        channel = Channel(msg)
        await self._request_q.put(channel)
        log.debug("Websocket awaiting channel for msg {}".format(msg))
        return await channel.get()

    def _decrement_fail_counter(self):
        if self._fail_count > 0:
            self._fail_count -=1

    async def _call(self,ws):
        log.debug("Websocket transport on. Running _call")
        while ws.open:
            try:
                self._decrement_fail_counter()
                channel = None
                try:
                    channel = await aio.wait_for(self._request_q.get(),1)
                except aio.TimeoutError:
                    pass
                if channel:
                    channel = channel
                    log.debug("Websocket got object from queue")
                    try:
                        msg = channel.request
                        msg = msg if not self._encoder else self._encoder.dumps(msg)
                    except Exception as e:
                        raise MessageError
                    log.debug("Websocket sending message {}".format(msg))
                    await aio.wait_for(ws.send(msg),15)
                    msg = await aio.wait_for(ws.recv(),15)
                    try:
                        msg = msg if not self._encoder else self._encoder.loads(msg)
                        log.debug("Websocket decoded recv'd msg as {}".format(msg))
                    except Exception as e:
                        raise MessageError
                    channel.set_response(msg)
                    log.debug("Websocket set channel msg as {}".format(msg))
            except MessageError as e:
                log.debug("Websocket MessageError")
                channel.set_exception(MessageError)
            except ConnectionClosed as e:
                if e.code == 1009:
                    channel.set_exception(ConnectionClosed)
                else:
                    await self._request_q.put(channel)
                    raise e
            except Exception as e:
                await self._request_q.put(channel)
                raise e

    async def _monitor(self, tasks):
        self._fail_count = 0
        done, pending = await aio.wait(
        tasks,return_when=aio.FIRST_COMPLETED,)
        for task in pending:
            task.cancel()
        raise ConnectionFailure

    async def run(self):
        if self._restart:
            await self._run_with_restart()
        else:
            await self._run_without_restart()

    async def _run_with_restart(self):
        while not self._canary.is_set():
            await self._handle()

    async def _run_without_restart(self):
        await self._handle()

    async def _handle(self):
        log.debug('WS run called')
        await aio.sleep(1)
        async with websockets.connect('ws://{}:{}'.format(self._host,self._port)) as ws:
            call_task = self._call(ws)
            close_task = self._canary.wait()
            log.debug('WS _canary created')
            try:
                await self._monitor([call_task,close_task])
            except Exception as e:
                log.debug('WS connection lost')
                self._fail_count += 1
                await self._exception_handler(e)

    async def _exception_handler(self, exception):
        log.debug("Websocket exception {}".format(exception))
        if self._restart:
            if self._fail_count >= self._fail_threshold:
                await self.close()
                raise exception
        if exception.__class__.__name__ in RAISE_EXCEPTIONS:
            raise exception
        elif exception.__class__.__name__ in RECONNECT_EXCEPTIONS:
            log.error('Suppressed exception {}. Reconnecting.'.format(str(exception)))
        elif exception.__class__.__name__ in BASED_ON_CODE:
            if exception.code in RAISE_CODES:
                raise exception
            elif exception.__class__.__name__ in RECONNECT_CODES:
                log.error('Suppressed exception {}. Reconnecting.'.format(str(exception)))
            else: #unknown case
                await self.close()
                raise exception
        else: #unknown case
            await self.close()
            raise exception
