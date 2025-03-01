# b8cdaf2b • 018 • refine_coder

---
```python
"""
1.  Identify Target Row: Scan the input grid from top to bottom and find the *first* row that contains exactly 5 white (0) pixels.
2.  Modify Target Row: In the identified row:
    *   Change the leftmost pixel (first column) to blue (1).
    *   Change the rightmost pixel (last column) to blue (1).
    *   Change all the pixels between the leftmost and rightmost to white(0).
3.  Preserve Other Rows: All other rows in the grid remain unchanged.
"""

import numpy as np

def find_row_with_n_white(grid, n):
    """Helper function to find the first row with n white pixels."""
    for i, row in enumerate(grid):
        if np.sum(row == 0) == n:
            return i
    return None  # Return None if no such row is found


def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)  # Initialize output as a copy of the input

    # Find the target row
    target_row_index = find_row_with_n_white(input_grid, 5)

    if target_row_index is not None:
        # Modify the target row
        output_grid[target_row_index, :] = 0  # Set all elements to white (0)
        output_grid[target_row_index, 0] = 1  # Set leftmost to blue (1)
        output_grid[target_row_index, -1] = 1  # Set rightmost to blue (1)

    return output_grid
```

