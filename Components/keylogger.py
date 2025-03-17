# This code is only for the main code to work with
import pynput.mouse
from pynput.mouse import Listener

def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y})")

with Listener(on_click=on_click) as listener:
    listener.join()