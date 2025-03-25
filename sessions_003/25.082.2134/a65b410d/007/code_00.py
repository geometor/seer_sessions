"""
Transforms an input grid by adding three rows of green pixels above a horizontal line of red pixels. The length of the first green row is equal to red row's length plus one and starts one position to the left.  The second green row has a length of red row's plus two, and begins at one position to the left. The third green row has a length of red row's plus three and begins at one position to the left. The rows above the red line are copied below the new green/red section and any original rows below the red line maintains relative position.
"""

import numpy as np

def find_red_line(grid):
    """Finds the row index, starting column index, and length of the horizontal red line."""
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            if pixel == 2:
                length = 0
                while j + length < len(row) and row[j + length] == 2:
                    length += 1
                return i, j, length
    return -1, -1, 0

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    input_grid = np.array(input_grid)
    red_row_index, red_col_index, red_length = find_red_line(input_grid)
    
    if red_row_index == -1:
        return input_grid

    # Calculate output grid dimensions.
    output_grid_width = max(input_grid.shape[1], red_col_index + red_length + 3) # accommodate longest green
    output_grid_height = input_grid.shape[0] + 3 # Add 3 rows for green lines


    output_grid = np.zeros((output_grid_height, output_grid_width), dtype=int)

    # Add green rows.
    green_lengths = [red_length + 1, red_length + 2, red_length + 3]
    green_start = max(0, red_col_index - 1)
    
    for i in range(3):
        for j in range(green_lengths[i]):
            if green_start + j < output_grid_width:
                output_grid[i, green_start + j] = 3

    # Copy red object.
    new_red_row = 3  # Always at row 3
    for j in range(red_length):
        if red_col_index + j < output_grid_width:
          output_grid[new_red_row, red_col_index + j] = 2

    # Copy rows above original red line.
    for i in range(red_row_index):
      for j in range(input_grid.shape[1]):
          output_grid[4 + i, j] = input_grid[i,j]

    # Copy rows below original red line.
    for i in range(red_row_index + 1, input_grid.shape[0]):  # Iterate from the row *after* red
      for j in range(input_grid.shape[1]):
          if i + 3 < output_grid.shape[0] +3 and j < output_grid_width:
              output_grid[i + 3, j] = input_grid[i, j] #copy below red.
    return output_grid