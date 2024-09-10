
ENABLED_APPS = [
    'control.contrib.webc'
]

# either "avionics" or "ground"
# determines whether to run the control apps in av or gnd mode
# av is usually setting up sensors and sending the data through phyc,
# while gnd is usually taking data from phyc and forwarding it to netc.
CONTROLLER_TYPE = "avionics"
