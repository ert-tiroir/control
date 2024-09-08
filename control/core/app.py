
import importlib
import importlib.util
from types import ModuleType
from typing import List
from control.utils.singleton import Singleton

from control.config import settings

class ApplicationManager(metaclass=Singleton):
    applications: "List[Application]"
    def __init__(self) -> None:
        self.applications = []
    
    def bind (self, path: str):
        self.path = path
        self._lpt = path
    def unbind (self):
        assert self.path is None, f"Improperly configured, could not find app for {self.path}"
    def add_application (self, application_type):
        assert self.path is not None, f"Improperly configured, two apps are being imported for {self._lpt}"

        try:
            self.applications.append( application_type(self.path) )
        except Exception:
            assert False, f"Could not instantiate app {self.path}"
        self.path = None

class Application(metaclass=Singleton):
    def __init__(self, path: str) -> None:
        self.__path = path
    def __init_subclass__(cls) -> None:
        ApplicationManager().add_application(cls)
    def init_application (self):
        pass
    def stop_application (self):
        pass
    def load_module (self, module: str) -> None | ModuleType:
        target = self.path + "." + module

        spec = importlib.util.find_spec(target)
        if spec is None: return None

        return importlib.import_module(target)

    @property
    def path (self):
        return self.__path

def init_applications ():
    manager = ApplicationManager()
    
    for application in settings.ENABLED_APPS:
        manager.bind(application)
        importlib.import_module( application + ".app" )

        manager.unbind()
    for application in manager.applications:
        application.init_application()
def stop_applications ():
    for application in ApplicationManager().applications:
        application.stop_application()