
import sys

from control.core.app import init_applications, prepare_applications, stop_applications

import control.config

def start_control ( settings: str ):
    from control.config.manager import ConfigManager

    ConfigManager().import_config( settings )
    
    control.config.settings.ENABLED_APPS.append("control.contrib.main")

    prepare_applications()

    from control.contrib.main.app import MainApplication
    application = MainApplication()
    application.run()
def stop_control ():
    from control.config.manager import ConfigManager
    if not ConfigManager().has_config(): return
    
    stop_applications()