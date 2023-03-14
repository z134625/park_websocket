import asyncio
from typing import Union, List, Tuple

import websockets
import time
from parkPro.utils import base, api, env
from parkPro import tools
from multiprocessing import Pool, Process
from .paras import WebSocketParas


async def _server(websocket, path):
    async for message in websocket:
        message = "I got your message: {}".format(message)
        await websocket.send(message)

        while True:
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            if str(t).endswith("0"):
                await websocket.send(t)
                break


def server(host, port):
    asyncio.get_event_loop().run_until_complete(
        websockets.serve(_server, host, port))
    asyncio.get_event_loop().run_forever()


class WebSocket(base.ParkLY):
    _inherit = 'web'
    paras = WebSocketParas()

    @api.command(
        keyword=['--websocket-port'],
        name='websocket_port',
        unique=True,
        priority=0
    )
    def websocket_port(
            self,
            port: int = 8679
    ) -> None:
        self.context.websocket_port = int(port)

    def main(
            self,
            _commands: Union[List[str], Tuple[str], None] = None,
            delay: Union[int, None] = None,
            epoch_show: bool = True
    ) -> None:
        p = Process(target=server, args=(self.context.host, self.context.websocket_port))
        p.start()
        super().main(_commands, delay, epoch_show)
