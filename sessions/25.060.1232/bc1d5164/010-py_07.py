"""
The transformation extracts a 3x3 subgrid from the input grid. The subgrid is formed by selecting the columns of the input grid that contain the first, middle, and last red pixels.
"""

import numpy as np

def get_red_columns(grid):
    red_columns = []
    rows, cols = grid.shape
    for j in range(cols):
        for i in range(rows):
            if grid[i][j] == 2:
                red_columns.append(j)
                break  # Move to the next column after finding a red pixel
    return red_columns

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find columns with Red Pixels
    red_columns_indices = get_red_columns(input_grid)
    
    # Find the relevant columns
    first = red_columns_indices[0]
    middle = red_columns_indices[len(red_columns_indices)//2]
    last = red_columns_indices[-1]
    
    # Create the output grid
    output_grid = np.array([
      input_grid[:, first],
      input_grid[:, middle],
      input_grid[:, last]
    ]).T


    return output_grid.tolist()