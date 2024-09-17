
from io import BytesIO
import threading
import time
from control.config import settings
from control.contrib.phyc.devices.device import PhysicalDevice
from control.contrib.protocol.abstract import AbstractProtocolApp
from control.core.app import Application, ApplicationManager
from control.filesystem.fs import FileSystem
from control.utils.bytequeue import ByteQueue
from control.utils.table import to_table

class PhysicalControllerApplication (Application):
    device: PhysicalDevice

    def prepare_application(self):
        self.protocol = AbstractProtocolApp( "protocol", "physical", "_packet_phy_index" )
        self.protocol.init_protocol()
    def init_application(self):
        self.device = None
        if not hasattr(settings, "PHYSICAL_DEVICE"):
            return
            assert False, "Missing Physical Device in settings (settings.PHYSICAL_DEVICE)"

        self.device = settings.PHYSICAL_DEVICE
        self.device.init_channel()

        def run_thread ():
            def on_receive_end (data: bytes):
                PhysicalControllerApplication().check_stats()
                protocol = PhysicalControllerApplication().protocol

                protocol.recv_buffer.put(data)
                protocol.check_receive()
            PhysicalControllerApplication().device.start_thread(
                on_receive_end
            )
        self.thread = threading.Thread( target=run_thread )
        self.thread.start()

        self.stat_lock = threading.Lock()

        self.file  = FileSystem.open_unique("protocol/physical_stats.txt", "w")
        self.lstat = time.time()

    def check_stats (self):
        with self.stat_lock:
            if time.time() - self.lstat <= settings.PHYSICAL_STATS_DELAY: return

            tx_stat, rx_stat = self.device.get_stream_stats()
            self.device.clear_stream_stats()

            delta = time.time() - self.lstat

            self.file.write(f"STATISTICS OVER THE LAST {delta} SECONDS - TIME = {time.time()}\n")
            self.file.write(f" - {tx_stat} bytes sent, {rx_stat} bytes received\n")
            self.file.write(f" - {tx_stat / delta} bytes / second sent, { rx_stat / delta } bytes / second received\n")
            self.file.write(f"\n")
            
            print(f"STATISTICS OVER THE LAST {delta} SECONDS - TIME = {time.time()}")
            print(f" - {tx_stat} bytes sent, {rx_stat} bytes received")
            print(f" - {tx_stat / delta} bytes / second sent, { rx_stat / delta } bytes / second received")
            self.lstat = time.time()
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
        self.check_stats()
        self.protocol.send(packet)

        queue = self.protocol.send_buffer
        self.device.start_transfer(queue.pop(len(queue)))
