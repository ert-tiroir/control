
import threading
from control.config import settings
from control.contrib.phyc.protocol import create_flush_packet
from control.contrib.protocol.fields.packet import MultiField
from control.core.app import Application
from control.filesystem.fs import FileSystem

class CameraApplication(Application):
    def __init__(self, path: str) -> None:
        super().__init__(path)

        self.lock = threading.Lock()

        if settings.CAMERA_COMMAND is None and settings.CAMERA_MODE == "WRITER":
            print("Improperly configured, CAMERA_COMMAND should contain an array of values")
            self.running   = False
            self.can_start = False
            return

        self.running = settings.CAMERA_AUTOSTART
        if self.running != False and self.running != True:
            print("Improperly configured, CAMERA_AUTOSTART can only be true or false")
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
        
        self.thread = CameraThread()
        self.thread.run()
    def close_thread (self, join = False):
        self.thread.stop()
        if join:
            self.thread.join()
        delattr(self, "thread")

    def on_start (self, packet: MultiField = None):
        if not self.can_start: return

        self.file = FileSystem.open_unique("media/video.mp4", "wb")
        
        if settings.CAMERA_MODE == "WRITER":
            self.init_thread()
        if packet is not None:
            settings.NEXT_ON_CONTROLLER_CHAIN(packet)
            settings.NEXT_ON_CONTROLLER_CHAIN( create_flush_packet() )
    def on_stop (self, packet: MultiField = None):
        if not self.can_start: return
        
        if settings.CAMERA_MODE == "WRITER":
            self.close_thread()

        with self.lock:
            self.file.close()
            self.file = None
        if packet is not None:
            settings.NEXT_ON_CONTROLLER_CHAIN(packet)
            settings.NEXT_ON_CONTROLLER_CHAIN( create_flush_packet() )
    def on_data (self, packet: MultiField):
        if not self.can_start: return
        
        with self.lock:
            if self.file is not None:
                self.file.write(packet.data)
                self.file.flush()

        settings.NEXT_ON_MODEL_CHAIN(packet)
