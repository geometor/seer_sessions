# b8825c91 • 012 • refine_coder

---
```python
"""
Identify horizontal lines of yellow (4) pixels. If a horizontal line of yellow pixels is at the top of the grid, or is preceded by a row that does not contain any yellow, change the color of the yellow pixels to blue (1) if there are not other objects directly above. Otherwise leave all other pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row
    for r in range(rows):
        row = input_grid[r, :]
        # Check if the entire row is yellow
        if np.all(row == 4):
            # Check if it's the top row or the preceding row has no yellow
            if r == 0 or not np.any(input_grid[r-1, :] == 4):
                output_grid[r, :] = 1  # Change all yellow to blue

    return output_grid
```

