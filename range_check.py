import time
from pyautogui import position
try:
    while True:
        print(position())
        time.sleep(1)
except KeyboardInterrupt:
    pass