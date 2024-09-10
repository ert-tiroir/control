
import threading
import time
from typing import List
from control.contrib.protocol.fields.packet import MultiField
from control.contrib.sensors.csv import CSVDataSheets
from control.contrib.sensors.device import AbstractDevice
from control.contrib.sensors.protocol.control.start import StartSensorPacket
from control.core.app import Application

from control.config import settings

class SensorsApp(Application):
    sheets: CSVDataSheets
    devices: List[AbstractDevice]

    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.sheets = CSVDataSheets()

        self.devices      = [x for x in settings.SENSORS_LIST]
        self.next_measure = []

        self.running = settings.SENSORS_AUTOSTART
        if self.running != False and self.running != True:
            print("Improperly configured, SENSORS_AUTOSTART can only be true or false")
            self.running = False
        
        self.closed  = False
    def init_application(self):
        next_devices = []

        for device in self.devices:
            try:
                device.init_device()
            except Exception as exception:
                print("Device", device.get_name(), "failed to initialize")
                print(exception)
                continue
            
            next_devices.append(device)
            self.next_measure.append(time.time() + device.get_time_period())
            self.sheets.init_device(device)
        
        self.devices = next_devices

        if len(self.devices) == 0: return

        def run_thread ():
            while not self.closed:
                start = time.time()
                end   = time.time() + 1

                if self.running:
                    for i in range(len(self.next_measure)):
                        if self.next_measure[i] < start:
                            try:
                                packet = self.devices[i].read_device_packet()

                                self.on_data(self.devices[i], packet)
                            except Exception:
                                pass
                            self.next_measure[i] = start + self.devices[i].get_time_period()

                        end = min(end, self.next_measure[i])

                time.sleep(end - start)

        self.thread = threading.Thread(target=run_thread)
        self.thread.start()

    def stop_application(self):
        self.closed = True

        if hasattr(self, "thread"):
            self.thread.join()

        for device in self.devices:
            device.stop_device()
        
        self.sheets.close()

    def on_start (self, packet: MultiField):
        settings.NEXT_ON_CONTROLLER_CHAIN( packet )
        self.running = True
    def on_stop (self, packet: MultiField):
        settings.NEXT_ON_CONTROLLER_CHAIN( packet )
        self.running = False
    def on_data (self, device: AbstractDevice, data: MultiField):
        self.sheets.put_device(device, data)

        settings.NEXT_ON_MODEL_CHAIN(data)