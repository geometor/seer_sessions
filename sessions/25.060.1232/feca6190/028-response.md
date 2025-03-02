# feca6190 • 028 • example_5 • investigate_coder

---
```python
"""
Transforms a single-row grid into a square grid where the non-zero element of the input
is replicated diagonally from the top-right to the bottom-left. The size of the output
grid corresponds to the position of the non-zero element in the input row, counting
from right to left.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid into a square output grid.

    Args:
        input_grid: A 2D numpy array representing the input grid (single row).

    Returns:
        A 2D numpy array representing the output grid.
    """
    # Find the non-zero element and its index.
    non_zero_indices = np.nonzero(input_grid)[1]
    if len(non_zero_indices) == 0:
        return input_grid.copy() #if there aren't any, we won't do anything
    
    non_zero_index = non_zero_indices[0]
    non_zero_value = input_grid[0, non_zero_index]
    
    # Determine the size of the output grid (counting position from right to left).
    grid_size = len(input_grid[0]) - non_zero_index
    
    # Create an output grid filled with zeros.
    output_grid = np.zeros((grid_size, grid_size), dtype=int)
    
    # Fill the diagonal with the non-zero element.
    for i in range(grid_size):
        output_grid[i, grid_size - 1 - i] = non_zero_value

    return output_grid
```
