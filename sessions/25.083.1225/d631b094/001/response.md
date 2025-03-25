```python
"""
The function extracts all non-zero pixels from the input grid and creates a new grid. The new grid contains the non-zero colors repeated the number of times they appear in the input grid.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to numpy array
    input_grid = np.array(input_grid)

    # Find non-zero pixels
    non_zero_pixels = input_grid[input_grid != 0]

    # Initialize output grid
    output_grid = non_zero_pixels.flatten()
    
    return output_grid.tolist()
```