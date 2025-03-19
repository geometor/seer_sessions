"""
1.  **Check for Non-white Pixels:** Inspect the entire input grid.
    -   If only white is present, set all positions to white and add a single yellow pixel in the center of the bottom row.
    -   Otherwise return the input grid
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_grid = np.array(input_grid)
    
    # Check if the input grid contains only white pixels (value 0).
    if np.all(input_grid == 0):
        # Create an output grid that's a copy of the all white input
        output_grid = input_grid.copy()
        # Determine the center column index.
        _, cols = output_grid.shape
        middle_col = cols // 2
        # Set the bottom-middle pixel to yellow (value 4).
        output_grid[-1, middle_col] = 4
    else:
        # return the original input grid
        output_grid = input_grid

    return output_grid.tolist()