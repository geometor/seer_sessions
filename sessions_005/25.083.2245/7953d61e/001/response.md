```python
"""
The transformation creates a 2x2 "tiled" version of the original grid, where each tile is a reflection (horizontal, vertical, or both) of the original.
"""

import numpy as np

def reflect_horizontal(grid):
    return np.fliplr(grid)

def reflect_vertical(grid):
    return np.flipud(grid)

def reflect_both(grid):
    return np.flipud(np.fliplr(grid))

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((2 * rows, 2 * cols), dtype=int)

    # Top-Left Quadrant: Copy the input grid
    output_grid[:rows, :cols] = input_grid

    # Top-Right Quadrant: Horizontal reflection
    output_grid[:rows, cols:] = reflect_horizontal(input_grid)

    # Bottom-Left Quadrant: Vertical reflection
    output_grid[rows:, :cols] = reflect_vertical(input_grid)

    # Bottom-Right Quadrant: Both reflections
    output_grid[rows:, cols:] = reflect_both(input_grid)

    return output_grid.tolist()
```