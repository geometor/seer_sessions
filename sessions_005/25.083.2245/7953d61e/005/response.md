```python
"""
The transformation rule involves creating a 2x2 tiled grid from the input grid.

1.  **Tiling:** Divide the output grid into a 2x2 grid of tiles, where each tile has the same dimensions as the input grid.
2.  **Top-Left Quadrant:** The top-left tile of the output grid is a direct copy of the input grid.
3.  **Top-Right Quadrant:**  The top-right quadrant is a 90-degree clockwise rotation of the input grid.
4.  **Bottom-Left Quadrant:** The bottom-left quadrant is a 90-degree counter-clockwise rotation of the input grid.
5.  **Bottom-Right Quadrant:** The bottom-right quadrant is a 180-degree rotation of the input grid.
6. **Output Size**: The output is double the size of the input in width and height.
"""

import numpy as np

def rotate_90_clockwise(grid):
    return np.rot90(grid, k=-1).tolist()

def rotate_90_counter_clockwise(grid):
    return np.rot90(grid, k=1).tolist()

def rotate_180(grid):
    return np.rot90(grid, k=2).tolist()

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((2 * rows, 2 * cols), dtype=int)

    # Top-Left Quadrant: Copy the input grid
    output_grid[:rows, :cols] = input_grid

    # Top-Right Quadrant: 90-degree clockwise rotation
    output_grid[:rows, cols:] = rotate_90_clockwise(input_grid)

    # Bottom-Left Quadrant: 90-degree counter-clockwise rotation
    output_grid[rows:, :cols] = rotate_90_counter_clockwise(input_grid)

    # Bottom-Right Quadrant: 180-degree rotation
    output_grid[rows:, cols:] = rotate_180(input_grid)

    return output_grid.tolist()
```