"""
Identifies the single non-white object in the input grid, finds the topmost row occupied by this object, and changes the color of all object pixels in that specific row to red (2), leaving all other pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing the color of the topmost row of the non-white object to red.

    Args:
        input_grid (list of lists or np.ndarray): The input grid containing pixel values (0-9).

    Returns:
        np.ndarray: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_array)

    # Find the coordinates of all non-white pixels (pixels > 0)
    non_white_pixels_coords = np.argwhere(input_array > 0)

    # If there are no non-white pixels, return the grid as is
    if non_white_pixels_coords.size == 0:
        return output_grid

    # Find the minimum row index among the non-white pixels
    # This identifies the topmost row containing part of the object
    top_row_index = non_white_pixels_coords[:, 0].min()

    # Iterate through each column index in the grid
    num_cols = input_array.shape[1]
    for col_index in range(num_cols):
        # Check if the pixel in the input grid at (top_row_index, col_index) is non-white
        if input_array[top_row_index, col_index] > 0:
            # If it is non-white (part of the object), change its color to red (2) in the output grid
            output_grid[top_row_index, col_index] = 2

    # Return the modified grid
    return output_grid.tolist() # Convert back to list of lists if required by the environment