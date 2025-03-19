"""
1.  **Find Blue Region:** Locate the contiguous region of blue pixels (value 1) within the input grid.
2.  **Determine Dimensions:** Calculate the height and width of this blue region.
3.  **Create Output Grid:** Create a new output grid with the same dimensions as the blue region found in the input.
4.  **Fill with Blue:** Fill every cell of the newly created output grid with a blue pixel (value 1).
5. Ignore all non-blue pixels.
"""

import numpy as np

def find_blue_region_dimensions(grid):
    # Find coordinates of all blue pixels.
    blue_pixels = np.argwhere(grid == 1)
    
    # If no blue pixels are found, return (0, 0) for dimensions.
    if blue_pixels.size == 0:
        return (0, 0)
    
    # Find the minimum and maximum row and column indices to define the bounding box.
    min_row, min_col = np.min(blue_pixels, axis=0)
    max_row, max_col = np.max(blue_pixels, axis=0)
    
    # Calculate height and width.
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    
    return (height, width)

def transform(input_grid):
    # Determine the dimensions of the blue region in the input grid.
    height, width = find_blue_region_dimensions(input_grid)

    # Create a new grid with the determined dimensions, filled with blue pixels.
    output_grid = np.ones((height, width), dtype=int)

    return output_grid