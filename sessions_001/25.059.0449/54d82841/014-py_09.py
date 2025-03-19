"""
1. Find Green: Locate all green pixels (value 3) in the input grid.
2. Identify Bottom-Most Green Row: Find the row with the largest row index containing at least one green pixel.
3. Identify Target Green Pixel:  From the bottom-most green row, select the left-most green pixel.
4. Transform: Change the white pixel directly below the target green pixel (from step 3) from white (0) to yellow (4). If the target green pixel is on the last row, no transformation occurs.
"""

import numpy as np

def find_green_pixels(grid):
    # Find coordinates of all green pixels.
    green_coords = np.argwhere(grid == 3)
    return green_coords

def find_bottom_most_left_most_green_pixel(grid, green_coords):
    # Find the bottom-most row containing green pixels.
    if len(green_coords) == 0:
        return None  # No green pixels
    max_row = np.max(green_coords[:, 0])
    # Get all green pixels in the bottom-most row
    bottom_row_green_pixels = green_coords[green_coords[:, 0] == max_row]
    # Get the leftmost green pixel from bottom row
    min_col = np.min(bottom_row_green_pixels[:, 1])
    target_green_pixel = (max_row, min_col)

    return target_green_pixel

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid.
    output_grid = np.copy(input_grid)

    # Find green pixels.
    green_pixels = find_green_pixels(output_grid)

    # Find the bottom-most, left-most green pixel.
    target_green_pixel = find_bottom_most_left_most_green_pixel(output_grid, green_pixels)
   
    # Change the pixel directly below the target green pixel to yellow if found and within bounds.
    if target_green_pixel:
        row, col = target_green_pixel
        if row + 1 < output_grid.shape[0] and output_grid[row + 1, col] == 0:
            output_grid[row + 1, col] = 4

    return output_grid