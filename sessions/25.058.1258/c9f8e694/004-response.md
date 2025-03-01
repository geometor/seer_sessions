# c9f8e694 • 004 • example_1 • investigate_coder

---
```python
"""
Iterates through each pixel in the grid. Identifies gray (5) pixels and checks
the pixel immediately to the left. If the left-neighbor is blue (1) or red (2),
it replaces the color of the current gray (5) pixel with the color of its left
neighbor. If the left neighbor is white (0), gray(5) or does not exist, the gray pixel remains unchanged.
"""

import numpy as np

def get_left_neighbor_color(grid, row, col):
    """Gets the color of the left neighbor of a pixel.
    Returns 0 if no left neightbor exists
    """
    if col > 0:
        return grid[row, col - 1]
    else:
        return 0 #treat out of bounds as white

def transform(input_grid):
    """Transforms the input grid according to the rule."""

    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each pixel in the grid.
    for row in range(rows):
        for col in range(cols):
            # Identify gray (5) pixels.
            if output_grid[row, col] == 5:
                # Check the left neighbor.
                left_neighbor_color = get_left_neighbor_color(output_grid, row, col)

                # Replace color if the left neighbor is blue or red.
                if left_neighbor_color in (1, 2):
                    output_grid[row, col] = left_neighbor_color

    return output_grid
```
