# ed36ccf7 • 002 • example_1 • investigate_coder

---
```python
"""
Identify a 2x2 square in the top-left corner of the input grid. Rotate the colors within this square 90 degrees clockwise.
"""

import numpy as np

def rotate_90(grid):
    """Rotates a 2x2 grid 90 degrees clockwise."""
    return np.rot90(grid, k=-1)

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Extract the 2x2 subgrid
    subgrid = output_grid[:2, :2]

    # Rotate the subgrid
    rotated_subgrid = rotate_90(subgrid)

    # Place the rotated subgrid back into the output_grid
    output_grid[:2, :2] = rotated_subgrid

    return output_grid
```
