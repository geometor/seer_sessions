"""
Transforms an input grid by expanding non-zero pixels horizontally and vertically.

1. **Iterate:** Go through each row of the input grid, from top to bottom.
2. **Horizontal Expansion:** Within each row, examine each pixel. If a pixel is non-zero, expand it horizontally to the right edge of the grid, creating a continuous line of that color. This forms a new, expanded row.
3. **Count and Replicate:** Count the total number of non-zero pixels in the *original* input grid that are in the *current row or below*.
4. **Vertical Placement:**
    * Place the first horizontally-expanded row in the output.
    * Place subsequent copies of the expanded row directly *below* the previous one until the required number of vertically stacked rows are created (from Step 3). If the output grid would exceed the boundaries, complete only the rows that fit, ensuring we never write out of bounds.
5. **Zero Preservation:** Zero-valued pixels in the input remain zero-valued pixels in the output, and are not expanded.
"""

import numpy as np

def count_nonzero_pixels_below(input_grid, row_index):
    """Counts non-zero pixels below (and including) a given row."""
    input_grid = np.array(input_grid)
    return np.count_nonzero(input_grid[row_index:])

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""

    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)
    output_row_index = 0

    for row_index in range(rows):
        for col_index in range(cols):
            pixel_value = input_grid[row_index, col_index]
            if pixel_value != 0:
                # Horizontal Expansion
                expanded_row = np.array([0] * cols)  # initialize the expanded row with zeros
                expanded_row[:col_index] = input_grid[row_index, :col_index] #copy to the expansion
                expanded_row[col_index:] = pixel_value #fill with the pixel value

                # Vertical Placement and Replication
                num_copies = count_nonzero_pixels_below(input_grid, row_index)

                for _ in range(num_copies):
                    if output_row_index < rows:
                        output_grid[output_row_index] = expanded_row
                        output_row_index += 1
        # if we've reached the end and the rest are 0, copy them
        if all(input_grid[row_index] == 0):
            output_grid[output_row_index] = input_grid[row_index]
            output_row_index += 1

    return output_grid