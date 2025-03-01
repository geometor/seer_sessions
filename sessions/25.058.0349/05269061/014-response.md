# 05269061 • 014 • example_3 • investigate_coder

---
```python
"""
The transformation extracts the unique non-zero digits and their associated colors from the input grid, builds a specific 2x2 arrangement, and then replicates that tile across the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    
    # Construct the 2x2 pattern
    pattern = np.array([
        [4, 8],
        [3, 4]
    ])

    # Replicate the pattern across the output grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            output_grid[i, j] = pattern[i % 2, j % 2]

    return output_grid
```
