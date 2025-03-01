"""
The transformation rule is to crop the input grid to a 3x3 area centered on the blue pixel. If the 3x3 area extends beyond the boundaries of the input grid, pad the output with black pixels (0) to maintain the 3x3 size.
"""

import numpy as np

def find_blue_pixel(grid):
    # Find the coordinates of the blue pixel (value 1).
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 1:
                return (i, j)
    return None  # Should not happen in the intended cases

def transform(input_grid):
    """
    Crops the input grid to a 3x3 area centered on the blue pixel,
    padding with black (0) as needed to ensure a 3x3 output.
    """
    # Find the blue pixel.
    blue_pixel_coords = find_blue_pixel(input_grid)

    if blue_pixel_coords is None:
        return input_grid # defaults to returning input if not found


    # Create a 3x3 output grid filled with black (0).
    output_grid = np.zeros((3, 3), dtype=int)

    # Determine the cropping region.
    row, col = blue_pixel_coords
    start_row = row - 1
    end_row = row + 2
    start_col = col - 1
    end_col = col + 2

    # Calculate the valid ranges for copying from the input grid.
    input_start_row = max(0, start_row)
    input_end_row = min(input_grid.shape[0], end_row)
    input_start_col = max(0, start_col)
    input_end_col = min(input_grid.shape[1], end_col)

    # Calculate the corresponding ranges in the output grid.
    output_start_row = input_start_row - start_row
    output_end_row = output_start_row + (input_end_row - input_start_row)
    output_start_col = input_start_col - start_col
    output_end_col = output_start_col + (input_end_col - input_start_col)
    
    # Copy the valid region from the input grid to the output grid.
    output_grid[output_start_row:output_end_row, output_start_col:output_end_col] = input_grid[input_start_row:input_end_row, input_start_col:input_end_col]
    
    return output_grid