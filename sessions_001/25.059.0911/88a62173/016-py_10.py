"""
Extracts a 2x2 subgrid from the input grid, preserving the color and relative position of the four corner pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the four corner pixels of the input grid and forms a 2x2 output grid.
    """
    # Convert input to numpy array for easier manipulation.
    input_array = np.array(input_grid)
    
    # Get dimensions of the input grid.
    rows, cols = input_array.shape
    
    # Initialize the output grid as a 2x2 array.  Fill with a default value (e.g., 0)
    output_grid = np.zeros((2, 2), dtype=int)
    
    # Extract the corner pixels and place them in the output grid.
    output_grid[0, 0] = input_array[0, cols - 1]  # Top-right
    output_grid[0, 1] = input_array[0,0] #top-left
    output_grid[1, 0] = input_array[rows-1, cols-1] #bottom-right
    output_grid[1, 1] = input_array[rows - 1, 0]    # Bottom-left

    output_grid[0, 0], output_grid[0, 1] = output_grid[0, 1], output_grid[0, 0]
    output_grid[1, 0], output_grid[1, 1] = output_grid[1, 1], output_grid[1, 0]
    
    return output_grid.tolist() # Convert back to list