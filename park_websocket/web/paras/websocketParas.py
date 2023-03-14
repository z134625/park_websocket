from parkPro.tools import _Context
from parkPro.utils.paras import Paras


class WebSocketParas(Paras):

    @staticmethod
    def init() -> dict:
        context = _Context({
            'websocket_port': 8679,
        })
        return locals()