# 25d8a9c8 • 020 • example_4 • investigate_coder

---
```python
"""
The transformation rule is: The bottom row colors change to gray, all other cells change to white.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rule:
    The bottom row colors change to gray, all other cells change to white.
    """
    # Initialize output_grid as a copy of the input grid to preserve dimensions.
    output_grid = np.copy(input_grid)
    
    # Get the height of the grid.
    height = output_grid.shape[0]

    # Iterate through all rows except the last one and set them to white (0).
    for i in range(height - 1):
        output_grid[i, :] = 0
        
    # Set the bottom row to gray (5).
    output_grid[height-1, :] = 5

    return output_grid
```

