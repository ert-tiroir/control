
from control.contrib.camera.protocol.control.start import StartCameraPacket, start_camera
from control.contrib.camera.protocol.control.stop import StopCameraPacket, stop_camera
from control.contrib.camera.protocol.model.data import DataPacket, handle_data_packet
from control.contrib.camera.protocol.model.event import OnEndCamera, OnStartCamera
from control.contrib.protocol.abstract import model_send_and_flush

net = [
    ("/camera/control/start", StartCameraPacket, start_camera),
    ("/camera/control/stop",  StopCameraPacket,  stop_camera),

    ("/camera/model/media", DataPacket, None), # Data packet can't be received on net, only on physical
    ("/camera/model/event/start", OnStartCamera, None),
    ("/camera/model/event/end",   OnEndCamera,   None),
]

physical = [
    ("/camera/control/start", StartCameraPacket, start_camera),
    ("/camera/control/stop",  StopCameraPacket,  stop_camera),

    ("/camera/model/media",       DataPacket,    handle_data_packet()),
    ("/camera/model/event/start", OnStartCamera, model_send_and_flush),
    ("/camera/model/event/end",   OnEndCamera,   model_send_and_flush)
]
