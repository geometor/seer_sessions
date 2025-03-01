"""
1.  **Identify Target Rows:** Examine each row in the input grid. A row is a "target row" if it contains the colors blue (1) and red (2) in any sequence.
2.  **Double Target Rows:** If a row is a target row, create a new row by concatenating the original row with itself. This doubles the row horizontally.
3.  **Pad Non-Target Rows:** If a row is *not* a target row, create a new row of zeros with a length equal to twice the width of the original input grid.
4.  **Assemble Output:** Create the output grid by stacking the newly created rows (either doubled target rows or zero-padded rows). The height of the output grid remains the same as the input grid, and the width is double.
"""

import numpy as np

def _is_target_row(row):
    """Checks if a row contains both blue (1) and red (2)."""
    return (1 in row) and (2 in row)

def transform(input_grid):
    # Initialize output_grid with doubled width, same height, filled with 0s.
    output_grid = np.zeros((input_grid.shape[0], input_grid.shape[1] * 2), dtype=int)

    # Iterate through each row of the input grid.
    for i, row in enumerate(input_grid):
        # Check if the row is a target row (contains 1 and 2).
        if _is_target_row(row):
            # Double the row horizontally.
            output_grid[i] = np.concatenate((row, row))
        else:
            # Pad with zeros to the correct width.
            output_grid[i] = np.concatenate((row, np.zeros_like(row)))  # Use zeros_like for correct length

    return output_grid