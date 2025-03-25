```python
"""
Copies the third column (index 2) of the input grid to the output grid and sets all other cells in the output grid to zero.
"""

import numpy as np

def transform(input_grid):
    # Initialize an output grid with the same dimensions as the input grid, filled with zeros.
    output_grid = np.zeros_like(input_grid)

    # Copy the values from the third column (index 2) of the input grid to the output grid.
    output_grid[:, 2] = input_grid[:, 2]

    return output_grid
```