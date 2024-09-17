
########################################################
# ONLINE AVIONICS CONFIGURATION                        #
# ===========================+======================== #
# Applications               | Sensors                 #
#                            | Camera                  #
#                            | Physical Controller     #
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
# Physical Device            | eSPI Device             #
# ===========================+======================== #
# Control Chain              | None                    #
# Model Chain                | Physical Controller     #
########################################################

from control.config.default.settings import *
from control.contrib.phyc.devices.espi import ESpiDevice
from control.contrib.phyc.sender import send_to_phyc
from control.contrib.sensors.devices.dps310 import DPS310Device

ENABLED_APPS = [
    "control.contrib.camera",
    "control.contrib.sensors",
    "control.contrib.phyc"
]

SENSORS_LIST = [
    DPS310Device()
]

SENSORS_AUTOSTART = False
SENSORS_MODE      = "WRITER"

CAMERA_AUTOSTART = False
CAMERA_COMMAND   = [ "libcamera-vid", "-t", "0", "-o", "-"]
CAMERA_MODE      = "WRITER"

NEXT_ON_MODEL_CHAIN = send_to_phyc()

PHYSICAL_DEVICE = ESpiDevice()
