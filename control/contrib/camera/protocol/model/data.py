

from control.contrib.protocol.fields.bytes import BytesField
from control.contrib.protocol.fields.integer import IntegerField
from control.contrib.protocol.fields.packet import MultiField

class DataPacket(MultiField):
    id   = IntegerField()
    data = BytesField()

class handle_data_packet ():
    def __init__(self) -> None:
        self.app = None
    def __call__(self, *args, **kwargs):
        if self.app is None:
            from control.contrib.camera.app import CameraApplication

            self.app = CameraApplication()
        self.app.on_data(*args, **kwargs)
