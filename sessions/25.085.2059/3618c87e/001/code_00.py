"""
Moves each blue pixel (color 1) vertically downwards to the last row of the grid, within the same column. 
The original position of the blue pixel becomes white (color 0). 
The destination cell in the last row becomes blue (color 1), overwriting its previous content. 
All other pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a deep copy of the input grid
    output_grid = np.copy(input_grid_np)
    
    # Get the dimensions of the grid
    height, width = input_grid_np.shape
    
    # Determine the index of the bottom row
    bottom_row_index = height - 1
    
    # Iterate through each cell (row, column) of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell contains a blue pixel (color 1)
            if input_grid_np[r, c] == 1:
                # Change the original position in the output grid to white (0)
                output_grid[r, c] = 0
                # Change the corresponding cell in the bottom row to blue (1)
                output_grid[bottom_row_index, c] = 1
                
    # Convert back to list of lists if necessary, or return numpy array
    # Assuming the standard ARC format expects list of lists
    return output_grid.tolist()
