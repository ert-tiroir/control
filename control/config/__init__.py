
from typing import Any

from control.config.manager import ConfigManager


class LazySettings ():
    def __getattribute__(self, name: str) -> Any:
        return getattr(ConfigManager().get_config(), name)

settings = LazySettings()
