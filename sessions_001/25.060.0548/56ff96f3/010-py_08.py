"""
1.  **Identify** all non-white pixels in the input grid.
2.  For each non-white pixel:
    *   Create a rectangle of the *same color* as the identified pixel.
    *   The rectangle's *height* is 3.
    *   The rectangle's *width* is 1.
    *  The rectangle's top-left corner aligns with the *row 0 and the column of the original pixel*.
    * The rectangle's bottom-right corner is always two rows below the top-left corner, and in the same column.
3.  Any cells not covered by a colored rectangle are filled with white (0).
4.  Return the resulting grid.
"""

import numpy as np

def get_non_white_pixels(grid):
    """Finds the coordinates and colors of all non-white pixels."""
    pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                pixels.append(((r, c), grid[r, c]))
    return pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    
    # get all the non-white pixels
    pixels = get_non_white_pixels(input_grid)

    # change output pixels 
    for (row, col), color in pixels:
        # create a 3x1 rectangle
        # the rectangle starts at row 0 and extends down 2 rows
        height = 3
        width = 1
        start_row = 0
        end_row = start_row + height
        start_col = col
        end_col = start_col + width
        
        for r in range(start_row, min(output_grid.shape[0], end_row)):
            for c in range(start_col, end_col):
              output_grid[r,c] = color

    return output_grid