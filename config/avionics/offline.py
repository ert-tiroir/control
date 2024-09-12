
########################################################
# OFFLINE AVIONICS CONFIGURATION                       #
# ===========================+======================== #
# Applications               | Sensors                 #
#                            | Camera                  #
# ===========================+======================== #
# Sensor List                | DPS310                  #
#                            | BNO055                  #
# Sensor Autostart           | True                    #
# ===========================+======================== #
# Camera Mode                | WRITER                  #
# Camera Autostart           | True                    #
# Camera Command             | libcamera-vid -t 0 -o - #
# ===========================+======================== #
# Control Chain              | None                    #
# Model Chain                | None                    #
########################################################

from control.config.default.settings import *
from control.contrib.sensors.devices.dps310 import DPS310Device

ENABLED_APPS = [
    "control.contrib.camera",
    "control.contrib.sensors"
]

SENSORS_LIST = [
    DPS310Device()
]

SENSORS_AUTOSTART = True

CAMERA_AUTOSTART = True
CAMERA_COMMAND   = [ "libcamera-vid", "-t", "0", "-o", "-"]
CAMERA_MODE      = "WRITER"
