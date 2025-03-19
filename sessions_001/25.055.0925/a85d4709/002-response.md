# a85d4709 • 002 • example_1 • investigate_coder

---
```python
"""
The transformation rule replaces colors in the input grid based on their position and initial color.
- Corner cells with gray (5) are replaced with green (3).
- Center cells with gray (5) are replaced with yellow (4).
- White(0) cells anywhere become red(2)
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    output_grid = np.zeros_like(input_grid)  # Initialize output grid with zeros
    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid
    for i in range(rows):
        for j in range(cols):
            # Corner Rule: gray(5) becomes green(3)
            if input_grid[i, j] == 5 and ((i == 0 and j == 0) or (i == 0 and j == cols - 1) or (i == rows - 1 and j == 0) or (i == rows - 1 and j == cols - 1)):
                output_grid[i, j] = 3
            # Center Rule: gray(5) becomes yellow(4)
            elif input_grid[i, j] == 5 and i == rows // 2 and j == cols // 2:
                output_grid[i, j] = 4
            # White becomes Red Rule: white(0) becomes red
            elif input_grid[i,j] == 0:
                output_grid[i,j] = 2
            
    return output_grid
```
