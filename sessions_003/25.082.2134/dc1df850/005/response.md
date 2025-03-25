```python
"""
The transformation rule identifies non-zero pixels and creates a blue (value 1) expansion/filling adjacent to the original pixel on all sides, but only orthogonally (up, down, left, right). The original non-zero pixel is preserved. The expansion occurs iteratively: newly added blue pixels also expand in subsequent steps.
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

def expand_halo_iteratively(input_grid, output_grid, max_iterations=2):
    """Expands halo pixels (1) around non-zero cells orthogonally, iteratively."""

    for _ in range(max_iterations):
        temp_grid = output_grid.copy()  # Work on a copy to avoid immediate modification
        rows, cols = temp_grid.shape
        for row in range(rows):
            for col in range(cols):
                if temp_grid[row, col] != 0:  # Check the TEMP grid for expansion sources
                    neighbors = get_orthogonal_neighbors(input_grid, row, col)
                    for nr, nc in neighbors:
                        if input_grid[nr,nc] == 0 and output_grid[nr, nc] == 0 :  #expand from input, but only if currently 0 in output
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

    # Expand the halo iteratively.
    expand_halo_iteratively(input_grid, output_grid)

    return output_grid
```