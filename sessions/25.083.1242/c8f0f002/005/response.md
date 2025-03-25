```python
"""
1. Identify Orange Regions: Find all contiguous regions of orange (7) pixels.
2. Identify the Perimeter: The perimeter consists of all pixels which have the color orange (7).
3. Transform Perimeter Pixels: Change all orange pixels on the perimeter to gray (5).
4. Retain Other Pixels: All other pixels retain their original color.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell of the grid
    for row in range(rows):
        for col in range(cols):
            # Check if cell is orange
            if output_grid[row, col] == 7:
                # Change to gray
                output_grid[row, col] = 5

    return output_grid
```
