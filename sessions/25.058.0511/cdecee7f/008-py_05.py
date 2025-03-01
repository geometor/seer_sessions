"""
1. **Selection:** Examine the input grid and select all non-zero (non-white) pixels.
2. **Ordering of selected pixels:** Sort to-be-outputted pixels based on their original row position from lowest to highest.
3.  **Arrangement:** Arrange these pixels in a way that preserves the spatial relationship relative to each other based on row and relative col locations, fitting into the bounds of a 3x3 matrix.
4. **Output:** form into a 3 x 3 grid
"""

import numpy as np

def get_nonzero_pixels(grid):
    """
    Finds and returns the coordinates and values of non-zero pixels in a grid.
    """
    pixels = []
    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            if value != 0:
                pixels.append(((row_idx, col_idx), value))
    return pixels


def transform(input_grid):
    """
    Transforms the input grid into a 3x3 output grid by selecting non-zero
    pixels, ordering them by row, and arranging in original relative positions.
    """
    # 1. Selection: Get all non-zero pixels.
    nonzero_pixels = get_nonzero_pixels(input_grid)

    # 2. Ordering: Sort pixels by their original row index.
    sorted_pixels = sorted(nonzero_pixels, key=lambda item: item[0][0])

    # 3. Arrangement: Place into the output grid.
    output_grid = np.zeros((3, 3), dtype=int)
    
    # build output row by row
    output_row = 0
    output_col = 0
    
    while len(sorted_pixels) > 0 and output_row < 3:
        row_pixels = []
        base_row_index = sorted_pixels[0][0][0]
        
        # build up the row with up to 3 pixels
        while len(sorted_pixels) > 0 and sorted_pixels[0][0][0] == base_row_index and len(row_pixels) < 3:
            row_pixels.append(sorted_pixels.pop(0))

        # sort row pixels by column index
        row_pixels.sort( key=lambda item: item[0][1])

        # place into this row of the output
        output_col = 0
        while len(row_pixels) > 0 and output_col < 3:
            pixel = row_pixels.pop(0)
            output_grid[output_row, output_col] = pixel[1]
            output_col += 1

        # finished with row, move down
        output_row += 1
    

    return output_grid