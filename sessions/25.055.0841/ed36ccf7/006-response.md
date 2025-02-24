# ed36ccf7 • 006 • example_2 • investigate_coder

---
```python
"""
The transformation rule involves rotating the input grid to the right by one position. 
Pixels that are white (0) in the input remain unchanged. 
Pixels that are magenta (6) in the first row of the input grid are changed to white (0) in the output grid.
Magenta(6) on corners remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Rotate the grid to the right by transposing and flipping.
    output_grid = np.rot90(input_grid, k=-1)

    # Apply the rule. The original first row becomes the last column in rotated grid.
    for i in range(rows):
      if input_grid[0][i] == 6:
        output_grid[i][-1] = 0


    return output_grid
```
