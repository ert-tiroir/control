
import subprocess
import threading

from control.config import settings
from control.contrib.camera.protocol.model.data import DataPacket

class CameraThread:
    def __init__(self):
        self.running = False
    def join (self):
        if hasattr(self, "thread") and self.proc is not None:
            self.thread.join()
            delattr(self, "thread")
    def run (self):
        self.running = True

        def run_thread ():
            self.on_start()
        
        self.thread = threading.Thread(target=run_thread)
        self.thread.start()
        
    def on_start (self):
        from control.contrib.camera.app import CameraApplication
        
        self.proc = None
        self.proc = subprocess.Popen( settings.CAMERA_COMMAND, stdout=subprocess.PIPE )

        id = 0
        while self.running:
            data = self.proc.stdout.read(16_384)
            if len(data) == 0:
                break
            
            packet = DataPacket()
            packet.id = id
            packet.data = data
            id += 1
            CameraApplication().on_data(packet)
        
        self.proc.kill()
        self.proc.terminate()
        self.proc = None

    def stop (self):
        self.running = False
