"""
1.  Identify Colored Pixels: Locate all pixels within the input grid that are not white (0).
2.  Apply Transformation to Each Colored Pixel: For each non-white pixel:
    *   Change Color:
        *   If the pixel is Red (2), change it to Green (3).
        *   If the pixel is Green (3), change it to Yellow (4).
        *   If the pixel is Yellow (4), change it to Red (2).
    *   Move Pixel: Move the pixel one position up and one position to the left.
    *   Wrap Around:
        *   If the new row index would be -1, wrap around to the last row (height - 1).
        *   If the new column index would be -1, wrap around to the last column (width - 1).
3.  Clear Other Pixels: All other pixels in the grid that were not transformed in step 2 should be set to White (0).
4. Return Grid: Return the updated grid.
"""

import numpy as np

def find_colored_pixels(grid):
    # Find the coordinates and colors of all non-white pixels.
    rows, cols = np.where(grid != 0)
    return [(rows[i], cols[i], grid[rows[i], cols[i]]) for i in range(len(rows))]

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    height = input_grid.shape[0]
    width = input_grid.shape[1]

    # Find all colored pixels in the input grid.
    colored_pixels = find_colored_pixels(input_grid)

    # Apply transformation to each colored pixel
    for row, col, color in colored_pixels:
        # change output pixels
        new_row = (row - 1) % height  # wrap rows
        new_col = (col - 1) % width  # wrap cols
        new_color = {
            2: 3,  # Red to Green
            3: 4,  # Green to Yellow
            4: 2,  # Yellow to Red
        }.get(color)
        output_grid[new_row, new_col] = new_color

    return output_grid