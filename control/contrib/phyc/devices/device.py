
import enum
from typing import Literal, Tuple

class PhysicalDevice:
    def init_channel (self):
        assert False, "Not implemented"
    def get_name (self):
        assert False, "Not implemented"

    def get_stream_stats (self) -> Tuple[int, int]:
        assert False, "Not implemented"
    def clear_stream_stats (self):
        assert False, "Not implemented"
    def start_transfer (self, buffer: bytes):
        assert False, "Not implemented"
    
    def stop_thread (self):
        assert False, "Not implemented"
    def start_thread (self, on_receive_end):
        assert False, "Not implemented"