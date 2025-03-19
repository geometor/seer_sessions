# 05269061 • 006 • refine_coder

---
```python
"""
The transformation operates on each column of the input grid independently. For each column, the entire sequence of colors is replicated in the corresponding output column. The replicated sequence is shifted downward by one position, with the bottom color wrapping to the top. After replication and shifting, if a cell in the output has the same color as the cell directly above it, it's changed to black (0).
"""

import numpy as np

def shift_down_wrap(column):
    """Shifts the elements of a column down by one, wrapping the last element to the top."""
    return np.roll(column, 1)

def transform(input_grid):
    """Transforms the input grid column by column, shifting colors down and wrapping."""
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Iterate through each column
    for j in range(cols):
        # Extract the current column
        input_column = input_grid[:, j]

        # Shift the column down and wrap
        output_column = shift_down_wrap(input_column)

        # Place the shifted column into the output grid
        output_grid[:, j] = output_column

    # Apply the black color filter vertically
    for i in range(1, rows):
        for j in range(cols):
            if output_grid[i, j] == output_grid[i - 1, j]:
                output_grid[i, j] = 0

    return output_grid
```
