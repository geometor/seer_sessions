# 9dfd6313 • 002 • example_1 • investigate_coder

---
```python
"""
The transformation preserves the main diagonal elements (0 and 5) of a 3x3 grid. The element at input_grid[1][0] moves to output_grid[0][1]. All other non-diagonal elements become 0.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Preserve diagonal elements. This part isn't strictly necessary
    # since we copy the array and modify, but shown for program clarity.
    for i in range(3):
        output_grid[i, i] = input_grid[i, i]

    # Capture moving element
    moving_element = input_grid[1, 0]

    # zero out other non-diagonal elements
    for i in range(3):
      for j in range(3):
        if i != j:
          output_grid[i,j] = 0

    # Move the specific non-diagonal element.
    output_grid[0, 1] = moving_element

    return output_grid
```
