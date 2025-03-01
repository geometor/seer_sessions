# 0d3d703e • 008 • example_2 • investigate_coder

---
```python
"""
Transforms each pixel in the input grid by adding 4 to its value.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by adding 4 to the value of each pixel.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Iterate over each cell in the grid
    for row_index in range(output_grid.shape[0]):
        for col_index in range(output_grid.shape[1]):
            # change output pixels by adding 4
            output_grid[row_index, col_index] = output_grid[row_index, col_index] + 4

    return output_grid
```
