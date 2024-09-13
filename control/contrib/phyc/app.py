
from io import BytesIO
import threading
from control.config import settings
from control.contrib.phyc.devices.device import PhysicalDevice
from control.contrib.protocol.abstract import AbstractProtocolApp
from control.core.app import Application, ApplicationManager
from control.utils.bytequeue import ByteQueue
from control.utils.table import to_table

class PhysicalControllerApplication (Application):
    device: PhysicalDevice

    def prepare_application(self):
        self.protocol = AbstractProtocolApp( "protocol", "physical", "_packet_phy_index" )
        self.protocol.init_protocol()
    def init_application(self):
        self.device   = None
        if not hasattr(settings, "PHYSICAL_DEVICE"):
            return
            assert False, "Missing Physical Device in settings (settings.PHYSICAL_DEVICE)"

        self.device = settings.PHYSICAL_DEVICE

        def run_thread ():
            def on_receive_end (data: bytes):
                print(data[:40])
                PhysicalControllerApplication().protocol.check_receive()
            PhysicalControllerApplication().device.start_thread(
                on_receive_end
            )

            PhysicalControllerApplication().device.start_transfer(bytes(
                "Hello, SPI !", encoding="utf-8"
            ) + bytes([0] * (1023 - len( "Hello, SPI !" ))))
        self.thread = threading.Thread( target=run_thread )
        self.thread.start()

    def stop_application(self):
        super().stop_application()
        self.protocol.stop_protocol()

        if hasattr(self, "device") and self.device is not None:
            self.device.stop_thread()
            delattr(self, "device")
        
        if hasattr(self, "thread"):
            self.thread.join()
            delattr(self, "thread")
    def send (self, packet):
        self.protocol.send(packet)

        queue = self.protocol.send_buffer
        self.device.start_transfer(queue.pop(len(queue)))

def send_to_phyc (packet):
    PhysicalControllerApplication().send(packet)