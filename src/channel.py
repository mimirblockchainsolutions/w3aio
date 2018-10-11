import asyncio as aio
import logging


log = logging.getLogger(__name__)


class Channel(object):
    __slots__=["_event","_request","_response","_exception"]

    def __init__(self,request):
        self._event = aio.Event()
        self._request = request
        self._response = None
        self._exception = None

    async def get(self):
        await self._event.wait()
        if self._exception:
            raise self._exception
        else:
            return self._response

    async def aio_set_response(self,response):
        self.set_response(response)

    def set_response(self,response):
        self._response = response
        self._event.set()

    def set_exception(self, exception):
        self._exception = exception
        self._event.set()

    @property
    def request(self):
        return self._request
