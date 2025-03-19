# feca6190 • 030 • refine_coder

---
```python
"""
The input is a single-row grid containing a single non-zero pixel. The output is a square grid.
The size of the output grid is determined by the position of the non-zero pixel in the input row,
counting from right to left (size = length of input row - index of non-zero pixel).
The output grid contains a diagonal line of the non-zero pixel's color, running from the top-right
to the bottom-left. The number of colored pixels in the output is equal to the output grid's dimension.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid (single-row) into a square output grid with a diagonal.

    Args:
        input_grid: A 2D numpy array representing the input grid (single row).

    Returns:
        A 2D numpy array representing the square output grid.
    """
    # Find the non-zero pixel and its index.
    non_zero_indices = np.nonzero(input_grid)[1]
    if len(non_zero_indices) == 0:
        return input_grid.copy()  # Return input if no non-zero pixel
    non_zero_index = non_zero_indices[0]
    non_zero_value = input_grid[0, non_zero_index]

    # Determine the size of the output grid.
    grid_size = input_grid.shape[1] - non_zero_index

    # Create an output grid filled with zeros.
    output_grid = np.zeros((grid_size, grid_size), dtype=int)

    # Fill the diagonal with the non-zero element.
    for i in range(grid_size):
        output_grid[i, grid_size - 1 - i] = non_zero_value

    return output_grid
```
