
from control.contrib.camera.app import CameraApplication
from control.contrib.protocol.fields.bytes import BytesField
from control.contrib.protocol.fields.integer import IntegerField
from control.contrib.protocol.fields.packet import MultiField

class DataPacket(MultiField):
    id   = IntegerField()
    data = BytesField()

def handle_data_packet (packet: DataPacket):
    CameraApplication().on_data(packet)
