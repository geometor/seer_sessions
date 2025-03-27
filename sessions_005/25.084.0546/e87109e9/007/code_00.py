"""
Remove the top five rows of the input grid. Move all azure (8) pixels that were originally within the top five rows to the top of the output grid, preserving their original column positions. The rest of the grid below the top five rows should remain unchanged, except empty spaces are filled with white (0).
"""

import numpy as np

def transform(input_grid):
    rows, cols = input_grid.shape
    new_rows = rows - 5
    output_grid = np.zeros((new_rows, cols), dtype=int)

    # Copy the lower part of the input grid to the output grid.
    output_grid[5:, :] = input_grid[5:, :]

    # Track the next available row for azure pixels in each column.
    next_azure_row = np.zeros(cols, dtype=int)

    # Iterate through the top 5 rows of the input grid.
    for r in range(min(5, rows)):
        for c in range(cols):
            if input_grid[r, c] == 8:
                # Move the azure pixel to the top of the output grid.
                output_grid[next_azure_row[c], c] = 8
                next_azure_row[c] += 1

    # Copy the section from rows 5 onwards
    output_grid[:new_rows, :] = input_grid[5:,:]
    
    # Move azure pixels that were in top-5 rows
    next_row = [0] * cols
    for col in range(cols):
      for row in range(5):
        if(input_grid[row,col] == 8):
            output_grid[next_row[col],col] = 8
            next_row[col] += 1


    return output_grid