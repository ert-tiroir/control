
from typing import Any, Callable, List, Literal, Tuple

from control.config.manager import ConfigManager
from control.contrib.protocol.fields.packet import MultiField
from control.contrib.protocol.flush import Flushable
from control.contrib.sensors.device import AbstractDevice


class LazySettings ():
    ENABLED_APPS: List[str]

    NEXT_ON_CONTROLLER_CHAIN : Flushable
    NEXT_ON_MODEL_CHAIN      : Flushable

    SENSORS_AUTOSTART : bool
    SENSORS_LIST      : List[AbstractDevice]
    SENSORS_MODE      : Literal["WRITER"] | Literal["TRANSFER"]

    CAMERA_AUTOSTART : bool
    CAMERA_COMMAND   : List[str] | Literal[None]
    CAMERA_MODE      : Literal["WRITER"] | Literal["TRANSFER"]

    PHYSICAL_STATS_DELAY : float

    def __getattribute__(self, name: str) -> Any:
        return getattr(ConfigManager().get_config(), name)

settings = LazySettings()
