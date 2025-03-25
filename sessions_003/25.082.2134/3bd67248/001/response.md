```python
"""
1.  **Preserve the Leftmost Line:** Copy the leftmost vertical line of the input grid (of color *C*) to the same position (column 0) in the output grid.
2.  **Create Diagonal Line:** Create a diagonal line of red (2) pixels. Start at the top-right corner of the grid. Extend the line diagonally down and to the left, one pixel at a time. The total number of red pixels is equal to height of input grid - 1.
3.  **Create Horizontal Line:** Create a horizontal line of yellow (4) pixels in the last row of the grid. Start this line at the second column (index 1) from the left edge. The length of the horizontal line will be the (number of rows of the grid) - 1.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    height = output_grid.shape[0]
    width = output_grid.shape[1]

    # Create the diagonal line (red - 2).
    for i in range(height - 1):
        output_grid[i, width - 1 - i] = 2

    # Create the horizontal line (yellow - 4).
    for j in range(height - 1):
        output_grid[height - 1, j + 1] = 4
        
    return output_grid
```
