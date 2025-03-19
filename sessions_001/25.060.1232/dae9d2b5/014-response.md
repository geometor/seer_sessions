# dae9d2b5 • 014 • refine_coder

---
```python
"""
Transforms a grid by compressing columns by half and applying a color substitution rule. 
If an entire row is white, the corresponding output row remains white. 
Otherwise, pairs of columns are examined: if either pixel in a pair is non-white, 
the corresponding output pixel is magenta; otherwise, it's white.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with dimensions half the width of the input
    input_rows, input_cols = input_grid.shape
    output_grid = np.zeros((input_rows, input_cols // 2), dtype=int)

    # Iterate through the input grid row by row
    for i in range(input_rows):
        # Check if the entire row is white
        if np.all(input_grid[i] == 0):
            # If the entire row is white, keep it white in output
            output_grid[i, :] = 0
        else:
            # compress the grid by two columns at a time
            for j in range(input_cols // 2):
                # If either pixel is non-white, output is magenta
                if input_grid[i, 2*j] != 0 or input_grid[i, 2*j + 1] != 0:
                    output_grid[i,j] = 6 # set to magenta
                else:
                    output_grid[i,j] = 0 # Otherwise, output is white.

    return output_grid
```

