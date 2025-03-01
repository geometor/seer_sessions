# 74dd1130 • 002 • example_4 • investigate_coder

---
```python
"""
The transformation rule is a 90-degree counter-clockwise rotation of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees counter-clockwise.

    Args:
        input_grid: A 3x3 list of lists representing the input grid.

    Returns:
        A 3x3 list of lists representing the rotated output grid.
    """
    # initialize output_grid as a 3x3 array of zeros
    output_grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # Rotate the grid 90 degrees counter-clockwise
    for i in range(3):
        for j in range(3):
            output_grid[i][j] = input_grid[j][2 - i]

    return output_grid
```
