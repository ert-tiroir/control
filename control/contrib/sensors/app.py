
import threading
import time
from typing import List
from control.contrib.protocol.fields.packet import MultiField
from control.contrib.sensors.csv import CSVDataSheets
from control.contrib.sensors.device import AbstractDevice
from control.core.app import Application

class SensorsApp(Application):
    sheets: CSVDataSheets
    devices: List[AbstractDevice]

    def __init__(self, path: str) -> None:
        self.sheets = CSVDataSheets()

        self.devices      = []
        self.next_measure = []

        self.closed = False
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

        def run_thread ():
            while not self.closed:
                start = time.time()
                end   = time.time() + 1

                for i in range(len(self.next_measure)):
                    if self.next_measure[i] < start:
                        try:
                            packet = self.devices[i].read_device_packet()

                            self.on_data(self.devices[i], packet)
                        except Exception:
                            pass
                        self.next_measure[i] = start + self.devices[i].get_time_period()

                    end = min(end, self.next_measure[i])
                print("SLEEPING")
                time.sleep(end - start)

        self.thread = threading.Thread(target=run_thread)
        self.thread.start()

    def stop_application(self):
        self.closed = True
        self.thread.join()

        for device in self.devices:
            device.stop_device()
        
        self.sheets.close()

    def on_start (self):
        pass
    def on_stop (self):
        pass
    def on_data (self, device: AbstractDevice, data: MultiField):
        self.sheets.put_device(device, data)