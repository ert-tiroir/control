
from control.contrib.protocol.fields.integer import IntegerField
from control.contrib.protocol.fields.packet  import MultiField

class StartCameraPacket(MultiField):
    control_salt = IntegerField()
    control_key  = IntegerField()

def start_camera (packet: StartCameraPacket):
    # TODO validate controls

    from control.contrib.camera.app import CameraApplication
    
    CameraApplication().on_start(packet)
