"""
1.  **Identify:** Find the single non-black pixel within the input grid.  Note its color.
2.  **Determine Target Location:** Calculate a location that is in the top row, and inset by 2 from both the left and right edges of the grid.
3.  **Create Output:** Create an output grid of the same dimensions as the input grid, filled entirely with black (0) pixels.
4.  **Place Pixel:** Place the identified colored pixel from step 1 into the calculated target location from Step 2 in the output grid, *keeping its original color*.
5.  **Return:** The output grid is the result.
"""

import numpy as np

def find_colored_pixel(grid):
    """Finds the coordinates of the single non-black pixel in a grid."""
    non_black_pixels = np.where(grid != 0)
    if non_black_pixels[0].size > 0:
        return non_black_pixels[0][0], non_black_pixels[1][0]
    return None

def transform(input_grid):
    """Transforms the input grid according to the rule."""

    # 1. Identify the colored pixel and its color.
    colored_pixel_coords = find_colored_pixel(input_grid)
    if colored_pixel_coords is None:
        return input_grid.copy()  # Return a copy if no colored pixel is found.

    color = input_grid[colored_pixel_coords]

    # 2. Determine Target Location: Top row, inset by 2 from left and right edges.
    rows, cols = input_grid.shape
    target_row = 0
    target_col = 2 if cols > 4 else cols - 1 #check if large enough

    # 3. Create Output: Initialize with all black pixels.
    output_grid = np.zeros_like(input_grid)

    # 4. Place Pixel: Place the colored pixel at the target location.
    output_grid[target_row, target_col] = color

    # 5. Return the output grid.
    return output_grid