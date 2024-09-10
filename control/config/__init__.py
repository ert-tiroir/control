
from typing import Any, Callable, List, Tuple

from control.config.manager import ConfigManager
from control.contrib.protocol.fields.packet import MultiField
from control.contrib.sensors.device import AbstractDevice


class LazySettings ():
    ENABLED_APPS: List[str]

    NEXT_ON_CONTROLLER_CHAIN : Callable[[MultiField], Any]
    NEXT_ON_MODEL_CHAIN      : Callable[[MultiField], Any]

    SENSORS_AUTOSTART : bool
    SENSORS_LIST      : List[AbstractDevice]

    def __getattribute__(self, name: str) -> Any:
        return getattr(ConfigManager().get_config(), name)

settings = LazySettings()
