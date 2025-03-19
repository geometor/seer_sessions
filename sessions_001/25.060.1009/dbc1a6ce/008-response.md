# dbc1a6ce • 008 • refine_coder

---
```python
"""
For each blue (1) pixel in the input grid, draw an azure (8) cross centered on that blue pixel.
The original blue pixel remains unchanged. The cross consists of four arms extending from the
center pixel in the four cardinal directions (up, down, left, and right). Each arm extends
until it encounters a pixel that is not white (0) or reaches the boundary of the grid.
All other pixels in the input grid remain unchanged.
"""

import numpy as np

def extend_arm(grid, start_row, start_col, direction):
    """
    Extends an arm of the cross from a starting point in a given direction.

    Args:
        grid: The numpy array representing the grid.
        start_row: The starting row index.
        start_col: The starting column index.
        direction: A tuple (row_delta, col_delta) representing the direction.

    Returns:
        A list of (row, col) tuples representing the cells the arm occupies.
    """
    rows, cols = grid.shape
    row = start_row + direction[0]
    col = start_col + direction[1]
    arm_cells = []

    while 0 <= row < rows and 0 <= col < cols and grid[row, col] == 0:
        arm_cells.append((row, col))
        row += direction[0]
        col += direction[1]

    return arm_cells

def transform(input_grid):
    """
    Transforms the input grid by drawing azure crosses centered on each blue pixel.
    Arms of the crosses extend until a non-white pixel or the grid edge is reached.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find all blue pixels
    blue_pixels = np.argwhere(input_grid == 1)

    # For each blue pixel, draw an azure cross
    for row, col in blue_pixels:
        # Extend arms in all four directions
        for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
            arm_cells = extend_arm(output_grid, row, col, direction)
            # Set the arm cells to azure
            for r, c in arm_cells:
                output_grid[r, c] = 8

    return output_grid
```
