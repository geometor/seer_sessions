```python
"""
Replaces '0' (white) pixels in the input grid based on these rules:

1. Leading Zeros: At the beginning of each row, before any non-zero pixel:
    - Replace with 5 unless a different non-zero color is encountered first. If so, use that color.
2. Propagation: For remaining '0's, replace them with the value of the nearest non-zero pixel to their left within that row.
3. All-Zero Rows: If a row is all '0's after step 1:
    - If the previous row is uniform (all same non-zero color) and did *not* derive its color from *its* previous row, set the current row to the previous row's color.
    - Otherwise, set the row to '5'. The very first row, if all zeros, is always set to '5'.
"""

import numpy as np

def _get_leftmost_non_zero(row):
    """Finds the index and value of the leftmost non-zero element in a row."""
    for i, val in enumerate(row):
        if val != 0:
            return i, val
    return -1, 0

def _is_uniform(row):
    """Checks if all non-zero elements in the row are the same. Returns the uniform value or None."""
    first = None
    for x in row:
        if x != 0:
            if first is None:
                first = x
            elif x != first:
                return None
    return first

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)
    prev_row_uniform_color = None
    prev_row_derived_from_above = False

    for r in range(rows):
        row = input_grid[r]
        leftmost_non_zero_index, first_non_zero_color = _get_leftmost_non_zero(row)

        # Leading Zeros
        if leftmost_non_zero_index > 0:
            output_grid[r, :leftmost_non_zero_index] = first_non_zero_color if first_non_zero_color else 5
        elif leftmost_non_zero_index == -1:
            # All-Zero Rows
            if r > 0:
                prev_row_uniform_color = _is_uniform(output_grid[r-1])
                if prev_row_uniform_color is not None and not prev_row_derived_from_above:
                    output_grid[r] = np.full(cols, prev_row_uniform_color)
                    current_row_derived_from_above = True
                else:
                    output_grid[r] = np.full(cols, 5)
                    current_row_derived_from_above = False
            else:
                output_grid[r] = np.full(cols, 5)  # First row always 5
                current_row_derived_from_above = False
        else:
             current_row_derived_from_above = False # Reset flag if not all-zero


        # Propagation
        for c in range(leftmost_non_zero_index + 1, cols):
            if output_grid[r, c] == 0:
                for c_left in range(c - 1, -1, -1):
                    if output_grid[r, c_left] != 0:
                        output_grid[r, c] = output_grid[r, c_left]
                        break

        prev_row_derived_from_above = current_row_derived_from_above


    return output_grid
```