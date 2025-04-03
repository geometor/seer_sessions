"""
1. Start with the input grid (a single row).
2. Scan the grid to find the single, isolated non-white pixel (the "target pixel"). 
   An isolated pixel is defined as a non-white pixel whose immediate left and right neighbors are white (0) or grid boundaries.
3. Record the color of the target pixel (`target_color`) and its column position (`target_col`). 
   Ignore any non-isolated non-white pixels (like the initial 3-pixel block).
4. Create a new grid (the output grid) initially identical to the input grid.
5. In the output grid, set the color of the pixel at column `target_col - 1` to `target_color`.
6. Set the color of the pixel at column `target_col` to `target_color`.
7. Set the color of the pixel at column `target_col + 1` to `target_color`. 
   (Ensure column indices remain within grid bounds).
8. The resulting grid is the final output.
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
    # Assuming grid is always 1 row based on examples
    if grid.shape[0] != 1:
        # Handle unexpected dimensions if necessary
        return None 

    row = 0
    width = grid.shape[1]
    for col in range(width):
        color = grid[row, col]
        if color != 0: # Found a non-white pixel
            # Check left neighbor (or boundary is considered white)
            is_left_white = (col == 0) or (grid[row, col - 1] == 0)
            # Check right neighbor (or boundary is considered white)
            is_right_white = (col == width - 1) or (grid[row, col + 1] == 0)

            # If both neighbors are white (or boundary), it's isolated
            if is_left_white and is_right_white:
                return row, col, color # Return info for the first one found
                
    return None # No isolated pixel found

def transform(input_grid):
    """
    Transforms the input grid by finding a single isolated non-white pixel
    and replacing the pixel, its left neighbor, and its right neighbor 
    with a 1x3 block of the isolated pixel's color.

    Args:
        input_grid (np.array): A 1xN numpy array representing the input grid.

    Returns:
        np.array: The transformed grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape # Get dimensions

    # Find the target isolated pixel
    target_info = find_isolated_pixel(input_grid)

    # If an isolated pixel was found
    if target_info:
        row, target_col, target_color = target_info

        # Define the 3 columns to be modified
        # Start one column to the left of the target pixel
        col_start = target_col - 1
        col_mid = target_col
        col_end = target_col + 1

        # Apply the transformation: create a 1x3 block
        # Check bounds before modifying
        if col_start >= 0:
            output_grid[row, col_start] = target_color
        
        # The middle pixel (original target_col) is always within bounds if target_info was found
        output_grid[row, col_mid] = target_color
            
        if col_end < width:
            output_grid[row, col_end] = target_color
            
    # If no isolated pixel is found, the grid remains unchanged (due to the copy)
    return output_grid