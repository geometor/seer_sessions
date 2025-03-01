# 44d8ac46 • 004 • example_1 • investigate_coder

---
```python
"""
The transformation identifies the "interior" gray pixels of shapes within the grid, and then colors those interior pixels to red. The outer "border" of the shapes remain gray.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Get the valid neighbors of a cell in a grid.
    """
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors


def is_interior(grid, row, col, color):
    """
    Checks if a pixel at (row, col) of the given color is an interior pixel.
    """
    # Check if the current cell is of the specified color.
    if grid[row, col] != color:
        return False

    # Check if all neighbors are of the same color.
    neighbors = get_neighbors(grid, row, col)
    for r, c in neighbors:
        if grid[r, c] != color:
            return False  # It's a border pixel
    return True  # All neighbors are the same color

def transform(input_grid):
    """
    Transforms the input grid by changing interior gray pixels to red.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # Check if the pixel is an interior gray pixel
            if is_interior(output_grid, row, col, 5):
                output_grid[row, col] = 2  # Change to red

    return output_grid
```
