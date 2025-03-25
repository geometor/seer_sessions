```python
"""
The transformation rule identifies non-zero pixels and creates a blue (value 1) expansion/filling adjacent to the original pixel on all sides, but only orthogonally (up, down, left, right). The original non-zero pixel is preserved.
"""

import numpy as np

def get_orthogonal_neighbors(grid, row, col):
    """Gets the valid orthogonal neighboring coordinates for a given cell."""
    rows, cols = grid.shape
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
        nr, nc = row + dr, col + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors


def expand_halo_orthogonally(grid, row, col, output_grid):
    """Expands halo pixels (1) around the given cell orthogonally."""
    
    neighbors = get_orthogonal_neighbors(grid, row, col)

    for nr, nc in neighbors:
        if output_grid[nr, nc] == 0:  # Only expand if the output cell is 0
            output_grid[nr, nc] = 1

def transform(input_grid):
    """Transforms the input grid according to the rule."""
    # Initialize output_grid with zeros and same shape as input.
    output_grid = np.zeros_like(input_grid)

    rows, cols = input_grid.shape
    # Iterate through the input grid.
    for row in range(rows):
        for col in range(cols):
            # Identify colored pixels (non-zero).
            if input_grid[row, col] != 0:
                # Preserve the colored pixel.
                output_grid[row, col] = input_grid[row, col]
                # Expand the halo orthogonally.
                expand_halo_orthogonally(input_grid, row, col, output_grid)

    return output_grid
```
