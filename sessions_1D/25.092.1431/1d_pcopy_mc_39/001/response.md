```python
"""
1.  Start with the input grid (a single row).
2.  Scan the grid to find the single, isolated non-white pixel (the "target pixel"). 
    An isolated pixel is defined as a non-white pixel whose immediate left and right neighbors are white (or grid boundaries).
3.  Record the color of the target pixel (`target_color`) and its column position (`target_col`). 
    Ignore any blocks of three non-white pixels or other non-isolated pixels.
4.  Create a new grid (the output grid) initially identical to the input grid.
5.  In the output grid, set the color of the pixel at column `target_col` to `target_color`.
6.  Set the color of the pixel at column `target_col + 1` to `target_color`.
7.  Set the color of the pixel at column `target_col + 2` to `target_color`. 
    Assume there is always enough space to the right based on examples.
8.  The resulting grid is the final output.
"""

import numpy as np

def find_isolated_pixel(grid):
    """
    Finds the first single, isolated non-white pixel in a 1-row grid.
    An isolated pixel has white (0) neighbors (or is at a boundary).

    Args:
        grid (np.array): A 1xN numpy array representing the input grid row.

    Returns:
        tuple: (row, col, color) of the isolated pixel, or None if not found.
               Since it's a 1-row grid, row will always be 0.
    """
    if grid.shape[0] != 1:
        # This function assumes a 1-row grid based on the examples
        # Handle potential multi-row grids if necessary, though unlikely for this task
        print("Warning: Expected a 1-row grid.")
        return None # Or adapt logic for multi-row

    row = 0
    width = grid.shape[1]
    for col in range(width):
        color = grid[row, col]
        if color != 0: # Found a non-white pixel
            # Check left neighbor (or boundary)
            is_left_white = (col == 0) or (grid[row, col - 1] == 0)
            # Check right neighbor (or boundary)
            is_right_white = (col == width - 1) or (grid[row, col + 1] == 0)

            if is_left_white and is_right_white:
                # This is the isolated pixel
                return row, col, color
    return None # No isolated pixel found

def transform(input_grid):
    """
    Transforms the input grid by finding a single isolated non-white pixel
    and expanding it into a 1x3 block of the same color.

    Args:
        input_grid (np.array): A 1xN numpy array representing the input grid.

    Returns:
        np.array: The transformed grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # Find the target isolated pixel
    target_info = find_isolated_pixel(input_grid)

    if target_info:
        row, target_col, target_color = target_info

        # Apply the transformation: expand the pixel to a 1x3 block
        # The pixel itself is already the correct color in the copy
        # We just need to color the next two pixels to the right
        # Ensure we don't go out of bounds (though examples suggest it's safe)
        if target_col + 1 < width:
            output_grid[row, target_col + 1] = target_color
        if target_col + 2 < width:
            output_grid[row, target_col + 2] = target_color
            
    # If no isolated pixel is found, the grid remains unchanged (per the copy)
    return output_grid

```