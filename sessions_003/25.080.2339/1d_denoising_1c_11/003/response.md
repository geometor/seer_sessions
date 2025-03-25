```python
"""
Remove any single pixel that has a different color than *both* of its neighbors.
"""

import numpy as np

def transform(input_grid):
    """Transforms a 1D grid by removing isolated single pixels."""

    output_grid = input_grid.copy()
    grid_length = len(input_grid)

    # Iterate over the grid
    for i in range(grid_length):
        # Get neighbor values, handling edge cases.  Treat edge pixels as *keeping* the pixel.
        left_neighbor = input_grid[i - 1] if i > 0 else input_grid[i]
        right_neighbor = input_grid[i + 1] if i < grid_length - 1 else input_grid[i]

        # Check if the current pixel is different from both neighbors
        if input_grid[i] != left_neighbor and input_grid[i] != right_neighbor:
            output_grid[i] = 0  # Remove the pixel (set to 0)

    return output_grid
```
