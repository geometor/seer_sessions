```python
"""
Transforms a grid of black (0) pixels into a grid with an azure (8) border and a black (0) interior. The output grid is one unit smaller in each dimension than the input grid.
"""

import numpy as np

def transform(input_grid):
    # Determine Output Dimensions
    input_rows, input_cols = input_grid.shape
    output_rows = input_rows - 1 + (input_rows>1) # handle 1 row grids
    output_cols = input_cols - 1 + (input_cols>1) # handle 1 col grids

    # Create Output Grid
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Draw Border and Fill Interior
    for r in range(output_rows):
        for c in range(output_cols):
            if r == 0 or r == output_rows - 1 or c == 0 or c == output_cols - 1:
                output_grid[r, c] = 8  # Azure border
            # no need to test and set 0, since we initialized to zero
            # else:
            #   output_grid[r,c] = 0
    return output_grid
```