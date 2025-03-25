```python
"""
Transforms a 3x3 input grid (containing 0s and 1s) to a 3x3 output grid (containing 0s and 2s)
based on the following rule:
If a row starts with a contiguous sequence of 1s from left to right, then only those contiguous 1s are replaced by 2s.  If a 1 appears in a row that is not connected to the left-most cell, it remains unchanged.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    output_grid = np.copy(input_grid)  # Initialize output as a copy

    # Iterate through each row
    for i in range(output_grid.shape[0]):
        # Iterate through columns, checking for contiguous 1s from the left
        for j in range(output_grid.shape[1]):
            if j == 0 and output_grid[i, j] == 1:  # First element in row is 1
                output_grid[i, j] = 2
            elif j > 0 and output_grid[i, j] == 1 and output_grid[i, j-1] == 2: # Subsequent contiguous 1
                output_grid[i, j] = 2
            else:
                # If not contiguous, the chain of 1s changes is done
                break

    return output_grid
```