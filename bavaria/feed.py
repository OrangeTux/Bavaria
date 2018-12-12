import json
import asyncio
import websockets

from bavaria.api.messages import to_dataclass

URL = 'wss://tralis.sbahnm.geops.de/ws'

async def create_feed(url=URL):
    f = Feed(url)
    await f.connect()

    return f

class Feed:
    def __init__(self, url=URL):
        self.url = url

        self.channel = set()

    async def connect(self):
        self._connection = await websockets.connect(self.url)

    async def get(self, channel):
        """ Get current info on channel. """
        await self._connection.send(f'GET {channel}')

    async def subscribe(self, channel):
        """ Subscribe to channel. """
        if channel not in self.channel:
            await self._connection.send(f'SUB {channel}')
            self.channel.add(channel)

    async def disconnect(self):
        await self._connection.disconnect()

    def __aiter__(self):
        return self

    async def __anext__(self):
        msg = await self._connection.recv()
        data = json.loads(msg)

        return to_dataclass(data)
