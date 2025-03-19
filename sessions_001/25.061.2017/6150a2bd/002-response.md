# 6150a2bd • 002 • example_2 • investigate_coder

---
```python
"""
The transformation involves a 90-degree clockwise rotation of the input grid.
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
    # Initialize the output grid with the same dimensions as the input grid.
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = np.zeros((rows, cols), dtype=int)

    # Rotate the grid 90 degrees clockwise.
    for i in range(rows):
        for j in range(cols):
            output_grid[j][rows - 1 - i] = input_grid[i][j]

    return output_grid
```
