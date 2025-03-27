```python
"""
Copies the input grid to the output grid. Blue (1) pixels are changed to white (0) in all rows except the last one.
In the last row, blue pixels are changed to gray (5), and, only if there were any blue pixels in the input's last row, gray pixels are changed to blue (1).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Check if there were any blue pixels in the last row of the input
    last_row_has_blue = np.any(input_grid[-1] == 1)

    # Iterate through each cell of the input grid
    for i in range(rows):
        for j in range(cols):
            # If not the last row and the cell is blue (1), change it to white (0)
            if i != rows - 1 and input_grid[i, j] == 1:
                output_grid[i, j] = 0
            # For the last row, apply specific transformations
            elif i == rows - 1:
                if input_grid[i, j] == 1:
                    output_grid[i, j] = 5  # Change blue to gray
                elif last_row_has_blue and input_grid[i,j] == 5:
                    output_grid[i,j] = 1

    return output_grid.tolist()
```