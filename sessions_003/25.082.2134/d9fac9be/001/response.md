```python
"""
Examine the input grid.
Identify the values of the pixels at four corners.
If any corners have a value other than 0, prioritize these for next step.
Select and output any non-zero corner value from the input grid.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to numpy array for easier manipulation
    grid = np.array(input_grid)
    rows, cols = grid.shape

    # Identify corner values
    top_left = grid[0, 0]
    top_right = grid[0, cols - 1]
    bottom_left = grid[rows - 1, 0]
    bottom_right = grid[rows - 1, cols - 1]

    corners = [top_left, top_right, bottom_left, bottom_right]

    # Prioritize and select non-zero corner values
    for corner_value in corners:
        if corner_value != 0:
            return corner_value
    
    return 0 # should not happen in provided cases, all had a non-zero corner
```