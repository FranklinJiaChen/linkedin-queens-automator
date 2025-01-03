import pyautogui
from random import randint
import time

start_time = time.time()
for clicks in range(100):
    pyautogui.doubleClick(randint(800, 1425), randint(400, 1030))

print("Time taken: ", time.time()-start_time)
print("Clicks per second: ", 100/(time.time()-start_time))
