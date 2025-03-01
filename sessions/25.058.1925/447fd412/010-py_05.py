"""
The transformation preserves a central blue cross shape and reflects red pixels across it, 
turning the mirrored pixels blue if the mirrored pixel is white.
"""

import numpy as np

def find_blue_cross_center(grid):
    # Find all blue pixels
    blue_pixels = np.argwhere(grid == 1)
    if blue_pixels.size == 0:
        return None

    # Calculate the center of the blue pixels
    center_row = int(np.mean(blue_pixels[:, 0]))
    center_col = int(np.mean(blue_pixels[:, 1]))
    return (center_row, center_col)

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Find the center of the blue cross
    cross_center = find_blue_cross_center(input_grid)
    if cross_center is None:
        return output_grid  # Return original if no blue cross
    
    # Locate all red pixels
    red_pixels = np.argwhere(input_grid == 2)
    
    # For each red pixel, calculate its mirrored position and change the output_grid
    for row, col in red_pixels:
        # Calculate the mirrored position relative to the cross center
        row_offset = row - cross_center[0]
        col_offset = col - cross_center[1]
        mirrored_row = cross_center[0] - row_offset
        mirrored_col = cross_center[1] - col_offset

        #check bounds
        if 0 <= mirrored_row < output_grid.shape[0] and 0 <= mirrored_col < output_grid.shape[1]:
            # Change the mirrored pixel to blue if white
            if output_grid[mirrored_row, mirrored_col] == 0:
                output_grid[mirrored_row, mirrored_col] = 1
    
    return output_grid