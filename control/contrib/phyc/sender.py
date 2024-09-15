
from typing import Any

class send_to_phyc:
    def __init__(self) -> None:
        self.app = None
    def __call__(self, packet) -> Any:
        if self.app is None:
            from control.contrib.phyc.app import PhysicalControllerApplication

            self.app = PhysicalControllerApplication()
        self.app.send(packet)
