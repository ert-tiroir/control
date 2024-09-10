
from typing import Any, List, Type

from control.contrib.protocol.fields.number import FloatField
from control.contrib.protocol.fields.packet import MultiField
from control.contrib.sensors.device import AbstractDevice

import board
from adafruit_dps310.basic import DPS310

class DPS310Device(AbstractDevice):
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
