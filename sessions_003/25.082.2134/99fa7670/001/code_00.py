"""
Transforms an input grid by expanding non-zero pixels horizontally and vertically.

1. **Identify:** Iterate through the input grid, row by row, and identify all non-zero pixels.
2. **Expand Horizontally:** For each non-zero pixel found, replicate its color value horizontally to the right edge of the grid, creating a row of that color.
3. **Expand Vertically:** Create copies of the the horizontally-expanded rows. Make copies until you've created N new rows, including the first expanded row, where N is the count of all non-zero pixels in the original input grid found at and below the row of current non-zero pixel.
4.  **Maintain Background**: If a pixel in the input is 0, it remains 0 in the output.
"""

import numpy as np

def count_nonzero_pixels_below(input_grid, row_index):
    """Counts non-zero pixels below (and including) a given row."""
    count = 0
    for r in range(row_index, len(input_grid)):
        for val in input_grid[r]:
            if val != 0:
                count += 1
    return count

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""

    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape
    output_row_index = 0

    for row_index in range(rows):
        for col_index in range(cols):
            pixel_value = input_grid[row_index, col_index]
            if pixel_value != 0:
                # Expand Horizontally
                expanded_row = np.concatenate([input_grid[row_index, :col_index], np.full(cols - col_index, pixel_value)])

                # Expand Vertically
                num_copies = count_nonzero_pixels_below(input_grid, row_index)
                for _ in range(num_copies):
                    if output_row_index < rows:
                        output_grid[output_row_index] = expanded_row
                        output_row_index += 1
    return output_grid