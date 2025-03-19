# db3e9e38 • 008 • example_2 • investigate_coder

---
```python
"""
Transforms an input grid with a vertical orange line into an output grid with an expanded pattern of orange and azure pixels. 
The transformation creates a checkered pattern of orange and azure, originating from the orange line in the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed pattern.
    """
    output_grid = np.copy(input_grid)  # Initialize output grid as a copy of the input
    rows, cols = input_grid.shape

    # Iterate through the grid
    for r in range(rows):
        for c in range(cols):
            # Check for orange pixels
            if input_grid[r, c] == 7:
                output_grid[r,c] = 7
                # Check if right neighbor is within bounds and white
                if c + 1 < cols and input_grid[r, c + 1] == 0:
                        output_grid[r, c + 1] = 8  # change to azure

    return output_grid
```
