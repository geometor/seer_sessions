"""
Transforms an input grid by focusing on elements along the main anti-diagonal.
If the grid has odd dimensions, the center element becomes yellow (4).
Pixels on the main anti-diagonal have their symmetrical counterparts
changed to yellow (4), if the pixel values match. All other pixels
remain unchanged.
"""

import numpy as np

def get_symmetrical_counterpart(row, col, rows, cols):
    """
    Calculates the diagonally symmetrical counterpart's coordinates.
    """
    return rows - 1 - row, cols - 1 - col

def transform(input_grid):
    """
    Transforms the input grid according to the anti-diagonal rule.
    """
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)

    # Iterate through each pixel
    for row_index in range(rows):
        for col_index in range(cols):
            # Central pixel rule (odd dimensions)
            if rows % 2 != 0 and row_index + col_index == rows -1 :
                if rows // 2 == row_index and cols // 2 == col_index:
                    output_grid[row_index,col_index]=4
            # Symmetrical pair rule
            if row_index + col_index == rows - 1 :
                mirrored_row, mirrored_col = get_symmetrical_counterpart(row_index, col_index, rows, cols)

                if 0 <= mirrored_row < rows and 0 <= mirrored_col < cols:
                    if input_grid[row_index, col_index] == input_grid[mirrored_row, mirrored_col]:
                         output_grid[mirrored_row, mirrored_col] = 4



    return output_grid