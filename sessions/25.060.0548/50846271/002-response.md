# 50846271 • 002 • example_4 • investigate_coder

---
```python
"""
1.  **Identify Cross Shapes:** Locate all red (2) "cross" shapes within the input grid. A cross shape can be a single red pixel or a contiguous + shaped set of red pixels.
2.  **Inner Pixel Check.** Examine the red pixels. Replace with azure (8) the red(2) pixels that are *not* at the extremities of the cross.
3.  **Output:** Create the output grid, which will contain:
    *   All non-red pixels from the input grid without changing the value.
    *   The edited pixels of the initial red crosses

Essentially, we preserve the non-red pixels and selectively edit the existing red crosses. The key is to find the "inner" pixels to transform the color from red to azure.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell in a grid (diagonal not considered)."""
    neighbors = []
    rows, cols = grid.shape
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def is_inner_cross_pixel(grid, row, col):
    """Checks if a red pixel is an 'inner' part of a cross."""
    if grid[row, col] != 2:
        return False

    neighbors = get_neighbors(grid, row, col)
    red_neighbors = 0
    for r, c in neighbors:
        if grid[r, c] == 2:
            red_neighbors += 1

    # if it has more than one neighbor then its not an extremity
    return red_neighbors > 1

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""
    input_grid = np.array(input_grid)  # Ensure numpy array
    output_grid = np.copy(input_grid)    # Initialize output grid

    rows, cols = input_grid.shape

    # Iterate through each cell
    for row in range(rows):
        for col in range(cols):
            # check if red and 'inner'
            if is_inner_cross_pixel(input_grid, row, col):
                output_grid[row, col] = 8  # change to azure

    return output_grid.tolist()
```
