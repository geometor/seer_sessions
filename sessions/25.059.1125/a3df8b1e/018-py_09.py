"""
1. Identify the single-colored pixel present in the input grid. Note its color.
2. Create a diagonal line running from the top-right corner to the bottom-left corner of the grid.
3. The color of this diagonal line should be the same as the color of the single-colored pixel identified in step 1.
4. If the color of that pixel is blue, replace the pixel with white. Otherwise, keep the pixel in place.
"""

import numpy as np

def find_single_pixel(grid):
    """Finds the coordinates of the single-colored pixel in the grid."""
    rows, cols = grid.shape
    unique_colors = np.unique(grid)
    
    if len(unique_colors) > 1:
        for color in unique_colors:
            if np.sum(grid == color) == 1:
              row, col = np.where(grid == color)
              return row[0], col[0], color

    return None, None, None

def transform(input_grid):
    """Transforms the input grid according to the rules described above."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 1. Find the single-colored pixel and its color.
    single_pixel_row, single_pixel_col, single_pixel_color = find_single_pixel(input_grid)

    # 2 & 3. Create the diagonal line with the same color.
    for r in range(rows):
        for c in range(cols):
            if r == rows - 1 - c:
                output_grid[r, c] = single_pixel_color

    # 4. Replace the blue pixel with white if existed.
    if single_pixel_color == 1:
        if single_pixel_row is not None: # added a check for no single pixel
           output_grid[single_pixel_row, single_pixel_col] = 0

    return output_grid