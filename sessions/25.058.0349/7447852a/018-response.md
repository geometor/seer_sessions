# 7447852a • 018 • refine_coder

---
```python
"""
Iterate through the grid. If a pixel is red (color 2), check the pixel immediately to its right and the pixel immediately below it. If either of those adjacent pixels is white (color 0), change that white pixel to yellow (color 4). Do not change any other pixels. Importantly, do *not* recursively apply this rule to newly created yellow pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)  # Initialize output_grid as a copy of the input_grid
    rows, cols = input_grid.shape

    # Iterate through the grid, looking for red pixels *only*.
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 2:  # Found a red pixel
                # Check the pixel to the right
                if c + 1 < cols and input_grid[r, c + 1] == 0:
                    output_grid[r, c + 1] = 4
                # Check the pixel below
                if r + 1 < rows and input_grid[r + 1, c] == 0:
                    output_grid[r + 1, c] = 4
    return output_grid
```

