
import time
from control.core import stop_control
from control.core.app import init_applications


def run_command (args):
    init_applications()

    
    if len(args) != 0 and args[0] == '--non-blocking': 
        return

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        stop_control()
