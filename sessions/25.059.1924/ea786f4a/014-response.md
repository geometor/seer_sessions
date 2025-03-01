# ea786f4a • 014 • refine_coder

---
```python
"""
The transformation rule is to replace each white pixel in the input grid with a 3x3 cross-shaped arrangement of white pixels, keeping all other pixels red. The cross is centered on the original white pixel's location and is truncated if it extends beyond the grid boundaries.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by creating a 3x3 cross of white pixels centered at each white pixel's location.
    The cross is truncated at the grid boundaries.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    
    # Find the dimensions of the grid.
    rows, cols = input_grid.shape
    
    # Find the coordinates of all white pixels.
    white_rows, white_cols = np.where(input_grid == 0)
    white_pixels = list(zip(white_rows, white_cols))

    # Iterate through each white pixel and create a 3x3 cross.
    for center_row, center_col in white_pixels:
        # Create the 3x3 cross by setting the appropriate pixels to white (0).
        # Handle boundary conditions.
        for i in range(max(0, center_row - 1), min(rows, center_row + 2)):
            output_grid[i, center_col] = 0
        for j in range(max(0, center_col - 1), min(cols, center_col + 2)):
            output_grid[center_row, j] = 0

    return output_grid
```

