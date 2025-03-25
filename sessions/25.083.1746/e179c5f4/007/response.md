```python
"""
The transformation rule creates a checkerboard pattern of blue (1) and azure (8) pixels in the output grid. The output grid has the same dimensions as the input grid. The top-left cell (0, 0) of the output grid is always azure (8). The rest of the grid follows the checkerboard pattern, where each cell's color alternates based on its row and column indices. If the sum of the row and column indices (row + col) is even, the cell is azure (8); otherwise, it's blue (1). The location of the blue pixel within the input is irrelevant.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # Initialize output_grid with the same dimensions as the input grid
    output_grid = np.empty_like(input_grid)
    rows, cols = input_grid.shape

    # Generate checkerboard pattern
    for r in range(rows):
        for c in range(cols):
            if (r + c) % 2 == 0:
                output_grid[r, c] = 8  # Azure
            else:
                output_grid[r, c] = 1  # Blue

    return output_grid
```
