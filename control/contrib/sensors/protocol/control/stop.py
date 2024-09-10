
from control.contrib.protocol.fields.integer import IntegerField
from control.contrib.protocol.fields.packet  import MultiField

class StopSensorPacket(MultiField):
    control_salt = IntegerField()
    control_key  = IntegerField()

def stop_sensors (packet: StopSensorPacket):
    # TODO validate controls

    from control.contrib.sensors.app import SensorsApp
    
    SensorsApp().on_stop(packet)
