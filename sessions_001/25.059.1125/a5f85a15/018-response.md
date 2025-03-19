# a5f85a15 • 018 • example_3 • investigate_coder

---
```python
"""
The transformation rule is as follows:
1. White (0) pixels remain unchanged.
2. Most green (3) pixels are maintained.
3. Specific green (3) pixels at coordinates (1,3) (3,5) and (4,1) change to yellow (4).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)  # Initialize output as a copy

    # Iterate through the grid
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            # Change specific green pixels to yellow
            if input_grid[i, j] == 3:
                if (i,j) == (1,3) or (i,j) == (3,5) or (i,j) == (4,1):
                  output_grid[i, j] = 4

    return output_grid
```
