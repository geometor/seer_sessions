"""
Iterate through each pixel of the input grid. If the pixel's color is Magenta (6), change the corresponding pixel in the output grid to Red (2). Otherwise, keep the pixel's original color. The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing Magenta (6) pixels with Red (2) pixels.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed output grid.
    """
    # Convert input_grid to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Get the dimensions of the input grid
    height, width = input_array.shape
    
    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_array)
    
    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Check the color of the current pixel
            if input_array[r, c] == 6:  # If the color is Magenta (6)
                # Change the corresponding pixel in the output grid to Red (2)
                output_grid[r, c] = 2
            # No explicit 'else' needed because we initialized output_grid as a copy
            # If the color is not 6, it remains unchanged (e.g., Orange (7) stays Orange (7))

    return output_grid.tolist() # Return as list of lists, common format for ARC
