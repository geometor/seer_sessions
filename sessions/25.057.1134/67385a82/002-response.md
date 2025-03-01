# 67385a82 • 002 • example_1 • investigate_coder

---
```python
"""
Iterates through each cell of the input grid.
If the cell's value is 3 (green), it changes it to 8 (azure).
Otherwise, it keeps the cell's original value.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)  # Initialize output grid
    rows, cols = output_grid.shape

    # Iterate through each cell
    for i in range(rows):
        for j in range(cols):
            # Check if the cell should change from color 3 to 8
            if output_grid[i, j] == 3 and not (i == 0 or i == rows - 1 or j == 0 or j == cols - 1):
                output_grid[i, j] = 8

    return output_grid
```
