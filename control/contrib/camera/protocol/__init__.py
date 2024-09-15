
from control.contrib.camera.protocol.control.start import StartCameraPacket, start_camera
from control.contrib.camera.protocol.control.stop import StopCameraPacket, stop_camera
from control.contrib.camera.protocol.model.data import DataPacket, handle_data_packet


net = [
    ("/camera/control/start", StartCameraPacket, start_camera),
    ("/camera/control/stop",  StopCameraPacket,  stop_camera),

    ("/camera/model/media", DataPacket, None) # Data packet can't be received on net, only on physical
]

physical = [
    ("/camera/control/start", StartCameraPacket, start_camera),
    ("/camera/control/stop",  StopCameraPacket,  stop_camera),

    ("/camera/model/media", DataPacket, handle_data_packet)
]
