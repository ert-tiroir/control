
from typing import Any

from control.contrib.phyc.protocol import create_flush_packet
from control.contrib.protocol.flush import Flushable

class send_to_phyc(Flushable):
    def __init__(self) -> None:
        self.app = None
    def __call__(self, packet) -> Any:
        if self.app is None:
            from control.contrib.phyc.app import PhysicalControllerApplication

            self.app = PhysicalControllerApplication()
        self.app.send(packet)
    def flush(self):
        self( create_flush_packet() )