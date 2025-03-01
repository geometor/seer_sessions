"""
Moves the maroon (9) pixel from the top right corner to the bottom right corner, and repositions other non-white pixels in the last column accordingly, while all other pixels keep original locations.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the initial position of the maroon (9) pixel
    maroon_pos = np.argwhere(input_grid == 9)
    if maroon_pos.size > 0:
      maroon_row, maroon_col = maroon_pos[0]

      # Move the maroon pixel to the bottom right corner
      output_grid[maroon_row, maroon_col] = 0  # Clear original position
      output_grid[rows - 1, maroon_col] = 9      # Set new position

    # Find azure (8) in second row and same column as original
    azure_pos = np.argwhere((input_grid == 8) & (np.arange(rows) == 1)[:, None])

    if azure_pos.size > 0:
        
      azure_row, azure_col = azure_pos[0]
      # move it to the 5th row (index 4)
      output_grid[azure_row, azure_col] = 0
      output_grid[4, azure_col] = 8
    

    return output_grid