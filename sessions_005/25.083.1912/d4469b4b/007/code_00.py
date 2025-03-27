"""
The transformation creates a 3x3 output grid. If the input grid contains only zeros, the output is a 3x3 grid of zeros. If non-zero values exist, a "cross-like" pattern of gray (5) pixels is created. The position of the cross depends on the maximum column index of the non-zero values.
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
        
        # Determine the center column of the cross.
        max_col = np.max(cols)
        center_col = 1 if max_col < input_grid.shape[1] * (2/3) else 2

        # Create cross centered at (1, center_col)
        output_grid[1, center_col] = 5
        output_grid[0, center_col] = 5
        output_grid[2, center_col] = 5
        output_grid[1, max(0, center_col - 1)] = 5
        output_grid[1, min(2, center_col + 1)] = 5
    return output_grid.tolist()