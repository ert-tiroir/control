
from control.core import start_control, stop_control

import time
import argparse

if __name__ == "__main__":
    with open("target.txt", "r") as file:
        start_control(file.read())