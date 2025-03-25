```python
"""
The transformation rule is a 180-degree rotation of the input grid.
"""

import numpy as np

def rotate_180(grid):
    """Rotates a 2D array by 180 degrees."""
    return np.rot90(grid, 2)

def transform(input_grid):
    # Convert input grid to numpy array
    input_np = np.array(input_grid)

    # Rotate the grid by 180 degrees
    output_np = rotate_180(input_np)

    # Convert back to list of lists
    output_grid = output_np.tolist()

    return output_grid
```