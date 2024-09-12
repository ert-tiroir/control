
import enum
from typing import Literal

class DeviceStatus(enum.Enum):
    ONLINE  = 2
    UNKNOWN = 1
    OFFLINE = 0

class PhysicalDevice:
    def init_channel (self):
        assert False, "Not implemented"
    def get_name (self):
        assert False, "Not implemented"

    def start_transfer (self, buffer: bytes):
        assert False, "Not implemented"
    
    def get_status (self) -> DeviceStatus:
        assert False, "Not implemented"
    
    def stop_thread (self):
        assert False, "Not implemented"
    def start_thread (self, on_receive_end):
        assert False, "Not implemented"