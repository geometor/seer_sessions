# 53b68214 • 016 • example_3 • investigate_coder

---
```python
"""
The transformation rule is to identify the pattern of red pixels in the input grid, extend the grid by two rows,
and continue the pattern of red pixels in the extended rows, filling the rest with white pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Extends the input grid by two rows and continues an alternating red pixel pattern.
    """
    input_height, input_width = input_grid.shape
    output_height = input_height + 2
    output_width = input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Copy existing pattern
    output_grid[:input_height, :] = input_grid

    # Extend the pattern
    for row in range(input_height, output_height):
        for col in range(2):  # First two columns
          if (row % 2 == 0 and col==0) or (row % 2 !=0 and col ==1) :
            output_grid[row, col] = 2

    return output_grid
```
