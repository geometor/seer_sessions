```python
"""
The transformation rule is a 90-degree clockwise rotation of the input grid.

1. Create Output Grid: Create an output grid with swapped dimensions (width becomes height, height becomes width) of the input grid.
2. Map Pixels: For each pixel at position (x, y) in the input grid, place it at position (y, height - 1 - x) in the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((cols, rows), dtype=int)

    # change output pixels 
    for x in range(rows):
        for y in range(cols):
            output_grid[y, rows - 1 - x] = input_grid[x, y]

    return output_grid.tolist()
```
