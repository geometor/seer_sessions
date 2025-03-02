# d22278a0 • 016 • example_3 • investigate_coder

---
```python
"""
The transformation creates expanding checkerboard patterns from the initial colored pixels, filling the grid based on alternating color propagation rules.
"""

import numpy as np

def get_seed_pixels(grid):
    # Find coordinates of non-white pixels.
    coords = np.argwhere(grid != 0)
    seed_pixels = []
    for r, c in coords:
        seed_pixels.append( (r,c, grid[r,c]) )
    return seed_pixels

def transform(input_grid):
    """
    Transforms the input grid according to the checkerboard propagation rule.
    """
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Get seed pixels (non-white pixels).
    seed_pixels = get_seed_pixels(input_grid)

    # Propagate color for each seed pixel.
    for r, c, color in seed_pixels:
        # Propagate horizontally.
        for j in range(c, cols):
            if (j - c) % 2 == 0:
                output_grid[r, j] = color

        # Propagate vertically based on starting direction
        if color == 2:  # Red propagates down
            for i in range(r, rows):
                if (i - r) % 2 == 0:
                    for j in range(c,cols):
                        if (j - c) % 2 == 0:
                            output_grid[i,j] = color
        elif color == 4: # Yellow propagates up
             for i in range(r, -1, -1):
                if (r - i) % 2 == 0:
                    for j in range(c,cols):
                        if (j - c) % 2 == 0:
                            output_grid[i,j] = color

    return output_grid
```
