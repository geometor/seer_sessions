```python
"""
Transforms an input grid by performing a flood fill operation with '1's, starting from the top and left edges, and stopping when encountering any non-'1' pixel.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rules.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Flood Fill (Top to Bottom)
    for c in range(cols):
        for r in range(rows):
            if output_grid[r,c] != 1:
                break  # Stop at non-1 pixels
            else:
                output_grid[r, c] = 1

    # Flood Fill (Left to Right)
    for r in range(rows):
        for c in range(cols):
            if output_grid[r,c] != 1:
                break  # Stop at non-1 pixels
            else:
                output_grid[r, c] = 1
            
    return output_grid
```
