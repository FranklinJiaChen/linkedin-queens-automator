import pyautogui
from PIL import Image
import numpy as np
from datetime import datetime
from collections import defaultdict

# Capture a screenshot of a specific region
screenshot = pyautogui.screenshot(region=(800, 400, 1425-800, 1030-400))

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

# Get the current date in year-month-day format
current_date = datetime.now().strftime('%Y-%m-%d')

# Save the cropped image with the date in the filename
cropped_image.save(f'{current_date}_puzzle.png')


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

# create a dictionary of {colour: [(x, y), (x, y), ...]}
colour_dict = defaultdict(list)
for x in range(resized_image.width):
    for y in range(resized_image.height):
        r, g, b = resized_image.getpixel((x, y))
        colour_dict[(r, g, b)].append((x, y))

from pysat.solvers import Glucose3
from itertools import combinations

solver = Glucose3()
size = unique_colours

def coord_to_index(i: int, j: int) -> int:
    """
    Convert a cell coordinate (i, j) to a unique variable index.

    Parameters:
    i: The row index. Zero-based.
    j: The column index. Zero-based.

    Returns:
    The variable index corresponding to the cell (i, j).
    the index is 1-based and row-major order.
    """
    return i * size + j + 1

def index_to_coord(index: int) -> tuple[int, int]:
    """
    Convert a variable index to cell coordinates (i, j).

    Parameters:
    index: The variable index.

    Returns:
    A tuple of row and column indices (i, j).
    """
    return (index - 1) // size, (index - 1) % size

# Generate clauses for Queens constraints
# One queen per row
for i in range(size):
    # Each row must have at least one queen
    solver.add_clause([coord_to_index(i, j) for j in range(size)])

    # Each row must have at most one queen (no two queens in the same row)
    for j1, j2 in combinations(range(size), 2):
        solver.add_clause([-coord_to_index(i, j1), -coord_to_index(i, j2)])

# Step 2: One queen per column
for j in range(size):
    # Each column must have at least one queen
    solver.add_clause([coord_to_index(i, j) for i in range(size)])

    # Each column must have at most one queen (no two queens in the same column)
    for i1, i2 in combinations(range(size), 2):
        solver.add_clause([-coord_to_index(i1, j), -coord_to_index(i2, j)])

# Step 3: No two queens can touch adjacentally
# We just need to add diagonally adjacent constraints
for i in range(size - 1):
    for j in range(size):
        # Check for adjacent lower-right diagonal
        if j < size - 1:
            solver.add_clause([-coord_to_index(i, j), -coord_to_index(i + 1, j + 1)])

        # Check for adjacent lower-left diagonal
        if j > 0:
            solver.add_clause([-coord_to_index(i, j), -coord_to_index(i + 1, j - 1)])


colours = colour_dict.values()
colours = [[(j, i) for i, j in colour] for colour in colours]

# Step 4: One queen per colour
for colour in colours:
    # Each colour must have at most one queen (no two queens in the same colour)
    for (i1, j1), (i2, j2) in combinations(colour, 2):
        solver.add_clause([-coord_to_index(i1, j1), -coord_to_index(i2, j2)])

    # Each colour must have at least one queen
    solver.add_clause([coord_to_index(i, j) for i, j in colour])

# Find and print all solutions
solutions = []
while solver.solve():
    solution = solver.get_model()
    print(solution)
    solutions.append(solution)

    # Print the current solution
    print(f"Solution {len(solutions)}:")
    board = [['.' for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if solution[coord_to_index(i, j) - 1] > 0:
                board[i][j] = 'Q'
    for row in board:
        print(" ".join(row))
    print()

    # Add clause to block the current solution
    solver.add_clause([-var for var in solution])

solver.delete()

# Print total solutions found
print(f"Total Solutions: {len(solutions)}")

box = [800+min_x, 400+min_y, max_x-min_x, max_y-min_y]
for var in solution:
    if var > 0:
        i, j = index_to_coord(var)
        # double click
        pyautogui.doubleClick(((j+1)/(unique_colours+1)*box[2] + box[0])//1, ((i+1)/(unique_colours+1)*box[3] + box[1])//1)

