# c1d99e64 • 004 • example_1 • investigate_coder

---
```python
"""
Copy the input grid to the output grid, preserving all 0 values.
Calculate the center row and center column of the output grid.
Change the value of every cell in the center row to 2.
Change the value of every cell in the center column to 2.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by preserving 0s and drawing a red cross at the center.
    """
    # Create a copy of the input grid to serve as the output grid.
    output_grid = np.copy(input_grid)
    
    # Get the dimensions of the grid.
    rows, cols = output_grid.shape
    
    # Calculate the center row and column indices.
    center_row = rows // 2
    center_col = cols // 2
    
    # Set all pixels in the center row to 2 (red).
    output_grid[center_row, :] = 2
    
    # Set all pixels in the center column to 2 (red).
    output_grid[:, center_col] = 2

    # Copy 0's
    for row in range(rows):
        for col in range(cols):
            if input_grid[row,col] == 0:
                output_grid[row,col] = 0

    return output_grid
```

