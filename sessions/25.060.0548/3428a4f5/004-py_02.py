"""
The transformation rule involves three main steps:
1. Remove the single horizontal row of color 4 (yellow).
2. Change all instances of color 2 (red) to color 3 (green).
3. Reduce the grid vertically by consolidating every two consecutive rows into one, prioritizing color 3.
"""

import numpy as np

def remove_yellow_row(grid):
    # Find the row index with all 4s
    yellow_row_index = np.where((grid == 4).all(axis=1))[0]
    # Remove the row if found
    if yellow_row_index.size > 0:
        return np.delete(grid, yellow_row_index, axis=0)
    return grid

def change_color(grid, old_color, new_color):
    # Replace all instances of old_color with new_color
    grid[grid == old_color] = new_color
    return grid

def vertical_reduction(grid):
    # Initialize an empty list to hold the new rows
    new_rows = []
    # Iterate through the rows, taking two at a time
    for i in range(0, grid.shape[0], 2):
        # if we're on the last row, and the last row is odd, just add it
        if i + 1 == grid.shape[0]:
          new_rows.append(grid[i,:])
        # if not, get this and the next row
        else:
            row1 = grid[i, :]
            row2 = grid[i+1, :]
            # For each column, choose color 3 if present in either row, otherwise 0
            new_row = np.where((row1 == 3) | (row2 == 3), 3, 0)
            new_rows.append(new_row)
    # Convert the list of new rows into a NumPy array
    return np.array(new_rows)

def transform(input_grid):
    # Convert input grid to a NumPy array
    grid = np.array(input_grid)

    # 1. Remove the row of 4s
    grid = remove_yellow_row(grid)

    # 2. Change color 2 to 3
    grid = change_color(grid, 2, 3)

    # 3. Vertical reduction
    output_grid = vertical_reduction(grid)

    return output_grid.tolist()