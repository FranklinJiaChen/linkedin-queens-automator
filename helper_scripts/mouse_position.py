"""
Helper script
mouse position - Used to find the mouse's coordinates
and the color of the pixel at that coordinate.

Usage:
    press the 'z' key to print the current mouse coordinates.
    Press the 'q' key to terminate the program.
"""

import pyautogui
import time
import keyboard

while not keyboard.is_pressed('q'):
    if keyboard.is_pressed('z'):
        x, y = pyautogui.position()
        pixel_color = pyautogui.screenshot().convert('RGB').getpixel((x, y))
        print(f'The color at pixel ({x}, {y}) is: {pixel_color}')
        time.sleep(0.1)
