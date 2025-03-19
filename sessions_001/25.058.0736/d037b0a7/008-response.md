# d037b0a7 • 008 • example_2 • investigate_coder

---
```python
"""
1.  **Identify Non-Zero Pixels:** Locate all pixels in the input grid that have a value other than 0.

2.  **Copy to Center and replicate:**
    - the red 2 in position [0,1] (row, col) is copied to [1,1]
    - the second row is copied to the third row
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Copy the value from input_grid[0, 1] to output_grid[1, 1]
    output_grid[1, 1] = input_grid[0, 1]

    # Copy the second row of input_grid to the third row of output_grid
    output_grid[2, :] = input_grid[1, :]

    return output_grid
```
