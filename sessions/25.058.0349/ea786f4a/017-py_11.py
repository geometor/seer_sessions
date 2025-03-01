"""
1.  **Identify Rows with White:** Determine which rows in the input grid contain at least one white pixel. The count of these rows determines the height of the output grid.
2.  **Locate White Columns:** Find the x-coordinates (column indices) of all white pixels in the input grid.
3. **Translate Gray:** For each gray pixel in the input, copy gray pixels to the same row and column of the output as long as the row and column exist within the bounds of the output shape.
4.  **Create White Lines:** For each column identified in step 2, create a vertical line of white pixels in the output grid. The line's height is determined in step 1, and its x-coordinate is the same as the input white pixel's column.
"""

import numpy as np

def _get_rows_with_white(input_grid):
    # Find rows with at least one white pixel
    return np.any(input_grid == 0, axis=1)

def _get_white_cols(input_grid):
    #find column indexes that have white
    return np.where(np.any(input_grid == 0, axis=0))[0]

def transform(input_grid):
    # Determine output height based on rows with white pixels
    rows_with_white = _get_rows_with_white(input_grid)
    output_height = np.sum(rows_with_white)
    
    # Get the x-coordinates of the white pixels
    white_cols = _get_white_cols(input_grid)
    
    # Initialize the output grid with the correct height and the same width as the input
    output_grid = np.full((output_height, input_grid.shape[1]), 5, dtype=int)

    # Fill in the white lines based on the located white columns
    for col in white_cols:
        output_grid[:, col] = 0

    return output_grid