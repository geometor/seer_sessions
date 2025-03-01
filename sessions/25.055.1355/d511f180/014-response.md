# d511f180 • 014 • example_3 • investigate_coder

---
```python
"""
The transformation swaps the colors of specific pairs of pixels in a 3x3 grid:
1. The top-middle pixel swaps with the left-middle pixel.
2. The bottom-middle pixel swaps with the bottom-left pixel.
3. All other pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Swap top-middle and left-middle pixels.
    output_grid[0, 1], output_grid[1, 0] = output_grid[1, 0], output_grid[0, 1]

    # Swap bottom-middle and bottom-left pixels.
    output_grid[2, 1], output_grid[2, 0] = output_grid[2, 0], output_grid[2, 1]

    return output_grid
```
