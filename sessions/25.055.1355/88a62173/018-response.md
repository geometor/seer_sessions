# 88a62173 • 018 • refine_coder

---
```python
"""
The transformation identifies the largest contiguous block of azure (color 8)
pixels that forms a 2x2 square in the input grid and copies this 2x2 square to
the output grid.
"""

import numpy as np

def find_azure_square(grid):
    """
    Finds the top-left coordinates of the first 2x2 azure square.
    """
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if (grid[r, c] == 8 and grid[r + 1, c] == 8 and
                grid[r, c + 1] == 8 and grid[r + 1, c + 1] == 8):
                return r, c  # Return top-left coordinates
    return None  # No azure square found


def transform(input_grid):
    """
    Transforms the input grid by copying the 2x2 azure square.
    """
    # Convert input grid to a NumPy array.
    input_np = np.array(input_grid)

    # Find the top-left coordinates of the azure square.
    coords = find_azure_square(input_np)

    # Create the output grid.
    if coords:
        r, c = coords
        output_grid = input_np[r:r+2, c:c+2].tolist()
    else:
        output_grid = [[0]] # Default 1x1 white, needs further context in future
    return output_grid
```
