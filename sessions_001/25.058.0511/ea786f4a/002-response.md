# ea786f4a • 002 • example_1 • investigate_coder

---
```python
"""
Iterate through each cell of the input grid. If the cell's value is 1 (blue), change its value to 0 (white). Otherwise, leave the cell's value unchanged. The resulting grid is the output.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input grid.
    output_grid = np.copy(input_grid)

    # Iterate through each cell of the input grid.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # If the cell's value is 1 (blue), change its value to 0 (white).
            if output_grid[i, j] == 1:
                output_grid[i, j] = 0

    return output_grid
```

