"""
1.  **Examine the Top Row:** Inspect the top row of the input grid.
2.  **Check for all Zeros**: if all values are zero, change element (0,0) to 6.
3.  **Locate Non-Zero:** Otherwise, identify the *first* non-zero number within the top row.
4.  **Transform Value:**
    *   If the value is 7, replace with 5.
    *   Otherwise, double the value.
5.  **Replace First Non-Zero:** In the top row, replace the first non-zero value encountered (scanning from left to right) with the transformed value.
6. **Preserve Rest:** All other rows, and elements within the top row, in the grid remain unchanged.
7.  **Output:** The modified grid is the final output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the first non-zero element in the top row
    first_non_zero_index = -1
    first_non_zero_value = 0
    for j in range(cols):
        if output_grid[0, j] != 0:
            first_non_zero_index = j
            first_non_zero_value = output_grid[0,j]
            break

    # Apply transformation rules
    if first_non_zero_index == -1:
        # All zeros in the top row
        output_grid[0, 0] = 6
    else:
        # Transform based on value
        if first_non_zero_value == 7:
            output_grid[0, first_non_zero_index] = 5
        else:
            output_grid[0, first_non_zero_index] = first_non_zero_value * 2

    return output_grid