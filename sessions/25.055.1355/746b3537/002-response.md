# 746b3537 • 002 • example_1 • investigate_coder

---
```python
"""
The input grid is transformed into a single-column grid by taking the values from each row of the input and placing them in a single cell, preserving the vertical order. The output grid has the same number of rows as the input, but only one column.
"""

import numpy as np

def transform(input_grid):
    # Get the dimensions of the input grid.
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Initialize the output grid as a list of lists (to build it dynamically)
    output_grid = []
    
    # Iterate each row in input
    for i in range(rows):
        # Append each complete row array to the output list.
        output_grid.append([input_grid[i][0]])

    return output_grid
```
