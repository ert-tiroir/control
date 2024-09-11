
import datetime
import os
from control.utils.singleton import Singleton

class FileSystem(metaclass=Singleton):
    def __init__(self):
        self.folder = FileSystem.unique_name("saves/run")

    @staticmethod
    def unique_name (name: str):
        time = datetime.datetime.now().isoformat().replace(":", "-")

        chunks = name.split(os.path.pathsep)
        if len(chunks) == 1:
            words = chunks[0].split(".")
            offset = -2
            if len(words) == 1: offset = -1

            words[offset] = words[offset] + "_" + time

            return ".".join(words)
        else:
            chunks[-1] = FileSystem.unique_name(chunks[-1])
            return os.path.pathsep.join(chunks)
    @staticmethod
    def init_file_system ():
        fs = FileSystem() # Locks folder
    @staticmethod
    def open (path, *args, **kwargs):
        fs = FileSystem()

        true_path = os.path.join(fs.folder, path)
        if not os.path.exists(os.path.dirname(true_path)):
            os.makedirs(os.path.dirname(true_path))
        return open(true_path, *args, **kwargs)
    @staticmethod
    def open_unique (path, *args, **kwargs):
        return FileSystem.open(
            FileSystem.unique_name(path),
            *args,
            **kwargs
        )
