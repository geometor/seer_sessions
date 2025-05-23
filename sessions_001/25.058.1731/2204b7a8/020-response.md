# 2204b7a8 • 020 • refine_coder

---
```python
"""
Identify all green (3) pixels within the input grid. 
If green is in the top half of the grid, replace it with azure (8).
If green is in the bottom half, replace it with maroon (9).
All other pixels remain unchanged. The middle row in grids with an odd
number of rows should be included in the bottom half.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)  # Initialize output grid as a copy of the input
    rows, cols = output_grid.shape
    
    # Iterate through each cell of the grid
    for i in range(rows):
        for j in range(cols):
            # Check if the pixel is green (3)
            if output_grid[i, j] == 3:
                # Replace with azure (8) if in the top half
                if i < (rows + 1) // 2:
                    output_grid[i, j] = 8
                # Replace with maroon (9) if in the bottom half
                else:
                    output_grid[i, j] = 9

    return output_grid
```

