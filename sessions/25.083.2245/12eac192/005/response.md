```python
"""
1.  Identify Seed Pixels: Find all blue (value 1) pixels in the input grid.
2. Initial Green Conversion
    - If the blue is on the top row, change to green
    - If the blue is on the leftmost column, change to green
3.  Propagate Green: Iteratively, for each blue pixel (value 1) in the input grid:
    - If a blue pixel is directly adjacent (up, down, left, or right, *not* diagonal) to a green pixel (value 3) *and* that blue pixel is not adjacent to any pixels with the value 8, change the blue pixel to green (value 3).
    - Repeat this propagation step until no more blue pixels can be changed to green.
4.  Preserve Other Pixels: All pixels that are not blue, or do not meet the conditions for change to green remain their original values.
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

    # Initial Green Conversion (Step 2)
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == 1:
                if i == 0 or j == 0:
                    output_grid[i,j] = 3

    # Propagate Green (Step 3)
    while True:
        changes_made = False
        for i in range(rows):
            for j in range(cols):
                if input_grid[i,j] == 1 and output_grid[i,j] !=3:
                    adjacent_output_values = get_adjacent_pixels(output_grid, i, j)
                    adjacent_input_values = get_adjacent_pixels(input_grid, i,j)
                    if 3 in adjacent_output_values and 8 not in adjacent_input_values :
                        output_grid[i, j] = 3
                        changes_made = True
        if not changes_made:
             break # Exit loop if propagation is complete

    return output_grid
```