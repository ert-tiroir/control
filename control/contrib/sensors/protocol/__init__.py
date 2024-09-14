
from control.config import settings
from control.contrib.sensors.protocol.control.start import start_sensors, StartSensorPacket
from control.contrib.sensors.protocol.control.stop import StopSensorPacket, stop_sensors


net = [
    ("/control/start", StartSensorPacket, start_sensors),
    ("/control/stop",  StopSensorPacket,  stop_sensors)
]

physical = net

for device in settings.SENSORS_LIST:
    net.append( device.get_custom_protocol() )
