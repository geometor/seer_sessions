# 77fdfe62 • 014 • example_3 • investigate_coder

---
```python
"""
The transformation rule extracts the colors from the four corner pixels of the input grid and uses them to fill corresponding 2x2 quadrants in the output grid. The output grid is half the size of the input grid in each dimension. Each quadrant in the output is filled with three pixels matching the color from its input corner, with one background pixel in the opposite corner.
"""

import numpy as np

def get_corner_colors(grid):
    # Get the colors of the four corner pixels
    top_left = grid[0, 0]
    top_right = grid[0, -1]
    bottom_left = grid[-1, 0]
    bottom_right = grid[-1, -1]
    return top_left, top_right, bottom_left, bottom_right

def fill_quadrant(output_grid, quadrant, color):
    # Fill a 2x2 quadrant in the output grid based on the corner and color
    row_start = 0 if quadrant in (0, 1) else output_grid.shape[0] // 2
    col_start = 0 if quadrant in (0, 2) else output_grid.shape[1] // 2

    if quadrant == 0:  # Top-left
      output_grid[row_start:row_start + 2, col_start:col_start + 2] = color
      output_grid[row_start + 1, col_start + 1] = 0
        
    elif quadrant == 1:  # Top-right
      output_grid[row_start:row_start + 2, col_start:col_start + 2] = color
      output_grid[row_start + 1, col_start] = 0

    elif quadrant == 2:  # Bottom-left
      output_grid[row_start:row_start + 2, col_start:col_start + 2] = color
      output_grid[row_start, col_start + 1] = 0

    elif quadrant == 3:  # Bottom-right
      output_grid[row_start:row_start + 2, col_start:col_start + 2] = color
      output_grid[row_start, col_start] = 0

    return output_grid

def transform(input_grid):
    # Initialize output grid with half the dimensions of the input grid
    input_height, input_width = input_grid.shape
    output_height = input_height // 2
    output_width = input_width // 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Get the colors from the four corners of the input grid
    top_left_color, top_right_color, bottom_left_color, bottom_right_color = get_corner_colors(input_grid)

    # Fill each quadrant of the output grid
    output_grid = fill_quadrant(output_grid, 0, top_left_color)  # Top-left
    output_grid = fill_quadrant(output_grid, 1, top_right_color)  # Top-right
    output_grid = fill_quadrant(output_grid, 2, bottom_left_color)  # Bottom-left
    output_grid = fill_quadrant(output_grid, 3, bottom_right_color)  # Bottom-right

    return output_grid
```
