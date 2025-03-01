# b60334d2 • 008 • refine_coder

---
```python
"""
Transforms a grid by replacing each gray pixel (5) with a blue cross (1) centered on that pixel's location. The gray pixel itself also becomes blue. The cross extends one pixel in each cardinal direction (up, down, left, right), but is truncated at the grid boundaries.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specified color."""
    return np.argwhere(grid == color)

def create_blue_cross(grid, center_row, center_col):
    """Creates a blue cross centered at the given coordinates."""
    rows, cols = grid.shape
    # Replace center with blue
    grid[center_row, center_col] = 1

    # Extend cross arms, respecting boundaries
    if center_row > 0:
        grid[center_row - 1, center_col] = 1  # Up
    if center_row < rows - 1:
        grid[center_row + 1, center_col] = 1  # Down
    if center_col > 0:
        grid[center_row, center_col - 1] = 1  # Left
    if center_col < cols - 1:
        grid[center_row, center_col + 1] = 1  # Right
    return grid

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find gray pixels (centers)
    gray_pixels = find_pixels_by_color(input_grid, 5)


    # Create a blue cross at each gray pixel location
    for row, col in gray_pixels:
      output_grid = create_blue_cross(output_grid, row, col)
      

    return output_grid.tolist()
```

