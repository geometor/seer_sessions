"""
Transforms an input grid by identifying all 2x2 blocks of white (0) pixels
and changing those pixels to red (2) in the output grid. Gray (5) pixels
and white pixels not part of a 2x2 white block remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Identifies 2x2 white blocks in the input grid and colors them red in the output.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed output grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    
    # Initialize the output grid as a copy of the input grid
    output_array = np.copy(input_array)
    
    # Get the dimensions of the grid
    height, width = input_array.shape
    
    # Define the target color (white) and the replacement color (red)
    target_color = 0
    replacement_color = 2

    # Iterate through all possible top-left corners (row, col) of a 2x2 block
    # The loops stop one row/column early to avoid going out of bounds
    for r in range(height - 1):
        for c in range(width - 1):
            # Extract the 2x2 subgrid from the input array
            subgrid = input_array[r:r+2, c:c+2]
            
            # Check if all pixels in the 2x2 subgrid are the target color (white)
            if np.all(subgrid == target_color):
                # If it's a 2x2 white block, change the corresponding
                # pixels in the output array to the replacement color (red)
                output_array[r:r+2, c:c+2] = replacement_color

    # Convert the final NumPy array back to a list of lists for the required output format
    output_grid = output_array.tolist()
    
    return output_grid
