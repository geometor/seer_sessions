```python
"""
Expands non-white pixels to the left until a non-white pixel or the grid edge is encountered.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by expanding non-white pixels to the left.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row
    for r in range(rows):
        # Iterate through each pixel in the row, from right to left
        for c in range(cols):
            # Check if the pixel is non-white
            if input_grid[r, c] != 0:
                # Expand to the left
                for c_left in range(c - 1, -1, -1):
                    if output_grid[r, c_left] == 0:  # Check output_grid, not input_grid
                        output_grid[r, c_left] = input_grid[r, c]
                    else:
                        break  # Stop when hitting another non-white pixel (or edge)

    return output_grid
```
