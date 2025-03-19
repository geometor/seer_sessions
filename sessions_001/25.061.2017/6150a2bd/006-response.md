# 6150a2bd • 006 • refine_coder

---
```python
"""
The input grid is rotated 90 degrees clockwise.  This means:

1.  The number of rows in the output grid equals the number of columns in the input grid.
2.  The number of columns in the output grid equals the number of rows in the input grid.
3.  Each pixel at position (row, column) in the input grid moves to position (column, number_of_rows - 1 - row) in the output grid. The colors of the pixels are preserved during the rotation.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees clockwise.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the rotated output grid.
    """
    rows = len(input_grid)
    cols = len(input_grid[0])
    # Initialize the output grid with swapped dimensions.
    output_grid = np.zeros((cols, rows), dtype=int)

    # Rotate the grid 90 degrees clockwise.
    for i in range(rows):
        for j in range(cols):
            output_grid[j][rows - 1 - i] = input_grid[i][j]

    return output_grid
```

