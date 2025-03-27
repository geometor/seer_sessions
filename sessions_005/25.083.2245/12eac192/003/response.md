```python
"""
1.  Identify Seed Pixels: Locate all blue (value 1) pixels in the input grid.
2. Conditional Replacement:
    -  If a blue pixel is in the top row, replace it with green (3).
    -  If a blue pixel is in the leftmost column, replace it with green (3).
3.  Preserve Other Pixels: All other pixels retain their original values.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rules described above.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through all cells using indices.
    for i in range(rows):
        for j in range(cols):
            # Check for blue pixels (value 1).
            if input_grid[i, j] == 1:
                # Replace with green (3) if in the top row or leftmost column.
                if i == 0 or j == 0:
                    output_grid[i, j] = 3

    return output_grid
```