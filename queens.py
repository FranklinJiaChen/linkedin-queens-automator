"""

"""
from pysat.solvers import Glucose3
from itertools import combinations

solver = Glucose3()
size = 7

def coord_to_index(i: int, j: int) -> int:
    """
    Convert a cell coordinate (i, j) to a unique variable index.

    Parameters:
    i: The row index.
    j: The column index.

    Returns:
    The variable index corresponding to the cell (i, j).
    the index is 1-based and row-major order.
    """
    return i * size + j + 1

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

# purple = [[0, 0], [0, 1], [0, 2], [1, 0], [2, 0], [2, 1]]
# orange = [[3, 0], [4, 0], [3, 1], [4, 1], [5, 1], [3, 2], [4, 2], [5, 2], [6, 2], [0, 3], [1, 3], [2, 3], [3, 3], [4, 3], [5, 3], [6, 3], [0, 4], [1, 4], [2, 4], [3, 4], [1, 5], [2, 5], [3, 5], [2, 6], [3, 6]]
# yellow = [[0, 5], [0, 6], [1, 6]]
# green = [[1, 1], [1, 2], [2, 2]]
# grey = [[4, 4], [4, 5], [5, 4]]
# blue = [[6, 0], [5, 0], [6, 1]]
# red = [[6, 6], [5, 5], [5, 6], [6, 5], [4, 6], [6, 4]]

# colours = [purple, orange, yellow, green, grey, blue, red]

# # Step 4: One queen per colour
# for colour in colours:
#     # Each colour must have at most one queen (no two queens in the same colour)
#     for i, j in colour:
#         for i1, j1 in colour:
#             if i != i1 or j != j1:
#                 solver.add_clause([-coord_to_index(j, i), -coord_to_index(j1, i1)])

#     # Each colour must have at least one queen
#     solver.add_clause([coord_to_index(j, i) for i, j in colour])

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
