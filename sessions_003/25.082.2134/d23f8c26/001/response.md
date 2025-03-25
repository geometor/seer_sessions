```python
"""
Extracts the third column (index 2) from the input grid and creates an output grid where all other values are set to 0.
"""

import numpy as np

def transform(input_grid):
    # Create an output grid of the same dimensions as the input, filled with 0.
    output_grid = np.zeros_like(input_grid)

    # Copy the values from the third column (index 2) of the input grid to the output grid.
    output_grid[:, 2] = input_grid[:, 2]

    return output_grid
```