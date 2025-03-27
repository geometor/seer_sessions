```python
"""
The transformation takes a 7x7 input grid and produces a 6x6 output grid.
The first row and first column of the input grid are removed to form the output grid.
"""

import numpy as np

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Remove the first row and first column
    output_grid = input_grid[1:, 1:]

    return output_grid.tolist()
```