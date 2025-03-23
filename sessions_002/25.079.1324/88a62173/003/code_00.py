"""
Extracts a 2x2 subgrid from the input grid. The subgrid is located in the upper-left quadrant.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)

    # Initialize output_grid as an empty 2x2 array.
    output_grid = np.zeros((2,2), dtype=int)
    
    # Extract top left 2x2 subgrid
    output_grid = input_grid[0:2, 0:2].copy()

    return output_grid.tolist()