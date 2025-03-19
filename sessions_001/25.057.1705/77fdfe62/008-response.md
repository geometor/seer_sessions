# 77fdfe62 • 008 • example_2 • investigate_coder

---
```python
"""
Extracts the values from the four corners of the input grid and creates a new 2x2 grid using those values, maintaining their relative positions.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extracting the corner pixel values and
    creating a 2x2 output grid with those values.
    """
    # Get the dimensions of the input grid
    rows, cols = input_grid.shape

    # Initialize the output grid as a 2x2 numpy array
    output_grid = np.zeros((2, 2), dtype=int)

    # Extract the corner values from the input grid and populate the output grid
    output_grid[0, 0] = input_grid[0, 0]  # Top-left
    output_grid[0, 1] = input_grid[0, cols - 1]  # Top-right
    output_grid[1, 0] = input_grid[rows - 1, 0]  # Bottom-left
    output_grid[1, 1] = input_grid[rows - 1, cols - 1]  # Bottom-right

    return output_grid
```
