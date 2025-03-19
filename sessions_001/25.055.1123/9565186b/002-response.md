# 9565186b • 002 • example_1 • investigate_coder

---
```python
"""
Replace all blue (1) and azure (8) pixels with gray (5) pixels, while preserving the red (2) pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing blue and azure pixels with gray,
    keeping red pixels unchanged.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid.
    """
    # Initialize output_grid as a copy of input_grid to avoid modifying the original.
    output_grid = [row[:] for row in input_grid]
    
    # Get the dimensions of the grid.
    rows = len(output_grid)
    cols = len(output_grid[0]) if rows > 0 else 0

    # Iterate through each cell of the grid.
    for i in range(rows):
        for j in range(cols):
            # Check if the pixel is blue (1) or azure (8).
            if output_grid[i][j] == 1 or output_grid[i][j] == 8:
                # Replace the pixel with gray (5).
                output_grid[i][j] = 5

    return output_grid
```

