
import subprocess
import threading

from control.config import settings
from control.contrib.camera.protocol.model.data import DataPacket
from control.utils.logger import Logger

class CameraThread:
    def __init__(self):
        self.running = False

        self.camera_thread_logs = Logger( "logs/camera/thread.txt" )
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
        
        self.camera_thread_logs.success("Successfully started camera thread")
        self.proc = None
        self.proc = subprocess.Popen( settings.CAMERA_COMMAND, stdout=subprocess.PIPE )
        self.camera_thread_logs.success("Successfully created camera subprocess")

        CameraApplication().model_start()

        id = 0
        while self.running:
            data = self.proc.stdout.read(16_384)
            if len(data) == 0:
                self.camera_thread_logs.warning("No more data from pipe, might be due to an error")
                break
            
            self.camera_thread_logs.info("Found data from camera process")
            packet = DataPacket()
            packet.id = id
            packet.data = data
            id += 1
            CameraApplication().on_data(packet)
        
        self.camera_thread_logs.success("Ended camera subprocess")
        self.proc.kill()
        self.proc.terminate()
        self.proc = None
        
        CameraApplication().model_end()
        self.camera_thread_logs.close()

    def stop (self):
        self.camera_thread_logs.info("Asking camera thread to stop")
        self.running = False
