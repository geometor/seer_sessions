"""
Transforms an input grid by adding rows of green and blue pixels above a horizontal line of red pixels. The length of the green rows is three more than the length of the red row. The length of the blue is equal to the difference between the length of the green and blue lines. The number of blue rows is determined by the original y-position of the red object minus the new y-position of the red object.
"""

import numpy as np

def find_red_line(grid):
    """Finds the row index and length of the horizontal red line."""
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            if pixel == 2:
                length = 0
                while j + length < len(row) and row[j + length] == 2:
                    length += 1
                return i, j, length
    return -1, -1, 0  # Return -1, -1 if no red line is found.

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    input_grid = np.array(input_grid)
    red_row_index, red_col_index, red_length = find_red_line(input_grid)
    
    if red_row_index == -1:  # no red pixels in grid
      return input_grid

    green_length = red_length + 3
    blue_length = 1


    # Initialize output grid with extra space at the top.
    # We might add up to 2 green rows.  Blue rows depend on red_row_index
    output_grid_height = len(input_grid) + 2
    output_grid = np.zeros((output_grid_height, len(input_grid[0])), dtype=int)


    # Add green rows, but only as many as fit
    green_rows_added = 0
    for i in range(min(2,output_grid_height)):
        output_grid[i,:green_length] = 3
        green_rows_added += 1

    # Determine how many blue rows.
    new_red_row = red_row_index + green_rows_added - 2 if (red_row_index + green_rows_added -2) >= 0 else 0

    num_blue_rows = new_red_row #red_row_index - 2 if red_row_index >= 2 else 0
    for i in range(green_rows_added, green_rows_added+num_blue_rows): # add before red
        if i < output_grid_height: # fit within bounds
          output_grid[i,:blue_length] = 1

    # Copy red object to correct index.
    output_grid[new_red_row, :red_length] = 2

    # Copy other portions of the grid below this.
    rows_to_copy = input_grid.shape[0] - red_row_index # original grid height - original red row
    for i in range(rows_to_copy):
      y = new_red_row + 1 + i # original red object index plus one plus counter
      if y < output_grid.shape[0]: # check if y position is within new grid
        row_size = input_grid.shape[1]
        for j in range(row_size): # check for the original row
          if input_grid[red_row_index+1+i,j] != 2: # do not add 2s
            output_grid[y, j] = input_grid[red_row_index+1+i, j]

    return output_grid