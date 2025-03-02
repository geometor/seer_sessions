# 28e73c20 • 012 • refine_coder

---
```python
"""
Copies the input grid, creates a green border, and conditionally adds a white cross in the center. The output grid has the same dimensions as the input grid. A cross is added only if both dimensions are greater than 2.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Get the dimensions of the grid
    rows, cols = output_grid.shape

    # Handle 1x1 and 2x2 grids: all green
    if rows <= 2 or cols <= 2:
        output_grid[:] = 3
        return output_grid
    
    # Change all pixels on the outer border to green (3)
    for i in range(rows):
        for j in range(cols):
            if i == 0 or i == rows - 1 or j == 0 or j == cols - 1:
                output_grid[i, j] = 3
            
    # Create a plus pattern of white pixels inside the frame, only if dimensions are > 2
    if rows > 2 and cols > 2:
        # Calculate the center row and column.  Use integer division to handle both even and odd dimensions.
        center_row = rows // 2
        center_col = cols // 2

        # Set the center row and column to white (0), excluding the border.
        for i in range(1, rows - 1):
            output_grid[i, center_col] = 0
        for j in range(1, cols - 1):
            output_grid[center_row, j] = 0
        
    return output_grid
```

