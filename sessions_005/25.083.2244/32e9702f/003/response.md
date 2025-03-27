```python
"""
The transformation converts all '0' (white) pixels to '5' (gray). Non-zero pixels
adjacent to '0' pixels (horizontally or vertically) are also converted to '5' (gray).
Other non-zero pixels remain unchanged. This effectively fills the background with
gray and erodes the edges of colored shapes by one pixel.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Helper function to check adjacency
    def is_adjacent_to_zero(r, c, grid):
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 0:
                return True
        return False

    # Iterate through each cell of the input grid
    for i in range(rows):
        for j in range(cols):
            # If the value is 0, replace it with 5
            if input_grid[i, j] == 0:
                output_grid[i, j] = 5
            # Check for adjacency to a zero pixel (now using the helper function)
            elif is_adjacent_to_zero(i, j, input_grid):
                output_grid[i, j] = 5

    return output_grid
```