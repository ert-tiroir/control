
import sys

from control.core.app import init_applications, stop_applications

def start_control ( settings: str ):
    from control.config.manager import ConfigManager

    ConfigManager().import_config( settings )

    init_applications()
def stop_control ():
    from control.config.manager import ConfigManager
    if not ConfigManager().has_config(): return
    
    stop_applications()