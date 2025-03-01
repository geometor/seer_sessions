# b27ca6d3 • 008 • refine_coder

---
```python
"""
1.  **Identify** all red (2) pixels within the input grid.
2.  **For each** red pixel:
    *   **Check for adjacent white pixels:** If there's a white (0) pixel directly to the left, change it to green (3).
    *   **Check for adjacent white pixels:** If there's a white (0) pixel directly to the right, change it to green (3).
    *   **Check for adjacent white pixels:** If there's a white (0) pixel directly above, change it to green (3).
    *   **Check for adjacent white pixels:** If there's a white (0) pixel directly below, change it to green (3).
3.  **All other pixels remain unchanged.** The transformation only affects white pixels that are immediately adjacent to a red pixel.
"""

import numpy as np

def get_red_pixels(grid):
    """Finds the coordinates of all red (2) pixels in the grid."""
    red_pixels = []
    for row_index, row in enumerate(grid):
        for col_index, pixel in enumerate(row):
            if pixel == 2:
                red_pixels.append((row_index, col_index))
    return red_pixels

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    red_pixels = get_red_pixels(input_grid)

    for row, col in red_pixels:
        # Check and change left neighbor
        if col > 0 and input_grid[row, col - 1] == 0:
            output_grid[row, col - 1] = 3
        # Check and change right neighbor
        if col < input_grid.shape[1] - 1 and input_grid[row, col + 1] == 0:
            output_grid[row, col + 1] = 3
        # Check and change above neighbor
        if row > 0 and input_grid[row - 1, col] == 0:
            output_grid[row - 1, col] = 3
        # Check and change below neighbor
        if row < input_grid.shape[0] - 1 and input_grid[row + 1, col] == 0:
            output_grid[row + 1, col] = 3

    return output_grid
```

