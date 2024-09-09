
from control.core import start_control, stop_control

import time
if __name__ == "__main__":
    start_control("conf")

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        stop_control()
    print("STOPPED CONTROL")