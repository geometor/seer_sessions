"""
The transformation creates a 3x3 output grid based on the presence of non-zero values in the input grid. If the input grid contains only zeros, the output is a 3x3 grid of zeros. If non-zero values exist, a "cross-like" pattern of gray (5) pixels is created. The position of the cross is determined by the general location of non-zero cells in the input, and it is always 5 pixels.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to a NumPy array.
    input_grid = np.array(input_grid)
    
    # Initialize a 3x3 output grid filled with zeros (white).
    output_grid = np.zeros((3, 3), dtype=int)
    
    # Check if there are any non-zero values in the input grid.
    if np.any(input_grid != 0):
        # Find the row and column indices of non-zero elements.
        rows, cols = np.nonzero(input_grid)
        
        # Determine the relative position of non-zero elements.
        # Calculate the average row and column index.
        avg_row = np.mean(rows)
        avg_col = np.mean(cols)

        # Create cross centered at (1,1)
        if avg_col < input_grid.shape[1] * (2/3):
          output_grid[0, 1] = 5
          output_grid[1, 0] = 5
          output_grid[1, 1] = 5
          output_grid[1, 2] = 5
          output_grid[2, 1] = 5

        # Create cross centered at (2,2)
        else:
          output_grid[0, 2] = 5
          output_grid[1, 2] = 5
          output_grid[2, 2] = 5
          output_grid[2, 1] = 5
          output_grid[2, 0] = 5

    return output_grid.tolist()