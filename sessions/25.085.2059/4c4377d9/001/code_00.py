"""
Transforms an input grid by creating a new grid with twice the height. 
The top half of the output grid contains the input grid flipped vertically. 
The bottom half of the output grid is a direct copy of the input grid.
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
    # Convert input list of lists to numpy array if necessary
    input_grid = np.array(input_grid)

    # 1. Determine the height (H) and width (W) of the input grid.
    height, width = input_grid.shape

    # 2. Create a new grid, the output grid, with height 2*H and width W.
    # Initialize with zeros (or any placeholder, as it will be overwritten)
    output_grid = np.zeros((2 * height, width), dtype=input_grid.dtype)

    # 3. Create a vertically flipped version of the input grid.
    # This means arranging the rows of the input grid in reverse order.
    flipped_grid = np.flipud(input_grid)

    # 4. Place this vertically flipped version into the top half of the output grid (rows 0 to H-1).
    output_grid[0:height, :] = flipped_grid

    # 5. Copy the original input grid directly into the bottom half of the output grid (rows H to 2*H-1).
    output_grid[height:2*height, :] = input_grid

    return output_grid.tolist() # Return as list of lists per ARC standard
