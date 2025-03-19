"""
The transformation extracts a 3x3 sub-grid from the input grid. The top-left corner of the sub-grid is determined by the first non-white (0) and non-black pixel encountered when scanning the input grid row by row.
"""

import numpy as np

def find_top_left(input_grid):
    # Iterate through rows and columns
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            # Check for non-white and non-black pixel
            if input_grid[r, c] != 0:
                return (r, c)
    return None  # Return None if no such pixel is found

def transform(input_grid):
    """
    Extracts a 3x3 subgrid from the input, starting from the first non-white pixel.
    """
    # Find the top-left corner of the subgrid
    top_left = find_top_left(input_grid)

    # If no non-white pixel is found, return an empty grid or a default value
    if top_left is None:
        return np.zeros((3, 3), dtype=int)

    row, col = top_left

    # Extract the 3x3 subgrid
    # Handle boundary conditions: ensure we don't go out of bounds
    rows, cols = input_grid.shape
    end_row = min(row + 3, rows)
    end_col = min(col + 3, cols)
    
    
    output_grid = input_grid[row:end_row, col:end_col]
     # Pad with zeros if subgrid is less than 3x3
    if output_grid.shape != (3,3):
      temp_grid = np.zeros((3,3),dtype=int)
      temp_grid[:output_grid.shape[0],:output_grid.shape[1]] = output_grid
      output_grid = temp_grid
    
    return output_grid