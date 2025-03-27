```python
"""
1.  **Identify Changed Rows:** Compare the input grid and the expected output grid row by row. Identify rows where there are *any* differences between the two grids.
2.  **Verify Orange Addition:** For each of the changed rows identified in step 1, verify that the change involves the addition of orange pixels (7) adjacent to the leftmost and rightmost green pixels.
3.  **Process Changed Rows**: For each row identified in step 1 and 2:
    *   Locate the leftmost green (3) pixel. If this pixel is *not* at the beginning of the row (index 0), insert an orange (7) pixel to its immediate left.
    *   Locate the rightmost green (3) pixel. If this pixel is *not* at the end of the row, insert an orange (7) pixel to its immediate right.
4. **Unchanged Rows:** All other rows in the output grid remain identical to their corresponding rows in the input grid.
"""

import numpy as np

def get_changed_rows(input_grid, expected_output):
    # returns rows that are different
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    diff = input_grid != expected_output
    changed_rows = np.any(diff, axis=1)
    return np.where(changed_rows)[0]

def get_green_indices(row):
    # find leftmost and rightmost green pixels
    green_indices = np.where(row == 3)[0]
    if green_indices.size == 0:  # Handle cases with no green pixels
        return None, None
    return green_indices[0], green_indices[-1]

def transform(input_grid, expected_output): # Added expected_output
    """Transforms the input grid by wrapping green blocks with orange pixels."""

    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    changed_rows = get_changed_rows(input_grid, expected_output)  # Use expected_output

    # Iterate through rows that have changed
    for row_index in changed_rows:
        row = input_grid[row_index]
        
        leftmost_green_index, rightmost_green_index = get_green_indices(row)

        # If there are no green pixels skip
        if leftmost_green_index is None:
            continue

        # bounds check and set left pixel to orange
        if leftmost_green_index > 0:
            output_grid[row_index, leftmost_green_index - 1] = 7
        # bounds check and set right pixel to orange
        if rightmost_green_index < len(row) - 1:
            output_grid[row_index, rightmost_green_index + 1] = 7

    return output_grid.tolist()
```