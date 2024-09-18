
from control.contrib.protocol.flush import send_to_void
from control.utils.logger import LogLevel


ENABLED_APPS = []

NEXT_ON_CONTROLLER_CHAIN = send_to_void()
NEXT_ON_MODEL_CHAIN      = send_to_void()

SENSORS_AUTOSTART = False
SENSORS_MODE = "TRANSFER"
SENSORS_LIST = []

CAMERA_AUTOSTART = False
CAMERA_COMMAND   = None
CAMERA_MODE      = "TRANSFER"

PHYSICAL_STATS_DELAY = 5.0

MAX_LOG_LEVEL = LogLevel.INFO
