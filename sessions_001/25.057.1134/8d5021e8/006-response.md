# 8d5021e8 • 006 • refine_coder

---
```python
"""
The transformation identifies azure pixels in the input grid and generates a new grid based on their positions. If there's one azure pixel, the output has four azure pixels at the corners. If there are two, their arrangement (diagonal or aligned) influences the output size and azure pixel placement, with either two or four azure pixels in the output.
"""

import numpy as np

def find_azure_pixels(grid):
    """Finds coordinates of azure pixels."""
    return np.where(grid == 8)

def are_diagonal(azure_coords):
    """Checks if two azure pixels are diagonally positioned."""
    if len(azure_coords[0]) < 2:
        return False
    return azure_coords[0][0] != azure_coords[0][1] and azure_coords[1][0] != azure_coords[1][1]

def transform(input_grid):
    # Find azure pixels in the input grid.
    azure_coords = find_azure_pixels(input_grid)
    num_azure = len(azure_coords[0])

    # Determine output grid dimensions and place azure pixels.
    if num_azure == 1:
        # Output dimensions for single azure pixel.
        output_height = 4
        output_width = max(input_grid.shape) + 4
        output_grid = np.zeros((output_height, output_width), dtype=int)
        # Place four azure pixels at the extreme corners.
        output_grid[0, 0] = 8
        output_grid[0, -1] = 8
        output_grid[-1, 0] = 8
        output_grid[-1, -1] = 8
    elif num_azure == 2:
        diagonal = are_diagonal(azure_coords)
        if diagonal:
            # Output dimensions for diagonal case.
            max_row = max(azure_coords[0])
            max_col = max(azure_coords[1])
            output_height = max_row + 4
            output_width = max_col + 7
            output_grid = np.zeros((output_height, output_width), dtype=int)

            # Place two azure pixels.
            output_grid[max_row, max_col + 6] = 8
            output_grid[max_row + 3, 0] = 8
        else:  # same row or column
            output_height = 4
            max_dim = max(input_grid.shape)
            output_width = max_dim + 4

            output_grid = np.zeros((output_height, output_width), dtype=int)
             # Place four azure pixels at the extreme corners.
            output_grid[0, 0] = 8
            output_grid[0, -1] = 8
            output_grid[-1, 0] = 8
            output_grid[-1, -1] = 8


    else:
        # Handle cases with other numbers of azure pixels (shouldn't occur in examples).
        output_grid = np.zeros_like(input_grid)

    return output_grid
```
