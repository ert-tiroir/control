
import csv
from control.contrib.protocol.fields.packet import MultiField
from control.contrib.sensors.device import AbstractDevice
from control.filesystem.fs import FileSystem


class CSVDataSheet:
    def __init__(self, device: AbstractDevice) -> None:
        self.device = device

        self.file = FileSystem.open( f"sensors/{device.get_name()}.csv", 'w', newline='' )
        self.wrtr = csv.writer(self.file)
    def put (self, packet: MultiField):
        data = list(map(str, self.device.read_data_from_packet(packet)))
        self.wrtr.writerow(data)
        self.file.flush()
    def close (self):
        self.file.close()

class CSVDataSheets:
    def __init__(self):
        self.writers = {}
    def init_device (self, device: AbstractDevice):
        assert device.get_name() not in self.writers, "Expected device to be present only once"

        self.writers[device.get_name()] = CSVDataSheet(device)
    def close (self):
        for key in self.writers.keys():
            self.writers[key].close()
    def put_device (self, device: AbstractDevice, data: MultiField):
        self.writers[device.get_name()].put(data)