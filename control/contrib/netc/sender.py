
from typing import Any

from control.contrib.protocol.flush import Flushable

class send_to_netc(Flushable):
    def __init__(self) -> None:
        self.app = None
    def __call__(self, packet) -> Any:
        if self.app is None:
            from control.contrib.netc.app import NetControllerApplication

            self.app = NetControllerApplication()
        self.app.send(packet)
    def flush(self):
        pass