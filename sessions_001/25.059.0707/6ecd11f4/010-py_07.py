"""
Find the 3x3 block of colored pixels. Copy it, but remove any white pixels, leaving only the colored pixels in their original positions within the 3x3 output.
"""

import numpy as np

def find_non_white_subgrid(grid, size=3):
    # Iterate through the grid to find a subgrid of given size
    rows, cols = grid.shape
    for i in range(rows - size + 1):
        for j in range(cols - size + 1):
            subgrid = grid[i:i+size, j:j+size]
            # Check if the subgrid contains any non-white pixels
            if np.any(subgrid != 0):
                return i, j  # Return top-left corner coordinates
    return None, None

def transform(input_grid):
    # Convert input_grid to a NumPy array
    input_grid = np.array(input_grid)

    # Find the top-left corner of the 3x3 non-white subgrid
    start_row, start_col = find_non_white_subgrid(input_grid)

    # Initialize the output grid (3x3)
    output_grid = np.zeros((3, 3), dtype=int)

    if start_row is not None and start_col is not None:
        # Extract the 3x3 subgrid
        subgrid = input_grid[start_row:start_row+3, start_col:start_col+3]

        # copy non zero pixels from the subgrid
        for i in range(3):
            for j in range(3):
                if subgrid[i,j] != 0:
                    output_grid[i,j] = subgrid[i,j]
    
    # now go through and set the non-zero numbers to 
    # the output grid, keep the same relative position
    
    return output_grid.tolist()