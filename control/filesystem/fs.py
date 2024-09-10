
import datetime
import os
from control.utils.singleton import Singleton

class FileSystem(metaclass=Singleton):
    def __init__(self):
        self.time   = datetime.datetime.now().isoformat().replace(":", "-")
        self.folder = f"saves/run_{self.time}"

    @staticmethod
    def init_file_system ():
        fs = FileSystem() # Locks folder
    @staticmethod
    def open (path, *args, **kwargs):
        fs = FileSystem()

        true_path = os.path.join(fs.folder, path)
        os.makedirs(os.path.dirname(true_path))
        return open(true_path, *args, **kwargs)
