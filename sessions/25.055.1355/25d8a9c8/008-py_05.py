"""
1. Identify the input grid (3x3).
2. Select the pixels in the middle row.
3. Change selected middle row the pixel colors to gray (value 5).
4. Replace all other pixels with white (0)
5. Output the modified grid.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""

    # Initialize the output grid with the same dimensions as the input, filled with white (0).
    output_grid = np.zeros_like(input_grid)

    # Get the middle row index.
    middle_row_index = input_grid.shape[0] // 2

    # Change the middle row to gray (5).
    output_grid[middle_row_index, :] = 5
    
    return output_grid