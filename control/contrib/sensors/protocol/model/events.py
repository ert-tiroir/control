
from control.config import settings
from control.contrib.protocol.fields.integer import IntegerField
from control.contrib.protocol.fields.packet import MultiField


class OnEndSensors(MultiField): pass

class __OnStart_Sensors: pass

for device in settings.SENSORS_LIST:
    setattr(__OnStart_Sensors, device.get_name(), IntegerField())

class OnStartSensors(MultiField, __OnStart_Sensors): pass
