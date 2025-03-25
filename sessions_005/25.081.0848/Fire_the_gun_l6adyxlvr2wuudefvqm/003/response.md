```python
"""
1. Scan the input grid: Examine each pixel.
2. Identify White Pixels: Focus on pixels that are white (value 0).
3. Check for Gray Neighbors: For each white pixel, examine its immediate neighbors (up, down, left, and right).
4. Determine horizontal/vertical runs: Transform a white (0) pixel into a red pixel (2) ONLY IF, looking from the the perspective of the current pixel position, extending to the left AND right OR above AND below, a gray (5) is encountered in *both* directions and the current pixel is to the immediate left of gray.
"""

import numpy as np

def get_adjacent_pixels(grid, row, col):
    """Gets the values of adjacent pixels (up, down, left, right)."""
    rows, cols = grid.shape
    adjacent = []
    if row > 0:
        adjacent.append((row - 1, col, grid[row - 1, col]))  # Up
    if row < rows - 1:
        adjacent.append((row + 1, col, grid[row + 1, col]))  # Down
    if col > 0:
        adjacent.append((row, col - 1, grid[row, col - 1]))  # Left
    if col < cols - 1:
        adjacent.append((row, col + 1, grid[row, col + 1]))  # Right
    return adjacent

def check_horizontal(grid, row, col):
    """Checks for gray pixels to the left and right."""
    rows, cols = grid.shape
    left = False
    right = False

    # Check left
    for c in range(col - 1, -1, -1):
        if grid[row, c] == 5:
            left = True
            break

    # Check Right
    for c in range(col + 1, cols):
        if grid[row,c] == 5 and col == c - 1:
            right = True
            break
    return left and right

def check_vertical(grid, row, col):
    rows, cols = grid.shape

    above = False
    below = False

    # check above
    for r in range(row - 1, -1, -1):
        if grid[r,col] == 5:
            above = True
            break

    # check below
    for r in range(row + 1, rows):
        if grid[r,col] == 5 and row == r - 1:
            below = True
            break

    return above and below

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)  # Ensure numpy array
    output_grid = np.copy(input_grid)

    rows, cols = input_grid.shape

    # change output pixels
    for row in range(rows):
        for col in range(cols):
            if input_grid[row,col] == 0:
                if check_horizontal(input_grid, row, col) or check_vertical(input_grid, row, col):
                    output_grid[row,col] = 2

    return output_grid
```
