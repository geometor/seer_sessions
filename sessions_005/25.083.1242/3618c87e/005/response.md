```python
"""
Copies the input grid. Changes blue (1) pixels to white (0) in all rows except the last. In the last row, changes blue (1) pixels to gray (5), and if the original input's last row contained any blue pixels, changes gray (5) pixels to blue (1) in the last row.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Check if the last row of the *original* input grid has blue (1)
    last_row_has_blue = np.any(input_grid[-1] == 1)

    for i in range(rows):
        for j in range(cols):
            # Non-last rows: blue (1) becomes white (0)
            if i != rows - 1 and input_grid[i, j] == 1:
                output_grid[i, j] = 0
            # Last row: blue (1) becomes gray (5)
            elif i == rows - 1:
                if input_grid[i, j] == 1:
                    output_grid[i, j] = 5
    
    # Last row: gray (5) becomes blue (1) *only if* input's last row had blue
    if last_row_has_blue:
        for j in range(cols):
            if output_grid[-1, j] == 5:
                output_grid[-1, j] = 1


    return output_grid.tolist()
```