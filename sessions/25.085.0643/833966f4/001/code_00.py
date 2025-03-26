"""
Rearrange pixels within a single-column grid by swapping adjacent pairs. Iterate through the column starting from index 0 with a step of 2. If an index i and the next index i+1 are both valid, swap the pixels at these positions. If i+1 is out of bounds (for odd-height columns), the pixel at index i remains unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Swaps adjacent pairs of pixels in a single-column input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid (Nx1).

    Returns:
        np.array: A 2D numpy array representing the output grid with pixels swapped.
    """
    # Make a copy of the input grid to modify
    output_grid = np.copy(input_grid)
    
    # Get the height (number of rows) of the grid
    height = input_grid.shape[0]
    
    # Iterate through the rows with a step of 2
    for i in range(0, height, 2):
        # Check if the next index (i+1) is within the grid bounds
        if i + 1 < height:
            # Swap the pixels at index i and i+1
            # Store the value at i temporarily
            temp = output_grid[i, 0]
            # Assign the value at i+1 to i
            output_grid[i, 0] = output_grid[i+1, 0]
            # Assign the temporary value (original value at i) to i+1
            output_grid[i+1, 0] = temp
            
    # If i+1 is out of bounds (odd height, i is the last index), 
    # the pixel at i remains unchanged, so no action needed.
            
    return output_grid
