import asyncio
import websockets
import time
from parkPro.utils import base, api, env
from parkPro import tools
from multiprocessing import Pool


class WebSocket(base.ParkLY):
    _inherit = 'web'

    def main(self):
        func = super().main
        pool = Pool(processes=2)
        pool.apply_async(self.server)
        pool.apply_async(func)
        pool.close()
        pool.join()

    def server(self):
        asyncio.get_event_loop().run_until_complete(
            websockets.serve(self._server, 'localhost', 8765))
        asyncio.get_event_loop().run_forever()

    @staticmethod
    async def _server(websocket, path):
        async for message in websocket:
            message = "I got your message: {}".format(message)
            await websocket.send(message)

            while True:
                t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                if str(t).endswith("0"):
                    await websocket.send(t)
                    break
