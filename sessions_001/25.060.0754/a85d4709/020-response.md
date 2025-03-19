# a85d4709 • 020 • refine_coder

---
```python
"""
The transformation rule is a direct color substitution. Every gray (5) pixel in the input grid becomes a red (2) pixel in the output grid. Every white (0) pixel in the input grid becomes a yellow (4) pixel in the output grid. The dimensions of the grid, and any pixels that are not gray or white, are unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.  This ensures
    # that the dimensions are the same and that colors other than gray and
    # white are preserved.
    output_grid = np.copy(input_grid)

    # Iterate through each cell of the input grid, using numpy's vectorized
    # operations for efficiency.
    output_grid[output_grid == 5] = 2  # Replace all gray (5) pixels with red (2)
    output_grid[output_grid == 0] = 4  # Replace all white (0) pixels with yellow (4)

    return output_grid
```

