# 1190e5a7 • 020 • refine_coder

---
```python
"""
The transformation identifies a "staircase" shape formed by blue (1) pixels and removes it from the input grid to produce the output grid. The staircase consists of a sequence of blue pixels where each subsequent pixel is either directly below or diagonally below and to the right of the previous one. The base of the staircase always lies on the second to last row. The remaining pixels are copied to their corresponding locations in the output.

"""

import numpy as np

def find_staircase(grid):
    """Finds the staircase pattern of blue (1) pixels."""
    rows, cols = grid.shape
    staircase_pixels = []

    # Find the starting point of the staircase (bottom row, blue pixel)
    for c in range(cols):
        if grid[rows - 2, c] == 1:
            start_col = c
            staircase_pixels.append((rows - 2, start_col))
            break
    else:
        return []  # No staircase found

    # Trace the staircase upwards
    current_row = rows - 2
    current_col = start_col

    while current_row > 0:
        # Check for blue pixel directly above
        if grid[current_row - 1, current_col] == 1:
            current_row -= 1
            staircase_pixels.append((current_row, current_col))
        # Check for blue pixel diagonally above and to the right
        elif current_col + 1 < cols and grid[current_row - 1, current_col + 1] == 1:
            current_row -= 1
            current_col += 1
            staircase_pixels.append((current_row, current_col))
        else:
            break  # End of staircase

    return staircase_pixels


def transform(input_grid):
    """Removes the blue staircase from the grid."""
    # Create a copy of the input grid to modify
    output_grid = input_grid.copy()
    rows, cols = output_grid.shape
    output_grid = output_grid[:rows-1] # remove last row

    # Find the staircase pixels
    staircase_pixels = find_staircase(input_grid)

    # Remove the staircase pixels from the output grid
    for row, col in staircase_pixels:
        if row < output_grid.shape[0]:
            output_grid[row, col] = input_grid[rows-1, col] # fill the void with color from the last row.

    return output_grid
```
