# 2204b7a8 • 004 • example_1 • investigate_coder

---
```python
"""
The program takes a 10x10 grid as input. It iterates through each pixel of the grid. If a pixel's color is green (3), it changes the pixel's color to blue (1). All other pixels remain unchanged. The program outputs the modified grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Iterate through each pixel of the grid.
    for row_index, row in enumerate(input_grid):
        for col_index, pixel_value in enumerate(row):
            # If the pixel's color is green (3), change it to blue (1).
            if pixel_value == 3:
                output_grid[row_index, col_index] = 1

    return output_grid
```

