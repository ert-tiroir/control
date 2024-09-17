
from control.contrib.protocol.fields.bytes import BytesField
from control.contrib.protocol.fields.packet import MultiField

class PhysicalFlushPacket(MultiField):
    data = BytesField()

def create_flush_packet ():
    packet = PhysicalFlushPacket()
    packet.data = bytes([0] * 1024)
    return packet

net = physical = [
    ("/physical/flush", PhysicalFlushPacket, lambda *args, **kwargs: None)
]
