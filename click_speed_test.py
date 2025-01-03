import pyautogui
from random import randint
import time

pyautogui.PAUSE = 0.025
start_time = time.time()
for clicks in range(100):
    pyautogui.doubleClick(randint(231, 457), randint(615, 827))

print("Time taken: ", time.time()-start_time)
print("Clicks per second: ", 100/(time.time()-start_time))
