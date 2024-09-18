
from control.config import settings
from control.contrib.protocol.abstract import model_send_and_flush
from control.contrib.sensors.protocol.control.start import start_sensors, StartSensorPacket
from control.contrib.sensors.protocol.control.stop import StopSensorPacket, stop_sensors
from control.contrib.sensors.protocol.model.events import OnEndSensors, OnStartSensors


net = [
    ("/sensors/control/start", StartSensorPacket, start_sensors),
    ("/sensors/control/stop",  StopSensorPacket,  stop_sensors),

    ("/sensors/model/event/start", OnStartSensors, model_send_and_flush()),
    ("/sensors/model/event/start", OnEndSensors, model_send_and_flush()),
]

print(OnStartSensors.__MultiField_meta_fields__)
physical = net

for device in settings.SENSORS_LIST:
    net.append( device.get_custom_protocol() )
