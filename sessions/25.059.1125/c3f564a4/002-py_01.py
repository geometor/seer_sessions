"""
The transformation rule is to remove all '0' (white) pixels from each row of the input grid,
effectively compressing the remaining digits horizontally while maintaining their original order.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by removing all '0' pixels from each row.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    # initialize output_grid as a list of lists
    output_grid = []

    # Iterate through each row of the input grid
    for row in input_grid:
        # Create a new row for the output
        new_row = []
        # Iterate through the input row
        for pixel in row:
            # If the pixel is not '0', append it to the new row
            if pixel != 0:
                new_row.append(pixel)
        # Append the compressed row to the output grid
        output_grid.append(new_row)

    # find max width of output grid
    max_width = 0
    for row in output_grid:
      if len(row) > max_width:
        max_width = len(row)

    # pad rows that are less than max_width with elements from the original input
    # rows based on modular arithmetic
    for i in range(len(output_grid)):
        row=output_grid[i]
        if len(row) < max_width:
            original_row = input_grid[i]
            padding_needed = max_width - len(row)
            for j in range(padding_needed):
              # find the next non-zero element
              k = 0
              next_pixel = 0
              while next_pixel == 0:
                next_pixel = original_row[(len(row) + k) % len(original_row)]
                k += 1
              row.append(next_pixel)

    return np.array(output_grid)