"""
Finds a contiguous shape of green pixels in the input grid and changes the color of one of its "center" pixels to yellow.
"""

import numpy as np

def find_green_shape(grid):
    # Find all green pixels
    green_pixels = np.argwhere(grid == 3)
    
    # If no green pixels, return None
    if len(green_pixels) == 0:
        return []

    # Return the coordinates of the green pixels
    return green_pixels

def find_center_pixel(grid, green_pixels):
    # Find a pixel within shape that does not touch boundary
    rows, cols = grid.shape
    
    for r, c in green_pixels:
        is_center = True
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr, nc] != 3:
                    is_center = False
                    break
            else:
                is_center = False # Consider boundary touches as not center
                break        
        if is_center:
             return (r,c)
    return None

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find the green shape
    green_shape_pixels = find_green_shape(input_grid)
    
    # if no green pixels are found return input grid
    if not green_shape_pixels.any():
       return output_grid

    # Find the "center" pixel of the green shape
    center_pixel = find_center_pixel(input_grid, green_shape_pixels)

    # Change the color of the center pixel to yellow (4)
    if center_pixel:
      output_grid[center_pixel] = 4

    return output_grid