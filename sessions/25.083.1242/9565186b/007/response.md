```python
"""
Iterates through each cell of the input grid. If a cell's color is one of the
trigger colors (1-blue, 2-red, 3-green, or 8-azure), it changes the cell's value
to 5 (gray) in the output grid. Otherwise, the cell's value is copied directly
from the input grid to the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    trigger_colors = [1, 2, 3, 8]

    # Iterate through each cell
    for i in range(rows):
        for j in range(cols):
            # Check if the cell's color is a trigger color
            if input_grid[i, j] in trigger_colors:
                # Change the cell's value to 5 (gray)
                output_grid[i, j] = 5
            # else:  the copy has already happened

    return output_grid
```