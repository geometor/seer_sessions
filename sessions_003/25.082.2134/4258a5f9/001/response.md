```python
"""
Transforms an input grid by creating a 3x3 block of '1's (blue) centered around each '5' (gray) pixel,
while keeping the '5' pixel unchanged. The remaining '0's (white) in the input remain '0's in the output.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the locations of '5's.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid with the same dimensions and filled with 0s
    output_grid = np.zeros_like(input_grid)

    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid
    for i in range(rows):
        for j in range(cols):
            # Conditional Transformation: check for '5'
            if input_grid[i, j] == 5:
                # Region Generation: Create 3x3 region of '1's
                for x in range(max(0, i - 1), min(rows, i + 2)):
                    for y in range(max(0, j - 1), min(cols, j + 2)):
                        output_grid[x, y] = 1
                output_grid[i,j] = 5 # set center to 5

    return output_grid
```
