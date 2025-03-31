```python
"""
Apply gravity to non-background pixels within each column independently.

The transformation simulates gravity acting on pixels that are not the background color (azure - 8). 
For each column of the input grid, all non-background pixels "fall" downwards until they either reach the bottom of the grid or land on top of another non-background pixel already settled in that column. The relative vertical order of non-background pixels within a column is preserved. The background color fills the remaining spaces.
"""

import numpy as np

def transform(input_grid):
    """
    Applies gravity independently to each column of the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed grid.
    """
    # Define the background color
    background_color = 8

    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Initialize the output grid with the background color
    output_grid = np.full((height, width), background_color, dtype=int)

    # Iterate through each column
    for c in range(width):
        # Initialize the target row index for placing the next non-background pixel
        # Start from the bottom row
        target_r = height - 1

        # Iterate through the rows of the current column from bottom to top
        for r in range(height - 1, -1, -1):
            # Get the color of the pixel in the input grid
            pixel_color = input_grid[r, c]

            # Check if the pixel is not the background color
            if pixel_color != background_color:
                # Place the non-background pixel in the output grid at the current target row
                output_grid[target_r, c] = pixel_color
                # Move the target row index up by one for the next non-background pixel
                target_r -= 1

    return output_grid
```