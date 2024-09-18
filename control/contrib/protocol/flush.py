
from typing import Any

from control.contrib.protocol.fields.packet import MultiField


class Flushable:
    def __call__(self, packet: MultiField) -> Any:
        pass
    def flush (self):
        pass

class send_to_void(Flushable):
    pass
