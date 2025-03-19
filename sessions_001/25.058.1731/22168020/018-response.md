# 22168020 • 018 • refine_coder

---
```python
"""
Identifies rows containing magenta (color 6) and azure (color 8) in the input grid. 
Fills the entire row with magenta if it contains magenta.
Fills the entire row with azure if it contains azure.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with the same dimensions as the input
    output_grid = np.zeros_like(input_grid)

    # Iterate through each row of the input grid
    for i in range(input_grid.shape[0]):
        row = input_grid[i, :]
        # Check if the row contains magenta (color 6)
        if 6 in row:
            # Fill the entire row in the output grid with magenta
            output_grid[i, :] = 6
        # Check if the row contains azure (color 8)
        elif 8 in row:
            # Fill the entire row in the output grid with azure
            output_grid[i, :] = 8

    return output_grid
```
