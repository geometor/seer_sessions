# 7447852a • 014 • example_3 • investigate_coder

---
```python
"""
Change a white pixel to yellow if it is immediately to the right or immediately below a red pixel, otherwise keep their original color.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule:
    A white pixel (0) changes to yellow (4) if it's immediately to the right or below a red pixel (2).
    """
    output_grid = np.copy(input_grid)  # Initialize output_grid as a copy of the input_grid
    rows, cols = input_grid.shape

    # Iterate through the grid
    for r in range(rows):
        for c in range(cols):
            # Check for red pixels
            if input_grid[r, c] == 2:
                # Change white pixel to the right to yellow
                if c + 1 < cols and input_grid[r, c + 1] == 0:
                    output_grid[r, c + 1] = 4
                # Change white pixel below to yellow
                if r + 1 < rows and input_grid[r + 1, c] == 0:
                    output_grid[r + 1, c] = 4
    return output_grid
```

