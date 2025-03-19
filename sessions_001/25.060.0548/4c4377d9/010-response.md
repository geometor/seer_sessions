# 4c4377d9 • 010 • example_2 • investigate_coder

---
```python
"""
The output grid is created from the input grid such that rows are mirrored and, for every two rows the elements are swapped.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with double the height of the input grid
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows * 2, cols), dtype=int)

    # Iterate through the rows of the input grid
    for i in range(rows):
        # Copy each row of the input grid to its mirrored position in the output grid
        output_grid[rows * 2 - 1 - i] = input_grid[i]

    # complete first mirrored set
    for i in range(rows):
      output_grid[i] = input_grid[rows - 1 - i]

    # swap adjacent
    for i in range(rows):
      for j in range(cols):
        if (i % 2 == 0):
          output_grid[i][j] = input_grid[rows - i -1][j]

    return output_grid
```
