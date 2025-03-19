# 746b3537 • 004 • example_1 • investigate_coder

---
```python
"""
The transformation rule is to extract the first column (index 0) of the input 3x3 grid to create the output 3x1 grid.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the first column of the input grid.
    """
    # Get the dimensions of the input grid.
    rows = len(input_grid)

    # Initialize the output grid as a list.  It will be a column.
    output_grid = []

    # Iterate through the rows of the input grid.
    for i in range(rows):
        # Add the element at the first column (index 0) to the output grid.
        output_grid.append(input_grid[i][0])

    return output_grid
```
