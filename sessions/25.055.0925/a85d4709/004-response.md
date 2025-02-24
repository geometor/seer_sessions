# a85d4709 • 004 • refine_coder

---
```python
"""
The transformation rule is as follows:
1. Any gray (5) pixel becomes green (3).
2. Any white (0) pixel becomes red (2).
3. All other pixels retain their original color.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    output_grid = np.copy(input_grid)  # Start with a copy of the input grid
    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid
    for i in range(rows):
        for j in range(cols):
            # Gray Transformation: gray(5) becomes green(3)
            if input_grid[i, j] == 5:
                output_grid[i, j] = 3
            # White Transformation: white(0) becomes red(2)
            elif input_grid[i, j] == 0:
                output_grid[i, j] = 2
            # All other pixels are already correctly copied.

    return output_grid
```

