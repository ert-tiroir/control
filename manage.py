
from control.core import start_control, stop_control

if __name__ == "__main__":
    with open("target.txt", "r") as file:
        start_control(file.read())