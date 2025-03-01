# b7249182 • 008 • refine_coder

---
```python
"""
Transforms red, blue, or magenta pixels in the input grid into cross-shaped patterns of the same color in the output grid.
The cross is centered at the same location of the original pixel and has an extension of 2.
Other pixels are preserved.
"""

import numpy as np

def create_cross(grid, row, col, color, extension):
    """
    Creates a cross shape in the grid centered at (row, col) with the given color and extension.
    """
    # Extend up
    for i in range(1, extension + 1):
        if row - i >= 0:
            grid[row - i, col] = color
    # Extend down
    for i in range(1, extension + 1):
        if row + i < grid.shape[0]:
            grid[row + i, col] = color
    # Extend left
    for i in range(1, extension + 1):
        if col - i >= 0:
            grid[row, col - i] = color
    # Extend right
    for i in range(1, extension + 1):
        if col + i < grid.shape[1]:
            grid[row, col + i] = color

    return grid

def transform(input_grid):
    """
    Transforms the input_grid according to the described rule.
    """
    # Initialize output_grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Iterate through each cell of the input_grid
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            # Check if the current cell is red, blue, or magenta
            if input_grid[i, j] in [1, 2, 6]:  # 1: blue, 2: red, 6: magenta
                # Get the color of the pixel
                color = input_grid[i, j]
                # Create a cross shape centered at the current cell with extension 2
                output_grid = create_cross(output_grid, i, j, color, 2)
                output_grid[i,j] = color # Ensure the center pixel is set.

    return output_grid
```
