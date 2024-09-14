
from typing import Any, Callable, List, Tuple, Type

from control.contrib.protocol.fields.packet import MultiField

class AbstractDevice:
    def init_device (self):
        assert False, "Not implemented"
    def get_name (self) -> str:
        assert False, "Not implemented"
    @staticmethod
    def get_packet_type () -> Type[MultiField]:
        assert False, "Not implemented"
    @staticmethod
    def get_data_format () -> List[str]:
        assert False, "Not implemented"
    @staticmethod
    def get_custom_protocol () -> Tuple[str, MultiField, Callable[[MultiField], Any]]:
        assert False, "Not implemented"
    def read_device_packet (self) -> MultiField:
        assert False, "Not implemented"
    def read_data_from_packet (self, packet: MultiField) -> List[Any]:
        assert False, "Not implemented"
    def get_time_period (self) -> float:
        assert False, "Not implemented"
    def stop_device (self):
        assert False, "Not implemented"
