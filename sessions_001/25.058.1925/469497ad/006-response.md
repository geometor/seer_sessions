# 469497ad • 006 • refine_coder

---
```python
"""
The transformation rule involves expanding the input grid to double its dimensions, positioning an azure square in the center, creating a green border around the azure square, and placing red pixels at the corners of the expanded grid. The green border in the output is always a single pixel wide and encloses the central azure square.
"""

import numpy as np

def get_objects_by_color(grid, color):
    """Finds objects of a specific color in the grid."""
    return np.array(np.where(grid == color)).T

def transform(input_grid):
    # Initialize output_grid (double the dimensions)
    output_grid = np.zeros((input_grid.shape[0] * 2, input_grid.shape[1] * 2), dtype=int)

    # Find the center of the output grid
    center_row = output_grid.shape[0] // 2
    center_col = output_grid.shape[1] // 2

    # Determine size of the azure square (it's always 2x2 in the output).
    azure_size = 2

    # Place Azure Square
    for r in range(azure_size):
        for c in range(azure_size):
            output_grid[center_row - azure_size//2 + r, center_col - azure_size//2 + c] = 8

    # create green border - find the min/max row/col of the azure square.
    azure_objects = get_objects_by_color(output_grid, 8)
    min_row = np.min(azure_objects[:, 0])
    max_row = np.max(azure_objects[:, 0])
    min_col = np.min(azure_objects[:, 1])
    max_col = np.max(azure_objects[:, 1])
    
    for r in range(min_row-1, max_row + 2):
        for c in range(min_col-1, max_col+2):
            if (r == min_row-1 or r == max_row+1 or c == min_col-1 or c==max_col+1):
                output_grid[r,c] = 3
                

    # Place red pixels at the corners
    output_grid[0, 0] = 2
    output_grid[0, output_grid.shape[1] - 1] = 2
    output_grid[output_grid.shape[0] - 1, 0] = 2
    output_grid[output_grid.shape[0] - 1, output_grid.shape[1] - 1] = 2

    return output_grid
```
