# 74dd1130 • 017 • refine_coder

---
```python
"""
1.  **Identify the Bottom Edge:** Focus only on the last row (row index 7) of the input grid.
2.  **Conditional Swapping on the Bottom Edge:** Starting from the second element and going up to the last element of the last row: swap the azure(8) and grey(5) colors
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through the last row
    for col in range(cols):
        #Swap grey and azure
        if output_grid[rows-1, col] == 5:
            output_grid[rows-1, col] = 8
        elif output_grid[rows-1, col] == 8:
            output_grid[rows-1, col] = 5
    return output_grid
```
