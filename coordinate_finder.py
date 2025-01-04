"""
used to find the coordinates of the puzzle on the screen
"""
import mss

POTENTIAL_X_START = 800
POTENTIAL_X_RANGE = 30
POTENTIAL_Y_START = 360
POTENTIAL_Y_RANGE = 100
POTENTIAL_DIMENSION_MIN = 580
POTENTIAL_DIMENSION_RANGE = 40
BORDER_OFFSET = 30
BORDER_OFFSET_INITIAL = 100
with mss.mss() as sct:
    long_screenshot = sct.grab({"left": POTENTIAL_X_START, "top": POTENTIAL_Y_START+BORDER_OFFSET_INITIAL,
                                "width": POTENTIAL_X_RANGE, "height": 1})
    for x in range(POTENTIAL_X_RANGE):
        if long_screenshot.pixel(x, 0) == (0, 0, 0):
            puzzle_x = POTENTIAL_X_START + x
            break
with mss.mss() as sct:
    long_screenshot = sct.grab({"left": puzzle_x + BORDER_OFFSET, "top": POTENTIAL_Y_START,
                                "width": 1, "height": POTENTIAL_Y_RANGE})
    for y in range(POTENTIAL_Y_RANGE):
        if long_screenshot.pixel(0, y) == (0, 0, 0):
            puzzle_y = POTENTIAL_Y_START + y
            break

with mss.mss() as sct:
    long_screenshot = sct.grab({"left": puzzle_x + POTENTIAL_DIMENSION_MIN, "top": puzzle_y + BORDER_OFFSET, "width": POTENTIAL_DIMENSION_RANGE, "height": 1})
    for x in range(POTENTIAL_DIMENSION_RANGE-1, -1, -1):
        if long_screenshot.pixel(x, 0) == (0, 0, 0):
            puzzle_width = POTENTIAL_DIMENSION_MIN + x + 1
            break

with mss.mss() as sct:
    long_screenshot = sct.grab({"left": puzzle_x + BORDER_OFFSET, "top": puzzle_y + POTENTIAL_DIMENSION_MIN, "width": 1, "height": POTENTIAL_DIMENSION_RANGE})
    for y in range(POTENTIAL_DIMENSION_RANGE-1, -1, -1):
        print(y)
        if long_screenshot.pixel(0, y) == (0, 0, 0):
            puzzle_height = POTENTIAL_DIMENSION_MIN + y + 1
            break

print(puzzle_x, puzzle_y, puzzle_width, puzzle_height)

with mss.mss() as sct:
    screenshot = sct.grab({"left": puzzle_x, "top": puzzle_y,
                           "width": puzzle_width, "height": puzzle_height})