```python
"""
Transforms an input grid by replacing 0s adjacent to a '1' with '8's and all 9s with 0s.
"""

import numpy as np

def find_marker(grid, marker_value=1):
    # find the coordinates (row, col) of the marker value
    rows, cols = np.where(grid == marker_value)
    if len(rows) > 0:
        return rows[0], cols[0]  # return first match
    return None

def get_adjacent_indices(grid, row, col):
    # Get indices of adjacent cells (up, down, left, right)
    rows, cols = grid.shape
    adjacent_indices = []
    if row > 0:
        adjacent_indices.append((row - 1, col))  # Up
    if row < rows - 1:
        adjacent_indices.append((row + 1, col))  # Down
    if col > 0:
        adjacent_indices.append((row, col - 1))  # Left
    if col < cols - 1:
        adjacent_indices.append((row, col + 1))  # Right
    return adjacent_indices

def transform(input_grid):
    # initialize output_grid with 0s
    output_grid = np.zeros_like(input_grid)

    rows, cols = input_grid.shape

    # replace 9s with 0s, and copy all other values to output
    for r in range(rows):
        for c in range(cols):
          if input_grid[r,c] == 9:
            output_grid[r,c] = 0
          else:
            output_grid[r,c] = 0

    # Find marker (value 1)
    marker_coords = find_marker(input_grid, 1)
    if marker_coords:
        marker_row, marker_col = marker_coords

        # Get adjacent cells
        adjacent_indices = get_adjacent_indices(input_grid, marker_row, marker_col)

        # change output pixels
        for r, c in adjacent_indices:
            if input_grid[r, c] == 0:
                output_grid[r, c] = 8

    return output_grid
```