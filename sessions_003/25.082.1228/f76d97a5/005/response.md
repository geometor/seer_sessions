```python
"""
1.  **Identify Edge Pixels:** An "edge" pixel is defined as any pixel located on the first row, last row, first column, or last column of the input grid.

2.  **Preserve Edge Values:** If a pixel is an edge pixel, and its color appears on ANY edge in the grid, its value remains the same in the output grid.

3.  **Zero Out Other Pixels:** If a pixel is not an edge pixel, its value is set to 0 in the output grid.

4.  **Zero Non-Edge Values** If a pixel *is* an edge pixel, but its color *does not* appear in another edge, its value is set to 0 in the output grid.
"""

import numpy as np

def is_edge_pixel(grid, row, col):
    """Checks if a pixel is on the edge of the grid."""
    rows, cols = grid.shape
    return row == 0 or row == rows - 1 or col == 0 or col == cols - 1

def get_edge_values(grid):
    """Returns a set of unique values present on the edges of the grid."""
    rows, cols = grid.shape
    edge_values = set()
    for r in range(rows):
        for c in range(cols):
            if is_edge_pixel(grid, r, c):
                edge_values.add(grid[r, c])
    return edge_values

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape
    edge_values = get_edge_values(input_grid)

    # change output pixels
    for r in range(rows):
        for c in range(cols):
            if is_edge_pixel(input_grid, r, c):
                if input_grid[r,c] in edge_values:
                    output_grid[r, c] = input_grid[r, c]

    return output_grid
```