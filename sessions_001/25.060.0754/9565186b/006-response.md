# 9565186b • 006 • refine_coder

---
```python
"""
Replace blue (1) and azure (8) pixels with gray (5) in a grid, leaving other colors unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    
    # Iterate through each cell of the grid.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Check if the pixel is blue (1) or azure (8).
            if output_grid[i, j] == 1 or output_grid[i, j] == 8:
                # Replace the pixel with gray (5).
                output_grid[i, j] = 5
    
    return output_grid
```

