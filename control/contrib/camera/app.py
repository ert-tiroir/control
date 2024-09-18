
import threading
from control.config import settings
from control.contrib.camera.protocol.model.event import OnEndCamera, OnStartCamera
from control.contrib.protocol.abstract import control_send_and_flush, model_send_and_flush
from control.contrib.protocol.fields.packet import MultiField
from control.core.app import Application
from control.filesystem.fs import FileSystem
from control.utils.logger import Logger

class CameraApplication(Application):
    def __init__(self, path: str) -> None:
        super().__init__(path)

        self.camera_logs = Logger( "logs/camera/application.txt" )

        self.lock = threading.Lock()

        if settings.CAMERA_COMMAND is None and settings.CAMERA_MODE == "WRITER":
            self.camera_logs.critical("Improperly configured, CAMERA_COMMAND should contain an array of values")
            self.running   = False
            self.can_start = False
            return

        self.running = settings.CAMERA_AUTOSTART
        if self.running != False and self.running != True:
            self.camera_logs.warning("Improperly configured, CAMERA_AUTOSTART can only be true or false")
            self.running = True
        self.closed = False

        self.can_start = True
    def init_application(self):
        if self.running:
            self.on_start()
    def stop_application(self):
        if hasattr(self, "thread"):
            self.close_thread(True)

    def init_thread (self):
        from control.contrib.camera.thread import CameraThread
        
        self.camera_logs.info("Starting Camera Thread")
        self.thread = CameraThread()
        self.thread.run()
    def close_thread (self, join = False):
        self.camera_logs.info("Stopping Camera Thread")
        self.thread.stop()
        if join:
            self.thread.join()
        delattr(self, "thread")

    def on_start (self, packet: MultiField = None):
        if not self.can_start: return

        self.camera_logs.info(f"Starting Camera in {settings.CAMERA_MODE} mode")
        self.file = FileSystem.open_unique("media/video.mp4", "wb")
        
        if settings.CAMERA_MODE == "WRITER":
            self.init_thread()
        if packet is not None:
            self.camera_logs.info(f"Forwarding start control packet")
            control_send_and_flush(packet)
    def on_stop (self, packet: MultiField = None):
        if not self.can_start: return
        
        self.camera_logs.info(f"Stopping Camera in {settings.CAMERA_MODE} mode")

        if settings.CAMERA_MODE == "WRITER":
            self.close_thread()

        with self.lock:
            self.file.close()
            self.file = None
        if packet is not None:
            self.camera_logs.info(f"Forwarding stop control packet")
            control_send_and_flush(packet)
    def on_data (self, packet: MultiField):
        if not self.can_start: return

        self.camera_logs.info(f"Received data packet, writing it and forwarding it")
        
        with self.lock:
            if self.file is not None:
                self.file.write(packet.data)
                self.file.flush()

        settings.NEXT_ON_MODEL_CHAIN(packet)
    def model_start (self):
        self.camera_logs.info(f"Sending on start event")
        model_send_and_flush (OnStartCamera())
    def model_end (self):
        self.camera_logs.info(f"Sending on end event")
        model_send_and_flush (OnEndCamera())