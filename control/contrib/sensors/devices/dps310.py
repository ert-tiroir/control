
from typing import Any, Callable, List, Tuple, Type

from control.contrib.protocol.fields.number import FloatField
from control.contrib.protocol.fields.packet import MultiField
from control.contrib.sensors.app import SensorsApp
from control.contrib.sensors.device import AbstractDevice

import board
from adafruit_dps310.basic import DPS310
from control.utils.singleton import Singleton

class DPS310Device(AbstractDevice, metaclass=Singleton):
    def init_device (self):
        self.i2c = board.I2C()
        self.dps = DPS310(self.i2c)
    def get_name (self) -> str:
        return "dps310"
    @staticmethod
    def get_packet_type () -> Type["DPS310Packet"]:
        return DPS310Packet
    @staticmethod
    def get_data_format () -> List[str]:
        return [ "temperature", "pressure" ]
    @staticmethod
    def get_custom_protocol() -> Tuple[str, MultiField, Callable[[MultiField], Any]]:
        return ( "/sensors/data/dps310", DPS310Packet, handle_dps310_packet )
    def read_device_packet (self) -> "DPS310Packet":
        packet = DPS310Packet()

        packet.temperature = self.dps.temperature
        packet.pressure    = self.dps.pressure

        return packet
    def read_data_from_packet (self, packet: "DPS310Packet") -> List[Any]:
        return [ packet.temperature, packet.pressure ]
    def get_time_period (self) -> float:
        return 1.0
    def stop_device (self):
        return

class DPS310Packet(MultiField):
    temperature = FloatField()
    pressure    = FloatField()

def handle_dps310_packet (packet: DPS310Packet):
    SensorsApp().on_data( DPS310Device(), packet )
