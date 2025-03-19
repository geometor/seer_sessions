# d406998b • 012 • refine_coder

---
```python
"""
Copy the input grid to the output grid. Then, change all gray pixels that are part of 2x2 gray squares to green.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing gray pixels that are part of 2x2
    gray squares to green.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    for r in range(rows - 1):
        for c in range(cols - 1):
            # Check for 2x2 gray square
            if (output_grid[r, c] == 5 and
                output_grid[r + 1, c] == 5 and
                output_grid[r, c + 1] == 5 and
                output_grid[r + 1, c + 1] == 5):
                # Change all pixels in the 2x2 square to green
                output_grid[r, c] = 3
                output_grid[r + 1, c] = 3
                output_grid[r, c + 1] = 3
                output_grid[r + 1, c + 1] = 3

    return output_grid
```
