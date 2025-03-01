# 94f9d214 • 006 • refine_coder

---
```python
"""
The output grid is the same size as the input grid. Within the top-left 3x3 region of the input, green pixels are replaced with red pixels in the output, and black pixels remain black. All other input pixels are copied to the output grid without change.
"""

import numpy as np

def transform(input_grid):
    # Create a copy of the input grid to serve as the output grid.
    output_grid = np.copy(input_grid)
    
    # Iterate through the top-left 3x3 subgrid of the input/output.
    for i in range(min(3, output_grid.shape[0])):  # Ensure we don't go out of bounds
        for j in range(min(3, output_grid.shape[1])):  # Ensure we don't go out of bounds
            # Apply the color transformation within the 3x3 region.
            if input_grid[i][j] == 3:
                output_grid[i][j] = 2
            elif input_grid[i][j] == 0:
                output_grid[i][j] = 0

    return output_grid
```
