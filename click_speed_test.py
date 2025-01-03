import pyautogui
from random import randint
import time

pyautogui.PAUSE = 0
positions = [(853, 466), (1048, 662), (1235, 862), (1376, 987)]
start_time = time.time()

x_positions = [pos[0] for pos in positions]
y_positions = [pos[1] for pos in positions]

for x in x_positions:
    for y in y_positions:
        pyautogui.doubleClick(x, y)
print("Time taken: ", time.time()-start_time)
