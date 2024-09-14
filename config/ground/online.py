
########################################################
# ONLINE GROUND STATION CONFIGURATION                  #
# ===========================+======================== #
# Applications               | Sensors                 #
#                            | Camera                  #
#                            | Physical Controller     #
#                            | Network Controller      #
# ===========================+======================== #
# Sensor List                | DPS310                  #
#                            | BNO055                  #
# Sensor Autostart           | False                   #
# Sensor Mode                | TRANSFER                #
# ===========================+======================== #
# Camera Mode                | TRANSFER                #
# Camera Autostart           | False                   #
# Camera Command             | libcamera-vid -t 0 -o - #
# ===========================+======================== #
# Physical Device            | eSPI Device             #
# ===========================+======================== #
# Control Chain              | None                    #
# Model Chain                | Physical Controller     #
########################################################

from control.config.default.settings import *
from control.contrib.netc.app import send_to_netc
from control.contrib.phyc.app import send_to_phyc
from control.contrib.phyc.devices.espi import ESpiDevice
from control.contrib.sensors.devices.dps310 import DPS310Device

ENABLED_APPS = [
    "control.contrib.camera",
    "control.contrib.sensors",
    "control.contrib.phyc",
    "control.contrib.netc"
]

SENSORS_LIST = [
    DPS310Device()
]

SENSORS_AUTOSTART = False
SENSORS_MODE      = "TRANSFER"

CAMERA_AUTOSTART = False
CAMERA_COMMAND   = [ "libcamera-vid", "-t", "0", "-o", "-"]
CAMERA_MODE      = "TRANSFER"

NEXT_ON_CONTROLLER_CHAIN = send_to_phyc
NEXT_ON_MODEL_CHAIN      = send_to_netc

PHYSICAL_DEVICE = ESpiDevice()
