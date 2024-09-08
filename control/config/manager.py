
import importlib
from typing import Any
from control.utils.singleton import Singleton


class ConfigManager(metaclass=Singleton):
    def __init__(self) -> None:
        self.config = None
    def has_config (self):
        return self.config is not None
    def import_config (self, path : str):
        assert not self.has_config()
        module = importlib.import_module(path)

        self.config = module
    def get_config (self):
        assert self.has_config()
        return self.config
