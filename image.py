import pyautogui
from PIL import Image
import numpy as np
from datetime import datetime
from collections import defaultdict

# # Capture a screenshot of a specific region
# screenshot = pyautogui.screenshot(region=(800, 400, 1425-800, 1030-400))
# open the image
screenshot = Image.open('2025-01-01_puzzle.png')

# Convert the screenshot (Pillow Image) into a format we can work with
image_rgb = screenshot.convert('RGB')

# Convert the image to grayscale
gray_image = image_rgb.convert('L')

# Convert the grayscale image to a numpy array
gray_np = np.array(gray_image)

# Create a mask for the non-white areas where pixel values are <= 245
non_white_mask = gray_np <= 245

# Find rows and columns that have any non-white pixel
rows = np.any(non_white_mask, axis=1)
cols = np.any(non_white_mask, axis=0)

# Find the bounding box coordinates based on the non-white pixels
min_y, max_y = np.where(rows)[0][[0, -1]]
min_x, max_x = np.where(cols)[0][[0, -1]]

# Crop the image based on the bounding box
cropped_image = image_rgb.crop((min_x + 3, min_y + 3, max_x - 3, max_y - 3))

box = [800+min_x, 400+min_y, max_x-min_x, max_y-min_y]
print(box)

# # Get the current date in year-month-day format
current_date = datetime.now().strftime('%Y-%m-%d')

# Save the cropped image with the date in the filename
cropped_image.save(f'{current_date}_puzzle.png')

# Show the cropped image
cropped_image.show()

colour_dict = defaultdict(int)

for x in range(cropped_image.width):
    for y in range(cropped_image.height):
        r, g, b = cropped_image.getpixel((x, y))
        colour_dict[(r, g, b)] += 1

# sort by value
sorted_colour_dict = dict(sorted(colour_dict.items(), key=lambda x: x[1], reverse=True))
print(sorted_colour_dict)
# count number of unique colours with values > 10
unique_colours = sum(1 for value in sorted_colour_dict.values() if value > 10)-1
print(unique_colours)

resized_image = cropped_image.resize((unique_colours, unique_colours), Image.NEAREST)
resized_image.show()
# large_image = resized_image.resize((resized_image.width * 30, resized_image.height * 30), Image.NEAREST)
# # Show the resized image
# large_image.show()

# create a dictionary of {colour: [(x, y), (x, y), ...]}
colour_dict = defaultdict(list)
for x in range(resized_image.width):
    for y in range(resized_image.height):
        r, g, b = resized_image.getpixel((x, y))
        colour_dict[(r, g, b)].append((x, y))

print(colour_dict)
