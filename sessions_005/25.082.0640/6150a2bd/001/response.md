```python
"""
The input grid is rotated 90 degrees clockwise, then the values are swapped along the vertical axis.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    # Rotate the grid 90 degrees clockwise.
    rotated_grid = np.rot90(input_grid, k=-1)

    # Create a copy to modify
    output_grid = rotated_grid.copy()
    rows, cols = output_grid.shape
    
    # Swap values based on vertical axis
    for r in range(rows):
       for c in range(cols):
            output_grid[r,c] = rotated_grid[r, cols -1 -c]
    
    return output_grid
```