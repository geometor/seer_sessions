"""
1.  **Identify Red Regions:** Examine the input grid to find contiguous regions of red pixels. Each contiguous region is treated as a single object.
2.  **Determine Bounding Box:** Calculate the bounding box of the red region. This is done by finding the minimum and maximum row and column indices occupied by red pixels.
3.  **Create Output Grid:** Create a new output grid. The dimensions of this grid are determined by the size of the bounding box calculated in the previous step.
4.  **Replicate with Gray:** Iterate through the coordinates within the bounding box. If the corresponding pixel in the input grid is red, set the corresponding pixel in the output grid to gray.
5.  **Handle No Red Pixels**: If no red pixels are found, return an output grid of size 1x1 containing a single black (color 0) pixel.
"""

import numpy as np

def find_red_regions(grid):
    """
    Finds contiguous regions of red pixels in the input grid.
    Returns a list of coordinates of red pixels.
    """
    red_pixels = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 2:  # Red pixel
                red_pixels.append((i, j))
    return red_pixels

def transform(input_grid):
    input_grid = np.array(input_grid)
    
    # Find the coordinates of all red pixels
    red_pixels = find_red_regions(input_grid)
    
    # Handle No Red Pixels
    if not red_pixels:
        return [[0]]

    # Determine Bounding Box
    min_row = min(r[0] for r in red_pixels)
    max_row = max(r[0] for r in red_pixels)
    min_col = min(r[1] for r in red_pixels)
    max_col = max(r[1] for r in red_pixels)

    # Create Output Grid
    output_grid = np.zeros((max_row - min_row + 1, max_col - min_col + 1), dtype=int)

    # Replicate with Gray
    for row, col in red_pixels:
        output_grid[row - min_row, col - min_col] = 5

    return output_grid.tolist()