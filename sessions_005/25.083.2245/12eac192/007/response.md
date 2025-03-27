```python
"""
1.  **Identify Seed Pixels:** Find all pixels with the value 1 (blue) on *any* edge of the input grid (top, bottom, left, or right).

2.  **Initial Green Conversion:** Change all identified seed pixels (blue edge pixels) to the value 3 (green).

3. **Iterative Green Propagation:**

    - Create a copy of input_grid, called output_grid
    - Iterate through output_grid.
    - If any blue pixel in output_grid is adjacent (up, down, left, or right) to any green pixel in output_grid, *and* if that same pixel is *not* adjacent (up, down, left right) to pixel with a value of 8 in the *input* grid, then change the blue pixel to green (value 3) in output_grid.
    - Repeat until no further propagation possible

4.  **Preservation:** All pixels that do not meet the conditions for color change retain their original values.
"""

import numpy as np

def get_adjacent_pixels(grid, row, col):
    """Gets the values of adjacent pixels (up, down, left, right)."""
    rows, cols = grid.shape
    adjacent = []
    if row > 0:
        adjacent.append(grid[row - 1, col])  # Up
    if row < rows - 1:
        adjacent.append(grid[row + 1, col])  # Down
    if col > 0:
        adjacent.append(grid[row, col - 1])  # Left
    if col < cols - 1:
        adjacent.append(grid[row, col + 1])  # Right
    return adjacent

def transform(input_grid):
    """
    Transforms the input grid according to the propagation rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Initial Green Conversion (Step 1 & 2)
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == 1:
                if i == 0 or i == rows - 1 or j == 0 or j == cols - 1:
                    output_grid[i,j] = 3

    # Propagate Green (Step 3)
    while True:
        changes_made = False
        temp_grid = np.copy(output_grid)  # Work on a copy for each iteration
        for i in range(rows):
            for j in range(cols):
                if temp_grid[i, j] == 1:
                    adjacent_output_values = get_adjacent_pixels(temp_grid, i, j)
                    adjacent_input_values = get_adjacent_pixels(input_grid, i, j)
                    if 3 in adjacent_output_values and 8 not in adjacent_input_values:
                        output_grid[i, j] = 3
                        changes_made = True
        if not changes_made:
            break  # Exit loop if propagation is complete

    return output_grid
```