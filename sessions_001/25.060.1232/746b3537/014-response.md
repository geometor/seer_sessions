# 746b3537 • 014 • example_4 • investigate_coder

---
```python
"""
The transformation rule identifies pairs of identical rows in the input grid and extracts a single representative row from each pair to construct the output grid, preserving the vertical order.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extracting a single representative row from each pair of identical rows.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the output grid.
    """
    output_grid = []
    rows = input_grid.shape[0]

    # Iterate through rows in pairs
    for i in range(0, rows, 2):
        # Check if there are enough rows for a pair
        if i + 1 < rows:
            # Check if the two rows are identical
            if np.array_equal(input_grid[i], input_grid[i+1]):
                # Add the first row of the pair to the output
                output_grid.append(input_grid[i][0])  # only need the first element if rows are same


    return np.array(output_grid).reshape(-1, 1)
```
