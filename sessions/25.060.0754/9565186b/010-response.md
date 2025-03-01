# 9565186b • 010 • example_2 • investigate_coder

---
```python
"""
1. Preserve the Top Row: Copy the top row of the input grid directly to the output grid.
2. Transform other colors to Gray: For the remaining rows (middle and bottom), change any pixel that is not blue (1) to gray (5).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Iterate through the rows starting from the second row (index 1)
    for i in range(1, output_grid.shape[0]):
        # Iterate through the columns
        for j in range(output_grid.shape[1]):
            # Check if the pixel is not blue (1)
            if output_grid[i, j] != 1:
                # Change the pixel to gray (5)
                output_grid[i, j] = 5

    return output_grid
```

