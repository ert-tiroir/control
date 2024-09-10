
from control.contrib.protocol.fields.integer import IntegerField
from control.contrib.protocol.fields.packet  import MultiField

class StartSensorPacket(MultiField):
    control_salt = IntegerField()
    control_key  = IntegerField()

def start_sensors (packet: StartSensorPacket):
    # TODO validate controls

    from control.contrib.sensors.app import SensorsApp
    
    # TODO either forward or init sensors
    SensorsApp().on_start()
