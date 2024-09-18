
########################################################
# TEST ON GROUND AVIONICS CONFIGURATION                #
# ===========================+======================== #
# Applications               | Sensors                 #
#                            | Camera                  #
#                            | Network Controller      #
# ===========================+======================== #
# Sensor List                | DPS310                  #
#                            | BNO055                  #
# Sensor Autostart           | False                   #
# Sensor Mode                | WRITER                  #
# ===========================+======================== #
# Camera Mode                | WRITER                  #
# Camera Autostart           | False                   #
# Camera Command             | libcamera-vid -t 0 -o - #
# ===========================+======================== #
# Control Chain              | None                    #
# Model Chain                | Network Controller      #
########################################################

from control.config.default.settings import *
from control.contrib.netc.sender import send_to_netc
from control.contrib.sensors.devices.dps310 import DPS310Device

ENABLED_APPS = [
    "control.contrib.camera",
    "control.contrib.sensors",
    "control.contrib.netc"
]

SENSORS_LIST = [
    DPS310Device()
]

SENSORS_AUTOSTART = False
SENSORS_MODE      = "WRITER"

CAMERA_AUTOSTART = False
CAMERA_COMMAND   = [ "libcamera-vid", "-t", "0", "-o", "-"]
CAMERA_MODE      = "WRITER"

NEXT_ON_MODEL_CHAIN = send_to_netc()
