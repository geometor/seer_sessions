# c1d99e64 • 008 • refine_coder

---
```python
"""
The output grid is the same size as the input grid. All the azure (8) colored pixels in the input grid are replaced with white (0) in the output grid. A red (2) cross is drawn on the output grid. The dimensions of the cross are determined by the dimensions of the input grid. The cross is centered and has a width and height equal to the dimensions of the input, minus 2 in each axis.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Replace all 8's with 0's.
    for r in range(rows):
        for c in range(cols):
            if output_grid[r,c] == 8:
                output_grid[r,c] = 0

    # Calculate the center row and column indices.
    center_row = rows // 2
    center_col = cols // 2

    # Calculate cross dimensions.
    cross_height = rows - 2
    cross_width = cols - 2
    
    # Draw vertical line of the cross.
    for r in range(center_row - cross_height // 2, center_row + cross_height // 2 + 1):
        if 0 <= r < rows:
          output_grid[r,center_col] = 2

    # Draw the horizontal line of the cross
    for c in range(center_col - cross_width // 2, center_col + cross_width //2 + 1):
        if 0 <= c < cols:
          output_grid[center_row,c] = 2

    return output_grid
```
