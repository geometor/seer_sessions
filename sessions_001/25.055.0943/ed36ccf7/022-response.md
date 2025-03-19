# ed36ccf7 • 022 • refine_coder

---
```python
"""
The transformation rule is a 90-degree clockwise rotation of the entire input grid. All of the white pixels (0) in the output are at the same coordinate locations as the input.
"""

import numpy as np

def rotate_grid_90_clockwise(grid):
    return np.rot90(grid, k=-1)

def transform(input_grid):
    """
    Rotates the input grid 90 degrees clockwise and preserves white pixels.
    """
    # Convert input_grid to a NumPy array
    input_np = np.array(input_grid)

    # Rotate the entire grid 90 degrees clockwise
    rotated_grid = rotate_grid_90_clockwise(input_np)

    # Create the output grid by copying the rotated grid
    output_grid = rotated_grid.copy()

    # Preserve white pixels (0) from the original input grid
    for i in range(input_np.shape[0]):
        for j in range(input_np.shape[1]):
            if input_np[i, j] == 0:
                output_grid[i, j] = 0

    return output_grid.tolist()
```
