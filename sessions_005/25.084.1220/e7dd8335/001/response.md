```python
"""
Identify all blue pixels (1) in the input grid. Determine the minimum (min_row) and maximum (max_row) row indices containing blue pixels. Calculate the dividing row index as floor((min_row + max_row) / 2). The row from which changes start is this dividing index + 1 (change_start_row). Create an output grid by copying the input grid. Iterate through the output grid; if a pixel is blue (1) and its row index is greater than or equal to change_start_row, change its color to red (2). Otherwise, keep the pixel's original color.
"""

import numpy as np
import math

def transform(input_grid):
    """
    Transforms the input grid by changing the color of blue pixels in the lower half
    of the shape's vertical extent to red.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    
    # Find the coordinates of all blue pixels (value 1)
    blue_pixels = np.where(grid == 1)
    blue_rows = blue_pixels[0]
    blue_cols = blue_pixels[1]

    # If there are no blue pixels, return the grid unchanged
    if len(blue_rows) == 0:
        return output_grid.tolist()

    # Determine the minimum and maximum row indices occupied by blue pixels
    min_row = np.min(blue_rows)
    max_row = np.max(blue_rows)

    # Calculate the row index that marks the beginning of the lower half
    # Use integer division // which is equivalent to floor for positive results
    # Note: ARC often uses integer math, floor seems appropriate here based on examples.
    dividing_row_index = math.floor((min_row + max_row) / 2)
    change_start_row = dividing_row_index + 1

    # Iterate through all blue pixels identified earlier
    for r, c in zip(blue_rows, blue_cols):
        # If a blue pixel's row index is greater than or equal to change_start_row
        if r >= change_start_row:
            # Change its color to red (2) in the output grid
            output_grid[r, c] = 2

    # Convert the numpy array back to a list of lists before returning
    return output_grid.tolist()

```