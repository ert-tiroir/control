
from control.contrib.protocol.fields.integer import IntegerField
from control.contrib.protocol.fields.packet  import MultiField

class StopCameraPacket(MultiField):
    control_salt = IntegerField()
    control_key  = IntegerField()

def stop_camera (packet: StopCameraPacket):
    # TODO validate controls

    from control.contrib.camera.app import CameraApplication
    
    CameraApplication().on_stop(packet)
