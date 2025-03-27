"""
The transformation rule can be described as follows:

1.  **Iterate** through the rows of the input grid.
2.  For each row, **select** elements (colored pixels) from left-to-right, skipping every other column, beginning the skip with the last (right-most) element.
3.  **Construct** a new row in the output grid using these selected elements.
4.  The output grid is composed of these new shortened rows, maintaining the original row order. In short: The output grid takes every other column from the input starting at the first.

Essentially every other column, starting with the last, is removed from the input.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by keeping every other column, starting from the first.
    """
    # Convert input grid to numpy array for easier manipulation
    input_array = np.array(input_grid)

    # Initialize output grid as an empty list
    output_grid = []

    # Iterate through each row
    for row in input_array:
        # Select every other element starting from index 0
        new_row = row[::2]
        # Append the modified row to output
        output_grid.append(new_row.tolist())

    return output_grid