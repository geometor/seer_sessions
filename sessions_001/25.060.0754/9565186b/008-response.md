# 9565186b • 008 • refine_coder

---
```python
"""
Inspect each pixel in the input grid. If a pixel's color is blue (1) or azure (8), change it to gray (5). Leave all other pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Iterate through each cell of the grid using nested loops.
    for row_index in range(output_grid.shape[0]):
        for col_index in range(output_grid.shape[1]):
            # Check if the current pixel's color is blue (1) or azure (8).
            if output_grid[row_index, col_index] == 1 or output_grid[row_index, col_index] == 8:
                # Change the pixel's color to gray (5).
                output_grid[row_index, col_index] = 5

    # Return the modified grid.
    return output_grid
```

